# coding: utf-8
"""DONDURMA · 4 Kasim 2026 · Swarm sprint oncesi · Hikayeci · model cagrisi YOK
Kaynak: DANISMAN_NOTU_DONDURMA_4KAS.md §2 ve son bolum, Turan "dondur dostum" (4 Kas ~22:45 TRT).
1. PREEXISTING_EK_31eki.md kapanir: eksik satirlar (2 Kas deneme kosusu, film_labirent sahnesi, 4 Kas dosyalari,
   DANISMAN_* notlari, guncellenmis iki taslagin bugunku ozeti) eklenir, "Kapanis" bolumu yazilir.
2. DONDURMA_4KAS.sha256: oyun_alani_v4 (luna/gizli dahil, yalniz ozet; __pycache__ haric), film_labirent/, oyun_alani_v3/defter.py.
   Defter dosyalarinin kendisi listede yok: defter her eklemede degisir, kendi SHA256 zinciri vardir.
3. KILIT_DEFTERI.jsonl'e tur "dondurma": liste dosyasinin ve kapanmis PREEXISTING listesinin ozeti.
Her adimdan sonra defter dogrulanir. Tekrar calistirilirsa durur (iki kez dondurma yazilmaz). Calistir: python -I -B dondurma_4kas.py"""
import hashlib
import importlib.util
import json
import os
import sys

V4 = os.path.dirname(os.path.abspath(__file__))
SPRINT = os.path.dirname(V4)
V3 = os.path.join(SPRINT, "oyun_alani_v3")
_s = importlib.util.spec_from_file_location("defter", os.path.join(V3, "defter.py"))
DF = importlib.util.module_from_spec(_s)
_s.loader.exec_module(DF)
PRE = os.path.join(V4, "PREEXISTING_EK_31eki.md")
LISTE = os.path.join(V4, "DONDURMA_4KAS.sha256")
BASLIK = "Swarm sprint öncesi dondurma · v4 dünya, kartlar, kayıtlar, kilitler, iki özet üreticisi, film sahnesi · PREEXISTING kapandı"


def h(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def dosyalar(kok, haric=()):
    for d, alt, fs in os.walk(kok):
        alt[:] = sorted(a for a in alt if a != "__pycache__")
        for f in sorted(fs):
            p = os.path.join(d, f)
            if os.path.abspath(p) not in haric:
                yield p


def klasor_ozeti(kok):
    """klasorun ozeti: siralanmis 'sha256  goreli_yol' satirlarinin ozeti"""
    sat = ["%s  %s" % (h(p), os.path.relpath(p, kok).replace("\\", "/")) for p in dosyalar(kok)]
    return hashlib.sha256(("\n".join(sat) + "\n").encode("utf-8")).hexdigest(), len(sat)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ok, kafa = DF.dogrula()
    if not ok:
        raise SystemExit("defter bozuk: %s" % kafa)
    L = [json.loads(s) for s in DF.oku()]
    if any(k["tur"] == "dondurma" and "4 Kas" in json.dumps(k["icerik"], ensure_ascii=False) and "Swarm" in k["baslik"] for k in L):
        raise SystemExit("4 Kas dondurmasi zaten defterde, ikinci kez yazilmaz")
    pre = open(PRE, encoding="utf-8").read()
    if "## Kapanış" in pre:
        raise SystemExit("PREEXISTING zaten kapali")
    # 1 · PREEXISTING kapanisi
    satir = lambda p, ne: "| %s | %s | %s |" % (p, ne, h(os.path.join(V4, p))[:16])
    film, film_n = klasor_ozeti(os.path.join(SPRINT, "film_labirent"))
    oz5b, oz_n = klasor_ozeti(os.path.join(V4, "luna", "ozet_ek5b"))
    so5b, so_n = klasor_ozeti(os.path.join(V4, "luna", "soru_ek5b"))
    deneme, den_n = klasor_ozeti(os.path.join(V4, "kosular", "v4_kosu4_deneme_2kas"))
    ek = ["", "## 2-4 Kasım satırları · kapanışta eklendi", "",
          "| dosya | ne | SHA256 ilk 16 |", "|---|---|---|",
          satir("DENEME_KOSU4_2KAS.md", "Koşu 4 deneme notu (2 Kas)"),
          "| kosular/v4_kosu4_deneme_2kas/ | Koşu 4 deneme koşusu, %d dosya; api_kayit.jsonl ve api_olcum.jsonl dahil (2 Kas) | %s |" % (den_n, deneme[:16]),
          satir("kosular/v4_kosu4_deneme_2kas.log", "deneme koşusu günlüğü (2 Kas)"),
          satir("TAHMIN_KILIDI_EK5_5C_2kas.md", "EK5 kilit metni, defter sira 22 (2 Kas)"),
          "| ../film_labirent/ | 3B tekrar sahnesi, kendi kayıtlarımız için, sprint öncesi · üç ham deneme klibi, anlatım ve kurgu yok · salt okunur, model çağrısı yok · %d dosya | %s |" % (film_n, film[:16]),
          "| luna/ozet_ek5b/ | EK5b dokuz özet (4 Kas), %d dosya | %s |" % (oz_n, oz5b[:16]),
          "| luna/soru_ek5b/ | EK5b dokuz soru (4 Kas), %d dosya | %s |" % (so_n, so5b[:16]),
          satir("dondurma_4kas.py", "bu dondurmanın betiği (4 Kas)")]
    for f in sorted(os.listdir(V4)):
        if f.startswith("DANISMAN_") and f.endswith(".md"):
            ek.append(satir(f, "danışman notu"))
    ek += [satir("TAHMIN_TASLAK_EK5_5C_31eki.md", "5c taslağının bugünkü hali; 31 Eki satırındaki özet ilk haline aitti, taslak aynı gün 21:54'te güncellendi, kilit metni ayrı (EK5)"),
           satir("TAHMIN_TASLAK_EK5B_VAKA_31eki.md", "EK5b taslağının bugünkü hali; 31 Eki satırındaki özet ilk haline aitti, taslak aynı gün 21:54'te güncellendi, kilit metni ayrı (EK5b)"),
           "", "## Kapanış · 4 Kasım 2026 · Turan \"dondur dostum\"", "",
           "Liste bu satırla kapandı. Bundan sonra yazılan dosyalar sprint işidir (sprint-time) ve bu listeye girmez. "
           "Klasör satırlarının özeti, sıralanmış \"sha256  göreli_yol\" satırlarının SHA256'sıdır. "
           "Bütün klasörün dosya dosya listesi DONDURMA_4KAS.sha256'dadır; o dosyanın ve bu listenin özeti kilit defterinde dondurma kaydındadır. "
           "Danışman notları dondurmadan sonra da ek alabilir; buradaki özet bu anın halidir.", ""]
    with open(PRE, "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(ek))
    # 2 · butun klasorun listesi
    haric = {os.path.abspath(LISTE)}
    sat = []
    for p in list(dosyalar(V4, haric)) + list(dosyalar(os.path.join(SPRINT, "film_labirent"))) + [os.path.join(V3, "defter.py")]:
        sat.append("%s  %s" % (h(p), os.path.relpath(p, SPRINT).replace("\\", "/")))
    with open(LISTE, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(sat) + "\n")
    gizli = [s for s in sat if "/luna/gizli/" in s]
    # 3 · defter
    icerik = {"dosyalar": {"oyun_alani_v4/DONDURMA_4KAS.sha256": h(LISTE), "oyun_alani_v4/PREEXISTING_EK_31eki.md": h(PRE),
                           "film_labirent/ (klasör özeti)": film},
              "dosya_sayisi": len(sat), "gizli_yalniz_ozet": len(gizli),
              "kaynak": "DANISMAN_NOTU_DONDURMA_4KAS.md §2 ve son bölüm · Turan \"dondur dostum\" 4 Kas ~22:45 TRT",
              "kapsam": "oyun_alani_v4 (dünya kodu, kartlar, kosular/ kayıtları, kilit metinleri, luna_ozet.py ve luna_ozet_ek5b.py, luna/ özetleri), film_labirent/, oyun_alani_v3/defter.py",
              "not": "luna/gizli/ dosyaları listede yalnız özetle durur, depoya 8 Kas'tan önce girmez. Anahtar dosyası (Desktop\\api) kapsam dışı. "
                     "Dondurmadan sonra donuk dosyalara dokunulmaz; 6 Kas'a kadar API çağrısı yok; Koşu 4 resmi açılış damgasından sonra. "
                     "Defter numarası: EK5b kilidi kilitten hemen sonra sira 23 olarak yazıldığı için bu dondurma sira 24'tür."}
    ozet = DF.ekle("dondurma", BASLIK, icerik)
    ok, kafa = DF.dogrula()
    if not ok or kafa != ozet:
        raise SystemExit("defter dogrulamasi tutmadi")
    L = [json.loads(s) for s in DF.oku()]
    print("dosya", len(sat), "· gizli yalniz ozet", len(gizli))
    print("liste", h(LISTE))
    print("PREEXISTING", h(PRE))
    print("film_labirent", film, film_n)
    print("defter sira", L[-1]["sira"], L[-1]["zaman"], "kafa", ozet)


if __name__ == "__main__":
    main()
