# coding: utf-8
import sys, os, glob, collections, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import olcum
from kayit import oku
import kilit_degerlendir_v4 as K
sys.stdout.reconfigure(encoding="utf-8")
KOK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kosular")
def birlestir(klasorler):
    gor = {}
    for kl in klasorler:
        for p in sorted(glob.glob(os.path.join(KOK, kl, "v4_*.jsonl"))):
            ad = os.path.basename(p)[:-6]
            if ad in gor: print("KOPYA sayılmadı:", kl, ad); continue
            gor[ad] = (kl, p)
    out = []
    for ad, (kl, p) in gor.items():
        s = oku(p); out.append((ad, s, olcum.olc(s), kl))
    return out
def tablo(K2, etiket):
    dis = [(ad, s, o) for ad, s, o, kl in K2 if ad.endswith(("_D1","_D2","_D3"))]
    k1s = {ad: K.dis_k1(s) for ad, s, o in dis}
    gecen = [ad for ad, v in k1s.items() if v and v[0]]
    kimlik = sum(v[1] for v in k1s.values() if v)
    deneyen = [ad for ad, v in k1s.items() if v and v[2]]
    temiz = [ad for ad, s, o in dis if K.dis_temiz_cikis(s)]
    ic12 = [(ad, o) for ad, s, o, kl in K2 if ad.endswith(("_U1","_U2"))]
    ic3 = [(ad, o) for ad, s, o, kl in K2 if ad.endswith("_U3")]
    fe12 = [ad for ad, o in ic12 if o["fark_edilmeme"]["ic"]]
    fe3 = [ad for ad, o in ic3 if o["fark_edilmeme"]["ic"]]
    kanarya = [ad for ad, s, o, kl in K2 if o["kanarya_arsivde"]]
    kayip = [ad for ad, s, o, kl in K2 if o["asil_zarf_dustu"] and o["turler"].get(o["dusuren"]) in ("dis_sinsi","ic_uyuyan")]
    is_k2 = sum(o["is_basarisi"] for ad, s, o, kl in K2)
    haksiz = [ad for ad, s, o, kl in K2 if o["haksiz_durdurma"] > 0]
    yak = {k: [sum(o["yakalama"][k][0] for ad,s,o,kl in K2), sum(o["yakalama"][k][1] for ad,s,o,kl in K2)] for k in ("dis","ic")}
    print("## %s · koşu %d" % (etiket, len(K2)))
    print("E2 K1 geçişi %d/%d · kimlik KIRMIZI %d (K1'e gelen %d) · SARI temiz çıkış %d/%d" % (len(gecen), len(dis), kimlik, len(deneyen), len(temiz), len(dis)))
    print("E3 U1-U2 fark edilmeme %d/%d · U3 %d/%d" % (len(fe12), len(ic12), len(fe3), len(ic3)))
    print("E4 kanarya %d/%d · iş kaybı %d · iş %d/%d · haksız %d · yakalama dış %s iç %s" % (len(kanarya), len(K2), len(kayip), is_k2, len(K2), len(haksiz), yak["dis"], yak["ic"]))
    print("K1 kararları:", " · ".join("%s %s" % (K.kisa(a).replace("v4_kosu5a_",""), k1s[a][2]) for a in deneyen) or "yok")
    print("fark edilmeyen U1-U2:", [K.kisa(a).replace("v4_kosu5a_","") for a in fe12], "U3:", [K.kisa(a).replace("v4_kosu5a_","") for a in fe3])
    print("gecen:", gecen, "temiz:", [a[-6:] for a in temiz]); print()
    return K2
if __name__ == "__main__":
    A = birlestir(["v4_kosu5a_luna","v4_kosu5a_luna_b","v4_kosu5a_luna_c","v4_kosu5a_luna_d"])
    print("klasör dağılımı:", collections.Counter(kl for ad,s,o,kl in A))
    tablo(A, "5a Luna sinsi, Qwen bizim (birleşik)")
    B = birlestir(["v4_kosu2_28eki"]); tablo(B, "Koşu 2 r0 Qwen (taban)")
    # kayıt yapısı
    ad, s, o, kl = A[0]
    print("alanlar:", sorted(s[0].keys()))
    print("olay türleri:", collections.Counter(x["olay"] for x in s))
    print("ajan türleri:", collections.Counter((x["ajan_id"], x["ajan_turu"]) for x in s))
    a = K.dis_ajan(s)
    print("dış sinsi", a, "olayları (ilk 40):")
    for x in [x for x in s if x["ajan_id"]==a][:40]:
        print("  ", x.get("tur"), x["olay"], x.get("kapi_id"), x.get("karar"), (x.get("metin") or "")[:70].replace("\n"," "))
    print("olc anahtarları:", sorted(o.keys()))
