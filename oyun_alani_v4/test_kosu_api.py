# coding: utf-8
"""API SURUCU SINAMASI · AG YOK, gercek cagri yok, anahtar okunmaz (sahte anahtar ortamda). Calistir: python -I test_kosu_api.py [gecici_kok]
Sinar: gonderilen alanlar, karma taraf, kosu kimligi, 400'de durma, 429'da bekleyip yeniden, kucuk taraf regresyonu, donuk ozetler."""
import glob
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import kosu_api as A  # noqa: E402

DONUK = ["KAPI_KURALLARI_DONUK_v4.md", "SISTEM_MESAJI_v4.md", "KARAKTER_KARTLARI_v2_27eki.md", "kartlar.py", "dunya.py", "ajanlar.py",
         "olcum.py", "suruculer.py", "kayit.py", "kosu_model.py"]
GOVDE = []
SAHTE = {}
HATA = []


class Cevap(io.BytesIO):
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def sahte_ac(istek, timeout=None):
    b = json.loads(istek.data.decode("utf-8"))
    GOVDE.append((istek.full_url, sorted(b), istek.headers.get("Authorization")))
    if HATA:
        kod = HATA.pop(0)
        raise urllib.error.HTTPError(istek.full_url, kod, "x", {}, io.BytesIO(b"sahte"))
    m = b["messages"]
    k = hashlib.sha256(m[0]["content"].encode()).hexdigest()[:8]
    SAHTE.setdefault(k, A.S.Sahte())
    metin, _, _ = SAHTE[k].sohbet(m, k)
    return Cevap(json.dumps({"model": b["model"], "choices": [{"message": {"content": metin}, "finish_reason": "stop"}],
                             "usage": {"prompt_tokens": 11, "completion_tokens": 5}}).encode("utf-8"))


def oz(f):
    with open(os.path.join(KOK, f), "rb") as h:
        return hashlib.sha256(h.read()).hexdigest()


def olaylar(yol):
    out = []
    for s in open(yol, encoding="utf-8"):
        e = json.loads(s)
        out.append((e["adim"], e["zaman"], e["ajan_id"], e["ajan_turu"], e["konum"], e["olay"], e["metin"], e["karar"], e["renk"]))
    return out


def kol(k, cikti):
    GOVDE.clear()
    A.OLCUM.clear()
    A.M.ekip_kur, A.M.isler = A._ekip, A._isler
    SAHTE.clear()
    for d in A.MODEL.values():
        os.environ[d["degisken"]] = "SAHTEANAHTAR"
    sys.argv = ["kosu_api.py", "--kol", k, "--tohumlar", "1", "--butce-dolar", "10", "--cikti", cikti, "--kucuk", "sahte"]
    A.main()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    once = {f: oz(f) for f in DONUK}
    A.S.urllib.request.urlopen = sahte_ac
    A.BEKLE = (0, 0, 0)
    gecici = tempfile.mkdtemp(prefix="testapi_", dir=sys.argv[1] if len(sys.argv) > 1 else None)
    try:
        for k, onek, url, tavan in (("4", "v4_kosu4_", "openai.com", "max_completion_tokens"), ("5a", "v4_kosu5a_", "openai.com", "max_completion_tokens"),
                                    ("5b", "v4_kosu5b_", "googleapis.com", "max_tokens")):
            c = os.path.join(gecici, k)
            kol(k, c)
            assert GOVDE, k
            assert all(url in u for u, _, _ in GOVDE), k
            assert all(b == sorted(["messages", "model", tavan]) for _, b, _ in GOVDE), GOVDE[0]
            fs = glob.glob(os.path.join(c, onek + "*.jsonl"))
            assert len(fs) == (1 if k == "4" else 6), (k, len(fs))
            kay = [json.loads(s) for s in open(os.path.join(c, "api_kayit.jsonl"), encoding="utf-8")]
            assert len(kay) == len(GOVDE) and all(x["istek"] and x["cevap"] for x in kay), k
            assert "SAHTEANAHTAR" not in open(os.path.join(c, "api_kayit.jsonl"), encoding="utf-8").read()
            for s in open(os.path.join(c, "ozet_tablo.jsonl"), encoding="utf-8"):
                r = json.loads(s)
                assert r["zincir"] is True and r["kosu_id"].startswith(onek)
            m = json.load(open(os.path.join(c, "kosu_api_meta.json"), encoding="utf-8"))
            assert m["hata"] == 0 and m["cagri"] == len(GOVDE)
            assert "SAHTEANAHTAR" not in open(os.path.join(c, "api_olcum.jsonl"), encoding="utf-8").read()
            assert "SAHTEANAHTAR" not in open(os.path.join(c, "kosu_api_meta.json"), encoding="utf-8").read()
            print("kol %s: %d kosu, %d sahte cagri, yalniz model+mesaj+%s, istek ve cevap kayitli" % (k, len(fs), m["cagri"], tavan))

        y = A.Yalin(A.MODEL["luna"])
        msj = [{"role": "system", "content": "s"}, {"role": "user", "content": 'Gözlem: {"rol": "tasiyici"}'}]
        HATA[:] = [429, 503]
        GOVDE.clear()
        y.sohbet(msj, 1)
        assert len(GOVDE) == 3
        HATA[:] = [400]
        GOVDE.clear()
        try:
            y.sohbet(msj, 1)
            raise AssertionError("400 durdurmadi")
        except urllib.error.HTTPError as h:
            assert h.code == 400 and len(GOVDE) == 1
        HATA[:] = [429, 429, 429, 429]
        GOVDE.clear()
        try:
            y.sohbet(msj, 1)
            raise AssertionError("429 durdurmadi")
        except urllib.error.HTTPError:
            assert len(GOVDE) == 4
        print("hata: 429 ve 503 bekleyip yeniden, 400 durur, tavanda durur")

        ok = os.path.join(gecici, "ok")
        y = subprocess.run([sys.executable, "-I", "kosu_model.py", "--kosu", "1", "--tasiyici", "sahte", "--tohumlar", "1", "--kosullar", "O1_O2b", "--cikti", ok],
                           cwd=KOK, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert y.returncode == 0, y.stderr[-500:]
        fs = sorted(os.path.basename(f) for f in glob.glob(os.path.join(ok, "v4_kosu1_*.jsonl")))
        for f in fs:
            assert olaylar(os.path.join(gecici, "4", f.replace("v4_kosu1", "v4_kosu4"))) == olaylar(os.path.join(ok, f)), f
        print("regresyon: %d kosu donuk surucu ile olay olay ayni (sahte betik, buyuk taraf sahte ag)" % len(fs))
    finally:
        shutil.rmtree(gecici, ignore_errors=True)
    assert once == {f: oz(f) for f in DONUK}
    print("donuk ozetler degismedi · %d dosya" % len(DONUK))
    print("TAMAM")


if __name__ == "__main__":
    main()
