# coding: utf-8
import sys, os, hashlib; KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, KOK); sys.stdout.reconfigure(encoding="utf-8")
from kayit import oku
R = ["v4_kosu4_luna_b/v4_kosu4_O1_O2b_t16", "v4_kosu5a_luna/v4_kosu5a_O1_O2b_t16_D2", "v4_kosu5b_gemini/v4_kosu5b_O1_O2b_t16_D1", "v4_5c_puanli_r0/v4_kosu2_O1_O2b_t37_D4", "v4_5c_puanli_r0/v4_kosu2_O1_O2b_t37_U4"]
for r in R:
    f = os.path.join(KOK, "kosular", r + ".jsonl"); s = oku(f)
    print("==", r, hashlib.sha256(open(f, "rb").read()).hexdigest()[:16], "tur", max(x["zaman"] for x in s))
    for x in s:
        if x["olay"] in ("kapi_karar", "zarf_yap", "durdu", "takildi") or (x["olay"] == "dogrula" and (x.get("metin") or "").startswith("atandı: T")) or (x["olay"] == "zarf_birak" and x.get("konum") == "CIKIS_ARSIV") or (x["olay"] == "isaret"):
            print("  t%d %s %s %s %s %s" % (x["zaman"], x["ajan_id"], x["olay"], x.get("kapi_id") or x.get("konum"), x.get("karar") or "", (x.get("metin") or "")[:50]))
