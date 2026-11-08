# coding: utf-8
"""SPRINT FILMI · ses. Kodla ses uretilmez: yalniz anlatim kaydi (Yaprak, bizim ses programi) yerine konur.
python -I karis.py bol      ses/ klasorundeki tek kaydi (anlatim_tam.*) paragraf aralarindaki 7 en uzun sessizlikten 8 parcaya boler
                           -> ses/anlatim_0..7.wav; her parcanin sozcuk hizi denetlenir, tutmazsa durur
python -I karis.py birlestir   goruntu.mp4 + ses/anlatim_N.wav, plan.json'daki baslangic anlarina -> SPRINT_FILMI.mp4
Sira: (bol) -> python -I metin.py -> python -I cik.py tam -> python -I karis.py birlestir"""
import glob
import json
import os
import re
import subprocess
import sys

KOK = os.path.dirname(os.path.abspath(__file__))
SES = os.path.join(KOK, "ses")


def sure(yol):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", yol], capture_output=True, text=True).stdout.strip())


def bol():
    tam = [y for y in glob.glob(os.path.join(SES, "anlatim_tam.*"))]
    assert len(tam) == 1, "ses/anlatim_tam.* tek dosya olmali: %s" % tam
    tam = tam[0]
    S = sure(tam)
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", tam, "-af", "silencedetect=noise=-38dB:d=0.45", "-f", "null", "-"], capture_output=True, text=True).stderr
    bas = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]
    son = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    ara = [(b, e) for b, e in zip(bas, son) if b > .5 and e < S - .5]
    en = sorted(sorted(ara, key=lambda x: x[1] - x[0], reverse=True)[:7])
    assert len(en) == 7, "yeterli sessizlik yok: %d" % len(en)
    kes = [0.0] + [(b + e) / 2 for b, e in en] + [S]
    an = [p for p in open(os.path.join(KOK, "ANLATIM_EN_8KAS.txt"), encoding="utf-8").read().split("\n\n") if p.strip()]
    sz = [len(p.split()) for p in an]
    hiz = sum(sz) / S
    print("toplam", round(S, 2), "sn", sum(sz), "sozcuk", round(hiz, 2), "sozcuk/sn")
    for i in range(8):
        d = kes[i + 1] - kes[i]
        oran = (sz[i] / d) / hiz
        print(i, "%.2f-%.2f" % (kes[i], kes[i + 1]), "%.2f sn" % d, sz[i], "sozcuk", "oran %.2f" % oran, "ara %.2f sn" % ((en[i][1] - en[i][0]) if i < 7 else 0))
        assert .6 < oran < 1.6, "parca %d sozcuk hizi tutmuyor, elle bakilmali" % i
    for i in range(8):
        a, b = kes[i], kes[i + 1]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tam, "-ss", "%.3f" % a, "-to", "%.3f" % b, "-af",
                        "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
                        "-ac", "1", "-ar", "48000", os.path.join(SES, "anlatim_%d.wav" % i)], check=True)
    print("bolundu: ses/anlatim_0..7.wav")


def birlestir():
    plan = json.load(open(os.path.join(KOK, "plan.json"), encoding="utf-8"))
    gor = os.path.join(KOK, "goruntu.mp4")
    girdi, fil = ["-i", gor], []
    for j, p in enumerate(plan):
        w = os.path.join(SES, "anlatim_%d.wav" % p["anlatim"])
        assert os.path.exists(w), w
        assert abs(sure(w) - p["anlatimSure"]) < .05, "plan eski: once metin.py ve cik.py tam (%s)" % w
        girdi += ["-i", w]
        ms = int(round(p["anlatimBas"] * 1000))
        fil.append("[%d:a]aresample=48000,adelay=%d|%d[a%d]" % (j + 1, ms, ms, j))
    fil.append("".join("[a%d]" % j for j in range(len(plan))) + "amix=inputs=%d:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[ses]" % len(plan))
    cik = os.path.join(KOK, "SPRINT_FILMI.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *girdi, "-filter_complex", ";".join(fil), "-map", "0:v", "-map", "[ses]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", cik], check=True)
    print("tamam", cik, round(sure(cik), 2), "sn")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    {"bol": bol, "birlestir": birlestir}[sys.argv[1]]()
