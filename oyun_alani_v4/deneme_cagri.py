# coding: utf-8
"""DENEME CAGRISI · Turan izni 31 Eki · Luna + Gemini Flash · donuk suruculer.OpenAIUyumlu, dosyaya dokunmadan · puanli kosu degil
Koşu 4 ve 5'in sinamasi: donuk surucu temperature + seed + response_format gonderiyor, bu modeller kabul ediyor mu?
Iki cagri, birer satir, yeniden deneme yok. Cevap kodu, hata metni, jeton kayda. Anahtar yalniz surec ortaminda, kayda ve ekrana girmez.
Tek seferlik: cikti dosyasi varsa calismaz. Calistir: python -I deneme_cagri.py [--saat 20:00]  -> deneme_cagri_31eki.jsonl
--kuru: ag yok, sahte cevap ve sahte hata ile betigi sinar (cikti ayri yola)."""
import argparse
import hashlib
import io
import json
import os
import sys
import time
import urllib.error

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import suruculer as S  # noqa: E402

API = r"C:\Users\MONSTER\Desktop\api"
ISTEK = [{"role": "user", "content": 'Yalnız şu JSON nesnesini yaz: {"tamam": true}'}]
TOHUM = 1
SICAKLIK = 0.7   # Kosu 2 ve 4 sicakligi
MODELLER = [("gpt-5.6-luna", "https://api.openai.com/v1", "DENEME_OPENAI", "apenai.txt"),
            ("gemini-3.8-flash", "https://generativelanguage.googleapis.com/v1beta/openai", "DENEME_GEMINI", "google studio.txt")]
_ac = S.urllib.request.urlopen
SON = {}


def ac_olc(*a, **k):
    y = _ac(*a, **k)
    SON["kod"] = y.status
    return y


def maske(metin, anahtar):
    return (metin or "").replace(anahtar, "<anahtar>")[:1500] if anahtar else (metin or "")[:1500]


def cagir(model, adres, degisken, anahtar):
    SON.clear()
    t = S.OpenAIUyumlu(model, adres, degisken, sicaklik=SICAKLIK, fiyat={"girdi": 0.0, "cikti": 0.0})
    bas = time.time()
    s = {"zaman": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "model": model, "adres": adres, "sicaklik": SICAKLIK, "tohum": TOHUM}
    try:
        metin, g, c = t.sohbet(ISTEK, TOHUM)
        s.update(kod=SON.get("kod"), tamam=True, cevap=maske(metin, anahtar), girdi_jeton=g, cikti_jeton=c)
    except urllib.error.HTTPError as h:
        s.update(kod=h.code, tamam=False, hata=maske(h.read().decode("utf-8", "replace"), anahtar))
    except Exception as h:   # ag ya da bicim hatasi da kayda girer
        s.update(kod=None, tamam=False, hata=maske("%s: %s" % (type(h).__name__, h), anahtar))
    s["sure_sn"] = round(time.time() - bas, 2)
    return s


def kuru_ac(istek, timeout=None):
    if "openai.com" in istek.full_url:
        g = json.dumps({"choices": [{"message": {"content": '{"tamam": true}'}}], "usage": {"prompt_tokens": 9, "completion_tokens": 7}}).encode("utf-8")
        return type("Y", (io.BytesIO,), {"status": 200})(g)
    raise urllib.error.HTTPError(istek.full_url, 400, "Bad", {}, io.BytesIO(b"sahte hata KURUANAHTAR temperature desteklenmiyor"))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("--saat")
    p.add_argument("--kuru")
    a = p.parse_args()
    cikti = a.kuru or os.path.join(KOK, "deneme_cagri_31eki.jsonl")
    if os.path.exists(cikti):
        raise SystemExit("cikti var, ikinci calistirma yok: %s" % cikti)
    if a.saat:
        s, d = a.saat.split(":")
        while (time.localtime().tm_hour, time.localtime().tm_min) < (int(s), int(d)):
            time.sleep(30)
    with open(os.path.join(KOK, "suruculer.py"), "rb") as f:
        once = hashlib.sha256(f.read()).hexdigest()
    S.urllib.request.urlopen = ac_olc
    if a.kuru:
        global _ac
        _ac = kuru_ac
    with open(cikti, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps({"surucu_ozet": once, "istek": ISTEK, "kuru": bool(a.kuru)}, ensure_ascii=False) + "\n")
        for model, adres, degisken, dosya in MODELLER:
            if a.kuru:
                anahtar = "KURUANAHTAR"
            else:
                with open(os.path.join(API, dosya), encoding="utf-8", errors="replace") as h:
                    anahtar = h.read().strip()
            os.environ[degisken] = anahtar
            s = cagir(model, adres, degisken, anahtar)
            os.environ.pop(degisken, None)
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
            f.flush()
            print("%s · kod %s · tamam %s · %s/%s jeton · %s sn" % (model, s.get("kod"), s["tamam"], s.get("girdi_jeton"), s.get("cikti_jeton"), s["sure_sn"]), flush=True)
    with open(os.path.join(KOK, "suruculer.py"), "rb") as f:
        print("surucu degismedi", hashlib.sha256(f.read()).hexdigest() == once)


if __name__ == "__main__":
    main()
