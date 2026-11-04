# coding: utf-8
"""31 Eki ucuncu gece zinciri · TAHMIN_KILIDI_EK4_GECE3_31eki.md · YALNIZ defter kaydindan sonra.
Sira kilitte yazili: K1 Kosu 1, K1 Kosu 2, K2 a, K2 b. 0xC0000142 gelirse 60 sn bekleyip 3 kez yeniden dener."""
import subprocess
import sys
import time

V4 = r"C:\Users\MONSTER\Desktop\sprint\oyun_alani_v4"
Q7 = "qwen2.5:7b-instruct-q4_K_M"
Q3 = "qwen2.5:3b-instruct-q4_K_M"


def dur():
    for m in (Q7, Q3):
        subprocess.run(["ollama", "stop", m], capture_output=True)


def kos(ad, arg):
    print("%s · %s BASLADI" % (time.strftime("%H:%M:%S"), ad), flush=True)
    for deneme in range(4):
        r = subprocess.run([sys.executable, "-I", "kosu_model.py", "--tasiyici", "yerel"] + arg, cwd=V4)
        if r.returncode != 3221225794:
            break
        print("%s · %s 0xC0000142, 60 sn sonra tekrar" % (time.strftime("%H:%M:%S"), ad), flush=True)
        time.sleep(60)
    print("%s · %s BITTI · kod %s" % (time.strftime("%H:%M:%S"), ad, r.returncode), flush=True)


def q3(klasor, tohum):
    return ["--kosu", "1", "--model", Q3, "--tohumlar", tohum, "--kosullar", "O1_O2b", "--cikti", "kosular/" + klasor]


dur()
kos("K1 KOSU1 T6-15 QWEN7B", ["--kosu", "1", "--model", Q7, "--tohumlar", "6-15", "--kosullar", "O1_O2b,taban",
                              "--cikti", "kosular/v4_e4_kosu1_t6_15_31eki"])
kos("K1 KOSU2 T6-15 QWEN7B", ["--kosu", "2", "--model", Q7, "--tohumlar", "6-15", "--kosullar", "O1_O2b",
                              "--cikti", "kosular/v4_e4_kosu2_t6_15_31eki"])
for t in range(6, 16):
    dur()
    kos("K2a T%d" % t, q3("v4_e4_3b_tek_t%d_31eki" % t, str(t)))
dur()
kos("K2b S1 T6-7 AYNI SUREC", q3("v4_e4_3b_b1_31eki", "6-7"))
dur()
kos("K2b S2 T6", q3("v4_e4_3b_b2_t6_31eki", "6"))
kos("K2b S2 T7 DURDURMADAN", q3("v4_e4_3b_b2_t7_31eki", "7"))
dur()
kos("K2b S3 T6", q3("v4_e4_3b_b3_t6_31eki", "6"))
dur()
kos("K2b S3 T7 DURDURARAK", q3("v4_e4_3b_b3_t7_31eki", "7"))
print("%s · ZINCIR TAMAM" % time.strftime("%H:%M:%S"), flush=True)
