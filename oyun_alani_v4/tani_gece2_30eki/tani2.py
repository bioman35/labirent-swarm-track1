# coding: utf-8
"""TANI 2 · KOSU DEGIL. (a) 4096 tasinca Ollama sistem mesajini koruyor mu (b) Mistral t7'de kac cagri tasti (c) 3B t6-15 ikinci gecis"""
import json,os,sys,subprocess,urllib.request
V4=r"C:\Users\MONSTER\Desktop\sprint\oyun_alani_v4"
SP=r"C:\Users\MONSTER\AppData\Local\Temp\claude\c--Users-MONSTER-Triamind-App\a04217b9-e26f-4d22-badf-e2f8e65b262e\scratchpad"
M="mistral:7b-instruct-q4_K_M"; Q3="qwen2.5:3b-instruct-q4_K_M"
sys.stdout.reconfigure(encoding="utf-8")
def cagir(model,mesaj,ctx,uz=40):
    b=json.dumps({"model":model,"messages":mesaj,"stream":False,"format":"json","options":{"num_ctx":ctx,"num_predict":uz,"temperature":0,"seed":1}}).encode()
    return json.loads(urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:11434/api/chat",b,{"Content-Type":"application/json"}),timeout=600).read().decode())
dolgu=[]
for i in range(30):
    dolgu+=[{"role":"user","content":"Gözlem: %d numaralı oda boş, duvarda eski bir saat var, yerde toz, pencere kapalı ve dışarıda yağmur yağıyor. "%i*3},{"role":"assistant","content":'{"kod":"bekle"}'}]
s={"role":"system","content":'Her cevabın tam olarak şu JSON olsun: {"kod":"ZEBRA41"}. Başka hiçbir şey yazma.'}
son={"role":"user","content":"Şimdi cevap ver."}
kisa=cagir(M,[s,son],4096); uzun=cagir(M,[s]+dolgu+[son],4096); gercek=cagir(M,[s]+dolgu+[son],16384,1)
print("(a) kisa:",kisa["message"]["content"][:50],"| tasan:",uzun["message"]["content"][:50],"| sayilan",uzun.get("prompt_eval_count"),"gercek",gercek.get("prompt_eval_count"),flush=True)
os.chdir(V4); sys.path.insert(0,V4)
import suruculer as S
KAY=[]; _e=S.Ollama.sohbet
def sohbet(self,m,t):
    r=_e(self,m,t); KAY.append((len(m),r[1],r[2],sum(len(x["content"]) for x in m))); return r
S.Ollama.sohbet=sohbet
import kosu_model as K
sys.argv=["kosu_model.py","--tasiyici","yerel","--kosu","1","--model",M,"--tohumlar","7","--kosullar","O1_O2b","--cikti",os.path.join(SP,"tani2_m7")]
try: K.main()
except SystemExit: pass
json.dump(KAY,open(os.path.join(SP,"tani2_m7.json"),"w"))
oran=4832/9241
print("(b) cagri",len(KAY),"tasan (karakterden, 1 kr=%.3f tok):"%oran,sum(k[3]*oran>4096 for k in KAY),"sayilan<gercek tahmini fark>200:",sum(k[3]*oran-k[1]>200 for k in KAY),flush=True)
S.Ollama.sohbet=_e
r=subprocess.run([sys.executable,"-I","kosu_model.py","--tasiyici","yerel","--kosu","1","--model",Q3,"--tohumlar","6-15","--kosullar","O1_O2b","--cikti",os.path.join(SP,"tani2_q3_gecis2")],cwd=V4,capture_output=True,text=True,encoding="utf-8",errors="replace")
print("\n".join(t[:92] for t in r.stdout.splitlines() if " is " in t),flush=True)
print("TANI2 BITTI",flush=True)
