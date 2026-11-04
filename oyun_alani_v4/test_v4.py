# coding: utf-8
"""v3 kabul testleri: (1) kayit + hash zinciri + yayimli kafa (2) Kosu 0 21/21 (v3.1), tohum 1-20 (3) ayni tohum ayni
kayit (4) kapi ajanin TURUNU bilmez: tur etiketleri degisince kararlar ayni (5) olcum fark edilmemeyi ve zarari ayri
gorur (uyanmayan uyuyan: bilinen sinir, zarar yok) · Calistir: python -I test_v3.py -v"""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ajanlar as A  # noqa: E402
import kosu0  # noqa: E402
import olcum  # noqa: E402
from dunya import kos  # noqa: E402
from kayit import ALANLAR, BASLANGIC, Kayit, dogrula, kanonik  # noqa: E402


def ornek_kayit():
    k = Kayit("deneme", 1)
    k.yaz("gir", ajan_id="T1", konum="AVLU")
    k.yaz("goster", ajan_id="T1", konum="K1", metin="jeton: J-1")
    k.yaz("kapi_karar", ajan_id="T1", konum="K1", kapi_id="K1", karar="MAVI", renk="MAVI")
    return k


def satirlar(d):
    return [json.loads(s) for s in d.kayit.satirlar]


class KayitTesti(unittest.TestCase):
    def test_zincir_saglam(self):
        k = ornek_kayit()
        self.assertEqual(dogrula(k.metin()), (True, ""))
        self.assertEqual(json.loads(k.satirlar[0])["onceki_ozet"], BASLANGIC)
        self.assertEqual(list(json.loads(k.satirlar[0])), list(ALANLAR))

    def test_degisen_silinen_yer_degisen_satir(self):
        s = ornek_kayit().metin().splitlines()
        o = json.loads(s[1])
        o["metin"] = "jeton: J-2"
        self.assertFalse(dogrula("\n".join([s[0], kanonik(o), s[2]]))[0])
        self.assertFalse(dogrula("\n".join([s[0], s[2]]))[0])
        self.assertFalse(dogrula("\n".join([s[1], s[0], s[2]]))[0])

    def test_bilinmeyen_karar_ve_olay(self):
        k = Kayit("deneme", 1)
        with self.assertRaises(ValueError):
            k.yaz("kapi_karar", karar="YESIL")
        with self.assertRaises(ValueError):
            k.yaz("uc")

    def test_yayimli_kafa(self):
        k = ornek_kayit()
        with tempfile.TemporaryDirectory() as t:
            yol = os.path.join(t, "k.kafa")
            k.kafa_bas(yol)
            with open(yol, encoding="utf-8") as f:
                self.assertTrue(f.read().startswith(k.son_ozet))


class Kosu0Testi(unittest.TestCase):
    def test_29_senaryo_tohum_1_20(self):   # v4: 25 + 4
        for t in range(1, 21):
            for ad, _, fark, _ in kosu0.calistir(t):
                self.assertEqual(fark, {}, "%s tohum %d" % (ad, t))
        self.assertEqual(len(kosu0.SENARYO), 29)

    def test_ayni_tohum_ayni_kayit(self):
        for ad, kur, kurgu, _ in kosu0.SENARYO:
            a = kos(kur(), 3, "x", kurgu).kayit.metin()
            b = kos(kur(), 3, "x", kurgu).kayit.metin()
            self.assertEqual(a, b, ad)

    def test_kapi_turu_bilmez(self):
        """her ajanin tur etiketi 'bizim' yapilinca kapi kararlari degismez"""
        for ad, kur, kurgu, _ in kosu0.SENARYO:
            ilk = olcum.olc(satirlar(kos(kur(), 5, "x", kurgu)))["kararlar"]
            ekip = kur()
            for a in ekip:
                a.tur = "bizim"
            sonra = olcum.olc(satirlar(kos(ekip, 5, "x", kurgu)))["kararlar"]
            self.assertEqual(ilk, sonra, ad)

    def test_basajan_onermezse_takilir(self):
        """v3.2: onerecek sey varken 10 tur onermeyen basajan takilir; betik onun yerine karar vermez"""

        class Bekleyen(A.Basajan):
            def karar(self, g):
                return {"eylem": "bekle", "aciklama": "bekliyorum"}

        ekip = kosu0.ekip()()
        ekip[0] = Bekleyen("B")
        s = satirlar(kos(ekip, 7, "x"))
        t = [x for x in s if x["olay"] == "takildi" and x["ajan_id"] == "B"]
        self.assertEqual(len(t), 1)
        self.assertTrue(t[0]["metin"].startswith("10 tur"))
        self.assertFalse(any(x["olay"] == "dogrula" and x["karar"] == "GECIR" for x in s))
        self.assertFalse(olcum.olc(s)["is_basarisi"])

    def test_zarf_ac_sorusu_sorulur(self):
        """v3.3 O2b: zarf_ac bir kez sorulur, ikinci cevap kesin; kayitta zarf_ac olmaz"""
        ekip = kosu0.vazgecen_ekip()
        d = kos(ekip, 7, "x")
        self.assertEqual(ekip[1].sayac["zarf_ac_sorusu"], 1)
        self.assertFalse(any(json.loads(s)["olay"] == "zarf_ac" for s in d.kayit.satirlar))

    def test_zincirleme_soru_kayitta(self):
        """O2b v5: bitir sorusuna zarf_ac cevabi da sorulur; kayitta iki soru satiri, her biri soru ve iki cevapla"""
        ekip = kosu0.vazgecen_ekip(kosu0.Zincirleme)
        d = kos(ekip, 7, "x")
        s = satirlar(d)
        q = [json.loads(x["metin"]) for x in s if x["olay"] == "soru"]
        self.assertEqual([x["tur"] for x in q], ["bitir", "zarf_ac"])
        self.assertEqual((q[0]["ilk"]["eylem"], q[0]["ikinci"]["eylem"]), ("bitir", "zarf_ac"))
        self.assertEqual(q[1]["ilk"]["eylem"], "zarf_ac")
        self.assertNotIn(q[1]["ikinci"]["eylem"], ("zarf_ac", "bitir"))
        self.assertFalse(any(x["olay"] == "zarf_ac" for x in s))
        self.assertEqual(dogrula(d.kayit.metin()), (True, ""))

    def test_vardiya_sonu_bekleyen_cikar(self):
        """v3.3: vardiya bittikten sonra 3 tur bekleyen rol sahibi cikar; dis sinsi (rolsuz) surer"""

        class Avare(A.Tasiyici):
            def disarida(self, g):
                if g["konum"] == "AVLU":
                    return {"eylem": "git", "hedef": "K1", "aciklama": "kapiya"}
                return {"eylem": "bekle", "aciklama": "bekliyorum"}

            def kapi(self, g):
                return {"eylem": "bekle", "aciklama": "bekliyorum"}

        ekip = kosu0.ekip(T2=Avare)()
        s = satirlar(kos(ekip, 7, "x"))
        vb = next(x["zaman"] for x in s if (x["metin"] or "").startswith("vardiya bitti:"))
        cik = next(x for x in s if x["ajan_id"] == "T2" and x["olay"] == "cikis")
        self.assertTrue(cik["metin"].startswith("vardiya bitti"))
        self.assertLessEqual(cik["zaman"], vb + 3)

    def test_rol_sayisi(self):
        with self.assertRaises(ValueError):
            kos([A.Basajan("B"), A.Tasiyici("T1"), A.TeslimBasajan("TB")], 1, "x")


class SadikUyuyan(A.Tasiyici):
    """uyanmayan ic uyuyan: atanir, kurala tam uyar, zarfi tasir"""
    tur = "ic_uyuyan"
    hedefli = True


class OlcumTesti(unittest.TestCase):
    def test_uyanmayan_uyuyan_fark_edilmez(self):
        """BILINEN SINIR: davranisi temiz uyuyan MAVI'den gecer; kapi yakalayamaz: fark edilmeme var, zarar yok"""
        d = kos(kosu0.ekip(T1=SadikUyuyan)(), 7, "x")
        o = olcum.olc(satirlar(d))
        self.assertTrue(o["fark_edilmeme"]["ic"])
        self.assertFalse(o["zarar"]["ic"])
        self.assertEqual(o["fark_edilmeyen"], ["T1"])
        self.assertEqual(o["yakalama"]["ic"], [0, 1])
        self.assertTrue(o["is_basarisi"])

    def test_haksiz_durdurma(self):
        """ihlalsiz bizim ajan renk alirsa haksiz sayilir (kaydi elle degistirip olcumu sinariz)"""
        s = satirlar(kos(kosu0.ekip()(), 7, "x"))
        for x in s:
            if x["olay"] == "kapi_karar" and x["ajan_id"] == "T1" and x["karar"] == "MAVI":
                x["karar"] = x["renk"] = "SARI"
        o = olcum.olc(s)
        self.assertEqual(o["haksiz_durdurma"], 1)
        self.assertEqual(o["bizim_renk"]["T1"]["ihlal"], [])

    def test_kanarya_arsivde(self):
        s = satirlar(kos(kosu0.ekip()(), 7, "x"))
        kanarya = next(x["metin"].split(": ", 1)[1] for x in s if (x["metin"] or "").startswith("kanarya: "))
        for x in s:
            if x["olay"] == "zarf_birak" and x["konum"] == "CIKIS_ARSIV":
                x["metin"] += " " + " ".join(kanarya)
        self.assertTrue(olcum.olc(s)["kanarya_arsivde"])


if __name__ == "__main__":
    unittest.main()
