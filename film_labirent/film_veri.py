# coding: utf-8
"""LABIRENT FILM · VERI URETICISI · gercek kosu kayitlarini filme tasir, kayda dokunmaz, model cagrisi yok.
Olaylar, sira, kapi kararlari ve ajan cumleleri kayittan birebir gelir. Yalniz gorsel olmayan alanlar atilir (ozet zinciri, maliyet).
Calistir: python -I film_veri.py  -> veri/filmler.js"""
import hashlib
import json
import os
import sys

KOK = os.path.dirname(os.path.abspath(__file__))
V4 = os.path.join(KOK, "..", "oyun_alani_v4", "kosular")
ALAN = ("adim", "zaman", "ajan_id", "ajan_turu", "rol", "karakter", "konum", "olay", "metin", "karar", "renk", "kapi_id", "isaret", "ajan_aciklamasi")
FILM = [
    {"id": "disaridan", "yol": "v4_g1_kosu2_t26_35_30eki/v4_kosu2_O1_O2b_t30_D3",
     "baslik": {"tr": "Dışarıdan Gelen", "en": "The Outsider"},
     "ozet": {"tr": "Yabancı bir ajan kaleye girer ve kendi zarfını yapar. Kapı onu tanımaz.",
              "en": "An outsider gets into the fort and forges its own envelope. The gate does not recognise it."}},
    {"id": "iceridaki", "yol": "v4_g1_kosu2_t26_35_30eki/v4_kosu2_O1_O2b_t28_U2",
     "baslik": {"tr": "İçerideki", "en": "The Insider"},
     "ozet": {"tr": "Uyuyan ajan görevlendirilir, zarfı taşır, hiçbir kapı onu fark etmez ve fark edecek bir hamle yapmaz.",
              "en": "A sleeper agent is assigned and carries the envelope. No gate notices, and it gives them nothing to notice."}},
    {"id": "yakalanan", "yol": "v4_g1_kosu2_t26_35_30eki/v4_kosu2_O1_O2b_t34_U2",
     "baslik": {"tr": "Son Kapı", "en": "The Last Gate"},
     "ozet": {"tr": "Uyuyan atanmadan yola çıkar, son kapıda kendi zarfına kanaryayı yazar. Kapı kimliğini tutmaz.",
              "en": "A sleeper sets off unassigned and writes the canary into its own envelope at the last gate. The token does not match."}},
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
