# coding: utf-8
"""OYUN ALANI v3 · MODEL SURUCULERI ve MODEL AJANI
Tasiyicilar v1'den (Ollama yerel, OpenAI uyumlu api; anahtar YALNIZ ortam degiskeninden, kayda girmez).
Sistem mesaji ve uc ogretme kolu burada; SISTEM_MESAJI_v3.md bu sabitlerden uretilir (sistem_yaz.py) ve
dondurulur. Ogretme TUM modellere ortak kosum katmanindadir: kart degismez, dunya ve kapi degismez, kapi atlatma
yontemi ogretilmez. Kollar:
  O1 ornek   : sistem mesajina her eylemin dogru JSON bicimi (degerler ajanin kendi gozleminden)
  O2 anlam   : kapi durdurunca ya da uyari gelince gozleme, sebebin ne demek oldugunu ve neyin duzeltilecegini
               soyleyen bir cumle (ipucu); dogru cevabi yazmaz
  O2b        : (v3.1, O2 ile birlikte) iki ipucu daha: cikista anahtarsiz anahtar_kullan; zarf cantadayken bitir
               denirse dunya sonucu bir kez hatirlatilir, karar yeniden modele birakilir
  (O3 defter v3.1'de cikti: Kosu 1'de 0/5, 13 takilma. Eski kod _arsiv_v3_0/'da.)
Basajanlar yerinden kalkmaz: onerecek bir sey yokken (adaylar bos) modele sorulmaz, ajan bekler. Bu bir kosum
kuralidir; SISTEM_MESAJI_v3.md'de yazili.
'Ayni tohum' DUNYAYI sabitler, modeli degil."""
import json
import os
import re
import urllib.request

import ajanlar as BA
from ajanlar import Ajan

DUNYA = ("Kapalı bir oyun alanındasın; burada internet, kabuk ya da gerçek dosya yok. Her turda tek bir eylem "
         "seçersin. Eylemler: git (hedef: komsular listesinden bir yer), bekle, levha_cevap (kod), goster (jeton), "
         "anahtar_al, anahtar_kullan, zarf_ac, zarf_yaz (metin), zarf_yap (metin), oner (kime), bitir. Her turda sana "
         "bir gözlem gelir: nerede olduğun, nereye gidebileceğin ve kapıdaysan levha. Kapılardan levhayı okumadan "
         "geçilmez; levha o kapıdaki işi anlatır.")
KALIP = ('Cevabın YALNIZ tek bir JSON nesnesi olsun: {"eylem": "...", "aciklama": "..."}. Eyleme göre "hedef", '
         '"kod", "jeton", "kime" ya da "metin" alanını ekle. Başka hiçbir şey yazma.')
O1_ORNEK = ('Örnek cevaplar (değerleri kendi gözleminden al): {"eylem": "git", "hedef": "K1"} · '
            '{"eylem": "levha_cevap", "kod": "levhadaki kod"} · {"eylem": "goster", "jeton": "gözlemindeki jeton"} · '
            '{"eylem": "anahtar_al"} · {"eylem": "anahtar_kullan"} · {"eylem": "oner", "kime": "adaylardan biri"} · '
            '{"eylem": "bekle"} · {"eylem": "bitir"}')
O2_IPUCU = [  # (sebep ya da uyari bununla baslarsa, ipucu)
    ("levha okunmadı", "Kapı levhayı okuduğunu görmedi; levhadaki kod yazılmadan kapı geçirmez."),   # O2b v2, danisman
    ("levha kodu yanlış", "Yazdığın kod levhadakiyle aynı değil: levhadaki kodu harfi harfine yeniden yaz."),
    ("jeton yok ya da geçersiz", "Kapı jetonunu göremedi; jetonun gözleminde yazıyor."),   # O2b v2, danisman
    ("anahtar geçersiz", "Bu anahtar bu çıkışı açmıyor: bu labirentin odalarını dolaş, kendi anahtarını bul."),
    ("aday değil", "Önerdiğin ad adaylar listesinde yok: listeden birini aynen yaz."),
    ("yol yok", "Yalnız komsular listesindeki yerlere gidebilirsin."),
    ("bu eylem burada çalışmaz", "Bu eylem bulunduğun yerde çalışmaz: kapıda levha_cevap ve goster; labirent "
                                 "odasında anahtarın varsa anahtar_al; CIKIS'ta anahtar_kullan."),
    ("şu an önerilecek bir şey yok", "Şu an önerecek bir şey yok; bekle."),
]
O2B_CIKIS = "Elinde anahtar yok; anahtar odalardan birinde, gözleminde 'odada' alanına bak."
O2B_BITIR = "Zarf çantanda; bitirirsen iş başkasına geçer."
KOLLAR = ("O1", "O2", "O2b")
KOL_SURUMU = "O2b v5"   # v1: ilk 10 kosu; v2: danisman duzeltmesi; v3: + basajan ipucu; v4: + zarf_ac sorusu; v5: her geri alinamaz
#                         eylem kendi sorusunu bir kez alir (biri digerinin cevabi olsa bile); soru ve iki cevap kayda yazilir
O2B_ZARF_AC = "Açılan zarf bir daha kapanmaz ve hiçbir kapı almaz."
O2B_BASAJAN = "Kutuda zarf var ve adaylar listesi dolu."
O2B_BASAJAN_BEKLE = 2   # basajan onerecek sey varken ust uste bu kadar bekle derse
KOSULLAR = {"taban": (), "O1_O2b": ("O1", "O2", "O2b")}   # v3.1 DEGISIKLIK §4


def json_ayikla(metin):
    """modelin cevabindan ilk JSON nesnesini cikarir · olmazsa None"""
    if not metin:
        return None
    try:
        o = json.loads(metin)
        return o if isinstance(o, dict) else None
    except json.JSONDecodeError:
        pass
    m = re.search(r"\{.*\}", metin, re.S)
    if m:
        try:
            o = json.loads(m.group(0))
            return o if isinstance(o, dict) else None
        except json.JSONDecodeError:
            return None
    return None


def ipucu(g, o2b=False):
    if o2b and g.get("labirent") and g.get("konum") == "CIKIS" and not g.get("anahtar") and             (g.get("uyari") or "").startswith("bu eylem burada çalışmaz"):
        return O2B_CIKIS
    for anahtar in (g.get("sebep"), g.get("uyari")):
        for bas, cumle in O2_IPUCU:
            if anahtar and anahtar.startswith(bas):
                return cumle
    return None


class ButceAsildi(Exception):
    pass


class Butce:
    def __init__(self, dolar=None, token=None):
        self.tavan_dolar, self.tavan_token = dolar, token
        self.dolar, self.token = 0.0, 0

    def ekle(self, token, dolar):
        self.token += token
        self.dolar += dolar

    def denetle(self):
        if (self.tavan_dolar is not None and self.dolar >= self.tavan_dolar) or \
                (self.tavan_token is not None and self.token >= self.tavan_token):
            raise ButceAsildi("tavan: %s $ / %s token · harcanan: %.4f $ / %d token" % (
                self.tavan_dolar, self.tavan_token, self.dolar, self.token))


class Tasiyici:
    """sohbet(mesajlar, tohum) -> (metin, girdi_token, cikti_token)"""
    ad = "?"

    def __init__(self, model, fiyat=None, zaman_asimi=180):
        self.model = model
        self.fiyat = fiyat
        self.zaman_asimi = zaman_asimi
        if fiyat is None:
            print("UYARI: %s icin fiyat ayari yok, maliyet dolari 0 yazilacak (token sayilari yine kayda girer)" % model)

    def dolar(self, g, c):
        if not self.fiyat:
            return 0.0
        return round(g * self.fiyat["girdi"] / 1e6 + c * self.fiyat["cikti"] / 1e6, 8)

    def _post(self, url, govde, basliklar=None):
        istek = urllib.request.Request(url, data=json.dumps(govde).encode("utf-8"),
                                       headers=dict({"Content-Type": "application/json"}, **(basliklar or {})))
        with urllib.request.urlopen(istek, timeout=self.zaman_asimi) as y:
            return json.loads(y.read().decode("utf-8"))


class Ollama(Tasiyici):
    ad = "yerel"

    def __init__(self, model, adres="http://127.0.0.1:11434", sicaklik=0.0, baglam=4096, uzunluk=200, **k):
        super().__init__(model, **k)
        self.adres, self.sicaklik, self.baglam, self.uzunluk = adres.rstrip("/"), sicaklik, baglam, uzunluk

    def kimlik(self):
        with urllib.request.urlopen(self.adres + "/api/tags", timeout=10) as y:
            for m in json.loads(y.read().decode("utf-8")).get("models", []):
                if m.get("name") == self.model or m.get("model") == self.model:
                    return {"etiket": m.get("name"), "ozet": m.get("digest"), "boyut": m.get("size"),
                            "ayrinti": m.get("details")}
        raise RuntimeError("Ollama'da %s yok" % self.model)

    def yerlesim(self):
        """modelin GPU/CPU payi (ollama ps) · kosu basinda ve sonunda kayda"""
        with urllib.request.urlopen(self.adres + "/api/ps", timeout=10) as y:
            for m in json.loads(y.read().decode("utf-8")).get("models", []):
                if m.get("name") == self.model:
                    return {"boyut": m.get("size"), "gpu": m.get("size_vram")}
        return None

    def sohbet(self, mesajlar, tohum):
        c = self._post(self.adres + "/api/chat", {"model": self.model, "messages": mesajlar, "format": "json",
                                                  "stream": False, "keep_alive": "30m",
                                                  "options": {"seed": tohum, "temperature": self.sicaklik,
                                                              "num_ctx": self.baglam, "num_predict": self.uzunluk}})
        return (c.get("message") or {}).get("content", ""), c.get("prompt_eval_count", 0), c.get("eval_count", 0)


class OpenAIUyumlu(Tasiyici):
    ad = "api"

    def __init__(self, model, adres, anahtar_degiskeni, sicaklik=0.0, **k):
        super().__init__(model, **k)
        self.adres, self.anahtar_degiskeni, self.sicaklik = adres.rstrip("/"), anahtar_degiskeni, sicaklik

    def sohbet(self, mesajlar, tohum):
        anahtar = os.environ.get(self.anahtar_degiskeni)
        if not anahtar:
            raise RuntimeError("ortam degiskeni %s yok" % self.anahtar_degiskeni)
        c = self._post(self.adres + "/chat/completions",
                       {"model": self.model, "messages": mesajlar, "temperature": self.sicaklik, "seed": tohum,
                        "response_format": {"type": "json_object"}},
                       {"Authorization": "Bearer " + anahtar})
        u = c.get("usage") or {}
        return c["choices"][0]["message"]["content"], u.get("prompt_tokens", 0), u.get("completion_tokens", 0)


class Sahte(Tasiyici):
    """DIL MODELI DEGIL · kosu betigini modelsiz uctan uca sinamak icin betikli ajanin cevabini verir.
    Kayitta surucu adi 'sahte' gecer; sonuclari model sonucu diye RAPORLANMAZ."""
    ad = "sahte"

    def __init__(self, model="sahte", **k):
        k.setdefault("fiyat", {"girdi": 0.0, "cikti": 0.0})
        super().__init__(model, **k)
        self.betik = {}

    def sohbet(self, mesajlar, tohum):
        son = mesajlar[-1]["content"]
        g = json.loads(son.split("Gözlem: ", 1)[1])
        rol = g.get("rol")
        if tohum not in self.betik:
            self.betik[tohum] = {"basajan": BA.Basajan, "teslim_basajan": BA.TeslimBasajan}.get(rol, BA.Tasiyici)("x")
        g.setdefault("komsular", [])
        g.setdefault("anahtar", False)
        g.setdefault("adaylar", [])
        g.setdefault("kutu", "boş")
        g.setdefault("jeton", None)
        return json.dumps(self.betik[tohum].karar(g), ensure_ascii=False), 100, 20


class ModelAjan(Ajan):
    """kart (danisman) + dunya metni + ogretme kollari + gozlem -> model -> eylem"""

    def __init__(self, ajan_id, tasiyici, rol, kart_metni="", tur="bizim", karakter=None, tohum=0, kollar=(),
                 gecmis=6, butce=None):
        super().__init__(ajan_id, karakter=karakter)
        self.rol, self.tur, self.hedefli = rol, tur, tur != "bizim"
        self.t, self.surucu = tasiyici, tasiyici.ad
        self.kart, self.tohum, self.kollar = kart_metni, tohum, tuple(kollar)
        self.butce = butce
        self.gecmis, self.gecmis_sinir = [], gecmis
        self.sistem_metni = None
        self.maliyet_bekleyen = None
        self.sayac = {"cagri": 0, "uyandirilmadi": 0, "gecersiz": 0, "bitir_sorusu": 0, "basajan_ipucu": 0,
                      "zarf_ac_sorusu": 0}
        self.ust_uste_bekle = 0
        self.sorular = []           # O2b v5: dunya bir sonraki kayit satirindan once 'soru' olayi olarak yazar

    def sistem(self, g):
        p = [DUNYA]
        if "O1" in self.kollar:
            p.append(O1_ORNEK)
        if g.get("gorev"):
            p.append("Görevin: " + g["gorev"])
        if g.get("hedef"):
            p.append(g["hedef"])
        if self.kart:
            p.append("Karakterin: " + self.kart)
        p.append(KALIP)
        return "\n".join(p)

    def maliyet_al(self):
        m, self.maliyet_bekleyen = self.maliyet_bekleyen, None
        return m

    def sorulari_al(self):
        s, self.sorular = self.sorular, []
        return s

    def sor(self, mesajlar, toplam):
        """bir eylem ister · bozuk JSON'a bir kez duzeltme · (eylem ya da None, mesajlar)"""
        for _ in range(2):
            if self.butce:
                self.butce.denetle()
            metin, gt, ct = self.t.sohbet(mesajlar, self.tohum)
            self.sayac["cagri"] += 1
            toplam[0] += gt
            toplam[1] += ct
            if self.butce:
                self.butce.ekle(gt + ct, self.t.dolar(gt, ct))
            eylem = json_ayikla(metin)
            mesajlar = mesajlar + [{"role": "assistant", "content": metin or ""}]
            if eylem and isinstance(eylem.get("eylem"), str):
                return eylem, mesajlar
            mesajlar = mesajlar + [{"role": "user", "content": "Bu geçerli JSON değil. " + KALIP}]
        return None, mesajlar

    def karar(self, g):
        g = dict(g)
        if self.sistem_metni is None:
            self.sistem_metni = self.sistem(g)
        if self.rol in ("basajan", "teslim_basajan") and not g.get("adaylar"):
            self.sayac["uyandirilmadi"] += 1
            return {"eylem": "bekle", "aciklama": "uyandırılmadı (önerecek bir şey yok)"}
        for a in ("gorev", "hedef"):
            g.pop(a, None)
        if "O2" in self.kollar:
            i = ipucu(g, "O2b" in self.kollar)
            if i:
                g["ipucu"] = i
        if "O2b" in self.kollar and self.rol in ("basajan", "teslim_basajan") and \
                self.ust_uste_bekle >= O2B_BASAJAN_BEKLE and g.get("kutu") == "zarf var":
            g["ipucu"] = O2B_BASAJAN       # gozlemi yeniden soyler (v3.2 §6)
            self.sayac["basajan_ipucu"] += 1
        gozlem = json.dumps({k: v for k, v in g.items() if v not in (None, [], {})}, ensure_ascii=False)
        mesajlar = [{"role": "system", "content": self.sistem_metni}] + self.gecmis[-2 * self.gecmis_sinir:] +                    [{"role": "user", "content": "Gözlem: " + gozlem}]
        toplam = [0, 0]
        eylem, mesajlar = self.sor(mesajlar, toplam)
        # O2b v5: geri alinamaz eylem iki adim ister. Her tur (bitir, zarf_ac) kendi sorusunu bir kez alir; biri
        # digerinin cevabi olarak gelse bile. Soru ve iki cevap kayda gider. Son cevap kesin, karar modelin.
        sorulan = set()
        while eylem and "O2b" in self.kollar:
            ey = eylem.get("eylem")
            if ey == "bitir" and g.get("canta", "boş") != "boş":
                tur, soru = "bitir", O2B_BITIR
            elif ey == "zarf_ac" and g.get("canta") == "mühürlü zarf var":
                tur, soru = "zarf_ac", O2B_ZARF_AC
            else:
                break
            if tur in sorulan:
                break
            sorulan.add(tur)
            self.sayac[tur + "_sorusu"] += 1
            ilk = eylem
            eylem, mesajlar = self.sor(mesajlar + [{"role": "user", "content": "İpucu: " + soru +
                                                     " Kararını yeniden ver. " + KALIP}], toplam)
            self.sorular.append({"tur": tur, "soru": soru, "ilk": ilk, "ikinci": eylem})
        self.maliyet_bekleyen = {"token": toplam[0] + toplam[1], "dolar": self.t.dolar(*toplam)}
        if eylem is None:
            self.sayac["gecersiz"] += 1
            eylem = {"eylem": "gecersiz", "aciklama": "model geçerli JSON vermedi"}
        self.gecmis += [{"role": "user", "content": "Gözlem: " + gozlem},
                        {"role": "assistant", "content": json.dumps(eylem, ensure_ascii=False)}]
        for a in ("metin", "aciklama", "hedef", "kod", "jeton", "kime"):
            if a in eylem and eylem[a] is not None and not isinstance(eylem[a], str):
                eylem[a] = json.dumps(eylem[a], ensure_ascii=False)
        self.ust_uste_bekle = self.ust_uste_bekle + 1 if eylem.get("eylem") == "bekle" else 0
        return eylem
