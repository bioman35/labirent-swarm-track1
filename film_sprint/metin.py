# coding: utf-8
"""SPRINT FILMI · metin uretici · FILM_METNI_8KAS.md ve ANLATIM_EN_8KAS.txt -> veri/sprint.js
Filmdeki her yazi (baslik, epigraf, bolum kapagi, kart, dip) metin dosyasindan birebir alinir; kodda yazi yok.
Anlatim sureleri: ses/anlatim_N.wav varsa olculur (kaynak "ses"), yoksa sozcuk / 2.5 sn tahmini (kaynak "tahmin").
Calistir: python -I metin.py"""
import json
import os
import re
import sys
import wave

KOK = os.path.dirname(os.path.abspath(__file__))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    m = open(os.path.join(KOK, "FILM_METNI_8KAS.md"), encoding="utf-8").read()
    L = m.split("\n")

    def satir(bas):
        r = [l for l in L if l.startswith(bas)]
        return r

    baslik = re.search(r"^KART \(EN\): \*\*(.+?)\*\*$", m, re.M).group(1)
    alt = re.search(r"^Alt yazı \(EN\): (.+)$", m, re.M).group(1)
    ep = re.search(r'^EPİGRAF.*?EN büyük: "(.+?)" TR küçük: "(.+?)"', m, re.M)
    bolum = []
    for l in satir("Bölüm kapağı (EN): "):
        g = re.match(r"Bölüm kapağı \(EN\): \*\*(\d) · (.+?)\*\*(?: · Alt yazı: (.+))?$", l)
        bolum.append({"no": g.group(1), "ad": g.group(2), "alt": g.group(3) or ""})
    kartlar = [l.split(": ", 1)[1] for l in L if re.match(r"^KART( \d)? \(EN\): (?!\*\*)", l)]
    # bolum 1-5 birer kart, bolum 6 iki kart
    assert len(kartlar) == 7, len(kartlar)
    for i in range(5):
        bolum[i]["kart"] = [kartlar[i]]
    bolum[5]["kart"] = kartlar[5:7]
    bolum[5]["kartDip"] = re.search(r"^Kart 2 altına küçük yazı \(EN\): (.+)$", m, re.M).group(1)
    i = L.index(next(l for l in L if l.startswith("KART (EN, tek ekran")))
    kapanis = [L[i + j][2:] for j in (1, 2, 3)]
    assert all(L[i + j].startswith("- ") for j in (1, 2, 3))
    dip = re.search(r"^Son ekran \(EN, küçük yazı\): (.+)$", m, re.M).group(1)
    an = [p.strip() for p in open(os.path.join(KOK, "ANLATIM_EN_8KAS.txt"), encoding="utf-8").read().split("\n\n") if p.strip()]
    assert len(an) == 8, len(an)
    anlatim = []
    for n, p in enumerate(an):
        w = os.path.join(KOK, "ses", "anlatim_%d.wav" % n)
        if os.path.exists(w):
            with wave.open(w, "rb") as f:
                s, kay = f.getnframes() / f.getframerate(), "ses"
        else:
            s, kay = round(len(p.split()) / 2.5, 2), "tahmin"
        anlatim.append({"metin": p, "sure": round(s, 3), "kaynak": kay})
    veri = {"baslik": baslik, "alt": alt, "epigraf": {"en": ep.group(1), "tr": ep.group(2)}, "bolum": bolum, "kapanis": kapanis, "dip": dip, "anlatim": anlatim}
    os.makedirs(os.path.join(KOK, "veri"), exist_ok=True)
    with open(os.path.join(KOK, "veri", "sprint.js"), "w", encoding="utf-8", newline="\n") as h:
        h.write("window.SPRINT=" + json.dumps(veri, ensure_ascii=False, separators=(",", ":")) + ";\n")
    for b in bolum:
        print(b["no"], b["ad"], "|", b["alt"][:40], "| kart", len(b["kart"]))
    for n, a in enumerate(anlatim):
        print("anlatim", n, a["sure"], a["kaynak"], len(a["metin"].split()), "sozcuk")


if __name__ == "__main__":
    main()
