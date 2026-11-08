# coding: utf-8
import sys, collections
sys.path.insert(0, r"C:\Users\MONSTER\AppData\Local\Temp\claude\f93968a4cb887da2\45cd0b44-cfc7-4323-b9e5-4d3ca22f3dc8\scratchpad")
from oku5a import birlestir, K
sys.stdout.reconfigure(encoding="utf-8")
for kls, et in ((["v4_kosu5b_gemini"], "5b Gemini"), (["v4_kosu5a_luna", "v4_kosu5a_luna_b", "v4_kosu5a_luna_c", "v4_kosu5a_luna_d"], "5a Luna"), (["v4_kosu2_28eki"], "Koşu 2 r0"), (["v4_kosu2_r1_30eki"], "r1"), (["v4_kosu2_r2_30eki"], "r2")):
    A = birlestir(kls)
    tur_say = collections.Counter(); sebep = collections.Counter(); zarf_yap = collections.Counter(); kosu_tur = []
    teslim = collections.Counter()
    for ad, s, o, kl in A:
        turler = {x["ajan_id"]: x["ajan_turu"] for x in s if x["ajan_turu"] != "betik"}
        for x in s:
            if x["olay"] == "kapi_karar" and x["karar"] == "TURUNCU":
                tur_say[turler.get(x["ajan_id"], "?")] += 1
                sebep[(turler.get(x["ajan_id"], "?"), (x["metin"] or "")[:30])] += 1
                kosu_tur.append(ad[-6:] + ":" + x["ajan_id"])
            if x["olay"] == "zarf_yap":
                zarf_yap[turler.get(x["ajan_id"], "?")] += 1
            if x["olay"] in ("zarf_birak", "zarf_al", "teslim", "ver") and turler.get(x["ajan_id"]) in ("dis_sinsi", "ic_uyuyan"):
                teslim[(x["olay"], (x["metin"] or "")[:25])] += 1
    print("### %s · TURUNCU ajan türüne göre %s · sebepler %s" % (et, dict(tur_say), dict(sebep)))
    print("   TURUNCU koşu:ajan", " ".join(kosu_tur))
    print("   zarf_yap türe göre %s · sinsi zarf olayları %s" % (dict(zarf_yap), dict(teslim)))
# 5b'de bizim TURUNCU alan koşularda sahte mührün kaynağı: S1'in zarf_yap / zarf_birak izleri
A = birlestir(["v4_kosu5b_gemini"])
for ad, s, o, kl in A:
    bz = [a for a, v in o["bizim_renk"].items() if any(k[1] == "TURUNCU" for k in v["kararlar"])]
    if not bz: continue
    sinsi = [x for x in s if x["ajan_turu"] in ("dis_sinsi", "ic_uyuyan") and x["olay"] in ("zarf_yap", "zarf_birak", "zarf_al", "mesaj", "oner", "yonlendir", "goster")]
    print(ad[-6:], "bizim TURUNCU", bz, "ihlal", {a: o["bizim_renk"][a]["ihlal"] for a in bz})
    for x in sinsi[:8]:
        print("    ", x["zaman"], x["ajan_id"], x["olay"], x.get("konum"), (x.get("metin") or "")[:90].replace("\n", " "))
    for x in [x for x in s if x["ajan_id"] in bz and x["olay"] in ("zarf_al", "zarf_yap", "kapi_karar") ][:6]:
        print("      ", x["zaman"], x["ajan_id"], x["olay"], x.get("kapi_id"), x.get("karar"), (x.get("metin") or "")[:70].replace("\n", " "))
