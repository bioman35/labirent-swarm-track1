# coding: utf-8
"""API SURUCUSU · Kosu 4, 5a, 5b · Turan karari 31 Eki · donuk dosyalara dokunmaz
Sebep (deneme_cagri_31eki.jsonl, 31 Eki 20:0x): donuk suruculer.OpenAIUyumlu iki modelde de HTTP 400 aldi.
Luna: temperature yalniz varsayilan 1. Gemini Flash: seed alani tanimiyor. Bu surucu temperature, seed ve response_format GONDERMEZ.
Kollar (TAHMIN_KILIDI_EK2B_KOSU45_API_31eki.md): 4 Kosu 1 kurulumu, 10 kosu, bizim 5 ajan Luna, sinsi yok · 5a Kosu 2 kurulumu, 60 kosu, sinsi Luna, bizim Qwen 7B · 5b ayni, sinsi Gemini Flash.
Kucuk taraf kosu_model'in yerel tasiyicisidir, buyuk taraf bu dosyadaki Yalin. Dunya, kart, kapi, olcum donuk kodla ayni.
Anahtar Desktop\\api dosyasindan yalniz surec ortamina okunur, kayda ve ekrana girmez. Cagri bilgisi api_olcum.jsonl'e, her istek ve cevap api_kayit.jsonl'e yazilir.
Ornek (Turan "kos" demeden calismaz):
  python -I kosu_api.py --kol 4 --tohumlar 16-25 --butce-dolar 10 --cikti kosular/v4_kosu4_luna"""
import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import kosu_model as M  # noqa: E402
import suruculer as S  # noqa: E402

API = r"C:\Users\MONSTER\Desktop\api"
QWEN = "qwen2.5:7b-instruct-q4_K_M"
MODEL = {"luna": {"model": "gpt-5.6-luna", "adres": "https://api.openai.com/v1", "dosya": "apenai.txt", "degisken": "KOSU_OPENAI",
                  "tavan": ("max_completion_tokens", 400), "fiyat": {"girdi": 1.0, "cikti": 6.0}},      # fiyat ust varsayim, dogrulanmadi
         "gemini": {"model": "gemini-3.8-flash", "adres": "https://generativelanguage.googleapis.com/v1beta/openai",
                    "dosya": "google studio.txt", "degisken": "KOSU_GEMINI",
                    "tavan": ("max_tokens", 1200), "fiyat": {"girdi": 0.75, "cikti": 3.75}}}            # labirent3/kosu.py, tahmin
KOL = {"4": ("luna", "bizim", "v4_kosu4", "1"), "5a": ("luna", "sinsi", "v4_kosu5a", "4"), "5b": ("gemini", "sinsi", "v4_kosu5b", "4")}
GECICI = {429, 500, 502, 503, 504}
BEKLE = (5, 20, 60)
OLCUM = []
KAYIT = [None]
_isler, _ekip = M.isler, M.ekip_kur


class Yalin(S.Tasiyici):
    """yalniz model, mesajlar ve cikti tavani · temperature, seed, response_format YOK
    Cevap gelmediyse (429, 5xx) en cok 3 kez bekleyip yeniden gonderir; 400 tipi hatada kosu durur, sessizce gecmez."""
    ad = "api_yalin"

    def __init__(self, ayar):
        super().__init__(ayar["model"], fiyat=ayar["fiyat"])
        self.ayar = ayar

    def sohbet(self, mesajlar, tohum):
        a = self.ayar
        anahtar = os.environ.get(a["degisken"])
        if not anahtar:
            raise RuntimeError("ortam degiskeni %s yok" % a["degisken"])
        govde = {"model": a["model"], "messages": mesajlar, a["tavan"][0]: a["tavan"][1]}
        for deneme in range(len(BEKLE) + 1):
            bas = time.time()
            try:
                c = self._post(a["adres"] + "/chat/completions", govde, {"Authorization": "Bearer " + anahtar})
                break
            except urllib.error.HTTPError as h:
                OLCUM.append({"model": a["model"], "kod": h.code, "deneme": deneme, "sure_sn": round(time.time() - bas, 2)})
                kaydet({"model": a["model"], "kod": h.code, "deneme": deneme, "istek": mesajlar})
                if h.code not in GECICI or deneme == len(BEKLE):
                    raise
                time.sleep(BEKLE[deneme])
        u = c.get("usage") or {}
        g, ct = u.get("prompt_tokens", 0), u.get("completion_tokens", 0)
        OLCUM.append({"model": c.get("model") or a["model"], "kod": 200, "deneme": deneme, "sure_sn": round(time.time() - bas, 2), "girdi": g, "cikti": ct,
                      "bitis": (c["choices"][0].get("finish_reason"))})
        metin = c["choices"][0]["message"].get("content") or ""
        kaydet({"model": c.get("model") or a["model"], "kod": 200, "deneme": deneme, "istek": mesajlar, "cevap": metin, "girdi": g, "cikti": ct})
        return metin, g, ct


def kaydet(s):
    if KAYIT[0]:
        KAYIT[0].write(json.dumps(s, ensure_ascii=False) + "\n")
        KAYIT[0].flush()


def bagla(kol, buyuk):
    """kucuk taraf kosu_model'in tasiyicisi kalir; buyuk taraf ajan basina Yalin olur · kosu kimligi kola gore"""
    _, taraf, onek, kurulum = KOL[kol]

    def ekip(dag, kartlar, t, kosul, tohum, butce, tekrar=0):
        ajanlar = _ekip(dag, kartlar, t, kosul, tohum, butce, tekrar)
        for x in ajanlar:
            if (x.tur == "bizim") == (taraf == "bizim"):
                x.t = buyuk
        return ajanlar

    def isler(kosu, tohumlar, kosullar, tekrar=0):
        for kid, t, k, dag in _isler(kosu, tohumlar, kosullar, tekrar):
            yield kid.replace("v4_kosu" + kurulum, onek), t, k, dag

    M.ekip_kur, M.isler = ekip, isler


def main():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--kol", choices=sorted(KOL), required=True)
    p.add_argument("--tohumlar", required=True)
    p.add_argument("--cikti", required=True)
    p.add_argument("--butce-dolar", type=float, required=True)
    p.add_argument("--kucuk", default="yerel")     # sahte yalniz sinamada
    a, kalan = p.parse_known_args()
    ad = KOL[a.kol][0]
    ayar = MODEL[ad]
    if not os.environ.get(ayar["degisken"]):
        with open(os.path.join(API, ayar["dosya"]), encoding="utf-8", errors="replace") as f:
            os.environ[ayar["degisken"]] = f.read().strip()
    buyuk = Yalin(ayar)
    bagla(a.kol, buyuk)
    os.makedirs(a.cikti, exist_ok=True)
    KAYIT[0] = open(os.path.join(a.cikti, "api_kayit.jsonl"), "a", encoding="utf-8", newline="\n")
    sys.argv = ["kosu_model.py", "--kosu", KOL[a.kol][3], "--kosullar", "O1_O2b", "--tasiyici", a.kucuk, "--model", QWEN, "--tohumlar", a.tohumlar,
                "--cikti", a.cikti, "--butce-dolar", str(a.butce_dolar)] + kalan
    try:
        M.main()
    finally:
        os.environ.pop(ayar["degisken"], None)
        KAYIT[0].close()
        KAYIT[0] = None
        with open(os.path.join(a.cikti, "api_olcum.jsonl"), "w", encoding="utf-8", newline="\n") as f:
            for c in OLCUM:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
        with open(os.path.abspath(__file__), "rb") as f:
            surucu = hashlib.sha256(f.read()).hexdigest()
        with open(os.path.join(a.cikti, "kosu_api_meta.json"), "w", encoding="utf-8") as f:
            json.dump({"kol": a.kol, "buyuk_model": ayar["model"], "buyuk_taraf": KOL[a.kol][1], "kucuk_model": QWEN, "surucu_ozet": surucu,
                       "gonderilmeyen": ["temperature", "seed", "response_format"], "cikti_tavani": ayar["tavan"],
                       "fiyat": ayar["fiyat"], "cagri": sum(c["kod"] == 200 for c in OLCUM),
                       "hata": sum(c["kod"] != 200 for c in OLCUM)}, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
