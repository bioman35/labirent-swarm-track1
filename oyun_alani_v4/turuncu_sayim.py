# coding: utf-8
"""TURUNCU SAYIM · Luna yargic on hazirligi · 31 Eki · yalniz kayit okur, kosu degil, KESIF.
Soru (danisman): Kosu 2'de TURUNCU'ya giden kac ajan var, Luna'nin yer gercegi ne?
Elle sayi yok. Calistir: python -I turuncu_sayim.py  -> TURUNCU_SAYIM_31eki.md"""
import collections
import glob
import json
import os
import re
import sys

KOK = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.join(KOK, "..", "oyun_alani_v3", "kosular")
KL = os.path.join(KOK, "kosular")
CIKTI = "TURUNCU_SAYIM_31eki.md"
KUME = [("v3.4 t6-15", "kodon yok", os.path.join(V3, "sinav_kosu2_27eki")),
        ("v4 t16-25 ablasyon", "kodon kapalı", os.path.join(KL, "v4_ablasyon_kosu2_30eki")),
        ("v4 t16-25 28 Eki", "kodon açık", os.path.join(KL, "v4_kosu2_28eki")),
        ("v4 t16-25 tekrar 1", "kodon açık", os.path.join(KL, "v4_kosu2_r1_30eki")),
        ("v4 t16-25 tekrar 2", "kodon açık", os.path.join(KL, "v4_kosu2_r2_30eki")),
        ("v4 t26-35 G1", "kodon açık", os.path.join(KL, "v4_g1_kosu2_t26_35_30eki")),
        ("v4 t6-15 Gece 3", "kodon açık", os.path.join(KL, "v4_e4_kosu2_t6_15_31eki"))]
TUR = ("bizim", "ic_uyuyan", "dis_sinsi")


def kume(d):
    r = {"kosu": 0, "tk": 0, "tur": collections.Counter(), "sebep": collections.Counter(), "bizim_haksiz": 0,
         "u12": 0, "u3": 0, "D": 0, "U": 0, "sinsisiz": 0}
    for f in sorted(glob.glob(os.path.join(d, "v*_kosu2_*.jsonl"))):
        r["kosu"] += 1
        vardi = False
        for s in open(f, encoding="utf-8"):
            e = json.loads(s)
            if e.get("olay") == "kapi_karar" and e.get("karar") == "TURUNCU":
                vardi = True
                r["tur"][e.get("ajan_turu")] += 1
                r["sebep"][(e.get("metin") or "").split(" (")[0]] += 1
        r["tk"] += vardi
        o = json.load(open(f[:-len(".jsonl")] + ".olcum.json", encoding="utf-8"))
        ad = re.sub(r"_r\d+$", "", os.path.basename(f)[:-len(".jsonl")])
        r[ad[-2]] += 1
        if not set(o["turler"].values()) & {"ic_uyuyan", "dis_sinsi"}:
            r["sinsisiz"] += 1
        r["bizim_haksiz"] += o["haksiz_durdurma"] > 0
        if o["fark_edilmeme"]["ic"]:
            r["u3" if ad.endswith("_U3") else "u12"] += 1
    return r


def topla(rs, anahtar):
    return sum(r[anahtar] for r in rs)


def tt(rs, t):
    return sum(r["tur"][t] for r in rs)


def main():
    sk = [(ad, tip, kume(d)) for ad, tip, d in KUME]
    out = ["# TURUNCU sayımı · Luna yargıç ön hazırlığı · 31 Ekim 2026 · KEŞİF", "",
           "Üretici: turuncu_sayim.py. Koşu değil, yalnız kayıt okunur. Sayılar `kapi_karar` olaylarından ve `.olcum.json` dosyalarından.", "",
           "| küme | dünya | koşu | TURUNCU'lu koşu | bizim | iç uyuyan | dış sinsi | kaçan U1-U2 | kaçan U3 |",
           "|---|---|---|---|---|---|---|---|---|"]
    for ad, tip, r in sk:
        out.append("| %s | %s | %d | %d | %d | %d | %d | %d | %d |" % (
            ad, tip, r["kosu"], r["tk"], r["tur"]["bizim"], r["tur"]["ic_uyuyan"], r["tur"]["dis_sinsi"], r["u12"], r["u3"]))
    gruplar = [("kodon açık", [r for a, t, r in sk if t == "kodon açık"]),
               ("danışmanın 240 kümesi (28 Eki, tekrar 1-2, ablasyon)",
                [r for a, t, r in sk if a in ("v4 t16-25 28 Eki", "v4 t16-25 tekrar 1", "v4 t16-25 tekrar 2", "v4 t16-25 ablasyon")]),
               ("hepsi", [r for a, t, r in sk])]
    out += ["", "| grup | koşu | D | U | sinsisiz koşu | TURUNCU kararı | bizim | iç uyuyan | dış sinsi | kaçan U1-U2 | kaçan U3 |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    for ad, rs in gruplar:
        b, i, d = tt(rs, "bizim"), tt(rs, "ic_uyuyan"), tt(rs, "dis_sinsi")
        out.append("| %s | %d | %d | %d | %d | %d | %d | %d | %d | %d | %d |" % (
            ad, topla(rs, "kosu"), topla(rs, "D"), topla(rs, "U"), topla(rs, "sinsisiz"), b + i + d, b, i, d, topla(rs, "u12"), topla(rs, "u3")))
    seb = collections.Counter()
    for a, t, r in sk:
        if t == "kodon açık":
            seb.update(r["sebep"])
    out += ["", "Kodon açık kümede TURUNCU sebepleri: " + " · ".join("%s %d" % kv for kv in seb.most_common()) + ".",
            "Haksız durdurmalı koşu, bütün kümelerde: %d." % topla([r for a, t, r in sk], "bizim_haksiz"), ""]
    metin = "\n".join(out) + "\n"
    with open(os.path.join(KOK, CIKTI), "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return metin


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(main())
