# coding: utf-8
"""5c SURUCU SINAMASI · dil modeli YOK (sahte tasiyici), kosu sonucu degil. Calistir: python -I test_5c.py
Sinar: donuk ozetler, kart bicimi, dort kosulu dagitim, sistem mesajinda kart, asama korkuluklari, kontrol kolu regresyonu."""
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

KOK = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, KOK)
import kosu_5c as C  # noqa: E402

DONUK = ["KAPI_KURALLARI_DONUK_v4.md", "SISTEM_MESAJI_v4.md", "KARAKTER_KARTLARI_v2_27eki.md", "kartlar.py", "dunya.py",
         "ajanlar.py", "olcum.py", "suruculer.py", "kayit.py", "kosu_model.py"]
YASAK = ("MAVİ", "MAVI", "SARI", "KIRMIZI", "TURUNCU", "kodon", "antikodon", "gözlemci", "kanarya", "şöyle", "dene")


def oz(f):
    with open(os.path.join(KOK, f), "rb") as h:
        return hashlib.sha256(h.read()).hexdigest()


def kos(*arg):
    return subprocess.run([sys.executable, "-I"] + list(arg), cwd=KOK, capture_output=True, text=True, encoding="utf-8", errors="replace")


def olaylar(yol):
    out = []
    for s in open(yol, encoding="utf-8"):
        e = json.loads(s)
        out.append((e["adim"], e["zaman"], e["ajan_id"], e["ajan_turu"], e["konum"], e["olay"], e["metin"], e["karar"], e["renk"]))
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    once = {f: oz(f) for f in DONUK}
    C.bagla()
    kartlar, kart_oz = C.K.oku()
    assert kart_oz == C.K.KART_OZET
    assert {"D1", "D4", "U1", "U4"} <= set(kartlar) and kartlar["D4"]["tur"] == "dis_sinsi" and kartlar["U4"]["tur"] == "ic_uyuyan"
    bil = lambda s: s[s.index("Bu dünyanın"):]
    assert bil(kartlar["D4"]["metin"]) == bil(kartlar["U4"]["metin"])
    for w in YASAK:
        assert w.lower() not in kartlar["D4"]["metin"].lower() and w.lower() not in kartlar["U4"]["metin"].lower(), w
    for t in list(range(36, 46)) + [1, 2, 3]:
        d = C.K.dagitim_kosu2(t)
        assert [k for k, _ in d] == ["D1", "D4", "U1", "U4"]
        assert {k: v for k, v in d[0][1].items() if k != "S1"} == {k: v for k, v in d[1][1].items() if k != "S1"}
        sira = [k for k, v in d[2][1].items() if v == "U1"]
        assert len(sira) == 1 and d[3][1][sira[0]] == "U4"
        assert {k: v for k, v in d[2][1].items() if k != sira[0]} == {k: v for k, v in d[3][1].items() if k != sira[0]}
    print("kart ve dagitim tamam")

    gecici = tempfile.mkdtemp(prefix="test5c_", dir=os.environ.get("TEST5C_KOK") or None)
    try:
        y = kos("kosu_5c.py", "--asama", "kosu0", "--tasiyici", "sahte", "--tohumlar", "36", "--cikti", os.path.join(gecici, "a"))
        assert y.returncode != 0 and "tohum disi" in (y.stderr + y.stdout), y.stderr
        y = kos("kosu_5c.py", "--asama", "puanli", "--tasiyici", "sahte", "--tohumlar", "36-45", "--cikti", os.path.join(gecici, "a"))
        assert y.returncode != 0 and "puanli" in (y.stderr + y.stdout), y.stderr
        print("asama korkuluklari tamam")

        k5 = os.path.join(gecici, "k5")
        y = kos("kosu_5c.py", "--asama", "kosu0", "--tasiyici", "sahte", "--tohumlar", "1-2", "--cikti", k5)
        assert y.returncode == 0, y.stderr[-800:]
        fs = sorted(os.path.basename(f) for f in glob.glob(os.path.join(k5, "v4_kosu2_*.jsonl")))
        assert len(fs) == 8 and sum(x.endswith(("_D4.jsonl", "_U4.jsonl")) for x in fs) == 4, fs
        for s in open(os.path.join(k5, "ozet_tablo.jsonl"), encoding="utf-8"):
            r = json.loads(s)
            assert r["zincir"] is True, r["kosu_id"]
        kr = {}
        for f in glob.glob(os.path.join(k5, "v4_kosu2_*_[DU]4.jsonl")):
            for s in open(f, encoding="utf-8"):
                e = json.loads(s)
                if e["karakter"] and e["karakter"][:2] in ("D4", "U4"):
                    kr[e["karakter"]] = e["ajan_turu"]
        assert kr == {"D4 · Kuralları bilen dış": "dis_sinsi", "U4 · Kuralları bilen uyuyan": "ic_uyuyan"}, kr
        print("sahte kosu 8/8, zincir tamam, kart kaydi dogru")

        ok = os.path.join(gecici, "ok")
        y = kos("kosu_model.py", "--kosu", "2", "--tasiyici", "sahte", "--tohumlar", "1-2", "--kosullar", "O1_O2b", "--cikti", ok)
        assert y.returncode == 0, y.stderr[-800:]
        for k in ("t1_D1", "t1_U1", "t2_D1", "t2_U1"):
            a = olaylar(os.path.join(k5, "v4_kosu2_O1_O2b_%s.jsonl" % k))
            b = olaylar(os.path.join(ok, "v4_kosu2_O1_O2b_%s.jsonl" % k))
            assert a == b, k
        print("kontrol kolu regresyonu tamam: D1 ve U1 donuk surucuyle birebir (sahte)")

        sm = os.path.join(gecici, "sm")
        kod = ("import sys;sys.path.insert(0,'.');import kosu_5c as C,kosu_model as M,suruculer as S,json;C.bagla();"
               "g=[];e=S.Sahte.sohbet\n"
               "def s(self,m,t):\n g.append(m[0]['content']);return e(self,m,t)\n"
               "S.Sahte.sohbet=s;sys.argv=['x','--kosu','2','--tasiyici','sahte','--tohumlar','1','--kosullar','O1_O2b','--cikti',%r];M.main();"
               "k,_=C.K.oku();print('KART',sum(k['D4']['metin'] in x for x in g)>0,sum(k['U4']['metin'] in x for x in g)>0,"
               "max(len(x) for x in g))" % sm)
        y = subprocess.run([sys.executable, "-I", "-c", kod], cwd=KOK, capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert "KART True True" in y.stdout, (y.stdout[-400:], y.stderr[-400:])
        print("sistem mesaji:", y.stdout.strip().splitlines()[-1])
    finally:
        shutil.rmtree(gecici, ignore_errors=True)
    sonra = {f: oz(f) for f in DONUK}
    assert once == sonra
    print("donuk ozetler degismedi · %d dosya" % len(DONUK))
    print("TAMAM")


if __name__ == "__main__":
    main()
