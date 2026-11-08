# coding: utf-8
"""OYUN ALANI v3 · KAYIT (KURALLAR_v3_SON_27eki §8; v1 kayit.py'den, alanlar ve olaylar genisledi)
Her olay tek satir JSON (JSONL), bir kosu bir dosya. Satirlar SHA256 zinciriyle bagli:
her satirin onceki_ozet alani, bir onceki satirin (kendi onceki_ozet'i dahil) kanonik metninin ozetidir.
Ilk satirin onceki_ozet'i 64 sifir. Bir satir degisirse, silinirse ya da araya satir girerse dogrula() yakalar.
zaman: duvar saati DEGIL, dunyanin tur sayaci (dunya yazar; ayni tohum + betikli ajanlar -> birebir ayni kayit).
Kosu sonunda zincirin kafasi ayri dosyaya basilir (yayimli kafa): kafa_bas().
Model kosularinda tekrar = kayittan oynatma; model kosulari yeniden uretilmez."""
import hashlib
import json

ALANLAR = ("kosu_id", "tohum", "adim", "zaman", "ajan_id", "ajan_turu", "rol", "karakter", "konum", "olay",
           "metin", "kapi_id", "karar", "renk", "zarf", "isaret", "ajan_aciklamasi", "maliyet", "onceki_ozet")
OLAYLAR = ("gir", "bekle", "levha_goster", "levha_cevap", "goster", "kapi_karar", "yonlendir", "zarf_al",
           "zarf_birak", "zarf_dustu", "zarf_ac", "zarf_yaz", "zarf_yap", "anahtar_al", "anahtar_kullan", "oner",
           "dogrula", "isaret", "mesaj", "durdu", "cikis", "takildi", "soru")   # soru: O2b v5, kosum sorusu ve iki cevap
KARARLAR = ("MAVI", "SARI", "KIRMIZI", "TURUNCU", "DURDUR", "GECIR", "UYARI")   # UYARI: v3.1 kapi uyarir, gecirmez
BASLANGIC = "0" * 64


def kanonik(satir):
    """alan sirasi sabit, bosluksuz, UTF-8 · ozet ve dosya ayni metinden"""
    return json.dumps({k: satir.get(k) for k in ALANLAR}, ensure_ascii=False, separators=(",", ":"))


def ozet(metin):
    return hashlib.sha256(metin.encode("utf-8")).hexdigest()


class Kayit:
    def __init__(self, kosu_id, tohum):
        self.kosu_id = kosu_id
        self.tohum = tohum
        self.satirlar = []          # kanonik metinler
        self.son_ozet = BASLANGIC
        self.zaman = 0               # dunya her turun basinda yazar

    def yaz(self, olay, **alanlar):
        if olay not in OLAYLAR:
            raise ValueError("bilinmeyen olay: %s" % olay)
        if alanlar.get("karar") is not None and alanlar["karar"] not in KARARLAR:
            raise ValueError("bilinmeyen karar: %s" % alanlar["karar"])
        bilinmeyen = set(alanlar) - set(ALANLAR)
        if bilinmeyen:
            raise ValueError("bilinmeyen alan: %s" % sorted(bilinmeyen))
        satir = dict.fromkeys(ALANLAR)
        satir.update(alanlar)
        satir.update(kosu_id=self.kosu_id, tohum=self.tohum, adim=len(self.satirlar), zaman=self.zaman,
                     olay=olay, onceki_ozet=self.son_ozet)
        if satir["maliyet"] is None:
            satir["maliyet"] = {"token": 0, "dolar": 0.0}
        k = kanonik(satir)
        self.satirlar.append(k)
        self.son_ozet = ozet(k)
        return satir

    def metin(self):
        return "".join(s + "\n" for s in self.satirlar)

    def kaydet(self, yol):
        with open(yol, "w", encoding="utf-8", newline="\n") as f:
            f.write(self.metin())

    def kafa_bas(self, yol):
        """yayimli kafa: son satirin ozeti, kosu, satir sayisi · kayittan AYRI dosya (tanik bunu saklar)"""
        with open(yol, "w", encoding="utf-8", newline="\n") as f:
            f.write("%s  %s  satir=%d\n" % (self.son_ozet, self.kosu_id, len(self.satirlar)))


def dogrula(metin):
    """(tamam, hata) · zincir, adim sirasi, alanlar ve tek kosu_id denetlenir"""
    onceki = BASLANGIC
    kosu = None
    for i, s in enumerate(metin.splitlines()):
        try:
            o = json.loads(s)
        except json.JSONDecodeError:
            return False, "satir %d JSON degil" % i
        if list(o) != list(ALANLAR):
            return False, "satir %d alanlari eksik ya da sirasi bozuk" % i
        if kanonik(o) != s:
            return False, "satir %d kanonik degil (elle degistirilmis olabilir)" % i
        if o["onceki_ozet"] != onceki:
            return False, "satir %d zincir kirik" % i
        if o["adim"] != i:
            return False, "satir %d adim %s, beklenen %d" % (i, o["adim"], i)
        if kosu is None:
            kosu = o["kosu_id"]
        elif o["kosu_id"] != kosu:
            return False, "satir %d baska kosuya ait" % i
        onceki = ozet(s)
    return True, ""


def oku(yol):
    with open(yol, encoding="utf-8") as f:
        metin = f.read()
    tamam, hata = dogrula(metin)
    if not tamam:
        raise ValueError("%s: %s" % (yol, hata))
    return [json.loads(s) for s in metin.splitlines()]
