# coding: utf-8
"""KARAKTER KARTLARI v2 · danismanin dosyasini okur (KARAKTER_KARTLARI_v2_27eki.md), DEGISTIRMEZ.
Kart metni sistem mesajina "Karakterin: ..." satiri olarak AYNEN girer (on ek surucude, kartta tekrarlanmaz).
Dagitim (kart dosyasi "Kosu dagilimi"):
  Kosu 1: yalniz G ve B. 3 tasiyici (G1 G2 G3 tohuma gore karisik), basajan B1 ya da B2 (tohuma gore),
          teslim basajan B1.
  Kosu 2: her tohumda alti kosu; ucunde DIS'tan bir dis sinsi (D1 D2 D3), ucunde tasiyicilardan biri ic uyuyan
          (U1 U2 U3; hangi sira oldugu tohuma gore). Bir tohumun alti kosusunda yalniz sinsi karti degisir."""
import hashlib
import os
import random
import re

KOK = os.path.dirname(os.path.abspath(__file__))
KART_DOSYA = os.path.join(KOK, "KARAKTER_KARTLARI_v2_27eki.md")
KART_OZET = "c143345714a933d379ce6fb834f83f24bf244ced96527b2a66d7bad395af47a6"   # danisman 27 Eki, dayanak v3.1 (kartlar ayni; onceki 32438482...)
KURAL_DOSYA = "KAPI_KURALLARI_DONUK_v4.md"   # v4 genetik kapi (28 Eki, kilitten sonra kesif); v3.4 10a9257a... oyun_alani_v3/
KURAL_OZET = "17077b0e9315e29befeab42183504ace287b63d0573eb56d7effa228063ab53d"  # donuk v4
SISTEM_DOSYA = "SISTEM_MESAJI_v4.md"
KART_DESEN = re.compile(r"^\*\*([GBDU]\d) · (.+?)\.\*\* Karakterin: (.+)$", re.M)
TUR = {"G": "bizim", "B": "bizim", "D": "dis_sinsi", "U": "ic_uyuyan"}


def oku(yol=KART_DOSYA, ozet_denetle=True):
    """{kod: {"ad", "metin", "tur"}} · ozet tutmazsa durur (kart dosyasi degismis)"""
    with open(yol, "rb") as f:
        ham = f.read()
    oz = hashlib.sha256(ham).hexdigest()
    if ozet_denetle and oz != KART_OZET:
        raise ValueError("kart dosyasi ozeti %s, beklenen %s" % (oz, KART_OZET))
    kartlar = {}
    for kod, ad, metin in KART_DESEN.findall(ham.decode("utf-8")):
        kartlar[kod] = {"ad": ad.strip(), "metin": metin.strip(), "tur": TUR[kod[0]]}
    return kartlar, oz


def dagitim_kosu1(tohum):
    """{"B": kod, "T1".."T3": kod, "TB": "B1"}"""
    r = random.Random("v3kosu1:%s" % tohum)
    g = ["G1", "G2", "G3"]
    r.shuffle(g)
    return {"B": r.choice(["B1", "B2"]), "T1": g[0], "T2": g[1], "T3": g[2], "TB": "B1"}


def dagitim_kosu2(tohum):
    """[(sinsi_kodu, dagitim)] · alti satir; dagitimda dis sinsi 'S1' anahtariyla, ic uyuyan bir T yerine"""
    temel = dagitim_kosu1(tohum)
    sira = random.Random("v3kosu2:%s" % tohum).choice(["T1", "T2", "T3"])
    out = []
    for s in ("D1", "D2", "D3"):
        out.append((s, dict(temel, S1=s)))
    for s in ("U1", "U2", "U3"):
        out.append((s, dict(temel, **{sira: s})))
    return out
