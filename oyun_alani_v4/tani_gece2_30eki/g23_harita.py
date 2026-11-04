# coding: utf-8
"""G2 G3 · sinir_haritasi.py AYNI KURAL (say) + baglam ve takilma ozeti · yalniz okur"""
import sys,os,glob,json,collections,re
V3=r"C:\Users\MONSTER\Desktop\sprint\oyun_alani_v3"; V4=r"C:\Users\MONSTER\Desktop\sprint\oyun_alani_v4"
sys.path.insert(0,V3); sys.stdout.reconfigure(encoding="utf-8")
import sinir_haritasi as H
KOL=[("Q7 v4 t16-25 ogretme",V4+r"\kosular\v4_kosu1_28eki","O1_O2b"),
     ("Q7 v4 t16-25 taban",V4+r"\kosular\v4_kosu1_28eki","taban"),
     ("Mistral v4 t6-15 ogretme",V4+r"\kosular\v4_g2_kosu1_mistral7b_30eki","O1_O2b"),
     ("Mistral v4 t6-15 taban",V4+r"\kosular\v4_g2_kosu1_mistral7b_30eki","taban"),
     ("Q3 v4 t6-15 ogretme",V4+r"\kosular\v4_g3_kosu1_qwen3b_30eki","O1_O2b")]
for ad,kl,k in KOL:
    fs=sorted(glob.glob(os.path.join(kl,"v4_kosu1_%s_t*.jsonl"%k)))
    top=collections.Counter(); olay=collections.Counter(); mx=0; toks=[]; is_=0; tekrar=[]
    for f in fs:
        n=H.say(f)
        top.update(n)
        o=json.load(open(f[:-6]+".olcum.json",encoding="utf-8")); is_+=o["is_basarisi"]
        s=[json.loads(t) for t in open(f,encoding="utf-8")]
        for x in s:
            t=(x.get("maliyet") or {}).get("token",0)
            if t: toks.append(t)
            if x["ajan_turu"]=="bizim" and x["olay"]=="yonlendir":
                olay[re.sub(r"\.? Burada geçerli.*","",(x["metin"] or ""))[:48]]+=1
        seri=collections.Counter()
        for a in {x["ajan_id"] for x in s if x["ajan_turu"]=="bizim"}:
            en=c=0;p=None
            for x in s:
                if x["ajan_id"]==a and x["olay"]=="yonlendir":
                    m=(x["metin"] or "")[:40]
                    c=c+1 if m==p else 1;p=m;en=max(en,c)
            seri[a]=en
        tekrar.append(max(seri.values() or [0]))
    print("\n##",ad,"kosu",len(fs),"is",is_)
    print("  harita /kosu:",{t[0]:round(top[t[0]]/max(1,len(fs)),1) for t in H.TURLER})
    toks.sort()
    if toks: print("  olay basi token: en cok",toks[-1],"p95",toks[int(len(toks)*.95)],"ort",sum(toks)//len(toks),"4096 ustu",sum(t>4096 for t in toks))
    print("  en uzun ayni red serisi (kosu basi):",tekrar)
    print("  en sik red:",olay.most_common(7))
