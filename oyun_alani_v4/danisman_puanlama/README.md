# Danışman puanlama betikleri · 7-8 Kasım 2026 · salt okunur, model çağrısı yok

Raporun 4.7, 4.12, Ek B.3-B.6 sayılarını kayıtlardan yeniden üretir. Bu klasör oyun_alani_v4/ içinde durur; KOK bir üst klasördür. Çalıştır: `python -I danisman_puanlama/<betik>.py` (oyun_alani_v4 içinden).

| betik | ne üretir | rapor |
|---|---|---|
| oku5a.py, sakla5a*.py | 5a dört klasör birleştirme (en erken kopya kuralı), T4/T5 ölçüleri | 4.7, DANISMAN_5A_SONUC_7KAS.md |
| oku5b.py, turuncu5b.py, zarfyap5b.py | 5b ölçüleri, TURUNCU ve zarf_yap sayımı | 4.7, DANISMAN_5B_SONUC_7KAS.md |
| puan_ek5a.py | EK5a / EK5a-2 yargıç tablosu (`cevap_ek5a` ya da `cevap_ek5a_2000` argümanı); luna/gizli/yer_gercegi.json gerekir | 4.7, B.5 |
| puan_5c.py, yol_5c.py | 5c r0+r1+r2 kilit ölçüleri; S1 kapı yolları, tohum 39/44 | 4.12, B.4 |
| k1_gecis.py | sprint kayıtlarındaki bütün K1 geçişleri, atama durumuyla | B.6 |
| film_kontrol.py | filmdeki beş koşunun sha256 ve olay sırası | film |

Not: sakla5a.py içe aktarılınca modül düzeyinde çalışır (7 Kas notu); sakla5a_c.py tekrar klasörlerindeki `_rN` sonekini ayırır. Sayılar DANISMAN_* dosyalarıyla birebir karşılaştırıldı (7-8 Kas).
