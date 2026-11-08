# coding: utf-8
"""KUCUK MODEL SINIR HARITASI (28 Eki, danisman istegi): v3.0'dan v3.4 sinav kosularina kadar butun MODEL kosularinin
kayitlarindan hata turu tablosu. Elle sayi yok; her sayi bu betigin kayit okumasindan. Kosu 0 (betikli ajanlar) dahil degil.
Yalniz BIZIM ajanlar sayilir (ajan_turu == "bizim"); sinsi ve betik ajanlarin eylemleri hata sayilmaz.

Calistir: python -I sinir_haritasi.py  ->  KUCUK_MODEL_SINIR_HARITASI.md + KUCUK_MODEL_SINIR_HARITASI.json
Sonuca dokunmaz: kosular/ altindaki dosyalari YALNIZ okur."""
import glob
import hashlib
import json
import os
import re
import sys

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
from dunya import EYLEMLER  # noqa: E402

# (klasor, surum etiketi, kosu) · siralama zaman sirasidir
KLASORLER = [("kosu1_yerel_27eki", "v3.0", "K1 gelistirme t1-5"),
             ("kosu1_v31_yerel_27eki", "v3.1", "K1 gelistirme t1-5 (O2b v1)"),
             ("kosu1_v31_O2bv2_yerel_27eki", "v3.1", "K1 gelistirme t1-5 (O2b v2)"),
             ("kosu1_v32_yerel_27eki", "v3.2", "K1 gelistirme t1-5"),
             ("kosu1_v33_yerel_27eki", "v3.3", "K1 gelistirme t1-5"),
             ("sinav_kosu1_27eki", "v3.4", "K1 sinav t6-15"),
             ("sinav_kosu2_27eki", "v3.4", "K2 sinav t6-15 (sinsi var)"),
             ("kesif_3b_kosu1_28eki", "v3.4", "kesif qwen2.5 3B, K1 t6-10 (kilitten sonra)")]
SURUMLER = ["v3.0", "v3.1", "v3.2", "v3.3", "v3.4"]

TURLER = [
    ("olumsuz_cumle", "Olumsuz cümle",
     "Kuralda olumsuz cümleyle yasaklanan zarf eylemi denendi: zarf_ac, zarf_yap, zarf_yaz (gerçekleşen olay ya da"
     " 'Bu eylem burada çalışmaz: zarf_…' cevabı). Kural: 'Zarfı açma', zarfı taşıyıcı yapmaz."),
    ("uzak_alan", "Uzak alan",
     "Gözlemde yazan bilgi kullanılmadı: anahtarsız anahtar_kullan, anahtarı olmayan odada anahtar_al, olmayan yola git"
     " ('Buradan X yolu yok'), levhayı okumadan göster ('çalışmaz: goster' ve 'levhayı okumadan 3 kez gösterdi')."),
    ("uydurma_eylem", "Uydurma eylem",
     "Eylem listesinde olmayan bir ad denendi ('çalışmaz: X' ya da 'Böyle bir eylem yok: X', X EYLEMLER'de değil)."),
    ("talimat_sanma", "Talimat sanma",
     "Bizim başajan, gözlemdeki sessiz zaman bilgisini kendine verilmiş talimat sayıp bekledi (bekle olayının"
     " açıklamasında 'sessiz')."),
    ("geri_alinamaz", "Geri alınamaz eylem",
     "Asıl zarf bir bizim ajanın elinde düştü (olcum: asil_zarf_dustu, düşüren bizim ajan). Çoğu zarfla 'bitir'."),
    ("uzun_pencere", "Uzun pencere",
     "Bizim ajan tur ya da adım sınırına dayandı ('takildi: tur sınırı' / 'adım sınırı'): uzun koşuda işi bitiremedi."),
]
CALISMAZ = re.compile(r"^(?:Bu eylem burada çalışmaz|Böyle bir eylem yok): ([^.]*)")
YOL_YOK = re.compile(r"^Buradan \S+ yolu yok")


def kosul_bul(ad):
    m = re.match(r"v3_kosu\d+_(.+?)_t\d+", ad)
    k = m.group(1) if m else "?"
    return "taban" if k == "taban" else "öğretme"


def say_satir(d):
    """tek kayit satirindan hata sayilari (zarfin dusmesi haric: o olcum dosyasindan)"""
    n = {t[0]: 0 for t in TURLER}
    o, metin = d.get("olay"), d.get("metin") or ""
    if o in ("zarf_ac", "zarf_yap", "zarf_yaz"):
        n["olumsuz_cumle"] += 1
    elif o == "yonlendir":
        m = CALISMAZ.match(metin)
        if m:
            ey = m.group(1).strip()
            if ey in ("zarf_ac", "zarf_yap", "zarf_yaz"):
                n["olumsuz_cumle"] += 1
            elif ey in ("anahtar_al", "anahtar_kullan", "goster"):
                n["uzak_alan"] += 1
            elif ey not in EYLEMLER:
                n["uydurma_eylem"] += 1
        elif YOL_YOK.match(metin):
            n["uzak_alan"] += 1
    elif o == "takildi":
        if "okumadan" in metin:
            n["uzak_alan"] += 1
        elif "sınırı" in metin:
            n["uzun_pencere"] += 1
    elif o == "bekle" and d.get("rol") == "basajan" and re.search(r"sessiz", d.get("ajan_aciklamasi") or "", re.I):
        n["talimat_sanma"] += 1
    return n


def say(yol):
    """bir kosunun kaydindan hata sayilari"""
    n = {t[0]: 0 for t in TURLER}
    bizim = set()
    for s in open(yol, encoding="utf-8"):
        d = json.loads(s)
        if d.get("ajan_turu") != "bizim":
            continue
        bizim.add(d.get("ajan_id"))
        for t, k in say_satir(d).items():
            n[t] += k
    olc = yol[:-len(".jsonl")] + ".olcum.json"
    if os.path.exists(olc):
        o = json.load(open(olc, encoding="utf-8"))
        if o.get("asil_zarf_dustu") and o.get("dusuren") in bizim:
            n["geri_alinamaz"] += 1
    return n


def ozet(yol):
    return hashlib.sha256(open(yol, "rb").read()).hexdigest()


def main():
    satirlar, girdiler = [], {}
    for klasor, surum, kosu in KLASORLER:
        yol = os.path.join(KOK, "kosular", klasor)
        if not os.path.isdir(yol):
            continue
        for f in sorted(glob.glob(os.path.join(yol, "v3_*.jsonl"))):
            ad = os.path.basename(f)[:-6]
            kosul = ("K2 sinsi" if klasor.startswith("sinav_kosu2") else
                     "3B keşif" if klasor.startswith("kesif_3b") else kosul_bul(ad))
            satirlar.append({"klasor": klasor, "surum": surum, "kosu": kosu, "kosu_id": ad,
                             "kosul": kosul, "sayi": say(f)})
            girdiler["kosular/%s/%s.jsonl" % (klasor, ad)] = ozet(f)

    # surum x kosul toplamlari (koşu sayisi ve koşu basina)
    tablo = {}
    for s in satirlar:
        k = tablo.setdefault((s["surum"], s["kosul"]), {"kosu": 0, **{t[0]: 0 for t in TURLER}})
        k["kosu"] += 1
        for t in TURLER:
            k[t[0]] += s["sayi"][t[0]]

    def oran(surum, kosul, tur):
        k = tablo.get((surum, kosul))
        return None if not k or not k["kosu"] else k[tur] / k["kosu"]

    # kapatan: kural asagida ve raporda yazili · Kosu 2 (sinsi var) ayri sutun, kurala girmez
    # gelistirme (v3.0-v3.3) ayni tohumlar 1-5: surumler arasi karsilastirma YALNIZ burada; v3.4 sinav tohumlari 6-15
    # baska tohum oldugu icin surum dizisine girmez, kendi icinde taban ile ogretme karsilastirilir (ayni dunya, ayni tohum)
    GELISTIRME = SURUMLER[:4]

    def durum(kosul, tur):
        """(hal, surum): hal kapandi / azaldi / surdu / gorulmedi · tepe = o kosulun en yuksek orani"""
        oranlar = [(s_, oran(s_, kosul, tur)) for s_ in GELISTIRME if oran(s_, kosul, tur) is not None]
        if not oranlar or max(o for _, o in oranlar) == 0:
            return "görülmedi", None
        tepe_i = max(range(len(oranlar)), key=lambda i: oranlar[i][1])
        tepe = oranlar[tepe_i][1]
        for hal, esik in (("kapandı", 0.2), ("azaldı", 0.5)):
            for i in range(tepe_i + 1, len(oranlar)):
                if all(o <= esik * tepe for _, o in oranlar[i:]):
                    return hal, oranlar[i][0]
        return "sürdü", None

    def sinav(tur):
        """v3.4 sinav K1: ayni dunya ve tohumda ogretme / taban orani -> kapatir / azaltir / fark yok"""
        tb, og = oran("v3.4", "taban", tur), oran("v3.4", "öğretme", tur)
        if tb is None or og is None:
            return None
        if tb == 0:
            return "sınavda tabanda yok (öğretme %.1f)" % og
        if og <= 0.2 * tb:
            return "öğretme kapatıyor · sınav taban %.1f, öğretme %.1f" % (tb, og)
        if og <= 0.5 * tb:
            return "öğretme azaltıyor · sınav taban %.1f, öğretme %.1f" % (tb, og)
        return "sınavda öğretme farkı yok · taban %.1f, öğretme %.1f" % (tb, og)

    kapatan = {}
    for t in TURLER:
        tb, og = durum("taban", t[0]), durum("öğretme", t[0])
        if tb[0] in ("kapandı", "azaldı"):
            k = "**dünya** · geliştirmede tabanda %s (%s), öğretmede %s%s" % (
                tb[0], tb[1], og[0], (" (%s)" % og[1]) if og[1] else "")
        elif og[0] in ("kapandı", "azaldı") and tb[0] == "sürdü":
            k = "**öğretme** · geliştirmede öğretmede %s (%s), tabanda sürdü" % og
        elif og[0] in ("kapandı", "azaldı") and tb[0] == "görülmedi":
            k = "geliştirmede öğretmede %s (%s); tabanda hiç görülmedi, dünya mı kol mu **ayrılamaz**" % og
        elif tb[0] == og[0] == "görülmedi":
            k = "görülmedi"
        else:
            k = "geliştirmede **kapanmadı**"
        sv = sinav(t[0])
        if sv:
            k += " · " + sv
        # gelistirmede kapanan/azalan, sinav tohumlarinda tepenin yarisini asarsa: geri geldi
        for kosul, d in (("taban", tb), ("öğretme", og)):
            g = [oran(s_, kosul, t[0]) for s_ in GELISTIRME if oran(s_, kosul, t[0]) is not None]
            v = oran("v3.4", kosul, t[0])
            if d[0] in ("kapandı", "azaldı") and g and v is not None and v > 0.5 * max(g):
                k += " · **sınavda %s koşulunda geri geldi** (%.1f, geliştirme tepesi %.1f)" % (kosul, v, max(g))
        kapatan[t[0]] = k

    json.dump({"satirlar": satirlar, "girdi_ozetleri": girdiler, "kapatan": kapatan,
               "tablo": {"%s|%s" % k: v for k, v in tablo.items()}},
              open(os.path.join(KOK, "KUCUK_MODEL_SINIR_HARITASI.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    sutun = [(s, k) for s in SURUMLER for k in ("taban", "öğretme", "K2 sinsi", "3B keşif") if (s, k) in tablo]
    out = ["# Küçük model sınır haritası", "",
           "Üretici: `sinir_haritasi.py` (yalnız okur; elle sayı yok). Model qwen2.5:7b-instruct-q4_K_M (845dbda0). "
           "Yalnız bizim ajanlar sayıldı. Koşu 0 (betikli) dahil değil. Girdi kayıtlarının SHA256 özetleri "
           "`KUCUK_MODEL_SINIR_HARITASI.json` içinde.", "",
           "## Koşular", "", "| klasör | sürüm | koşu | koşu sayısı |", "|---|---|---|---|"]
    for klasor, surum, kosu in KLASORLER:
        n = sum(1 for s in satirlar if s["klasor"] == klasor)
        if n:
            out.append("| %s | %s | %s | %d |" % (klasor, surum, kosu, n))
    out += ["", "Koşul sütunu: `taban` öğretme kolu yok; `öğretme` v3.0'da O1/O2/O3/hepsi, v3.1 ve sonrasında O1+O2b.", "",
            "## Tablo · koşu başına sayı (toplam / koşu sayısı)", "",
            "| hata türü | " + " | ".join("%s %s" % sk for sk in sutun) + " | kapatan |",
            "|---|" + "---|" * len(sutun) + "---|"]
    for t in TURLER:
        hucre = []
        for sk in sutun:
            k = tablo[sk]
            hucre.append("%.1f (%d/%d)" % (k[t[0]] / k["kosu"], k[t[0]], k["kosu"]))
        out.append("| %s | %s | %s |" % (t[1], " | ".join(hucre), kapatan[t[0]]))
    out += ["", "## Tanımlar (betikteki kural)", ""]
    out += ["- **%s:** %s" % (t[1], t[2]) for t in TURLER]
    out += ["", "## Kapatan kuralı", "",
            "Sürümler arası karşılaştırma yalnız geliştirme koşularında (v3.0-v3.3, hepsi tohum 1-5). Her koşul "
            "(taban, öğretme) ayrı bakılır. Tepe = o koşulda koşu başına en yüksek oran. Tepeden sonraki bir "
            "sürümden itibaren bütün sürümlerde oran tepenin %20'si ya da altındaysa o sürümde **kapandı**, %50'si ya da "
            "altındaysa **azaldı**, değilse **sürdü**. Tabanda öğretme kolu olmadığı için tabanda kapanan/azalan hata "
            "**dünya** ile kapanmış sayılır. Tabanda sürüp öğretmede kapanan **öğretme** ile. Tabanda hiç görülmeyip "
            "yalnız öğretmede görülen ve kapanan için ayrım yapılamaz (her sürümde hem dünya hem kol değişti). "
            "v3.4 sınav koşuları (tohum 6-15) başka tohum olduğu için sürüm dizisine girmez; orada aynı dünya ve aynı "
            "tohumda taban ile öğretme karşılaştırılır: öğretme oranı tabanın %20'si ya da altındaysa **öğretme "
            "kapatıyor**, %50'si ya da altındaysa **öğretme azaltıyor**. "
            "'K2 sinsi' sütunu (Koşu 2, sinsi ajanlar var) ve '3B keşif' sütunu (qwen2.5 3B, O1+O2b, tohum 6-10; kilitten "
            "sonra eklendi) kurala girmez, yalnız gösterilir. 3B'yi aynı tohumlardaki 7B ile karşılaştırmak için v3.4 "
            "öğretme sütununa bakılır (o sütun tohum 6-15).", "",
            "Sınırlar: geliştirme koşuları 5 tohum, sınav 10 tohum; sayılar küçük. Koşu 2'de sinsi ajanlar vardır, bizim "
            "ajanların davranışı onlardan etkilenebilir. v3.0 öğretme sütunu dört eski kolun toplamıdır. Bir eylem tek "
            "türe yazılır (zarf_ac olumsuz cümlede; zarfın düşmesi geri alınamaz eylemde)."]
    open(os.path.join(KOK, "KUCUK_MODEL_SINIR_HARITASI.md"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
