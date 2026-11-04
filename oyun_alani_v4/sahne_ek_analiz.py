# coding: utf-8
"""SAHNE SINAVI EK ANALIZ · sonuc gorulduktan SONRA yazildi (kilitli olcu degil, KESIF) · yalniz kosular/sahne_30eki/ kayitlarindan.
Ilk eylem ve oda yollari: model cikisa takilinca ne yapiyor, zarf disinda nerede kaliyor.
Calistir: python -I sahne_ek_analiz.py  -> SAHNE_SINAVI_EK_30eki.md"""
import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kayit import oku  # noqa: E402

KOK = os.path.dirname(os.path.abspath(__file__))
KLASOR = os.path.join(KOK, "kosular", "sahne_30eki")
KOLLAR = ("eski", "dunya", "dunya_ogretme")


def main():
    with open(os.path.join(KLASOR, "sonuc.jsonl"), encoding="utf-8") as f:
        sat = [json.loads(s) for s in f]
    ilk = {k: collections.Counter() for k in KOLLAR}
    oda = {k: collections.Counter() for k in KOLLAR}
    gidip = {k: 0 for k in KOLLAR}
    istek = {k: 0 for k in KOLLAR}
    ikinci = {k: collections.Counter() for k in KOLLAR}
    for r in sat:
        k = r["kol"]
        s = oku(os.path.join(KLASOR, r["kosu_id"] + ".jsonl"))
        ilk[k][r["ilk"]] += 1
        kon = [x["konum"].split(".")[-1] for x in s if x["ajan_id"] == "T1" and x["olay"] == "gir" and x["konum"].count(".") == 2]
        for o in set(kon):
            oda[k][o] += 1
        gidip[k] += any(a == "CIKIS" for a in kon)       # ODA2'den yeniden cikisa dondu
        sorular = [json.loads(x["metin"]) for x in s if x["olay"] == "soru"]
        z = [q for q in sorular if q["tur"] == "zarf_ac"]
        istek[k] += bool(z)
        for q in z:
            ikinci[k][(q["ikinci"] or {}).get("eylem")] += 1
    out = ["# Sahne sınavı · ek analiz · sonuç görüldükten SONRA · KEŞİF", "",
           "Üretici: sahne_ek_analiz.py. Kilitli ölçü değil. Yalnız kosular/sahne_30eki/ kayıtlarından, kol başına 50 mini koşu.", "",
           "| ölçü | eski metin | yalnız dünya | dünya + öğretme |", "|---|---|---|---|"]
    for ad in ("git", "bekle"):
        out.append("| ilk eylem %s | " % ad + " | ".join(str(ilk[k][ad]) for k in KOLLAR) + " |")
    out.append("| ilk eylem başka | " + " | ".join(str(sum(v for a, v in ilk[k].items() if a not in ("git", "bekle"))) for k in KOLLAR) + " |")
    for o in ("ODA2", "CIKIS", "ODA1", "ODA3"):
        out.append("| %s'e girdi (mini koşu) | " % o + " | ".join(str(oda[k][o]) for k in KOLLAR) + " |")
    out.append("| ODA2'den yeniden çıkışa döndü | " + " | ".join(str(gidip[k]) for k in KOLLAR) + " |")
    out.append("| en az bir kez zarf açmak istedi (soru tetiklendi) | " + " | ".join(str(istek[k]) for k in KOLLAR) + " |")
    out.append("| soru sonrası son cevap zarf_ac | " + " | ".join(str(ikinci[k]["zarf_ac"]) for k in KOLLAR) + " |")
    out.append("")
    metin = "\n".join(out) + "\n"
    with open(os.path.join(KOK, "SAHNE_SINAVI_EK_30eki.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return metin


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(main())
