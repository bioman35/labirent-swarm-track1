# coding: utf-8
"""KESIF · KUCUK EGRI (28 Eki, danisman): qwen2.5 3B ile 5 tohum (6-10), yalniz O1+O2b, ayni dunya v3.4.
Soru: hangi hata once geri geliyor. Ayni tohumlardaki 7B (sinav Kosu 1) ile karsilastirir. Elle sayi yok; kayitlari YALNIZ okur.
Kilitten sonra eklendi (defter kayit 4-5); tahmin kilidine girmez.

Calistir: python -I kesif_3b.py  ->  KESIF_3B_SONUC_28eki.md"""
import collections
import json
import os
import sys

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import sinir_haritasi as SH  # noqa: E402

TOHUM = range(6, 11)
MODELLER = [("3B", "kesif_3b_kosu1_28eki"), ("7B", "sinav_kosu1_27eki")]
AD = {t[0]: t[1] for t in SH.TURLER}


def oku(klasor, t):
    yol = os.path.join(KOK, "kosular", klasor, "v3_kosu1_O1_O2b_t%d" % t)
    ilk, top, soru, sonraki = {}, collections.Counter(), 0, collections.Counter()
    for s in open(yol + ".jsonl", encoding="utf-8"):
        d = json.loads(s)
        if d.get("olay") == "soru":
            soru += 1
            try:
                sonraki[(json.loads(d["metin"]).get("ikinci") or {}).get("eylem")] += 1
            except ValueError:
                pass
        if d.get("ajan_turu") != "bizim":
            continue
        for k, n in SH.say_satir(d).items():
            if n:
                top[k] += n
                ilk.setdefault(k, d.get("zaman", 0))
    olc = json.load(open(yol + ".olcum.json", encoding="utf-8"))
    if olc.get("asil_zarf_dustu"):
        top["geri_alinamaz"] += 1
    return {"is": bool(olc.get("is_basarisi")), "tur": olc.get("tur"), "ilk": ilk, "top": top, "soru": soru,
            "ikinci": sonraki}


def main():
    v = {m: {t: oku(k, t) for t in TOHUM} for m, k in MODELLER}
    out = ["# Keşif · küçük eğri (qwen2.5 3B)", "",
           "Üretici: `kesif_3b.py` (yalnız okur; elle sayı yok). Dünya v3.4, O1+O2b, tohum 6-10, sıcaklık 0. "
           "Kilitten sonra eklendi (defter kayıt 4-5); tahmin kilidine girmez. 7B sütunu aynı tohumlarda sınav Koşu 1.", "",
           "## İş", "", "| model | iş | koşu koşu (tur) |", "|---|---|---|"]
    for m, _ in MODELLER:
        out.append("| %s | %d/5 | %s |" % (m, sum(v[m][t]["is"] for t in TOHUM),
                                        " · ".join("t%d %s (%s)" % (t, "var" if v[m][t]["is"] else "yok", v[m][t]["tur"])
                                                   for t in TOHUM)))
    out += ["", "## Hangi hata önce geliyor (koşu içinde ilk görüldüğü tur)", "",
            "| tohum | 3B sıra | 7B sıra |", "|---|---|---|"]
    for t in TOHUM:
        h = []
        for m, _ in MODELLER:
            ilk = v[m][t]["ilk"]
            h.append(" → ".join("%s (tur %s)" % (AD[k], ilk[k]) for k in sorted(ilk, key=lambda k: ilk[k])) or "hata yok")
        out.append("| t%d | %s | %s |" % (t, h[0], h[1]))
    out += ["", "| model | ilk gelen hata (koşu sayısı) |", "|---|---|"]
    for m, _ in MODELLER:
        c = collections.Counter(min(v[m][t]["ilk"], key=lambda k: v[m][t]["ilk"][k]) for t in TOHUM if v[m][t]["ilk"])
        out.append("| %s | %s |" % (m, ", ".join("%s %d" % (AD[k], n) for k, n in c.most_common()) or "yok"))
    out += ["", "## Toplam hata (5 koşu)", "", "| hata türü | 3B | 7B |", "|---|---|---|"]
    for k, ad in AD.items():
        out.append("| %s | %d | %d |" % (ad, sum(v["3B"][t]["top"][k] for t in TOHUM), sum(v["7B"][t]["top"][k] for t in TOHUM)))
    out += ["", "## O2b sorusu ve ikinci cevap", "", "| model | soru sayısı | ikinci cevap olarak seçilen eylem |", "|---|---|---|"]
    for m, _ in MODELLER:
        c = sum((v[m][t]["ikinci"] for t in TOHUM), collections.Counter())
        out.append("| %s | %d | %s |" % (m, sum(v[m][t]["soru"] for t in TOHUM),
                                        ", ".join("%s %d" % (k, n) for k, n in c.most_common()) or "–"))
    open(os.path.join(KOK, "KESIF_3B_SONUC_28eki.md"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
