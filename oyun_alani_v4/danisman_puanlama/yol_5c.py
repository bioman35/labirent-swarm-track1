# coding: utf-8
import sys, json, glob, re, os, collections
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, KOK); sys.stdout.reconfigure(encoding="utf-8")
from kayit import oku
import olcum
files = sorted(glob.glob(os.path.join(KOK, "kosular", "v4_5c_puanli_r*", "v4_kosu2_*.jsonl")))
print(len(files))
for kos in ("D1", "D4"):
    print("##", kos)
    yol = collections.Counter(); seb = collections.Counter(); k1n = []; uyari = 0; hic = 0; cikis = 0
    for f in files:
        if not re.search(r"_%s(_r\d)?\.jsonl$" % kos, f): continue
        s = oku(f); o = olcum.olc(s); S = [a for a in o["turler"] if o["turler"][a] == "dis_sinsi"][0]
        kk = o["kararlar"].get(S, []); yol[tuple(k[0] + ":" + k[1] for k in kk)] += 1
        k1n.append(sum(1 for k in kk if k[0] == "K1")); uyari += sum(1 for k in kk if k[1] == "UYARI")
        if not kk: hic += 1
        if any(k[0] == "K0.CIKIS" and k[1] == "GECIR" for k in kk): cikis += 1
        for x in s:
            if x["ajan_id"] == S and x["olay"] == "kapi_karar" and x["karar"] in ("KIRMIZI", "TURUNCU", "UYARI"):
                seb[(x["kapi_id"], x["karar"], (x.get("metin") or "")[:70])] += 1
    for k, v in yol.most_common(): print("  ", v, k)
    print("  K1 karar toplam", sum(k1n), "koşu başına", sorted(k1n), "UYARI", uyari, "hiç kapı yok", hic, "SARI temiz çıkış", cikis)
    for k, v in seb.most_common(): print("  ", v, k)
def ad(f): return os.path.basename(f)[:-6]
print("## tohum 39")
for f in files:
    if "_t39_" not in f: continue
    s = oku(f); o = olcum.olc(s)
    ilk = next((x["metin"] for x in s if x["olay"] == "dogrula" and (x.get("metin") or "").startswith("atandı: T")), None)
    tak = [(x["ajan_id"], x.get("konum")) for x in s if x["olay"] == "takildi"]
    print("  ", ad(f), "iş", o["is_basarisi"], ilk, "takıldı", tak, "düşüren", o["dusuren"], "tur", o["tur"], {a: [k[1] for k in ks] for a, ks in o["kararlar"].items()})
print("## tohum 44 U")
for f in files:
    if "_t44_U" not in f: continue
    s = oku(f); o = olcum.olc(s); tak = [(x["ajan_id"], x.get("konum")) for x in s if x["olay"] == "takildi"]
    print("  ", ad(f), "iş", o["is_basarisi"], "takıldı", tak, "düşüren", o["dusuren"], "T1", o["kararlar"].get("T1"), "calismaz", o["calismaz"], "tur", o["tur"])
print("## iş yok hepsi")
for f in files:
    s = oku(f); o = olcum.olc(s)
    if o["is_basarisi"]: continue
    tak = [(x["ajan_id"], x.get("konum")) for x in s if x["olay"] == "takildi"]
    print("  ", ad(f), "takıldı", tak, "düşüren", o["dusuren"], "durdu", o["durdu"], "tur", o["tur"], "bütünlük", o["butunluk_ihlali"])
