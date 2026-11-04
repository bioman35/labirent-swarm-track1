# coding: utf-8
"""ozet_tablo.jsonl -> kosul basina tablo (markdown) · yalniz olcum ciktisindan, kayda yeniden bakmadan
Calistir: python -I kosu_ozet.py kosular/<klasor>   -> <klasor>/OZET.md"""
import json
import os
import sys

SIRA = ["taban", "O1", "O2", "O3", "hepsi", "O1_O2b"]


def durdurma(k):
    return sum(1 for ks in k.values() for _, karar in ks if karar == "DURDUR")


def tablo(satirlar):
    kosullar = [k for k in SIRA if any(s["kosul"] == k for s in satirlar)] + \
               sorted({s["kosul"] for s in satirlar} - set(SIRA))
    out = ["| koşul | koşu | iş | takılan | durdur | SARI/KIRMIZI/TURUNCU (bizim) | haksız | ort. tur | çağrı | geçersiz JSON | yol yok | süre (dk) |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in kosullar:
        ss = [s for s in satirlar if s["kosul"] == k]
        renk = sum(1 for s in ss for v in s["bizim_renk"].values() for x in v["kararlar"])
        out.append("| %s | %d | %d/%d | %d | %d | %d | %d | %.1f | %d | %d | %d | %.1f |" % (
            k, len(ss), sum(s["is"] for s in ss), len(ss), sum(len(s["takildi"]) for s in ss),
            sum(durdurma(s["kararlar"]) for s in ss), renk, sum(s["haksiz"] for s in ss),
            sum(s["tur"] for s in ss) / len(ss), sum(s["cagri"] for s in ss), sum(s["gecersiz"] for s in ss),
            sum(s["yol_yok"] for s in ss), sum(s["sure_duvar_sn"] for s in ss) / 60))
    return "\n".join(out)


def ayrinti(satirlar):
    out = ["| koşu | iş | tur | takılan | duran | kapı kararları |", "|---|---|---|---|---|---|"]
    for s in satirlar:
        kar = "; ".join("%s: %s" % (a, " ".join("%s %s" % (k, r) for k, r in ks)) for a, ks in s["kararlar"].items())
        out.append("| %s | %s | %d | %s | %s | %s |" % (s["kosu_id"], "var" if s["is"] else "yok", s["tur"],
                                                     ", ".join(s["takildi"]) or "-",
                                                     ", ".join("%s %s" % x for x in s["durdu"].items()) or "-", kar))
    return "\n".join(out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    klasor = sys.argv[1]
    with open(os.path.join(klasor, "ozet_tablo.jsonl"), encoding="utf-8") as f:
        satirlar = [json.loads(x) for x in f if x.strip()]
    with open(os.path.join(klasor, "kosu_meta.json"), encoding="utf-8") as f:
        meta = json.load(f)
    m = ["# %s · özet" % os.path.basename(klasor.rstrip("/\\")), "",
         "Model: %s (özet %s) · taşıyıcı %s · sıcaklık %s · kart %s · kural %s · sistem mesajı %s" % (
             meta["model"], ((meta.get("model_kimlik") or {}).get("ozet") or "-")[:12], meta["tasiyici"],
             meta["sicaklik"], meta["kart_ozet"][:12], meta["kural_ozet"][:12], meta["sistem_mesaji_ozet"][:12]),
         "", tablo(satirlar), "", "## Koşu koşu", "", ayrinti(satirlar), ""]
    with open(os.path.join(klasor, "OZET.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(m))
    print("\n".join(m))
