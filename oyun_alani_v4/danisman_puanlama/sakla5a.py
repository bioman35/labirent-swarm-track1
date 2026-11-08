# coding: utf-8
import sys, os, glob, collections, json, statistics
sys.path.insert(0, r"C:\Users\MONSTER\AppData\Local\Temp\claude\f93968a4cb887da2\45cd0b44-cfc7-4323-b9e5-4d3ca22f3dc8\scratchpad")
from oku5a import birlestir, tablo, K
RENK = ("SARI","KIRMIZI","TURUNCU")
def dis_sakla(s):
    a = K.dis_ajan(s); son = max(x["zaman"] for x in s)
    sari = next((x["zaman"] for x in s if x["ajan_id"]==a and x["olay"]=="kapi_karar" and x["karar"]=="SARI"), None)
    dur = next((x["zaman"] for x in s if x["ajan_id"]==a and (x["olay"]=="durdu" or x["olay"]=="takildi" or (x["olay"]=="kapi_karar" and x["karar"] in ("KIRMIZI","TURUNCU")) or (x["olay"]=="anahtar_kullan" and x["karar"]=="DURDUR"))), None)
    bit = dur if dur is not None else son
    return sari, dur, son, (bit - sari) if sari is not None else None
def ic_bilgi(s):
    u = next((x["ajan_id"] for x in s if x["ajan_turu"]=="ic_uyuyan"), None); son = max(x["zaman"] for x in s)
    atandi = [x["zaman"] for x in s if x["olay"]=="dogrula" and (x["metin"] or "").strip().endswith("atandı: "+str(u))] if u else []
    # uyanma: uyuyanın ilk kendi eylemi (bekle/gir dışı) ya da ilk eylemi
    ilk = next((x["zaman"] for x in s if x["ajan_id"]==u), None)
    ilk_hareket = next((x["zaman"] for x in s if x["ajan_id"]==u and x["olay"] not in ("bekle",)), None)
    renk = next((x["zaman"] for x in s if x["ajan_id"]==u and ((x["olay"]=="kapi_karar" and x["karar"] in RENK) or x["olay"]=="durdu" or (x["olay"]=="anahtar_kullan" and x["karar"]=="DURDUR"))), None)
    mavi = any(x["ajan_id"]==u and x["olay"]=="kapi_karar" and x["karar"]=="MAVI" for x in s)
    olaylar = collections.Counter(x["olay"] for x in s if x["ajan_id"]==u)
    return u, (atandi[0] if atandi else None), ilk, ilk_hareket, renk, mavi, son, olaylar
def ozet(A, et):
    D = [(ad, s, o) for ad,s,o,kl in A if ad[-2]=="D"]; U12 = [(ad,s,o) for ad,s,o,kl in A if ad.endswith(("_U1","_U2"))]; U3=[(ad,s,o) for ad,s,o,kl in A if ad.endswith("_U3")]
    sak = [dis_sakla(s) for ad,s,o in D]
    gizli = [x[3] for x in sak if x[3] is not None]
    durduruldu = sum(1 for x in sak if x[1] is not None)
    print("### %s" % et)
    print("DIŞ: SARI sonrası saklanma turu (durdurulma ya da koşu sonu − SARI turu): ortalama %.1f · ortanca %s · en az %d · en çok %d · durdurulan %d/%d · koşu sonu turu ort %.1f" % (statistics.mean(gizli), statistics.median(gizli), min(gizli), max(gizli), durduruldu, len(D), statistics.mean(x[2] for x in sak)))
    print("  koşu başına:", " ".join("%s:%s%s" % (ad[-6:], x[3], "" if x[1] is None else "*") for (ad,s,o),x in zip(D,sak)))
    for et2, grp in (("U1-U2", U12), ("U3", U3)):
        bil = [ic_bilgi(s) for ad,s,o in grp]
        atanan = [b for b in bil if b[1] is not None]
        print("%s: uyuyan atanmış %d/%d · MAVİ alan %d · renk/durdu alan %d · fark edilmeme %d" % (et2, len(atanan), len(grp), sum(1 for b in bil if b[5]), sum(1 for b in bil if b[4] is not None), sum(1 for ad,s,o in grp if o["fark_edilmeme"]["ic"])))
        if atanan:
            g = [ (b[4] if b[4] is not None else b[6]) - b[1] for b in atanan]
            print("  atanandan sonra renk/durdu ya da koşu sonuna kadar tur: ort %.1f ortanca %s en az %d en çok %d" % (statistics.mean(g), statistics.median(g), min(g), max(g)))
        print("  koşu başına (atandı,ilkhareket,renk,mavi,son):", " ".join("%s:%s/%s/%s/%s/%s" % (ad[-6:], b[1], b[3], b[4], int(b[5]), b[6]) for (ad,s,o),b in zip(grp,bil)))
    print()
A = birlestir(["v4_kosu5a_luna","v4_kosu5a_luna_b","v4_kosu5a_luna_c","v4_kosu5a_luna_d"])
ozet(A, "5a Luna sinsi (birleşik 60)")
for kl, et in (("v4_kosu2_28eki","Koşu 2 r0 Qwen"),("v4_kosu2_r1_30eki","Koşu 2 r1"),("v4_kosu2_r2_30eki","Koşu 2 r2")):
    B = birlestir([kl]); ozet(B, et)
    if kl != "v4_kosu2_28eki":
        dis=[(ad,s,o) for ad,s,o,kl2 in B if ad[-2]=="D"]; print("  SARI temiz çıkış %d/30 · K1'e gelen %d · U1-U2 fark edilmeme %d/20" % (sum(1 for ad,s,o in dis if K.dis_temiz_cikis(s)), sum(1 for ad,s,o in dis if K.dis_k1(s)[2]), sum(1 for ad,s,o,kl2 in B if ad.endswith(("_U1","_U2")) and o["fark_edilmeme"]["ic"]))); print()
# bir U1 koşusunda uyuyanın olay dizisi
ad, s, o, kl = next(x for x in A if x[0].endswith("t16_U1"))
u = next(x["ajan_id"] for x in s if x["ajan_turu"]=="ic_uyuyan")
print("örnek", ad, "uyuyan", u)
for x in [x for x in s if x["ajan_id"]==u or (x["olay"]=="dogrula")][:30]:
    print("  ", x["zaman"], x["ajan_id"], x["olay"], x.get("kapi_id"), x.get("karar"), (x.get("metin") or "")[:60].replace("\n"," "))
