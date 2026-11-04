# coding: utf-8
"""LUNA SIZINTI OLCUMU · ozet taniminin dayanagi · 31 Eki · yalniz kayit okur, model cagrisi yok, KESIF.
Kume: ablasyonsuz kodon acik 300 kosu. Soru: kayittaki hangi alan etiketi Luna'ya sizdirir?
Elle sayi yok. Calistir: python -I luna_sizinti_olc.py  -> LUNA_SIZINTI_31eki.txt"""
import collections
import glob
import json
import os
import re
import sys

KOK = os.path.dirname(os.path.abspath(__file__))
KL = os.path.join(KOK, "kosular")
KUME = ["v4_kosu2_28eki", "v4_kosu2_r1_30eki", "v4_kosu2_r2_30eki", "v4_g1_kosu2_t26_35_30eki", "v4_e4_kosu2_t6_15_31eki"]
CIKTI = "LUNA_SIZINTI_31eki.txt"
RENK = re.compile(r"MAVI|SARI|KIRMIZI|TURUNCU")
HEDEF = re.compile(r"hedef", re.I)


def main():
    c = collections.Counter()
    tepe = collections.Counter()
    for k in KUME:
        for f in sorted(glob.glob(os.path.join(KL, k, "v*_kosu2_*.jsonl"))):
            ad = re.sub(r"_r\d+$", "", os.path.basename(f)[:-len(".jsonl")])
            sinif = ad[-2:]
            o = json.load(open(f[:-len(".jsonl")] + ".olcum.json", encoding="utf-8"))
            kac = bool(o["fark_edilmeme"]["ic"])
            c["kosu"] += 1
            c["D" if sinif[0] == "D" else ("U12" if sinif != "U3" else "U3")] += 1
            if sinif[0] == "U":
                c[("kacan" if kac else "yakalanan") + ("_U3" if sinif == "U3" else "_U12")] += 1
            hedefli = collections.Counter()
            for s in open(f, encoding="utf-8"):
                e = json.loads(s)
                t, i = e["ajan_turu"], e["ajan_id"]
                if RENK.search(e.get("konum") or ""):
                    c["konumda_renk_olay"] += 1
                if e.get("renk") or e.get("olay") == "kapi_karar":
                    c["karar_renk_olay"] += 1
                if t in ("bizim", "ic_uyuyan") and HEDEF.search(e.get("ajan_aciklamasi") or ""):
                    hedefli[(t, i)] += 1
                if e.get("olay") in ("zarf_yap", "zarf_yaz"):
                    c["zarf_metin_" + t] += 1
                    if "KAN-" in (e.get("metin") or ""):
                        c["zarf_metin_kanarya_" + t] += 1
                if sinif[0] == "D" and t == "dis_sinsi":
                    c["s1_olay"] += 1
                tok = (e.get("maliyet") or {}).get("token") or 0
                if k.startswith("v4_e4") and e.get("olay") != "soru":
                    tepe[t] = max(tepe[t], tok)
            ic = [x for x in hedefli if x[0] == "ic_uyuyan"]
            biz = [x for x in hedefli if x[0] == "bizim" and x[1].startswith("T")]
            if sinif[0] == "U":
                d = "kacan" if kac else "yakalanan"
                c["hedef_uyuyan_" + d + ("_U3" if sinif == "U3" else "_U12")] += bool(ic)
            c["hedef_bizim_tasiyici_ajan"] += len(biz)
            c["bizim_tasiyici_ajan"] += 2 if sinif[0] == "U" else 3
    out = ["LUNA SIZINTI OLCUMU · ablasyonsuz kodon acik 300 kosu · uretici luna_sizinti_olc.py", ""]
    for k in sorted(c):
        out.append("%s = %d" % (k, c[k]))
    out += ["", "Gece 3 tek olayda en cok token (soru haric): " + str(dict(tepe)), ""]
    metin = "\n".join(out)
    with open(os.path.join(KOK, CIKTI), "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return metin


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(main())
