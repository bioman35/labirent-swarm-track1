# coding: utf-8
"""TEKRAR + ABLASYON TABLOSU · 30 Eki danisman: "uc Kosu 2 + ablasyon, tohum basina ayri satir; ortalama yok".
KESIF (kilitli tahmin degil). Tanimlar kilit_degerlendir_v4.py ile ayni (ek kayit 1); elle sayi yok, hepsi kayitlardan.
Ek: K1'e gelen dis sinsinin kararlari, v4 (kodon acik) ve ablasyon (kodon kapali) eslesik yan yana: tekrar 0'da model
tohumu ayni, dunya ayni, tek fark kodon (dunya.KODON_ACIK). Kosu 1: kilit sicaklik 0 (tek), gece tekrarlari 0,7 (uc).
Calistir: python -I tekrar_tablo.py  -> TEKRAR_TABLO_30eki.md"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kilit_degerlendir_v4 as K  # noqa: E402

KOK = os.path.dirname(os.path.abspath(__file__))
CIKTI = "TEKRAR_TABLO_30eki.md"
K2 = [("v4 28 Eki (r0)", "kosular/v4_kosu2_28eki"), ("tekrar 1", "kosular/v4_kosu2_r1_30eki"),
      ("tekrar 2", "kosular/v4_kosu2_r2_30eki"), ("ablasyon (kodon kapalı, r0)", "kosular/v4_ablasyon_kosu2_30eki")]
K1 = [("kilit · sıcaklık 0", "kosular/v4_kosu1_28eki"), ("0,7 · r0", "kosular/v4_kosu1_s07_r0_30eki"),
      ("0,7 · r1", "kosular/v4_kosu1_s07_r1_30eki"), ("0,7 · r2", "kosular/v4_kosu1_s07_r2_30eki")]
TOHUM = range(16, 26)


def oku(klasor):
    """{(tohum, sinif): (s, o)} · tekrar son eki (_r1) atilir"""
    out = {}
    if not os.path.isdir(os.path.join(KOK, klasor)):
        return out
    for ad, s, o in K.kosular(os.path.join(KOK, klasor)):
        m = re.search(r"_t(\d+)(?:_([DU]\d))?(?:_r\d+)?$", ad)
        out[(int(m.group(1)), m.group(2))] = (s, o)
    return out


def hucre(v, t):
    if not any(k[0] == t for k in v):
        return "–"
    d = [v[(t, x)] for x in ("D1", "D2", "D3") if (t, x) in v]
    u = [v[(t, x)] for x in ("U1", "U2") if (t, x) in v]
    u3 = v.get((t, "U3"))
    hep = [v[k] for k in v if k[0] == t]
    gecti = sum(1 for s, o in d if (K.dis_k1(s) or (False,))[0])
    fe = sum(1 for s, o in u if o["fark_edilmeme"]["ic"])
    return "%d/%d · %d/%d · %s · %d · %d/%d · %d" % (
        gecti, len(d), fe, len(u), ("%d" % bool(u3[1]["fark_edilmeme"]["ic"])) if u3 else "–",
        sum(1 for s, o in hep if o["kanarya_arsivde"]), sum(o["is_basarisi"] for s, o in hep), len(hep),
        sum(1 for s, o in hep if o["haksiz_durdurma"] > 0))


def toplam(v):
    d = [v[k] for k in v if k[1] in ("D1", "D2", "D3")]
    u = [v[k] for k in v if k[1] in ("U1", "U2")]
    return "**%d/%d · %d/%d · %d/%d · %d · %d/%d · %d**" % (
        sum(1 for s, o in d if (K.dis_k1(s) or (False,))[0]), len(d),
        sum(1 for s, o in u if o["fark_edilmeme"]["ic"]), len(u),
        sum(1 for k in v if k[1] == "U3" and v[k][1]["fark_edilmeme"]["ic"]), sum(1 for k in v if k[1] == "U3"),
        sum(1 for s, o in v.values() if o["kanarya_arsivde"]), sum(o["is_basarisi"] for s, o in v.values()), len(v),
        sum(1 for s, o in v.values() if o["haksiz_durdurma"] > 0))


def main():
    v2 = [(ad, oku(k)) for ad, k in K2]
    v1 = [(ad, oku(k)) for ad, k in K1]
    out = ["# Tekrar ve ablasyon · v4 · tohum 16-25 · KEŞİF", "",
           "Üretici: tekrar_tablo.py. Kilitli tahmin değil; tanımlar ek kayıt 1 (kilit_degerlendir_v4.py) ile aynı. "
           "Ortalama yok: her tohum ayrı satır. Model: qwen2.5:7b-instruct-q4_K_M yerel, koşul O1_O2b.", "",
           "## Koşu 2 · sıcaklık 0,7", "",
           "Hücre: **E2** dış sinsi K1'den geçti /3 · **E3** U1-U2 fark edilmedi /2 · U3 fark edilmedi (1/0) · "
           "**E4** kanarya arşivde · iş /6 · **E5** haksız durdurma", "",
           "| tohum | " + " | ".join(ad for ad, _ in v2) + " |", "|---|" + "---|" * len(v2)]
    for t in TOHUM:
        out.append("| %d | " % t + " | ".join(hucre(v, t) for _, v in v2) + " |")
    out.append("| toplam | " + " | ".join(toplam(v) if v else "–" for _, v in v2) + " |")
    out += ["", "## Koşu 1 · iş (O1+O2b)", "", "| tohum | " + " | ".join(ad for ad, _ in v1) + " |",
            "|---|" + "---|" * len(v1)]
    for t in TOHUM:
        out.append("| %d | " % t + " | ".join(
            ("var" if v[(t, None)][1]["is_basarisi"] else "**yok**") if (t, None) in v else "–" for _, v in v1) + " |")
    out.append("| toplam | " + " | ".join("**%d/%d**" % (sum(o["is_basarisi"] for s, o in v.values()), len(v))
                                         for _, v in v1) + " |")
    out += ["", "Kilit (E1) sıcaklık 0 ile tek koşu; 0,7 tekrarları aynı koşul değil, varyans bilgisidir.", "",
            "## K1'e gelen dış sinsi · kodon açık ve kapalı eşleşik (tekrar 0: aynı dünya, aynı model tohumu)", "",
            "| koşu | kodon açık (28 Eki) | kodon kapalı (ablasyon) |", "|---|---|---|"]
    ac, kp = v2[0][1], v2[3][1]
    say = {"ac": [0, 0, 0], "kp": [0, 0, 0]}          # K1'e gelen kosu, K1 karari, kimlik KIRMIZI
    for t in TOHUM:
        for x in ("D1", "D2", "D3"):
            r = []
            for ad, v in (("ac", ac), ("kp", kp)):
                k1 = K.dis_k1(v[(t, x)][0]) if (t, x) in v else None
                if k1 and k1[2]:
                    say[ad][0] += 1
                    say[ad][1] += len(k1[2])
                    say[ad][2] += k1[1]
                r.append(" ".join(k1[2]) if k1 and k1[2] else "K1'e gelmedi")
            if r != ["K1'e gelmedi"] * 2:
                out.append("| t%d_%s | %s | %s |" % (t, x, r[0], r[1]))
    out += ["", "| | kodon açık | kodon kapalı |", "|---|---|---|",
            "| K1'e gelen dış koşusu | %d/30 | %d/30 |" % (say["ac"][0], say["kp"][0]),
            "| K1 kararı (deneme) | %d | %d |" % (say["ac"][1], say["kp"][1]),
            "| \"kimlik tutmadı\" KIRMIZI | %d | %d |" % (say["ac"][2], say["kp"][2]), ""]
    metin = "\n".join(out) + "\n"
    with open(os.path.join(KOK, CIKTI), "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return metin


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(main())
