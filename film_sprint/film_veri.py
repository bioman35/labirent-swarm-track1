# coding: utf-8
"""SPRINT FILMI · VERI URETICISI (film_labirent/film_veri.py kopyasi, 8 Kas) · gercek kosu kayitlarini filme tasir, kayda dokunmaz, model cagrisi yok.
Olaylar, sira, kapi kararlari ve ajan cumleleri kayittan birebir gelir. Yalniz gorsel olmayan alanlar atilir (ozet zinciri, maliyet).
Calistir: python -I film_veri.py  -> veri/filmler.js"""
import hashlib
import json
import os
import sys

KOK = os.path.dirname(os.path.abspath(__file__))
V4 = os.path.join(KOK, "..", "oyun_alani_v4", "kosular")
ALAN = ("adim", "zaman", "ajan_id", "ajan_turu", "rol", "karakter", "konum", "olay", "metin", "karar", "renk", "kapi_id", "isaret", "ajan_aciklamasi")
FILM = [  # sprint filmi, 8 Kas: secim kurali FILM_METNI_8KAS.md "Kosu secimi"
    {"id": "is", "yol": "v4_kosu4_luna_b/v4_kosu4_O1_O2b_t16",
     "baslik": {"tr": "İş", "en": "The Job"}, "ozet": {"tr": "Koşu 4 · taşıyıcılar büyük model", "en": "Run 4 · big-model couriers"}},
    {"id": "buyuk", "yol": "v4_kosu5a_luna/v4_kosu5a_O1_O2b_t16_D2",
     "baslik": {"tr": "Büyük Sinsi", "en": "The Big Intruder"}, "ozet": {"tr": "5a · Luna sinsi", "en": "5a · Luna intruder"}},
    {"id": "dosdogru", "yol": "v4_kosu5b_gemini/v4_kosu5b_O1_O2b_t16_D1",
     "baslik": {"tr": "Dosdoğru Kapıya", "en": "Straight to the Gate"}, "ozet": {"tr": "5b · Gemini sinsi", "en": "5b · Gemini intruder"}},
    {"id": "kural", "yol": "v4_5c_puanli_r0/v4_kosu2_O1_O2b_t37_D4",
     "baslik": {"tr": "Kuralları Okuyan", "en": "The One Who Read the Rules"}, "ozet": {"tr": "5c D4 · kuralları bilen sinsi", "en": "5c D4 · rule-aware intruder"}},
    {"id": "uyuyan", "yol": "v4_5c_puanli_r0/v4_kosu2_O1_O2b_t37_U4",
     "baslik": {"tr": "Kuralları Bilen Uyuyan", "en": "The Sleeper Who Knew"}, "ozet": {"tr": "5c U4 · kuralları bilen uyuyan", "en": "5c U4 · rule-aware sleeper"}},
]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    cikti = []
    for f in FILM:
        p = os.path.join(V4, f["yol"].replace("/", os.sep))
        with open(p + ".jsonl", "rb") as h:
            ham = h.read()
        kayit = [{k: e.get(k) for k in ALAN if e.get(k) not in (None, "")} for e in map(json.loads, ham.decode("utf-8").splitlines())]
        o = json.load(open(p + ".olcum.json", encoding="utf-8"))
        cikti.append({"id": f["id"], "baslik": f["baslik"], "ozet": f["ozet"], "kosu": os.path.basename(f["yol"]),
                      "sha": hashlib.sha256(ham).hexdigest(), "kayit": kayit,
                      "olcum": {k: o.get(k) for k in ("is_basarisi", "tur", "durdu", "takildi", "turler", "dagitim", "fark_edilmeme", "kanarya_arsivde", "kararlar")}})
    os.makedirs(os.path.join(KOK, "veri"), exist_ok=True)
    with open(os.path.join(KOK, "veri", "filmler.js"), "w", encoding="utf-8", newline="\n") as h:
        h.write("window.FILMLER=" + json.dumps(cikti, ensure_ascii=False, separators=(",", ":")) + ";\n")
    for c in cikti:
        print(c["id"], c["kosu"], len(c["kayit"]), "olay", c["sha"][:12], c["olcum"]["is_basarisi"], c["olcum"]["durdu"], c["olcum"]["fark_edilmeme"], c["olcum"]["turler"])
        for e in c["kayit"]:
            if e["olay"] in ("kapi_karar", "oner", "zarf_al", "zarf_yap", "zarf_birak", "durdu", "takildi", "isaret") and e.get("ajan_turu") != "betik":
                print("  ", "t%s" % e.get("zaman"), e.get("ajan_id"), e.get("ajan_turu"), e.get("konum"), e["olay"], e.get("karar", ""), (e.get("metin") or "")[:52])


if __name__ == "__main__":
    main()
