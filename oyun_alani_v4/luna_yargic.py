# coding: utf-8
"""LUNA YARGIC GONDERICISI · EK5a (300) ve EK5b (9) · 7 Kasim 2026 · Hikayeci · danisman cevabi 7 Kas (a)+(b)
Yeni dosya, sprint ici is (Appendix D). Donuk dosyalara dokunmaz; hash listesindeki hicbir dosyaya yazmaz.
Bicim TAHMIN_KILIDI_EK5A_LUNA_31eki.md 'Sabitler · cagri' (EK5b ayni sabitlerle, TAHMIN_KILIDI_EK5B_VAKA_4kas.md):
  - tek kullanici mesaji = soru dosyasi + bos satir + ozet dosyasi (iki dosya da '\\n' ile biter: soru + '\\n' + ozet, bayt bayt)
  - sistem mesaji ve gecmis YOK · sira k0001 -> k0300 (EK5b v1 -> v9) · kosu basina TEK cagri, tekrar YOK
  - model gpt-5.6-luna, donen model adi kayda · temperature, seed, response_format GONDERILMEZ · max_completion_tokens 400
  - tavan 10 USD: usage jetonlarindan kosu_api.py MODEL['luna']['fiyat'] varsayimiyla TAHMIN; asilacaksa durur
Istemci kosu_api.Yalin aynen (govde, adres, ortam KOSU_OPENAI). Tek fark bu surecte: kosu_api.BEKLE = () -> 429/5xx'te
  yeniden gonderme YOK (kilit: tekrar yok). Ham cevap _post sarilarak tam JSON olarak alinir.
Durma: hash tutmazsa HIC baslamaz · ilk cagri herhangi bir hatayla donerse durur · 401/403/429 her an durur (model degistirilmez)
  · art arda 3 hata durur · baska hata (zaman asimi, 5xx, 400) o kosu icin kaydedilir, sonrakine gecer.
Betik ETIKET URETMEZ (ilk satir kuralini danisman uygular). Anahtar hicbir kayda, ekrana, hataya girmez (her satir yazilmadan denetlenir).
Ciktilar (cikti klasoru doluysa baslamaz):
  luna/cevap_ek5a/k0001.json ...  {kimlik, istek_govdesi (anahtarsiz), http, cevap (tam JSON) | hata}
  luna/cevap_ek5a/olcum.jsonl     her cagri: UTC bas/bit, http, usage, donen model, finish_reason, tahmini USD (birikimli)
  luna/cevap_ek5b/v1.json ... ve luna/cevap_ek5b/olcum.jsonl
Calistir (Turan "baslat" + danisman okuduktan sonra):  python -I luna_yargic.py --asama ek5a   |   --asama ek5b
Sinama (ag yok, sahte anahtar, gecici klasor):          python -I luna_yargic.py --asama ek5a --sina
SAPMA 7 Kas (Turan karari, defter 25, SAPMA_EK5B_TAVAN_7KAS.md): --tavan N yalniz max_completion_tokens degerini
  degistirir (varsayilan 400 = kilit). --klasor AD cikti klasorunu luna/AD yapar (varsayilan cevap_<asama>).
  Ikisi de verilmezse davranis fb412cbf ile ayni. kosu_api.py'ye dokunulmaz (A.MODEL kopyalanir, degistirilmez).
  EK5b:  python -I luna_yargic.py --asama ek5b --tavan 2000"""
import argparse
import datetime
import glob
import hashlib
import io
import json
import os
import socket
import sys
import tempfile
import urllib.error

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import kosu_api as A  # noqa: E402

LUNA = os.path.join(KOK, "luna")
TAVAN_USD = 10.0
OZET_5A = "379475bd056b9af3f4a73bd34291355ef1737b4a4d28731c1733ab0ea53a0d47"     # TAHMIN_KILIDI_EK5A tablo
SORU_5A = "f8e8537f241c7d8411a6c4113b7ebbf1e64562bd286ce9229d02e7f68b83f4b3"
DURDUR_KOD = {401, 403, 429}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def oku(p):
    with open(p, "rb") as f:
        return f.read()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-4] + "Z"


def isler_5a():
    """[(kimlik, mesaj_bayt)] · hash kilitle tutmazsa SystemExit"""
    dosyalar = sorted(glob.glob(os.path.join(LUNA, "ozet", "k*.txt")))
    soru = oku(os.path.join(LUNA, "soru.txt"))
    h = hashlib.sha256()
    for f in dosyalar:
        h.update(oku(f))
    if len(dosyalar) != 300 or h.hexdigest() != OZET_5A or sha(soru) != SORU_5A:
        raise SystemExit("EK5a HASH TUTMADI, baslamiyor: ozet %d dosya %s, soru %s" % (len(dosyalar), h.hexdigest()[:16], sha(soru)[:16]))
    return [(os.path.basename(f)[:-4], soru + b"\n" + oku(f)) for f in dosyalar]


def isler_5b():
    tablo = {}
    for s in open(os.path.join(LUNA, "EK5B_OZET_HASH_4kas.md"), encoding="utf-8"):
        p = [x.strip().strip("`") for x in s.split("|")]
        if len(p) > 4 and p[1].startswith("v") and p[1][1:].isdigit():
            tablo[p[1]] = (p[2], p[3])
    if sorted(tablo) != ["v%d" % i for i in range(1, 10)]:
        raise SystemExit("EK5b hash tablosu okunamadi: %s" % sorted(tablo))
    out = []
    for i in range(1, 10):
        k = "v%d" % i
        oz, so = oku(os.path.join(LUNA, "ozet_ek5b", k + ".txt")), oku(os.path.join(LUNA, "soru_ek5b", k + ".txt"))
        if (sha(oz), sha(so)) != tablo[k]:
            raise SystemExit("EK5b HASH TUTMADI (%s), baslamiyor" % k)
        out.append((k, so + b"\n" + oz))
    return out


def sahte_ag(tavan=400):
    """--sina: ag yok · gelen govdeyi denetler, sahte Luna cevabi doner"""
    def ac(istek, timeout=None):
        g = json.loads(istek.data.decode("utf-8"))
        assert sorted(g) == ["max_completion_tokens", "messages", "model"], sorted(g)
        assert g["max_completion_tokens"] == tavan and g["model"] == "gpt-5.6-luna", g["max_completion_tokens"]
        assert len(g["messages"]) == 1 and g["messages"][0]["role"] == "user", g["messages"]
        b = json.dumps({"id": "sahte", "model": "gpt-5.6-luna-sahte", "choices": [{"index": 0, "message": {"role": "assistant", "content": "yok"},
                        "finish_reason": "stop"}], "usage": {"prompt_tokens": 700, "completion_tokens": 40}}).encode("utf-8")

        class C(io.BytesIO):
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False
        return C(b)
    A.S.urllib.request.urlopen = ac


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--asama", choices=["ek5a", "ek5b"], required=True)
    p.add_argument("--sina", action="store_true")
    p.add_argument("--tavan", type=int, default=400)    # SAPMA 7 Kas, Turan karari · varsayilan kilit degeri
    p.add_argument("--klasor", default=None)            # luna/ altinda cikti klasoru · varsayilan cevap_<asama>
    a = p.parse_args()
    isler = isler_5a() if a.asama == "ek5a" else isler_5b()
    cikti = os.path.join(LUNA, a.klasor or "cevap_" + a.asama)
    ayar = dict(A.MODEL["luna"])
    ayar["tavan"] = (ayar["tavan"][0], a.tavan)
    if a.sina:
        cikti = tempfile.mkdtemp(prefix="luna_yargic_sina_")
        os.environ[ayar["degisken"]] = "sk-SAHTE-ANAHTAR-0123456789abcdef"
        sahte_ag(ayar["tavan"][1])
    if glob.glob(os.path.join(cikti, "*.json")) or os.path.exists(os.path.join(cikti, "olcum.jsonl")):
        raise SystemExit("cikti klasoru dolu, ustune yazilmaz: %s" % cikti)
    os.makedirs(cikti, exist_ok=True)
    disardan = bool(os.environ.get(ayar["degisken"]))
    if not disardan:                                   # kosu_api.main ile ayni yol: dosya -> yalniz surec ortami
        with open(os.path.join(A.API, ayar["dosya"]), encoding="utf-8", errors="replace") as f:
            os.environ[ayar["degisken"]] = f.read().strip()
    anahtar = os.environ[ayar["degisken"]]
    A.BEKLE = ()                                       # tekrar yok
    y = A.Yalin(ayar)
    son = {}
    _post = y._post

    def post(url, govde, basliklar=None):
        son["govde"] = govde
        son["cevap"] = _post(url, govde, basliklar)
        return son["cevap"]
    y._post = post

    def yaz(yol, nesne, ek=False):
        s = json.dumps(nesne, ensure_ascii=False)
        if anahtar and (anahtar in s or anahtar[:12] in s):
            raise SystemExit("ANAHTAR IZI kayda girecekti, durdu (yazilmadi)")
        with open(yol, "a" if ek else "w", encoding="utf-8", newline="\n") as f:
            f.write(s + ("\n" if ek else ""))

    olcum = os.path.join(cikti, "olcum.jsonl")
    usd, hata_seri, durum = 0.0, 0, "tamam"
    print("%s · %d cagri · cikti %s · %s" % (a.asama, len(isler), cikti, "SINAMA (ag yok)" if a.sina else "GERCEK"), flush=True)
    try:
        for n, (kid, mesaj) in enumerate(isler):
            if usd >= TAVAN_USD:
                durum = "tavan: tahmini %.4f USD >= %.0f, %s ve sonrasi gonderilmedi" % (usd, TAVAN_USD, kid)
                break
            son.clear()
            mesajlar = [{"role": "user", "content": mesaj.decode("utf-8")}]
            bas = utc()
            kayit = {"kimlik": kid, "istek_govdesi": {"model": ayar["model"], "messages": mesajlar, ayar["tavan"][0]: ayar["tavan"][1]}}
            olc = {"kimlik": kid, "bas_utc": bas}
            try:
                y.sohbet(mesajlar, 0)
                c = son["cevap"]
                u = c.get("usage") or {}
                g, ct = u.get("prompt_tokens", 0) or 0, u.get("completion_tokens", 0) or 0
                usd += g / 1e6 * ayar["fiyat"]["girdi"] + ct / 1e6 * ayar["fiyat"]["cikti"]
                kayit.update(http=200, cevap=c)
                olc.update(http=200, model=c.get("model"), usage=u, finish_reason=(c.get("choices") or [{}])[0].get("finish_reason"))
                hata_seri = 0
            except urllib.error.HTTPError as h:
                kayit.update(http=h.code, hata="HTTPError %d" % h.code)
                olc.update(http=h.code, hata="HTTPError %d" % h.code)
                hata_seri += 1
            except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, ValueError, KeyError) as h:
                kayit.update(http=None, hata=type(h).__name__)
                olc.update(http=None, hata=type(h).__name__)
                hata_seri += 1
            olc.update(bit_utc=utc(), usd_tahmini_birikimli=round(usd, 6), usd_not="usage x kosu_api varsayim fiyat, dogrulanmadi")
            yaz(os.path.join(cikti, kid + ".json"), kayit)
            yaz(olcum, olc, ek=True)
            print("%s %s http %s %s" % (olc["bit_utc"], kid, olc.get("http"), olc.get("hata", olc.get("finish_reason"))), flush=True)
            if "hata" in olc and (n == 0 or olc.get("http") in DURDUR_KOD or hata_seri >= 3):
                durum = "DURDU: %s (%s), ilk cagri=%s, art arda hata %d" % (kid, olc["hata"], n == 0, hata_seri)
                break
    finally:
        if not disardan:
            os.environ.pop(ayar["degisken"], None)
    print("SON · %s · tahmini %.4f USD (dogrulanmadi) · %s" % (a.asama, usd, durum), flush=True)
    if a.sina:
        tum = "".join(open(f, encoding="utf-8").read() for f in glob.glob(os.path.join(cikti, "*")))
        assert "SAHTE-ANAHTAR" not in tum and "Bearer" not in tum, "sinama: anahtar izi"
        print("sinama: %d dosya, anahtar izi yok" % len(os.listdir(cikti)))
    sys.exit(0 if durum == "tamam" else 2)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
