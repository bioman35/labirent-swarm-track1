# coding: utf-8
import sys, collections
sys.path.insert(0, r"C:\Users\MONSTER\AppData\Local\Temp\claude\f93968a4cb887da2\45cd0b44-cfc7-4323-b9e5-4d3ca22f3dc8\scratchpad")
from oku5a import birlestir, K
sys.stdout.reconfigure(encoding="utf-8")
for kls, et in ((["v4_kosu5b_gemini"], "5b Gemini"), (["v4_kosu5a_luna", "v4_kosu5a_luna_b", "v4_kosu5a_luna_c", "v4_kosu5a_luna_d"], "5a Luna"), (["v4_kosu2_28eki"], "Koşu 2 r0")):
    A = birlestir(kls)
    kan_es = 0; kan_var = 0; sinsi_zy = 0; bizim_zy_sonra = 0; bizim_zy_once = 0; ayni_konum = 0; bizim_zy_kosu = 0; sinsi_zy_kosu = 0; birlikte = 0
    konumlar = collections.Counter(); bizim_konum = collections.Counter(); ilk_bizim_zy_metin = collections.Counter()
    for ad, s, o, kl in A:
        turler = {x["ajan_id"]: x["ajan_turu"] for x in s if x["ajan_turu"] != "betik"}
        kanarya = next((x["metin"].split(": ", 1)[1] for x in s if x["olay"] == "mesaj" and x["konum"] == "GIRIS_ARSIV" and (x["metin"] or "").startswith("kanarya: ")), None)
        szy = [x for x in s if x["olay"] == "zarf_yap" and turler.get(x["ajan_id"]) in ("dis_sinsi", "ic_uyuyan")]
        bzy = [x for x in s if x["olay"] == "zarf_yap" and turler.get(x["ajan_id"]) == "bizim"]
        sinsi_zy += len(szy);
        if szy: sinsi_zy_kosu += 1
        if bzy: bizim_zy_kosu += 1
        if szy and bzy: birlikte += 1
        for x in szy:
            konumlar[x.get("konum")] += 1
            if kanarya and kanarya in (x.get("metin") or ""): kan_es += 1
            if "KAN-" in (x.get("metin") or ""): kan_var += 1
        for x in bzy:
            bizim_konum[x.get("konum")] += 1
            ilk_bizim_zy_metin[(x.get("metin") or "")[:45]] += 1
            if szy and x["zaman"] > min(y["zaman"] for y in szy): bizim_zy_sonra += 1
            else: bizim_zy_once += 1
    print("### %s · sinsi zarf_yap %d (koşu %d) konum %s · metinde KAN- %d · kanaryayla eş %d" % (et, sinsi_zy, sinsi_zy_kosu, dict(konumlar), kan_var, kan_es))
    print("   bizim zarf_yap %d (koşu %d; sinsiyle aynı koşu %d) · sinsinin ilk zarf_yap'ından SONRA %d, önce/sinsisiz %d · konum %s" % (sum(bizim_konum.values()), bizim_zy_kosu, birlikte, bizim_zy_sonra, bizim_zy_once, dict(bizim_konum)))
    print("   bizim zarf_yap metinleri:", ilk_bizim_zy_metin.most_common(8))
# kanarya örneği ve sinsinin zarf_yap kaydının tam hali (5b t17_D1)
A = birlestir(["v4_kosu5b_gemini"])
ad, s, o, kl = next(x for x in A if x[0].endswith("t17_D1"))
kanarya = next((x["metin"] for x in s if x["olay"] == "mesaj" and x["konum"] == "GIRIS_ARSIV"), None)
print("t17_D1 kanarya mesajı:", kanarya)
for x in s:
    if x["olay"] == "zarf_yap":
        print("  ", x["zaman"], x["ajan_id"], x["konum"], "metin:", (x.get("metin") or "")[:80].replace("\n", " "), "zarf:", str(x.get("zarf"))[:120])
# bizim T2'nin zarf_yap'tan önceki 3 olayı ve gördüğü şey (onceki_ozet)
for x in s:
    if x["olay"] == "zarf_yap" and x["ajan_id"] in ("T2", "T3"):
        print("  ", x["ajan_id"], "önceki özet:", (x.get("onceki_ozet") or "")[:300].replace("\n", " "))
        break
