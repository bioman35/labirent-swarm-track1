# coding: utf-8
"""Sprint boyunca K1 MAVI kararlarının hepsi atanmış taşıyıcıya mı gitti? 5a (4 klasör, kopya dahil), 5b, 5c r0-r2, Koşu 4_b."""
import sys, os, glob, re, collections
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, KOK); sys.stdout.reconfigure(encoding="utf-8")
from kayit import oku
KL = ["v4_kosu4_luna_b", "v4_kosu5a_luna", "v4_kosu5a_luna_b", "v4_kosu5a_luna_c", "v4_kosu5a_luna_d", "v4_kosu5b_gemini", "v4_5c_puanli_r0", "v4_5c_puanli_r1", "v4_5c_puanli_r2"]
top = collections.Counter(); ornek = []
for k in KL:
    fs = sorted(glob.glob(os.path.join(KOK, "kosular", k, "v4_kosu*_t*.jsonl")))
    c = collections.Counter(); n = 0
    for f in fs:
        s = oku(f); atanan = set(); n += 1
        for x in s:
            if x["olay"] == "dogrula" and x["karar"] == "GECIR" and (x.get("metin") or "").startswith("atandı: "):
                atanan.add(x["metin"].split(": ", 1)[1])
            if x["olay"] == "kapi_karar" and x["kapi_id"] == "K1" and x["karar"] in ("MAVI", "GECIR"):
                a = x["ajan_id"]; tur = x["ajan_turu"]
                key = ("atanmış" if a in atanan else "ATANMAMIŞ", tur)
                c[key] += 1; top[key] += 1
                if a not in atanan: ornek.append((k, os.path.basename(f), x["zaman"], a, tur))
    print(k, "koşu", n, dict(c))
print("TOPLAM", dict(top)); print("atanmamış örnek:", ornek[:10])
