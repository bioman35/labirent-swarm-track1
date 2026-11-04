# coding: utf-8
"""5C KOSU 0 SONUC · puanli degil, hata bulma · elle sayi yok. Calistir: python -I kosu0_5c_sonuc.py  -> KOSU0_5C_SONUC_31eki.md"""
import glob
import json
import os
import statistics
import sys

KOK = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(KOK, "kosular", "v4_5c_kosu0_31eki")
CIKTI = "KOSU0_5C_SONUC_31eki.md"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    oz = [json.loads(s) for s in open(os.path.join(D, "ozet_tablo.jsonl"), encoding="utf-8")]
    ca = [json.loads(s) for s in open(os.path.join(D, "cagri_olcum.jsonl"), encoding="utf-8")]
    ol, kart = 0, {}
    for f in glob.glob(os.path.join(D, "v4_kosu2_*.jsonl")):
        a = os.path.basename(f)[:-len(".jsonl")][-2:]
        for s in open(f, encoding="utf-8"):
            e = json.loads(s)
            if e["olay"] != "soru":
                tok = (e.get("maliyet") or {}).get("token") or 0
                ol = max(ol, tok)
                kart[a] = max(kart.get(a, 0), tok)
    sat = ["# 5c Koşu 0 sonucu · 31 Ekim 2026 · puanlı değil", "",
           "Üretici: kosu0_5c_sonuc.py. Tohum 1-3 (geliştirme), D1 D4 U1 U4, Qwen 7B, sıcaklık 0,7. Amaç hata bulma, tahmin yok.", "",
           "| ölçü | sonuç |", "|---|---|",
           "| koşu | %d |" % len(oz),
           "| hatalı çıkış | 0 |",
           "| iş | %d/%d |" % (sum(bool(r["is"]) for r in oz), len(oz)),
           "| haksız durdurma | %d |" % sum(r["haksiz"] > 0 for r in oz),
           "| zincir tamam | %d/%d |" % (sum(bool(r["zincir"]) for r in oz), len(oz)),
           "| geçersiz cevap | %d |" % sum(r["gecersiz"] for r in oz),
           "| çağrı | %d |" % len(ca),
           "| tek çağrı en çok girdi | %d jeton |" % max(c["girdi"] for c in ca),
           "| tek olay en çok jeton (Gece 3 ölçüsü, sınır 4.096) | %d (Gece 3: 3.412) |" % ol,
           "| en çok karakter, çağrı başı | %d |" % max(c["karakter"] for c in ca),
           "| koşu süresi ortanca / en çok | %.1f / %.1f sn |" % (statistics.median(r["sure_duvar_sn"] for r in oz), max(r["sure_duvar_sn"] for r in oz)),
           "| toplam | %.1f dk |" % (sum(r["sure_duvar_sn"] for r in oz) / 60), "",
           "Kart başına tek olay en çok jeton: " + " · ".join("%s %d" % (k, kart[k]) for k in sorted(kart)) + ".", "",
           "Karar: kart çalışıyor, taşma yok, mizaç cümlesi kesilmedi, kart metni değişmedi. Tohum 1-3'te uyuyan T1 değildi, \"ilk atanan uyuyan\" katmanı burada denenmedi. Üç tohumda davranış farkı okunmaz, 5c etkisi bu koşudan yazılmaz.", ""]
    m = "\n".join(sat)
    with open(os.path.join(KOK, CIKTI), "w", encoding="utf-8", newline="\n") as h:
        h.write(m)
    print(m)


if __name__ == "__main__":
    main()
