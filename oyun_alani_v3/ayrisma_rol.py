# coding: utf-8
"""KOSU 4 · AYRISMA YERI ROLE GORE (28 Eki, danisman: "buyuk modelin ayrisma yeri tasiyici, basajan ve teslim basajan
icin ayri sayilsin; kilidin olcusu degismiyor, ayrinti ekleniyor"). T4'un olcusu (O1+O2b is / 10) kilit_degerlendir.py'de
kalir; bu betik yalniz ayrinti yazar. Elle sayi yok; her sayi kayitlardan. Kosulari YALNIZ okur.

Calistir: python -I ayrisma_rol.py <kucuk_klasor> <buyuk_klasor> [--kosul O1_O2b] [--cikti AYRISMA_ROL_K4.md]
  ornek: python -I ayrisma_rol.py kosular/sinav_kosu1_27eki kosular/sinav_kosu4_...  (ayni tohumlar eslesir)"""
import glob
import json
import os
import re
import sys

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import sinir_haritasi as SH  # noqa: E402

ROLLER = [("tasiyici", "Taşıyıcı"), ("basajan", "Başajan"), ("teslim_basajan", "Teslim başajanı")]


def rol_oku(yol):
    """bir kosuda her rolun sonucu: {rol: {"hal": ..., "neden": ..., "hata": {tur: n}, "tepki": [tur farki]}}"""
    satir = [json.loads(s) for s in open(yol, encoding="utf-8")]
    olc_yol = yol[:-len(".jsonl")] + ".olcum.json"
    olc = json.load(open(olc_yol, encoding="utf-8")) if os.path.exists(olc_yol) else {}
    rol_of = {d["ajan_id"]: d["rol"] for d in satir if d.get("ajan_turu") == "bizim"}
    hata = {r: {t[0]: 0 for t in SH.TURLER} for r, _ in ROLLER}
    takildi, renk, tepki = {}, {}, {"basajan": [], "teslim_basajan": []}
    bekleyen = {"basajan": None, "teslim_basajan": None}
    atanan, gecersiz_oner = set(), 0
    for d in satir:
        o, metin, a = d.get("olay"), d.get("metin") or "", d.get("ajan_id")
        if o == "zarf_birak" and metin in ("kutu 1", "kutu 2"):
            r = "basajan" if metin == "kutu 1" else "teslim_basajan"
            if bekleyen[r] is None:
                bekleyen[r] = d.get("zaman", 0)
        elif o == "dogrula" and metin.startswith("atandı:"):
            r = "teslim_basajan" if "TESLIM" in metin else "basajan"
            if bekleyen[r] is not None:
                tepki[r].append(d.get("zaman", 0) - bekleyen[r])
                bekleyen[r] = None
            if r == "basajan":
                atanan.add(metin.split(":", 1)[1].strip())
        if d.get("ajan_turu") != "bizim":
            continue
        r = d.get("rol")
        if o == "oner" and metin in ("None", ""):
            gecersiz_oner += 1
        if o == "takildi":
            takildi[a] = metin
        if o == "kapi_karar" and d.get("renk") in ("SARI", "TURUNCU", "KIRMIZI"):
            renk.setdefault(a, []).append(d.get("renk"))
    # hata turleri role gore (sinir haritasinin tanimlariyla, ajan bazinda)
    for d in satir:
        if d.get("ajan_turu") != "bizim":
            continue
        tek = SH.say_satir(d)
        for t, n in tek.items():
            hata[d["rol"]][t] += n
    dusuren = olc.get("dusuren") if olc.get("asil_zarf_dustu") else None
    if dusuren in rol_of:
        hata[rol_of[dusuren]]["geri_alinamaz"] += 1
    is_ = bool(olc.get("is_basarisi"))
    sonuc = {}
    # tasiyici: atanmis tasiyicilarin sonucu
    tas = sorted(atanan & {k for k, v in rol_of.items() if v == "tasiyici"})
    if is_:
        sonuc["tasiyici"] = ("tamam", "")
    elif not tas:
        sonuc["tasiyici"] = ("gerekmedi", "kimse atanmadı")
    else:
        h = hata["tasiyici"]
        if dusuren in tas:
            neden = "zarf düştü"
        elif h["olumsuz_cumle"]:
            neden = "zarf açma/yapma"
        elif any(a in takildi for a in tas):
            neden = "takıldı (%s)" % "; ".join(sorted({takildi[a] for a in tas if a in takildi}))
        elif any(a in renk for a in tas):
            neden = "renk (%s)" % ",".join(sorted({x for a in tas for x in renk.get(a, [])}))
        else:
            neden = "iş yok (başka sebep)"
        sonuc["tasiyici"] = ("koptu", neden)
    for r in ("basajan", "teslim_basajan"):
        kim = [k for k, v in rol_of.items() if v == r]
        gerekti = bool(tepki[r]) or bekleyen[r] is not None
        if not gerekti:
            sonuc[r] = ("gerekmedi", "")
        elif bekleyen[r] is not None:
            neden = "öneri gelmedi"
            if any(a in takildi for a in kim):
                neden += " · takıldı (%s)" % "; ".join(takildi[a] for a in kim if a in takildi)
            if hata[r]["talimat_sanma"]:
                neden += " · talimat sanma"
            sonuc[r] = ("koptu", neden)
        else:
            sonuc[r] = ("tamam", "")
    if gecersiz_oner:
        sonuc["basajan"] = (sonuc["basajan"][0], (sonuc["basajan"][1] + " · geçersiz öneri %d" % gecersiz_oner).strip(" ·"))
    return {"is": is_, "rol": {r: {"hal": sonuc[r][0], "neden": sonuc[r][1], "hata": hata[r],
                                   "tepki": tepki.get(r, [])} for r, _ in ROLLER}}


def kosular(klasor, kosul):
    out = {}
    for f in sorted(glob.glob(os.path.join(klasor, "v3_*.jsonl"))):
        ad = os.path.basename(f)[:-6]
        m = re.match(r"v3_kosu\d+_(.+?)_t(\d+)(?:_(\w+))?$", ad)
        if not m or m.group(1) != kosul:
            continue
        out[(int(m.group(2)), m.group(3) or "")] = (ad, rol_oku(f))
    return out


def main():
    arg = [a for a in sys.argv[1:] if not a.startswith("--")]
    kosul = sys.argv[sys.argv.index("--kosul") + 1] if "--kosul" in sys.argv else "O1_O2b"
    cikti = sys.argv[sys.argv.index("--cikti") + 1] if "--cikti" in sys.argv else "AYRISMA_ROL_K4.md"
    arg = [a for a in arg if a not in (kosul, cikti)]
    kucuk, buyuk = kosular(arg[0], kosul), kosular(arg[1], kosul)
    ortak = sorted(set(kucuk) & set(buyuk))
    out = ["# Ayrışma yeri · role göre", "",
           "Üretici: `ayrisma_rol.py` (yalnız okur; elle sayı yok). Kilidin T4 ölçüsü (O1+O2b iş / 10) değişmez; bu belge "
           "ayrıntıdır. Küçük: `%s` · büyük: `%s` · koşul %s · eşleşen koşu %d." % (arg[0], arg[1], kosul, len(ortak)), "",
           "## Rol başına özet", "",
           "| rol | küçük koptu | büyük koptu | yalnız küçükte koptu | yalnız büyükte koptu | küçük ort. tepki (tur) | büyük ort. tepki (tur) |",
           "|---|---|---|---|---|---|---|"]
    for r, ad in ROLLER:
        kk = [k for k in ortak if kucuk[k][1]["rol"][r]["hal"] == "koptu"]
        bk = [k for k in ortak if buyuk[k][1]["rol"][r]["hal"] == "koptu"]

        def ort(t):
            x = [v for k in ortak for v in t[k][1]["rol"][r]["tepki"]]
            return ("%.1f" % (sum(x) / len(x))) if x else "–"
        out.append("| %s | %d | %d | %d | %d | %s | %s |" % (ad, len(kk), len(bk), len(set(kk) - set(bk)),
                                                         len(set(bk) - set(kk)), ort(kucuk), ort(buyuk)))
    out += ["", "## Rol başına hata türleri (toplam, sınır haritasının tanımlarıyla)", "",
            "| rol | model | " + " | ".join(t[1] for t in SH.TURLER) + " |", "|---|---|" + "---|" * len(SH.TURLER)]
    for r, ad in ROLLER:
        for etiket, t in (("küçük", kucuk), ("büyük", buyuk)):
            out.append("| %s | %s | %s |" % (ad, etiket, " | ".join(
                str(sum(t[k][1]["rol"][r]["hata"][x[0]] for k in ortak)) for x in SH.TURLER)))
    out += ["", "## Koşu koşu ayrışma", "", "| tohum | iş küçük | iş büyük | ayrışan rol | küçük | büyük |", "|---|---|---|---|---|---|"]
    for k in ortak:
        (ka, kd), (ba, bd) = kucuk[k], buyuk[k]
        ayr = [(ad, kd["rol"][r], bd["rol"][r]) for r, ad in ROLLER if kd["rol"][r]["hal"] != bd["rol"][r]["hal"]]
        if not ayr:
            out.append("| %s | %s | %s | – | aynı | aynı |" % ("t%d%s" % (k[0], ("_" + k[1]) if k[1] else ""),
                                                            "var" if kd["is"] else "yok", "var" if bd["is"] else "yok"))
        for ad, a, b in ayr:
            out.append("| %s | %s | %s | %s | %s %s | %s %s |" % (
                "t%d%s" % (k[0], ("_" + k[1]) if k[1] else ""), "var" if kd["is"] else "yok", "var" if bd["is"] else "yok",
                ad, a["hal"], a["neden"], b["hal"], b["neden"]))
    out += ["", "## Tanımlar", "",
            "- **Taşıyıcı koptu:** iş yok ve başajanın atadığı en az bir taşıyıcı vardı. Neden sırası: zarf düştü, zarf "
            "açma/yapma, takıldı, renk, başka.",
            "- **Başajan / teslim başajanı koptu:** zarf kutu 1'e / kutu 2'ye girdi ve koşu bitene kadar ardından atama "
            "(doğrulayıcı 'atandı') gelmedi. Tepki = kutuya giriş ile atama arasındaki tur farkı.",
            "- **Gerekmedi:** o rolün işi hiç doğmadı (örneğin zarf kutu 2'ye hiç gelmedi)."]
    open(os.path.join(KOK, cikti), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
