# coding: utf-8
import sys, os, glob, collections, json, statistics
sys.path.insert(0, r"C:\Users\MONSTER\AppData\Local\Temp\claude\f93968a4cb887da2\45cd0b44-cfc7-4323-b9e5-4d3ca22f3dc8\scratchpad")
from oku5a import birlestir, K, KOK
import olcum
from kayit import oku
def dis_son(s):
    a = K.dis_ajan(s)
    for x in s:
        if x["ajan_id"]!=a: continue
        if x["olay"]=="durdu": return "durdu:"+str(x.get("renk"))
        if x["olay"]=="takildi": return "takildi"
        if x["olay"]=="kapi_karar" and x["karar"] in ("KIRMIZI","TURUNCU"): return x["kapi_id"]+":"+x["karar"]
        if x["olay"]=="anahtar_kullan" and x["karar"]=="DURDUR": return "anahtar_DURDUR"
    return "serbest_bitti"
def dis_k1_geldi(s):
    v = K.dis_k1(s); return bool(v and v[2])
for kls, et in ((["v4_kosu5a_luna","v4_kosu5a_luna_b","v4_kosu5a_luna_c","v4_kosu5a_luna_d"],"5a Luna"),(["v4_kosu2_28eki"],"Koşu 2 r0"),(["v4_kosu2_r1_30eki"],"r1"),(["v4_kosu2_r2_30eki"],"r2")):
    A = birlestir(kls)
    if not A: print(et, "BOŞ", glob.glob(os.path.join(KOK, kls[0], "*"))[:3]); continue
    D = [(ad,s,o) for ad,s,o,kl in A if "_D" in ad[-3:]]
    sonlar = collections.Counter(dis_son(s) for ad,s,o in D)
    k1 = sum(1 for ad,s,o in D if dis_k1_geldi(s))
    temiz = sum(1 for ad,s,o in D if K.dis_temiz_cikis(s))
    serbest_k1siz = sum(1 for ad,s,o in D if dis_son(s)=="serbest_bitti" and not dis_k1_geldi(s))
    U12=[(ad,s,o) for ad,s,o,kl in A if ad.endswith(("_U1","_U2"))]
    print("### %s · dış %d: sonlar %s · K1'e gelen %d · SARI temiz çıkış %d · K1'e gelmeden serbest biten %d · U1-U2 fark edilmeme %d/%d · iş %d/%d · iş yok: %s" % (et, len(D), dict(sonlar), k1, temiz, serbest_k1siz, sum(1 for ad,s,o in U12 if o["fark_edilmeme"]["ic"]), len(U12), sum(o["is_basarisi"] for ad,s,o,kl in A), len(A), [ad[-6:] for ad,s,o,kl in A if not o["is_basarisi"]]))
# Koşu 1 t17 Qwen vs Koşu 4 t17 Luna: ayrışma yeri
for p in (os.path.join(KOK,"v4_kosu1_28eki"), os.path.join(KOK,"v4_kosu4_luna_b")):
    for f in sorted(glob.glob(os.path.join(p,"v4_*t17*.jsonl"))):
        s = oku(f); o = olcum.olc(s)
        print(os.path.basename(f), "iş", o["is_basarisi"], "takıldı", o["takildi"], "durdu", o["durdu"], "bizim_renk", {a:v["kararlar"] for a,v in o["bizim_renk"].items()}, "soru", o["soru"], "zarf_iade", o["zarf_iade"], "adim", o["adim"], "tur", o["tur"], "zarf düştü", o["asil_zarf_dustu"], o["dusuren"])
        son = [x for x in s if x["olay"] in ("zarf_dustu","takildi","durdu","zarf_birak","zarf_al","zarf_yap","cikis")]
        print("   ", " · ".join("%s %s %s %s" % (x["zaman"], x["ajan_id"], x["olay"], (x.get("metin") or "")[:40].replace("\n"," ")) for x in son[:14]))
