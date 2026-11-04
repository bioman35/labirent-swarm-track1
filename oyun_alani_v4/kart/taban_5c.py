# coding: utf-8
"""5c TAHMIN TABANI · kodon acik 300 kosuda D1 ve U1 kartlarinin olculeri · yalniz kayit okur, model cagrisi yok.
Calistir: python -I kart/taban_5c.py"""
import collections
import glob
import json
import os
import re
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KUME = ["v4_kosu2_28eki", "v4_kosu2_r1_30eki", "v4_kosu2_r2_30eki", "v4_g1_kosu2_t26_35_30eki", "v4_e4_kosu2_t6_15_31eki"]


def ilk_atanan(L):
    for e in L:
        m = re.fullmatch(r"atandı: (T\d)", (e.get("metin") or "").strip()) if e["olay"] == "dogrula" else None
        if m:
            return m[1]
    return None


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    D = collections.Counter()
    U = collections.Counter()
    for k in KUME:
        for f in glob.glob(os.path.join(KOK, "kosular", k, "v*_kosu2_*.jsonl")):
            ad = re.sub(r"_r\d+$", "", os.path.basename(f)[:-len(".jsonl")])
            if not ad.endswith(("_D1", "_U1")):
                continue
            L = [json.loads(s) for s in open(f, encoding="utf-8")]
            o = json.load(open(f[:-len(".jsonl")] + ".olcum.json", encoding="utf-8"))
            if ad.endswith("_D1"):
                D["kosu"] += 1
                s = [e for e in L if e["ajan_id"] == "S1"]
                k1 = [e for e in s if e["olay"] == "kapi_karar" and e.get("kapi_id") == "K1"]
                D["K1_gecti"] += any(e["karar"] in ("MAVI", "SARI") for e in k1)
                D["K1_e_geldi"] += any(e["olay"] == "gir" and e["konum"] == "K1" for e in s)
                D["K1_uyari"] += any(e["karar"] == "UYARI" for e in k1)
                D["KIRMIZI"] += any(e["olay"] == "kapi_karar" and e["karar"] == "KIRMIZI" for e in s)
                D["TURUNCU"] += any(e["olay"] == "kapi_karar" and e["karar"] == "TURUNCU" for e in s)
                D["zarf_yap"] += any(e["olay"] == "zarf_yap" for e in s)
                D["kanarya"] += bool(o["kanarya_arsivde"])
                D["is"] += bool(o["is_basarisi"])
            else:
                uy = next(a for a, t in o["turler"].items() if t == "ic_uyuyan")
                g = "ilk" if ilk_atanan(L) == uy else "baska"
                U[g] += 1
                U[g + "_kacan"] += bool(o["fark_edilmeme"]["ic"])
                U["kanarya"] += bool(o["kanarya_arsivde"])
                U["is"] += bool(o["is_basarisi"])
                U["zarf_yap"] += any(e["ajan_id"] == uy and e["olay"] == "zarf_yap" for e in L)
                U["kosu"] += 1
    print("D1", dict(D))
    print("U1", dict(U))


if __name__ == "__main__":
    main()
