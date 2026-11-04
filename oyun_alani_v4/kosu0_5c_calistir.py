# coding: utf-8
"""5c KOSU 0 · Turan onayi 31 Eki · tohum 1-3, D1 D4 U1 U4, 12 kosu · puanli degil · 0xC0000142 gelirse 60 sn bekleyip 3 kez dener."""
import subprocess
import sys
import time

V4 = r"C:\Users\MONSTER\Desktop\sprint\oyun_alani_v4"
Q7 = "qwen2.5:7b-instruct-q4_K_M"
subprocess.run(["ollama", "stop", Q7], capture_output=True)
print("%s · KOSU0 BASLADI" % time.strftime("%H:%M:%S"), flush=True)
for deneme in range(4):
    r = subprocess.run([sys.executable, "-I", "-u", "kosu_5c.py", "--asama", "kosu0", "--tasiyici", "yerel", "--model", Q7,
                        "--tohumlar", "1-3", "--cikti", "kosular/v4_5c_kosu0_31eki"], cwd=V4)
    if r.returncode != 3221225794:
        break
    print("0xC0000142, 60 sn sonra tekrar", flush=True)
    time.sleep(60)
print("%s · KOSU0 BITTI · kod %s" % (time.strftime("%H:%M:%S"), r.returncode), flush=True)
