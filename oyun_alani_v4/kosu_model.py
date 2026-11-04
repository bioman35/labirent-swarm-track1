# coding: utf-8
"""OYUN ALANI v3 · MODEL KOSULARI · Kosu 1 (taban, ogretme kollari) · Kosu 2 (karsi taraf) · Kosu 4 (buyuk model)
Kartlar danismanin dosyasindan (kartlar.py, ozet denetimli). Kural, sistem mesaji ve kod ozetleri kosu_meta.json'a.
Her kosu bir kayit + yayimli kafa + olcum; ozet_tablo.jsonl her kosudan sonra bir satir buyur (kosu yarida
kalsa da biten kosular durur).
Ornek:
  python -I kosu_model.py --kosu 1 --tasiyici yerel --model qwen2.5:7b-instruct-q4_K_M --tohumlar 1-5
  python -I kosu_model.py --kosu 1 --tasiyici sahte --tohumlar 1   (DIL MODELI DEGIL: betik denemesi)"""
import argparse
import hashlib
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kartlar as K  # noqa: E402
import olcum  # noqa: E402
import suruculer as S  # noqa: E402
from dunya import kos  # noqa: E402
from kayit import dogrula  # noqa: E402

KOK = os.path.dirname(os.path.abspath(__file__))
KOD = ["kayit.py", "dunya.py", "ajanlar.py", "olcum.py", "suruculer.py", "kartlar.py", "kosu_model.py"]
ROL = {"B": "basajan", "TB": "teslim_basajan", "S1": None}


def ozet_dosya(yol):
    with open(yol, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def tohum_listesi(m):
    out = []
    for p in m.split(","):
        a, _, b = p.partition("-")
        out += list(range(int(a), int(b or a) + 1))
    return out


def model_tohumu(tohum, sira, tekrar=0):
    """tekrar 0: eski koşularla birebir aynı model tohumu · 29 Eki danisman 'tekrar olcumu': tekrar>0 farkli model tohumu"""
    t = "v3:%s:%s" % (tohum, sira) if not tekrar else "v3:%s:%s:r%d" % (tohum, sira, tekrar)
    return int(hashlib.sha256(t.encode()).hexdigest()[:8], 16)


def isler(kosu, tohumlar, kosullar, tekrar=0):
    """(kosu_id, tohum, kosul, dagitim) · Kosu 1: once kosul, sonra tohum (gece yarida kalirsa kosullar tam olsun)"""
    if kosu == 1:
        for k in kosullar:
            for t in tohumlar:
                yield "v4_kosu1_%s_t%d%s" % (k, t, "_r%d" % tekrar if tekrar else ""), t, k, K.dagitim_kosu1(t)
    else:
        for t in tohumlar:
            for s, dag in K.dagitim_kosu2(t):
                for k in kosullar:
                    yield "v4_kosu%d_%s_t%d_%s%s" % (kosu, k, t, s, "_r%d" % tekrar if tekrar else ""), t, k, dag


def ekip_kur(dag, kartlar, t, kosul, tohum, butce, tekrar=0):
    sira = ["B", "T1", "T2", "T3", "TB"] + (["S1"] if "S1" in dag else [])
    out = []
    for i, aid in enumerate(sira):
        kod = dag[aid]
        k = kartlar[kod]
        out.append(S.ModelAjan(aid, t, ROL.get(aid, "tasiyici"), kart_metni=k["metin"], tur=k["tur"],
                               karakter="%s · %s" % (kod, k["ad"]), tohum=model_tohumu(tohum, i, tekrar),
                               kollar=S.KOSULLAR[kosul], butce=butce))
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("--kosu", type=int, choices=[1, 2, 4], required=True)
    p.add_argument("--tasiyici", choices=["yerel", "api", "sahte"], required=True)
    p.add_argument("--model", default="sahte")
    p.add_argument("--adres")
    p.add_argument("--anahtar-degiskeni")
    p.add_argument("--fiyat-girdi", type=float)
    p.add_argument("--fiyat-cikti", type=float)
    p.add_argument("--sicaklik", type=float, help="varsayilan: Kosu 1'de 0, Kosu 2 ve 4'te 0.7 (DEGISIKLIK v3.1 §5)")
    p.add_argument("--tohumlar", default="1-5")
    p.add_argument("--kosullar", default=",".join(S.KOSULLAR))
    p.add_argument("--butce-dolar", type=float)
    p.add_argument("--butce-token", type=int)
    p.add_argument("--cikti")
    p.add_argument("--kodon-kapali", action="store_true", help="29 Eki ablasyon: v4 dunyasi kodonsuz")
    p.add_argument("--tekrar", type=int, default=0, help="29 Eki tekrar olcumu: 0 = eski model tohumu, 1+ = yeni")
    a = p.parse_args()
    if a.kodon_kapali:
        import dunya as _D
        _D.KODON_ACIK = False

    if a.sicaklik is None:
        a.sicaklik = 0.0 if a.kosu == 1 else 0.7
    kartlar, kart_oz = K.oku()
    kural_oz = ozet_dosya(os.path.join(KOK, K.KURAL_DOSYA))
    if kural_oz != K.KURAL_OZET:
        raise SystemExit("kural dosyasi ozeti %s, beklenen %s" % (kural_oz, K.KURAL_OZET))
    fiyat = {"girdi": a.fiyat_girdi, "cikti": a.fiyat_cikti} if a.fiyat_girdi is not None else None
    if a.tasiyici == "yerel":
        t = S.Ollama(a.model, adres=a.adres or "http://127.0.0.1:11434", sicaklik=a.sicaklik,
                     fiyat=fiyat or {"girdi": 0.0, "cikti": 0.0})
    elif a.tasiyici == "api":
        t = S.OpenAIUyumlu(a.model, a.adres, a.anahtar_degiskeni, sicaklik=a.sicaklik, fiyat=fiyat)
    else:
        t = S.Sahte()
    kosullar = a.kosullar.split(",")
    butce = S.Butce(dolar=a.butce_dolar, token=a.butce_token)
    klasor = a.cikti or os.path.join(KOK, "kosular", "kosu%d_%s_%s" % (a.kosu, a.tasiyici, time.strftime("%Y%m%d_%H%M%S")))
    os.makedirs(klasor, exist_ok=True)
    meta = {"kosu": a.kosu, "tasiyici": a.tasiyici, "model": a.model, "sicaklik": a.sicaklik,
            "model_kimlik": t.kimlik() if hasattr(t, "kimlik") else None,
            "tohumlar": tohum_listesi(a.tohumlar), "kosullar": kosullar, "fiyat": t.fiyat,
            "butce": {"dolar": a.butce_dolar, "token": a.butce_token},
            "kart_ozet": kart_oz, "kural_ozet": kural_oz, "kol_surumu": S.KOL_SURUMU,
            "sistem_mesaji_ozet": ozet_dosya(os.path.join(KOK, K.SISTEM_DOSYA)),
            "kod_ozet": {f: ozet_dosya(os.path.join(KOK, f)) for f in KOD},
            "baslangic": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "not": "ayni tohum dunyayi sabitler, modeli degil",
            "kodon": not a.kodon_kapali, "tekrar": a.tekrar}
    if a.tasiyici == "sahte":
        meta["uyari"] = "SAHTE TASIYICI: dil modeli yok, yalniz betik denemesi; sonuc model sonucu DEGILDIR"
    with open(os.path.join(klasor, "kosu_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    tablo = os.path.join(klasor, "ozet_tablo.jsonl")
    n, durdu = 0, None
    for kosu_id, tohum, kosul, dag in isler(a.kosu, meta["tohumlar"], kosullar, a.tekrar):
        ajanlar = ekip_kur(dag, kartlar, t, kosul, tohum, butce, a.tekrar)
        bas = time.time()
        try:
            d = kos(ajanlar, tohum, kosu_id)
        except S.ButceAsildi as h:
            durdu = str(h)
            print("BUTCE TAVANI: %s · kosular durdu" % durdu, flush=True)
            break
        d.kayit.kaydet(os.path.join(klasor, kosu_id + ".jsonl"))
        d.kayit.kafa_bas(os.path.join(klasor, kosu_id + ".kafa"))
        tamam, _ = dogrula(d.kayit.metin())
        o = olcum.olc([json.loads(s) for s in d.kayit.satirlar])
        o.update(kosul=kosul, dagitim=dag, sure_duvar_sn=round(time.time() - bas, 1), zincir=tamam,
                 yerlesim=t.yerlesim() if hasattr(t, "yerlesim") else None,
                 cagri={x.id: x.sayac for x in ajanlar})
        with open(os.path.join(klasor, kosu_id + ".olcum.json"), "w", encoding="utf-8") as f:
            json.dump(o, f, ensure_ascii=False, indent=1)
        satir = {"kosu_id": kosu_id, "kosul": kosul, "tohum": tohum, "dagitim": dag, "is": o["is_basarisi"],
                 "kararlar": o["kararlar"], "takildi": o["takildi"], "durdu": o["durdu"],
                 "haksiz": o["haksiz_durdurma"], "bizim_renk": o["bizim_renk"],
                 "fark_edilmeme": o["fark_edilmeme"], "zarar": o["zarar"], "yakalama": o["yakalama"],
                 "turuncu": o["turuncu"], "yol_yok": o["yol_yok"], "anahtar_red": o["anahtar_red"],
                 "adim": o["adim"], "tur": o["tur"], "token": o["maliyet"]["token"], "dolar": o["maliyet"]["dolar"],
                 "gecersiz": sum(x.sayac["gecersiz"] for x in ajanlar),
                 "cagri": sum(x.sayac["cagri"] for x in ajanlar), "sure_duvar_sn": o["sure_duvar_sn"],
                 "zincir": tamam}
        with open(tablo, "a", encoding="utf-8") as f:
            f.write(json.dumps(satir, ensure_ascii=False) + "\n")
        n += 1
        print("%-24s is %-5s tur %3d takildi %-10s durdu %-16s cagri %4d gecersiz %3d %7.1f sn" % (
            kosu_id, o["is_basarisi"], o["tur"], ",".join(o["takildi"]) or "-", o["durdu"] or "-",
            satir["cagri"], satir["gecersiz"], o["sure_duvar_sn"]), flush=True)
    meta.update(bitis=time.strftime("%Y-%m-%dT%H:%M:%S%z"), kosu_sayisi=n, butce_durdu=durdu,
                harcanan={"token": butce.token, "dolar": round(butce.dolar, 6)})
    with open(os.path.join(klasor, "kosu_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    print("bitti · %d kosu · %s" % (n, klasor))


if __name__ == "__main__":
    main()
