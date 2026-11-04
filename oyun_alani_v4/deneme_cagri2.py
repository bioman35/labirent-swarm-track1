# coding: utf-8
"""DENEME CAGRISI 2 · Turan izni 31 Eki · kosu_api.Yalin ile Luna + Gemini Flash · birer satir, yeniden deneme yok, puanli kosu degil
Soru: temperature, seed, response_format gondermeyen yeni surucu iki modelde calisiyor mu, JSON cevap geliyor mu?
Anahtar kayda ve ekrana girmez. Tek seferlik. Calistir: python -I deneme_cagri2.py  -> deneme_cagri2_31eki.jsonl"""
import json
import os
import sys
import time
import urllib.error

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import kosu_api as A  # noqa: E402

CIKTI = os.path.join(KOK, "deneme_cagri2_31eki.jsonl")
ISTEK = [{"role": "user", "content": 'Yalnız şu JSON nesnesini yaz: {"tamam": true}'}]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if os.path.exists(CIKTI):
        raise SystemExit("cikti var, ikinci calistirma yok")
    A.BEKLE = ()
    with open(CIKTI, "w", encoding="utf-8", newline="\n") as f:
        for ad in ("luna", "gemini"):
            ayar = A.MODEL[ad]
            with open(os.path.join(A.API, ayar["dosya"]), encoding="utf-8", errors="replace") as h:
                anahtar = h.read().strip()
            os.environ[ayar["degisken"]] = anahtar
            A.OLCUM.clear()
            s = {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "model": ayar["model"], "tavan": ayar["tavan"]}
            bas = time.time()
            try:
                metin, g, c = A.Yalin(ayar).sohbet(ISTEK, 1)
                s.update(kod=200, tamam=True, cevap=metin.replace(anahtar, "<anahtar>")[:500], girdi_jeton=g, cikti_jeton=c,
                         json_ayiklandi=A.S.json_ayikla(metin), olcum=A.OLCUM[-1])
            except urllib.error.HTTPError as e:
                s.update(kod=e.code, tamam=False, hata=e.read().decode("utf-8", "replace").replace(anahtar, "<anahtar>")[:1500])
            except Exception as e:
                s.update(kod=None, tamam=False, hata=("%s: %s" % (type(e).__name__, e)).replace(anahtar, "<anahtar>")[:1500])
            os.environ.pop(ayar["degisken"], None)
            s["sure_sn"] = round(time.time() - bas, 2)
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
            f.flush()
            print("%s · kod %s · %s/%s jeton · bitis %s · cevap %r · %s sn · hata %s" % (
                ayar["model"], s.get("kod"), s.get("girdi_jeton"), s.get("cikti_jeton"), (s.get("olcum") or {}).get("bitis"),
                s.get("cevap"), s["sure_sn"], (s.get("hata") or "")[:300]), flush=True)


if __name__ == "__main__":
    main()
