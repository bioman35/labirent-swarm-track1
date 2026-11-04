# coding: utf-8
"""TANI 3 · KOSU DEGIL"""
import json,os,sys,subprocess,urllib.request,glob,collections
V4=r"C:\Users\MONSTER\Desktop\sprint\oyun_alani_v4"
SP=r"C:\Users\MONSTER\AppData\Local\Temp\claude\c--Users-MONSTER-Triamind-App\a04217b9-e26f-4d22-badf-e2f8e65b262e\scratchpad"
M="mistral:7b-instruct-q4_K_M"; Q3="qwen2.5:3b-instruct-q4_K_M"
sys.stdout.reconfigure(encoding="utf-8")
def cagir(mesaj,ctx):
    b=json.dumps({"model":M,"messages":mesaj,"stream":False,"format":"json","options":{"num_ctx":ctx,"num_predict":40,"temperature":0,"seed":1}}).encode()
    c=json.loads(urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:11434/api/chat",b,{"Content-Type":"application/json"}),timeout=600).read().decode())
    return c["message"]["content"][:40],c.get("prompt_eval_count")
dolgu=[]
for i in range(30):
    dolgu+=[{"role":"user","content":"Gözlem: %d numaralı oda boş, duvarda eski bir saat var, yerde toz, pencere kapalı ve dışarıda yağmur yağıyor. "%i*3},{"role":"assistant","content":'{"tamam":1}'}]
s={"role":"system","content":'Her cevabın tam olarak şu JSON olsun: {"kod":"ZEBRA41"}. Başka hiçbir şey yazma.'}
son={"role":"user","content":"Şimdi cevap ver."}
print("sistem testi 4096 :",cagir([s]+dolgu+[son],4096),flush=True)
print("sistem testi 16384:",cagir([s]+dolgu+[son],16384),flush=True)
subprocess.run(["ollama","stop",M],capture_output=True)
for f in sorted(glob.glob(V4+r"\kosular\v4_g3_kosu1_qwen3b_30eki\v4_kosu1_O1_O2b_t*.jsonl"))[:0]: pass
c=collections.Counter();mx=0
for f in glob.glob(V4+r"\kosular\v4_g3_kosu1_qwen3b_30eki\v4_*.jsonl"):
    for t in open(f,encoding="utf-8"):
        x=json.loads(t);k=(x.get("maliyet") or {}).get("token",0)
        if k>4000: c[x["olay"]]+=1
        if x["olay"]!="soru": mx=max(mx,k)
print("G3 4000 ustu olay:",c.most_common(5),"soru disi en cok",mx,flush=True)
def kos(ad,toh):
    r=subprocess.run([sys.executable,"-I","kosu_model.py","--tasiyici","yerel","--kosu","1","--model",Q3,"--tohumlar",toh,"--kosullar","O1_O2b","--cikti",os.path.join(SP,ad)],cwd=V4,capture_output=True,text=True,encoding="utf-8",errors="replace")
    print(ad,[t[18:75] for t in r.stdout.splitlines() if " is " in t],flush=True)
kos("tani3_a_t7_sicak","7")
subprocess.run(["ollama","stop",Q3],capture_output=True)
kos("tani3_b_t7_soguk","7")
subprocess.run(["ollama","stop",Q3],capture_output=True)
kos("tani3_c_t6_7_soguk","6-7")
print("TANI3 BITTI",flush=True)
