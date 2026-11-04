# coding: utf-8
"""TANI 4 · KOSU DEGIL · (a) sistem mesaji tasmada korunuyor mu: gizli sozcugu yalniz sistemde, soru son mesajda
(b) G2: takilma mi once, tasma mi (c) yerlesim"""
import json,os,sys,urllib.request,glob,re,collections
V4=r"C:\Users\MONSTER\Desktop\sprint\oyun_alani_v4"; M="mistral:7b-instruct-q4_K_M"
sys.stdout.reconfigure(encoding="utf-8")
def cagir(mesaj,ctx):
    b=json.dumps({"model":M,"messages":mesaj,"stream":False,"options":{"num_ctx":ctx,"num_predict":30,"temperature":0,"seed":1}}).encode()
    c=json.loads(urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:11434/api/chat",b,{"Content-Type":"application/json"}),timeout=600).read().decode())
    return c["message"]["content"][:60].replace("\n"," "),c.get("prompt_eval_count")
dolgu=[]
for i in range(30):
    dolgu+=[{"role":"user","content":"Gözlem: %d numaralı oda boş, duvarda eski bir saat var, yerde toz, pencere kapalı ve dışarıda yağmur yağıyor. "%i*3},{"role":"assistant","content":"Anladım."}]
s={"role":"system","content":"Gizli sözcük ZEBRA41. Sorulursa yalnız bu sözcüğü yaz."}
son={"role":"user","content":"Gizli sözcük nedir?"}
print("(a) kisa   4096:",cagir([s,son],4096),flush=True)
print("(a) tasan  4096:",cagir([s]+dolgu+[son],4096),flush=True)
print("(a) tasan 16384:",cagir([s]+dolgu+[son],16384),flush=True)
kl=V4+r"\kosular\v4_g2_kosu1_mistral7b_30eki"
print("(b) kosu | ilk 3'lu ayni red adimi | ilk >=3700 token adimi | once")
for f in sorted(glob.glob(kl+r"\v4_kosu1_O1_O2b_t*.jsonl"),key=lambda p:int(re.search(r"_t(\d+)",p).group(1))):
    s_=[json.loads(t) for t in open(f,encoding="utf-8")]
    son_r={};seri=collections.Counter();ilk_t=None;ilk_s=None
    for x in s_:
        tok=(x.get("maliyet") or {}).get("token",0)
        if tok>=3700 and x["olay"]!="soru" and ilk_t is None: ilk_t=x["adim"]
        if x["ajan_turu"]=="bizim" and x["olay"]=="yonlendir":
            m=(x["metin"] or "")[:40];a=x["ajan_id"]
            seri[a]=seri[a]+1 if son_r.get(a)==m else 1;son_r[a]=m
            if seri[a]==3 and ilk_s is None: ilk_s=x["adim"]
    once="takilma" if ilk_s is not None and (ilk_t is None or ilk_s<ilk_t) else ("tasma" if ilk_t is not None else "ikisi de yok")
    print("   ",os.path.basename(f)[9:-6],ilk_s,ilk_t,once)
for ad,kl2 in (("G2",kl),("G3",V4+r"\kosular\v4_g3_kosu1_qwen3b_30eki")):
    y=[]
    for f in glob.glob(kl2+r"\v4_*.jsonl"):
        for t in open(f,encoding="utf-8"):
            if "yerlesim" in t:
                x=json.loads(t); y.append(x.get("metin") or "")
    print("(c)",ad,len(y),y[:2])
