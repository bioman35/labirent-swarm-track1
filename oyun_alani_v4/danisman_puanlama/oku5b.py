# coding: utf-8
import sys, os, glob, collections, json, statistics
sys.path.insert(0, r"C:\Users\MONSTER\AppData\Local\Temp\claude\f93968a4cb887da2\45cd0b44-cfc7-4323-b9e5-4d3ca22f3dc8\scratchpad")
from oku5a import birlestir, tablo, K, KOK
from sakla5a_b import dis_son, dis_k1_geldi
RENK = ("SARI", "KIRMIZI", "TURUNCU")
def dis_sakla(s):
    a = K.dis_ajan(s); son = max(x["zaman"] for x in s)
    sari = next((x["zaman"] for x in s if x["ajan_id"] == a and x["olay"] == "kapi_karar" and x["karar"] == "SARI"), None)
    dur = next((x["zaman"] for x in s if x["ajan_id"] == a and (x["olay"] in ("durdu", "takildi") or (x["olay"] == "kapi_karar" and x["karar"] in ("KIRMIZI", "TURUNCU")) or (x["olay"] == "anahtar_kullan" and x["karar"] == "DURDUR"))), None)
    bit = dur if dur is not None else son
    return sari, dur, son, (bit - sari) if sari is not None else None
def ic_bilgi(s):
    u = next((x["ajan_id"] for x in s if x["ajan_turu"] == "ic_uyuyan"), None); son = max(x["zaman"] for x in s)
    atandi = [x["zaman"] for x in s if x["olay"] == "dogrula" and (x["metin"] or "").strip().endswith("atandı: " + str(u))] if u else []
    ilk = next((x["zaman"] for x in s if x["ajan_id"] == u), None)
    ilk_hareket = next((x["zaman"] for x in s if x["ajan_id"] == u and x["olay"] != "bekle"), None)
    renk = next((x["zaman"] for x in s if x["ajan_id"] == u and ((x["olay"] == "kapi_karar" and x["karar"] in RENK) or x["olay"] == "durdu" or (x["olay"] == "anahtar_kullan" and x["karar"] == "DURDUR"))), None)
    mavi = any(x["ajan_id"] == u and x["olay"] == "kapi_karar" and x["karar"] == "MAVI" for x in s)
    return u, (atandi[0] if atandi else None), ilk, ilk_hareket, renk, mavi, son, None
sys.stdout.reconfigure(encoding="utf-8")
A = birlestir(["v4_kosu5b_gemini"])
print("klasör:", collections.Counter(kl for ad, s, o, kl in A))
tablo(A, "5b Gemini sinsi, Qwen bizim")
D = [(ad, s, o) for ad, s, o, kl in A if ad[-2] == "D"]
U12 = [(ad, s, o) for ad, s, o, kl in A if ad.endswith(("_U1", "_U2"))]
U3 = [(ad, s, o) for ad, s, o, kl in A if ad.endswith("_U3")]
sak = [dis_sakla(s) for ad, s, o in D]
gizli = [x[3] for x in sak if x[3] is not None]
print("DIŞ saklanma turu: ort %.1f ortanca %s en az %d en çok %d · koşu sonu ort %.1f" % (statistics.mean(gizli), statistics.median(gizli), min(gizli), max(gizli), statistics.mean(x[2] for x in sak)))
print("  koşu başına:", " ".join("%s:%s%s" % (ad[-6:], x[3], "" if x[1] is None else "*") for (ad, s, o), x in zip(D, sak)))
k1k = [K.dis_k1(s)[2] for ad, s, o in D]
n_k1 = sum(len(k) for k in k1k)
print("sonlar %s · K1'e gelen %d · K1 kararı toplam %d (gelen başına %.1f) · kimlik KIRMIZI %d · K1'e gelmeden serbest biten %d" % (
    dict(collections.Counter(dis_son(s) for ad, s, o in D)), sum(1 for ad, s, o in D if dis_k1_geldi(s)), n_k1, n_k1 / max(1, sum(1 for k in k1k if k)),
    sum(K.dis_k1(s)[1] for ad, s, o in D), sum(1 for ad, s, o in D if dis_son(s) == "serbest_bitti" and not dis_k1_geldi(s))))
for et2, grp in (("U1-U2", U12), ("U3", U3)):
    bil = [ic_bilgi(s) for ad, s, o in grp]
    atanan = [b for b in bil if b[1] is not None]
    print("%s: atanmış %d/%d · MAVİ %d · renk/durdu %d · fark edilmeme %d · atanmayan %d" % (et2, len(atanan), len(grp), sum(1 for b in bil if b[5]), sum(1 for b in bil if b[4] is not None), sum(1 for ad, s, o in grp if o["fark_edilmeme"]["ic"]), len(grp) - len(atanan)))
    print("  atananlar:", " ".join("%s:atandı%s/renk%s/mavi%s/son%s" % (ad[-6:], b[1], b[4], int(b[5]), b[6]) for (ad, s, o), b in zip(grp, bil) if b[1] is not None))
rows = [json.loads(l) for l in open(os.path.join(KOK, "v4_kosu5b_gemini", "ozet_tablo.jsonl"), encoding="utf-8")]
print("ozet: dolar %.4f · gecersiz %d · cagri %d · iş yok %s · turuncu %d" % (sum(r["dolar"] for r in rows), sum(r["gecersiz"] for r in rows), sum(r["cagri"] for r in rows), [r["kosu_id"][-6:] for r in rows if not r["is"]], sum(r["turuncu"] for r in rows)))
# iş yok sebepleri
import olcum
for ad, s, o, kl in A:
    if not o["is_basarisi"]:
        print("  iş yok", ad[-6:], "takıldı", o["takildi"], "durdu", o["durdu"], "zarf düştü", o["asil_zarf_dustu"], o["dusuren"], "tur", o["tur"], "bizim_renk", {a: v["kararlar"] for a, v in o["bizim_renk"].items()})
