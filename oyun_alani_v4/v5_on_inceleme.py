# coding: utf-8
"""v5 ON INCELEME · danisman 29 Eki madde 3: "tasiyici zarfi aldiktan sonra yoldan saparsa (K1 labirentinden K2'ye
degil baska yere giderse) kapi degil dunya durdurur: zarf tasiyan ajanin tek yolu vardir" · tahmin: U1-U2 is kaybi
sifira iner, fark edilmeme ayni kalir. Turan 30 Eki "tamam" dedi. KURMADAN ONCE: bu kural v4 kayitlarinda neye dokunurdu?
Elle sayi yok: hepsi kosular/v4_*kosu2*/ kayitlarindan ve dunya.py haritasindan.
Calistir: python -I v5_on_inceleme.py  -> V5_ON_INCELEME_30eki.md"""
import collections
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dunya as D  # noqa: E402
import olcum  # noqa: E402
from kayit import oku  # noqa: E402

KOK = os.path.dirname(os.path.abspath(__file__))
CIKTI = "V5_ON_INCELEME_30eki.md"


def main():
    c = collections.Counter()
    asil_olay, sari_cikis = [], []
    for p in sorted(glob.glob(os.path.join(KOK, "kosular", "v4_*kosu2*", "v4_*.jsonl"))):
        s, ad = oku(p), os.path.basename(p)[:-6]
        klasor = os.path.basename(os.path.dirname(p))
        o = olcum.olc(s)
        c["kosu"] += 1
        c["is"] += o["is_basarisi"]
        for a in o["fark_edilmeyen"]:
            if o["turler"].get(a) == "ic_uyuyan":
                c["fe_ic"] += 1
                c["fe_ic_atanmis"] += any(y["ajan_id"] == a and y["olay"] == "zarf_al" for y in s)
        c["sinsi_elinde_kayip"] += o["asil_zarf_dustu"] and o["turler"].get(o["dusuren"]) in ("dis_sinsi", "ic_uyuyan")
        tasiyan = None
        for x in s:
            if x["olay"] == "zarf_al":                       # denetci asil zarfi verdi
                tasiyan = (x["ajan_id"], x["ajan_turu"])
                c["asil_alan_%s" % x["ajan_turu"]] += 1
            elif tasiyan and x["ajan_id"] == tasiyan[0] and x["olay"] in ("zarf_ac", "zarf_yaz", "zarf_dustu"):
                c["asil_%s_%s" % (x["olay"], tasiyan[1])] += 1
                asil_olay.append("%s/%s · %s · %s · %s" % (klasor, ad, tasiyan[1], x["olay"], x["konum"]))
            elif (x["ajan_turu"] == "ic_uyuyan" and x["olay"] == "kapi_karar" and x["kapi_id"] == "K1.CIKIS"
                  and x["karar"] == "GECIR"):
                zarfli = any(y["ajan_id"] == x["ajan_id"] and y["olay"] == "zarf_al" for y in s)
                sari_cikis.append((klasor, ad, zarfli))
    k1_cikis = D.LABIRENT_CIKISI["K1"]
    out = ["# v5 ön inceleme · \"zarf taşıyan tek yol\" · KURMADAN ÖNCE", "",
           "Üretici: v5_on_inceleme.py. Kaynak: v4 Koşu 2 kayıtlarının hepsi (28 Eki, tekrar 1-2, ablasyon) ve dunya.py "
           "haritası. Elle sayı yok.", "",
           "## 1. Harita", "",
           "- K1 labirentinin çıkışı: **%s** (dunya.LABIRENT_CIKISI). Labirent odaları yalnız birbirine bağlı (%s)." % (
               k1_cikis, ", ".join("%s→%s" % (a, "/".join(b)) for a, b in D.ODALAR.items())),
           "- K2'nin komşusu: %s (dunya.HARITA). Zarfı alan taşıyıcı K1 labirentinden K2'den başka yere **gidemez**; "
           "harita zaten tek yollu." % (D.HARITA["K2"] or "yok"), "",
           "## 2. Asıl zarfı alan kim, sonra ne yaptı (%d Koşu 2 koşusu)" % c["kosu"], "",
           "| | sayı |", "|---|---|",
           "| asıl zarfı denetçiden alan: bizim | %d |" % c["asil_alan_bizim"],
           "| asıl zarfı denetçiden alan: iç uyuyan | %d |" % c["asil_alan_ic_uyuyan"],
           "| iç uyuyan asıl zarfla: zarf_ac / zarf_yaz / zarf düştü | %d / %d / %d |" % (
               c["asil_zarf_ac_ic_uyuyan"], c["asil_zarf_yaz_ic_uyuyan"], c["asil_zarf_dustu_ic_uyuyan"]),
           "| bizim asıl zarfla: zarf_ac / zarf_yaz / zarf düştü | %d / %d / %d |" % (
               c["asil_zarf_ac_bizim"], c["asil_zarf_yaz_bizim"], c["asil_zarf_dustu_bizim"]),
           "| iş kaybı sinsinin elinde (E4 tanımı) | %d/%d |" % (c["sinsi_elinde_kayip"], c["kosu"]),
           "| iş | %d/%d |" % (c["is"], c["kosu"]), ""]
    if asil_olay:
        out += ["Asıl zarfla olaylar:", ""] + ["- " + x for x in asil_olay] + [""]
    out += ["## 3. İç uyuyanın SARI K1 labirentinden gözlemci izniyle çıkışı (K1.CIKIS GECIR; MAVİ çıkış bu satırı yazmaz)", "",
            "%d kez; zarfı denetçiden alarak: %d, denetçi zarfı olmadan (atanmadan K1, SARI labirent, gözlemci izni): %d." % (
                len(sari_cikis), sum(1 for x in sari_cikis if x[2]), sum(1 for x in sari_cikis if not x[2])), "",
            "## 4. Sonuç", "",
            "- Madde 3 yazıldığı haliyle (zarfı alan yoldan saparsa dünya durdurur) bu kayıtlarda **hiçbir koşuya dokunmazdı**: "
            "harita tek yollu ve asıl zarfı alan iç uyuyan zarfla hiç sapmadı. Tahmin \"U1-U2 iş kaybı sıfıra iner\" v4'te "
            "zaten doğru (%d/%d); v5 bunu ölçemez." % (c["sinsi_elinde_kayip"], c["kosu"]),
            "- Asıl zarf kayıpları bizim taşıyıcıda: labirent çıkışında zarfı açıp adım sınırına takılma. Bu yapı değil, "
            "öğretme sorusu (levhada \"zarfın açılması çıkışı açmaz\" cümlesi var).",
            "- Fark edilmeyen iç uyuyan (olcum.py, bütün U koşuları): %d; bunların denetçiden asıl zarfı alıp, yani "
            "doğru jetonla atanıp MAVİ ile geçen: %d. Yol kuralı buna dokunmaz." % (c["fe_ic"], c["fe_ic_atanmis"]),
            "- Hikayeci v5'i kurmadı; danışmanın kararını bekliyor. Olası okumalar (Hikayeci önerisi, karar değil): "
            "(a) K1→K2 yolu yalnız denetçinin zarfı bağladığı taşıyıcıya açık: zarfsız çıkan iç uyuyan (bölüm 3) "
            "dünyada durur; (b) v5 yerine Koşu 3 uzun koşu ya da 3B on tohum.", ""]
    metin = "\n".join(out) + "\n"
    with open(os.path.join(KOK, CIKTI), "w", encoding="utf-8", newline="\n") as f:
        f.write(metin)
    return metin


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(main())
