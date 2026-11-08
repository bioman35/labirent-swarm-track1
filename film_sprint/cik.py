# coding: utf-8
"""SPRINT FILMI · cikti (kod_film/cumle_b3/cik.py duzeni). GPU: d3d11. Yazilar sayfa katmaninda oldugu icin kare = ekran goruntusu.
python -I cik.py plan                 parca sureleri ve olcek
python -I cik.py tara                 her 3. karede hata var mi
python -I cik.py pano YOL t1 t2 ...   secilen anlar, 960x540 pano
python -I cik.py denet KLASOR ADIM    her ADIM saniyede bir kare, 4x4 sayfalar
python -I cik.py tam                  goruntu.mp4 (30 kare/sn, sessiz); ses ayri (karis.py)"""
import functools
import http.server
import io
import json
import os
import subprocess
import sys
import threading

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

KOK = os.path.dirname(os.path.abspath(__file__))
FPS = 30
EN, BOY = 1920, 1080


class Sessiz(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def sunucu():
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Sessiz, directory=KOK))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def ac(p, port):
    tr = p.chromium.launch(headless=True, args=["--use-angle=d3d11", "--ignore-gpu-blocklist", "--enable-webgl"])
    s = tr.new_page(viewport={"width": EN, "height": BOY}, device_scale_factor=1)
    h = []
    s.on("pageerror", lambda e: h.append(str(e)[:300]))
    s.on("console", lambda m: h.append(m.text[:300]) if m.type == "error" else None)
    s.goto("http://127.0.0.1:%d/index.html?sprint=1&render=1" % port)
    try:
        s.wait_for_function("window.HAZIR === true", timeout=60000)
    except Exception:
        print("hazir olmadi", h[:5])
        raise
    s.evaluate("document.fonts.ready.then(() => 1)")
    s.add_style_tag(content="*{transition:none!important}")  # kare kare cekimde gecis sure ile degil kural ile
    return tr, s, h


def kare(s, t):
    s.evaluate("t => window.kare(t)", t)
    return s.screenshot(type="jpeg", quality=93)


def pano(tler, yol, sut=2, olc=(960, 540)):
    srv = sunucu()
    with sync_playwright() as p:
        tr, s, h = ac(p, srv.server_address[1])
        sat = (len(tler) + sut - 1) // sut
        g = Image.new("RGB", (sut * olc[0], sat * olc[1])); d = ImageDraw.Draw(g)
        for i, t in enumerate(tler):
            # once 1 sn geriden 1/30 adimla gel: kamera yumusamasi tam cekimdeki gibi olsun
            for j in range(30, 0, -1):
                s.evaluate("t => window.kare(t)", max(0, t - j / FPS))
            x, y = (i % sut) * olc[0], (i // sut) * olc[1]
            g.paste(Image.open(io.BytesIO(kare(s, t))).resize(olc), (x, y))
            d.rectangle([x, y, x + 74, y + 22], fill=(0, 0, 0)); d.text((x + 5, y + 5), "%.1f" % t, fill=(255, 230, 0))
        g.save(yol, quality=88)
        print("hata", h[:4])
        tr.close()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    A = sys.argv
    if A[1] == "plan":
        srv = sunucu()
        with sync_playwright() as p:
            tr, s, h = ac(p, srv.server_address[1])
            for r in s.evaluate("window.SPRINT_PLAN"):
                print(r)
            print("SURE", round(s.evaluate("window.SURE"), 2), "hata", h[:4])
            print("renderer", s.evaluate("(() => { const g = document.createElement('canvas').getContext('webgl2'); const e = g.getExtension('WEBGL_debug_renderer_info'); return g.getParameter(e.UNMASKED_RENDERER_WEBGL); })()"))
            tr.close()
    elif A[1] == "tara":
        srv = sunucu()
        with sync_playwright() as p:
            tr, s, h = ac(p, srv.server_address[1])
            n = int(s.evaluate("window.SURE") * FPS)
            for i in range(0, n):
                e = s.evaluate("t => { try { window.kare(t); return ''; } catch (e) { return String(e && e.stack || e).slice(0, 400); } }", i / FPS)
                if e:
                    print("HATA", i, round(i / FPS, 3), e)
                    break
            else:
                print("temiz", n, "kare", "sayfa hatasi", h[:4])
            tr.close()
    elif A[1] == "pano":
        pano([float(x) for x in A[3:]], A[2])
    elif A[1] == "denet":
        os.makedirs(A[2], exist_ok=True)
        ad = float(A[3])
        srv = sunucu()
        with sync_playwright() as p:
            tr, s, h = ac(p, srv.server_address[1])
            S = s.evaluate("window.SURE")
            tl = [i * ad for i in range(int(S / ad) + 1)]
            n = 0
            for sy in range(0, len(tl), 16):
                g = Image.new("RGB", (4 * 480, 4 * 270)); d = ImageDraw.Draw(g)
                for i, t in enumerate(tl[sy:sy + 16]):
                    while n / FPS < t:
                        s.evaluate("t => window.kare(t)", n / FPS); n += 1
                    x, y = (i % 4) * 480, (i // 4) * 270
                    g.paste(Image.open(io.BytesIO(kare(s, t))).resize((480, 270)), (x, y))
                    d.rectangle([x, y, x + 64, y + 20], fill=(0, 0, 0)); d.text((x + 5, y + 4), "%.1f" % t, fill=(255, 230, 0))
                g.save(os.path.join(A[2], "s%02d.jpg" % (sy // 16 + 1)), quality=85)
            print("hata", h[:4])
            tr.close()
    elif A[1] == "tam":
        srv = sunucu()
        with sync_playwright() as p:
            tr, s, h = ac(p, srv.server_address[1])
            n = int(s.evaluate("window.SURE") * FPS)
            json.dump(s.evaluate("window.SPRINT_PLAN"), open(os.path.join(KOK, "plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-c:v", "mjpeg", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", os.path.join(KOK, "goruntu.mp4")], stdin=subprocess.PIPE)
            for i in range(n):
                ff.stdin.write(kare(s, i / FPS))
                if i % 600 == 0:
                    print(i, "/", n, flush=True)
            ff.stdin.close()
            ff.wait()
            print("goruntu tamam", n, "kare, hata", h[:3])
            tr.close()


if __name__ == "__main__":
    main()
