# coding: utf-8
"""KILIT DEFTERI · yalniz ekle, SHA256 zinciri (kayit.py ile ayni kanonik yazim)
Dondurulmus dosyalarin ozetleri ve tahmin kilidi metni buraya yazilir. Her kayit bir oncekinin ozetini tasir; bir
satir degisirse, silinirse ya da araya satir girerse dogrula() yakalar. Kafa ayri dosyaya basilir (yayimli kafa).
Kullanim:
  python -I defter.py dondur "<baslik>"           # KAYITLI dosyalarin (asagida) ozetlerini ve Kosu 0 / test sonucunu yazar
  python -I defter.py kilit "<baslik>" <dosya.md>  # kilit metnini (dosyanin tamami ve ozeti) yazar
  python -I defter.py dogrula
Cikti: KILIT_DEFTERI.jsonl · KILIT_DEFTERI.kafa · KILIT_DEFTERI.md (okunur hali, her eklemede yeniden uretilir)"""
import hashlib
import json
import os
import subprocess
import sys
import time

KOK = os.path.dirname(os.path.abspath(__file__))
DEFTER = os.path.join(KOK, "KILIT_DEFTERI.jsonl")
ALANLAR = ("sira", "zaman", "tur", "baslik", "icerik", "onceki_ozet")
BASLANGIC = "0" * 64
KAYITLI = ["KAPI_KURALLARI_DONUK_v3_4.md", "SISTEM_MESAJI_v3_4.md", "KARAKTER_KARTLARI_v2_27eki.md",
           "DEGISIKLIK_v3_1_27eki.md", "DEGISIKLIK_v3_2_27eki.md", "DEGISIKLIK_v3_3_27eki.md",
           "kayit.py", "dunya.py", "ajanlar.py", "olcum.py", "suruculer.py", "kartlar.py", "kosu_model.py", "kosu0.py",
           "kosu_ozet.py", "donuk_yaz.py", "sistem_yaz.py", "test_v3.py", "defter.py",
           "oynatici_v3.html", "oynatici3d_v3.html"]
DIS = {"KURALLAR_v3_SON_27eki.md": os.path.join(KOK, "..", "oyun_alani", "KURALLAR_v3_SON_27eki.md")}


def kanonik(k):
    return json.dumps({a: k.get(a) for a in ALANLAR}, ensure_ascii=False, separators=(",", ":"))


def ozet(metin):
    return hashlib.sha256(metin.encode("utf-8")).hexdigest()


def dosya_ozeti(yol):
    with open(yol, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def oku():
    if not os.path.exists(DEFTER):
        return []
    with open(DEFTER, encoding="utf-8") as f:
        return [x for x in f.read().splitlines() if x]


def dogrula(satirlar=None):
    onceki = BASLANGIC
    for i, s in enumerate(oku() if satirlar is None else satirlar):
        o = json.loads(s)
        if kanonik(o) != s or o["onceki_ozet"] != onceki or o["sira"] != i:
            return False, "satir %d bozuk" % i
        onceki = ozet(s)
    return True, onceki


def ekle(tur, baslik, icerik):
    satirlar = oku()
    tamam, onceki = dogrula(satirlar)
    if not tamam:
        raise SystemExit("defter bozuk: %s · ekleme yapilmadi" % onceki)
    k = {"sira": len(satirlar), "zaman": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "tur": tur, "baslik": baslik,
         "icerik": icerik, "onceki_ozet": onceki}
    s = kanonik(k)
    with open(DEFTER, "a", encoding="utf-8", newline="\n") as f:
        f.write(s + "\n")
    with open(os.path.join(KOK, "KILIT_DEFTERI.kafa"), "w", encoding="utf-8", newline="\n") as f:
        f.write("%s  KILIT_DEFTERI  satir=%d\n" % (ozet(s), len(satirlar) + 1))
    okunur()
    return ozet(s)


def okunur():
    m = ["# Kilit defteri · Labirent oyun alanı v3", "",
         "Yalnız eklenir; her kayıt bir öncekinin SHA256 özetini taşır (`python -I defter.py dogrula`). "
         "Kaynak: KILIT_DEFTERI.jsonl. Bu dosya ondan üretilir.", ""]
    for s in oku():
        k = json.loads(s)
        m.append("## %d · %s · %s" % (k["sira"], k["tur"], k["baslik"]))
        m.append("%s · önceki özet `%s…` · bu kaydın özeti `%s…`" % (k["zaman"], k["onceki_ozet"][:16], ozet(s)[:16]))
        m.append("")
        i = k["icerik"]
        if "dosyalar" in i:
            m.append("| dosya | SHA256 |\n|---|---|")
            for d, o in i["dosyalar"].items():
                m.append("| %s | `%s` |" % (d, o))
            m.append("")
        for a, v in i.items():
            if a not in ("dosyalar", "metin"):
                m.append("- %s: %s" % (a, v))
        if "metin" in i:
            m += ["", i["metin"]]
        m.append("")
    with open(os.path.join(KOK, "KILIT_DEFTERI.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(m) + "\n")


def calistir(betik):
    r = subprocess.run([sys.executable, "-I", os.path.join(KOK, betik)] + (["--cikti", ""] if betik == "kosu0.py" else []),
                       capture_output=True, text=True, encoding="utf-8", cwd=KOK)
    son = (r.stdout.strip().splitlines() or [""])[-1] if betik == "kosu0.py" else (r.stderr.strip().splitlines() or [""])[-1]
    return {"cikis_kodu": r.returncode, "son_satir": son}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    komut = sys.argv[1] if len(sys.argv) > 1 else "dogrula"
    if komut == "dondur":
        dosyalar = {d: dosya_ozeti(os.path.join(KOK, d)) for d in KAYITLI}
        dosyalar.update({d: dosya_ozeti(y) for d, y in DIS.items()})
        print(ekle("dondurma", sys.argv[2], {"dosyalar": dosyalar, "kosu0": calistir("kosu0.py"),
                                             "test": calistir("test_v3.py")}))
    elif komut == "kilit":
        with open(sys.argv[3], encoding="utf-8") as f:
            metin = f.read()
        print(ekle("kilit", sys.argv[2], {"kaynak": os.path.basename(sys.argv[3]), "kaynak_ozet": ozet(metin),
                                          "metin": metin}))
    else:
        print(dogrula())
