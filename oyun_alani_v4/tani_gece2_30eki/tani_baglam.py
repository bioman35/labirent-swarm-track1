# coding: utf-8
"""TANI · KOSU DEGIL · G2 O1_O2b t7 yeniden uretilir, her cagrinin prompt_eval_count'u yazilir. Cikti yalniz scratchpad'e.
Sonra en buyuk mesajlar num_ctx 16384 ile bir kez daha sayilir: kesilme var mi."""
import json,os,sys,urllib.request
V4=r"C:\Users\MONSTER\Desktop\sprint\oyun_alani_v4"
SP=r"C:\Users\MONSTER\AppData\Local\Temp\claude\c--Users-MONSTER-Triamind-App\a04217b9-e26f-4d22-badf-e2f8e65b262e\scratchpad"
MODEL,TOHUM,KOL=sys.argv[1],sys.argv[2],sys.argv[3]
os.chdir(V4); sys.path.insert(0,V4); sys.stdout.reconfigure(encoding="utf-8")
import suruculer as S
KAYIT=[]
_eski=S.Ollama.sohbet
def sohbet(self,mesajlar,tohum):
    r=_eski(self,mesajlar,tohum)
    KAYIT.append({"n":len(mesajlar),"gt":r[1],"ct":r[2],"kr":sum(len(m["content"]) for m in mesajlar),"m":mesajlar})
    return r
S.Ollama.sohbet=sohbet
import kosu_model as K
sys.argv=["kosu_model.py","--tasiyici","yerel","--kosu","1","--model",MODEL,"--tohumlar",TOHUM,"--kosullar",KOL,"--cikti",os.path.join(SP,"tani_%s_%s"%(MODEL.split(":")[0],TOHUM))]
try: K.main()
except SystemExit: pass
gt=sorted(k["gt"] for k in KAYIT)
print("CAGRI",len(KAYIT),"gt en cok",gt[-1],"p50",gt[len(gt)//2],"4000 ustu",sum(g>=4000 for g in gt),"mesaj sayisi en cok",max(k["n"] for k in KAYIT))
ust=sorted(KAYIT,key=lambda k:-k["kr"])[:3]
for k in ust:
    b=json.dumps({"model":MODEL,"messages":k["m"],"stream":False,"options":{"num_ctx":16384,"num_predict":1,"temperature":0}}).encode()
    y=urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:11434/api/chat",b,{"Content-Type":"application/json"}),timeout=300)
    c=json.loads(y.read().decode())
    print("EN UZUN mesaj: karakter",k["kr"],"n",k["n"],"4096'da sayilan",k["gt"],"16384'te gercek boy",c.get("prompt_eval_count"))
print("TANI BITTI")
