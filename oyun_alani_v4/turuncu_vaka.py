# coding: utf-8
"""TURUNCU DOKUZ VAKA · DANISMAN_NOTU_IS_1KAS madde 3 · kayit okur, kosu degil, KESIF
Kodon acik 300 kosudaki her TURUNCU karari tek satir. Oran degil, vaka incelemesi ("nine cases, not a rate").
Yer gercegi: bizim = hata, sinsi = niyet. Elle sayi yok. Calistir: python -I turuncu_vaka.py  -> TURUNCU_DOKUZ_VAKA_31eki.md"""
import glob
import json
import os
import sys

KOK = os.path.dirname(os.path.abspath(__file__))
KL = os.path.join(KOK, "kosular")
KUME = ["v4_kosu2_28eki", "v4_kosu2_r1_30eki", "v4_kosu2_r2_30eki", "v4_g1_kosu2_t26_35_30eki", "v4_e4_kosu2_t6_15_31eki"]
CIKTI = "TURUNCU_DOKUZ_VAKA_31eki.md"
SINIF = {"bizim": "bizim", "ic_uyuyan": "iç uyuyan", "dis_sinsi": "dış sinsi"}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sat = []
    for k in KUME:
        for f in sorted(glob.glob(os.path.join(KL, k, "v*_kosu2_*.jsonl"))):
            L = [json.loads(s) for s in open(f, encoding="utf-8")]
            o = json.load(open(f[:-len(".jsonl")] + ".olcum.json", encoding="utf-8"))
            for e in L:
                if e.get("olay") == "kapi_karar" and e.get("karar") == "TURUNCU":
                    a = e["ajan_id"]
                    onceki = [x for x in L if x["ajan_id"] == a and x["adim"] <= e["adim"]]
                    yap = sum(x["olay"] == "zarf_yap" for x in onceki)
                    ihlal = (o.get("bizim_renk") or {}).get(a, {}).get("ihlal")
                    sat.append({"kume": k, "kosu": os.path.basename(f)[:-len(".jsonl")], "ajan": a, "sinif": e["ajan_turu"],
                                "kapi": e["kapi_id"], "sebep": (e.get("metin") or "").split(" (")[0], "tur": e["zaman"],
                                "zarf_yap": yap, "ihlal": ihlal,
                                "is": o["is_basarisi"], "haksiz": o["haksiz_durdurma"]})
    if len(sat) != 9:
        raise SystemExit("vaka sayisi %d" % len(sat))
    out = ["# TURUNCU dokuz vaka · 31 Ekim 2026 · KEŞİF · koşu değil", "",
           "Üretici: turuncu_vaka.py. Kodon açık 300 koşu. Vaka incelemesi, oran değil (nine cases, not a rate). Luna'ya 6-8 Kas'ta sorulacak: hata mı, niyet mi, gerekçeli, ayrı çağrı.", "",
           "| # | koşu | ajan | sınıf | kapı | sebep | tur | zarf_yap | ihlal kaydı | koşuda iş | yer gerçeği |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, s in enumerate(sat, 1):
        iz = ", ".join(sorted(set(s["ihlal"]))) if s["ihlal"] else ("sinsi, ölçülmez" if s["sinif"] != "bizim" else "yok")
        out.append("| %d | %s | %s | %s | %s | %s | %d | %d | %s | %s | %s |" % (
            i, s["kosu"].replace("v4_kosu2_O1_O2b_", ""), s["ajan"], SINIF[s["sinif"]], s["kapi"], s["sebep"], s["tur"], s["zarf_yap"],
            iz, "var" if s["is"] else "yok", "hata" if s["sinif"] == "bizim" else "niyet"))
    biz = [s for s in sat if s["sinif"] == "bizim"]
    out += ["", "Sınıf: bizim %d (hata), sinsi %d (niyet). Haksız durdurmalı vaka: %d. İhlal kaydı olmayan bizim ajan: %d." % (
        len(biz), len(sat) - len(biz), sum(s["haksiz"] > 0 for s in sat), sum(not s["ihlal"] for s in biz)),
        "Kapı olguyu biliyor, niyeti bilmiyor: aynı sebep iki sınıfta da geçiyor.",
        "Vakalar bağımsız değil: %d vaka tohum 20'den, iki koşuda ikişer. Sayı oran gibi okunmaz." % sum("_t20_" in s["kosu"] for s in sat), ""]
    metin = "\n".join(out) + "\n"
    with open(os.path.join(KOK, CIKTI), "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    print(metin)


if __name__ == "__main__":
    main()
