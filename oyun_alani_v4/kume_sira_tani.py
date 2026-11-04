# coding: utf-8
"""KUME SIRA TANISI · 'tohum kumesi zor' ne demek · kayit ve dagitim okur, kosu degil, KESIF, kilitsiz (sonuc goruldukten sonra)
Soru: U1-U2 fark edilmeme, ic uyuyanin ilk atanan tasiyici olmasiyla mi geliyor? Tohum 36-45'te bu nasil dagiliyor?
Elle sayi yok. Calistir: python -I kume_sira_tani.py  -> KUME_SIRA_TANI_31eki.md"""
import collections
import glob
import json
import os
import re
import sys

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import kartlar as K  # noqa: E402

KL = os.path.join(KOK, "kosular")
CIKTI = "KUME_SIRA_TANI_31eki.md"
KUME = [("6-15", "Gece 3", "v4_e4_kosu2_t6_15_31eki"), ("16-25", "28 Eki", "v4_kosu2_28eki"), ("16-25", "tekrar 1", "v4_kosu2_r1_30eki"),
        ("16-25", "tekrar 2", "v4_kosu2_r2_30eki"), ("26-35", "G1", "v4_g1_kosu2_t26_35_30eki")]


def sira(t):
    d = dict(K.dagitim_kosu2(t))["U1"]
    return next(a for a, kod in d.items() if kod == "U1")


def ilk_atanan(f):
    for s in open(f, encoding="utf-8"):
        e = json.loads(s)
        m = re.fullmatch(r"atandı: (T\d)", (e.get("metin") or "").strip()) if e["olay"] == "dogrula" else None
        if m:
            return m[1]
    return None


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    out = ["# Küme sıra tanısı · 31 Ekim 2026 · KEŞİF · koşu değil, kilitsiz", "",
           "Üretici: kume_sira_tani.py. Sonuç görüldükten sonra yapıldı. Soru: \"tohum kümesi zor\" ne demek?", "",
           "## 1 · Uyuyan ilk atanan mı, fark edilmeme (U1-U2)", "",
           "| küme | ölçüm | ilk atanan uyuyan: kaçan | ilk atanan başkası: kaçan | ilk atanan uyuyan koşu payı |", "|---|---|---|---|---|"]
    top = collections.Counter()
    for toh, ad, k in KUME:
        c = collections.Counter()
        for f in glob.glob(os.path.join(KL, k, "v*_kosu2_*.jsonl")):
            a = re.sub(r"_r\d+$", "", os.path.basename(f)[:-len(".jsonl")])
            if not a.endswith(("_U1", "_U2")):
                continue
            o = json.load(open(f[:-len(".jsonl")] + ".olcum.json", encoding="utf-8"))
            uy = next(x for x, t in o["turler"].items() if t == "ic_uyuyan")
            g = "ilk" if ilk_atanan(f) == uy else "baska"
            c[g] += 1
            c[g + "_kac"] += bool(o["fark_edilmeme"]["ic"])
        top.update(c)
        out.append("| %s | %s | %d/%d | %d/%d | %d/%d |" % (toh, ad, c["ilk_kac"], c["ilk"], c["baska_kac"], c["baska"], c["ilk"], c["ilk"] + c["baska"]))
    out.append("| hepsi | | %d/%d | %d/%d | %d/%d |" % (top["ilk_kac"], top["ilk"], top["baska_kac"], top["baska"], top["ilk"], top["ilk"] + top["baska"]))
    out += ["", "## 2 · Uyuyanın sırası, tohum başına (dağıtım, koşu gerekmez)", "", "| küme | T1 | T2 | T3 |", "|---|---|---|---|"]
    for ad, ts in (("6-15", range(6, 16)), ("16-25", range(16, 26)), ("26-35", range(26, 36)), ("36-45", range(36, 46))):
        c = collections.Counter(sira(t) for t in ts)
        out.append("| %s | %d | %d | %d |" % (ad, c["T1"], c["T2"], c["T3"]))
    out += ["", "Tohum 36-45 sırası: " + " · ".join("t%d %s" % (t, sira(t)) for t in range(36, 46)) + ".", ""]
    metin = "\n".join(out) + "\n"
    with open(os.path.join(KOK, CIKTI), "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    print(metin)


if __name__ == "__main__":
    main()
