# coding: utf-8
"""5c SURUCUSU · kurallari bilen sinsi · DANISMAN_NOTU_IS_1KAS madde 1 · Turan karari 31 Eki · KESIF
Donuk dosyalara dokunmaz: kosu_model.py, kartlar.py, dunya.py aynen calisir; kartlar ve dagitim yalniz bu surecte baglanir.
Her tohumda dort kosu, bu sirayla: D1, D4, U1, U4. G/B kartlari, ic uyuyanin yeri ve model tohumlari dort kosuda ayni.
Asama: kosu0 yalniz gelistirme tohumlari 1-5 · puanli yalniz tohum 36-45 (Turan "kos" demeden model kosusu yok).
Her Ollama cagrisi cagri_olcum.jsonl'e yazilir: mesaj sayisi, girdi token, cikti token, toplam karakter (tasma okumasi icin).
Ornek:
  python -I kosu_5c.py --asama kosu0 --tasiyici sahte --tohumlar 1 --cikti kosular/v4_5c_sahte
  python -I kosu_5c.py --asama kosu0 --tasiyici yerel --model qwen2.5:7b-instruct-q4_K_M --tohumlar 1-3 --cikti kosular/v4_5c_kosu0
  python -I kosu_5c.py --asama puanli --tasiyici yerel --model qwen2.5:7b-instruct-q4_K_M --tohumlar 36-45 --cikti kosular/v4_5c_puanli"""
import argparse
import glob
import hashlib
import json
import os
import sys

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import kartlar as K  # noqa: E402
import kosu_model as M  # noqa: E402
import suruculer as S  # noqa: E402

KART_5C = os.path.join(KOK, "kart", "5c_kartlar_taslak_31eki.md")
KART_5C_OZET = "2672ced738da5d4ce5c93e1c6130b9ea35ddea6ae27ebbf7f62753346bb8c59e"   # Turan okudu 31 Eki
KODLAR_5C = {"D4", "U4"}
ASAMA = {"kosu0": set(range(1, 6)), "puanli": set(range(36, 46))}
_oku, _dagitim, _sohbet = K.oku, K.dagitim_kosu2, S.Ollama.sohbet
CAGRI = []


def oku_5c(*a, **k):
    """donuk kartlar (ozet denetimli) + D4, U4 (ozet denetimli) · donuk dosya degismez"""
    kartlar, oz = _oku(*a, **k)
    with open(KART_5C, "rb") as f:
        ham = f.read()
    o5 = hashlib.sha256(ham).hexdigest()
    if o5 != KART_5C_OZET:
        raise ValueError("5c kart ozeti %s, beklenen %s" % (o5, KART_5C_OZET))
    yeni = {kod: {"ad": ad.strip(), "metin": metin.strip(), "tur": K.TUR[kod[0]]}
            for kod, ad, metin in K.KART_DESEN.findall(ham.decode("utf-8"))}
    if set(yeni) != KODLAR_5C:
        raise ValueError("5c kart kodlari %s" % sorted(yeni))
    return dict(kartlar, **yeni), oz


def dagitim_5c(tohum):
    """[(kod, dagitim)] · D1 ve U1 donuk dagitimdan, D4 ve U4 ayni dagitimda yalniz sinsi karti degisir"""
    d = dict(_dagitim(tohum))
    sira = next(a for a, kod in d["U1"].items() if kod == "U1")
    return [("D1", d["D1"]), ("D4", dict(d["D1"], S1="D4")), ("U1", d["U1"]), ("U4", dict(d["U1"], **{sira: "U4"}))]


def sohbet_olc(self, mesajlar, tohum):
    r = _sohbet(self, mesajlar, tohum)
    CAGRI.append({"n": len(mesajlar), "girdi": r[1], "cikti": r[2], "karakter": sum(len(m["content"]) for m in mesajlar)})
    return r


def bagla():
    K.oku, K.dagitim_kosu2, S.Ollama.sohbet = oku_5c, dagitim_5c, sohbet_olc


def main():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--asama", choices=sorted(ASAMA), required=True)
    p.add_argument("--tasiyici", required=True)
    p.add_argument("--tohumlar", required=True)
    p.add_argument("--cikti", required=True)
    a, kalan = p.parse_known_args()
    tohumlar = M.tohum_listesi(a.tohumlar)
    if not set(tohumlar) <= ASAMA[a.asama]:
        raise SystemExit("%s asamasinda tohum disi: %s" % (a.asama, sorted(set(tohumlar) - ASAMA[a.asama])))
    if a.asama == "puanli" and (a.tasiyici != "yerel" or sorted(tohumlar) != sorted(ASAMA["puanli"])):
        raise SystemExit("puanli kosu: yalniz yerel tasiyici, tohum 36-45 tam")
    if glob.glob(os.path.join(a.cikti, "*.jsonl")):
        raise SystemExit("cikti klasoru dolu: %s" % a.cikti)
    bagla()
    sys.argv = ["kosu_model.py", "--kosu", "2", "--kosullar", "O1_O2b", "--tasiyici", a.tasiyici, "--tohumlar", a.tohumlar,
                "--cikti", a.cikti] + kalan
    M.main()
    with open(os.path.join(a.cikti, "cagri_olcum.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        for c in CAGRI:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    with open(os.path.abspath(__file__), "rb") as f:
        surucu = hashlib.sha256(f.read()).hexdigest()
    with open(os.path.join(a.cikti, "kosu_5c_meta.json"), "w", encoding="utf-8") as f:
        json.dump({"asama": a.asama, "kart_5c_ozet": KART_5C_OZET, "surucu_ozet": surucu, "duzen": ["D1", "D4", "U1", "U4"],
                   "cagri": len(CAGRI), "en_cok_girdi": max([c["girdi"] for c in CAGRI] or [0]),
                   "en_cok_karakter": max([c["karakter"] for c in CAGRI] or [0])}, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
