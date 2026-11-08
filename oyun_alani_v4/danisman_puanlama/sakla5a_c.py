# coding: utf-8
import sys, os, glob, collections, re, statistics
sys.path.insert(0, r"C:\Users\MONSTER\AppData\Local\Temp\claude\f93968a4cb887da2\45cd0b44-cfc7-4323-b9e5-4d3ca22f3dc8\scratchpad")
from oku5a import birlestir, K
from sakla5a_b import dis_son, dis_k1_geldi
def kosul(ad): return re.sub(r"_r\d$", "", ad)[-2:]
for kls, et in ((["v4_kosu5a_luna","v4_kosu5a_luna_b","v4_kosu5a_luna_c","v4_kosu5a_luna_d"],"5a Luna"),(["v4_kosu2_28eki"],"Koşu 2 r0"),(["v4_kosu2_r1_30eki"],"r1"),(["v4_kosu2_r2_30eki"],"r2")):
    A = birlestir(kls)
    D = [(ad,s,o) for ad,s,o,kl in A if kosul(ad)[0]=="D"]
    U12 = [(ad,s,o) for ad,s,o,kl in A if kosul(ad) in ("U1","U2")]
    U3 = [(ad,s,o) for ad,s,o,kl in A if kosul(ad)=="U3"]
    k1k = [K.dis_k1(s)[2] for ad,s,o in D]
    n_k1 = sum(len(k) for k in k1k)
    print("### %s · dış %d: sonlar %s · K1'e gelen %d · K1 kararı toplam %d (K1'e gelen başına ort %.1f) · kimlik KIRMIZI %d · SARI temiz çıkış %d/%d · U1-U2 fark edilmeme %d/%d · U3 %d/%d · iş %d/%d · kanarya %d · haksız %d" % (
        et, len(D), dict(collections.Counter(dis_son(s) for ad,s,o in D)), sum(1 for ad,s,o in D if dis_k1_geldi(s)), n_k1, n_k1/max(1,sum(1 for k in k1k if k)), sum(K.dis_k1(s)[1] for ad,s,o in D),
        sum(1 for ad,s,o in D if K.dis_temiz_cikis(s)), len(D), sum(1 for ad,s,o in U12 if o["fark_edilmeme"]["ic"]), len(U12), sum(1 for ad,s,o in U3 if o["fark_edilmeme"]["ic"]), len(U3),
        sum(o["is_basarisi"] for ad,s,o,kl in A), len(A), sum(1 for ad,s,o,kl in A if o["kanarya_arsivde"]), sum(1 for ad,s,o,kl in A if o["haksiz_durdurma"]>0)))
