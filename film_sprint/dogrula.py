# coding: utf-8
"""SPRINT FILMI · bitmis VIDEO denetimi (ses dosyasi degil video, kod_film 5 Kas dersi).
Her anlatim paragrafi plan.json'daki aninda videodan kesilir, faster_whisper large-v3 (cuda) ile okunur, ANLATIM_EN ile karsilastirilir.
Paragraflarin arasindaki bosluklarda konusma olmamali. python -I dogrula.py [video]"""
import difflib
import json
import os
import re
import subprocess
import sys

from faster_whisper import WhisperModel

KOK = os.path.dirname(os.path.abspath(__file__))
VID = os.path.join(KOK, sys.argv[1] if len(sys.argv) > 1 else "SPRINT_FILMI.mp4")
plan = json.load(open(os.path.join(KOK, "plan.json"), encoding="utf-8"))
an = [p.strip() for p in open(os.path.join(KOK, "ANLATIM_EN_8KAS.txt"), encoding="utf-8").read().split("\n\n") if p.strip()]
M = WhisperModel("large-v3", device="cuda", compute_type="float16")
kes = os.path.join(KOK, "_kes.wav")
SAYI = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}
sade = lambda m: re.sub(r"[^a-z0-9 ]", " ", m.lower().replace("seven-b", "7b").replace("seven b", "7b")).split()
sayisiz = lambda w: [SAYI.get(x, x) for x in w]
sys.stdout.reconfigure(encoding="utf-8")


def oku(bas, sure, vad=False):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.3f" % max(0, bas), "-t", "%.3f" % sure, "-i", VID, "-vn", "-ac", "1", "-ar", "16000", kes], check=True)
    s, _ = M.transcribe(kes, language="en", beam_size=5, vad_filter=vad)
    return " ".join(x.text.strip() for x in s)


tamam = 0
for p in plan:
    n, b, d = p["anlatim"], p["anlatimBas"], p["anlatimSure"]
    duy = oku(b - .15, d + .4)
    a, h = sayisiz(sade(an[n])), sayisiz(sade(duy))
    o = difflib.SequenceMatcher(None, a, h).ratio()
    ok = o >= .97
    tamam += ok
    print("%-9s %7.2f-%7.2f benzerlik %.3f %s" % (p["ad"], b, b + d, o, "TAMAM" if ok else "BAK"))
    for op in difflib.SequenceMatcher(None, a, h).get_opcodes():
        if op[0] != "equal":
            print("     ", op[0], " ".join(a[op[1]:op[2]]), "->", " ".join(h[op[3]:op[4]]))
# paragraf disi bosluklarda konusma
bos = []
son = 0.0
for p in plan:
    if p["anlatimBas"] - son > 2:
        bos.append((son + .5, p["anlatimBas"] - .5))
    son = p["anlatimBas"] + p["anlatimSure"]
taşan = 0
for x, y in bos:
    for i in range(int((y - x) // 25) + 1):
        a0 = x + i * 25
        d = min(25, y - a0)
        if d < 1:
            continue
        m = oku(a0, d, vad=True).strip()   # sessizlikte whisper uydurmasin
        if m and len(m.split()) > 1:
            taşan += 1
            print("  BOSLUKTA KONUSMA %.1f-%.1f: %s" % (a0, a0 + d, m[:120]))
print("sonuc: %d / %d paragraf; boslukta konusma %d" % (tamam, len(plan), taşan))
os.remove(kes)
