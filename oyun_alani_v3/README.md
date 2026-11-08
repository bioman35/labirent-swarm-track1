# Oyun alanı v3 · 27 Ekim 2026 · Hikayeci

KURALLAR_v3_SON_27eki.md'nin kurulumu. v1 (`../oyun_alani/`) ve Koşu 1 kayıtları olduğu gibi duruyor; buradan hiçbir şey oraya yazılmaz.

| dosya | ne |
|---|---|
| KAPI_KURALLARI_DONUK_v3.md + .sha256 | kodsuz, dondurulmuş kurallar (danışman kartlar v2'yi buna bakarak yazar) · `donuk_yaz.py` üretir |
| kayit.py | JSONL + SHA256 zinciri, yayımlı kafa (`.kafa`) |
| dunya.py | harita, kapılar (K0 K1 K2), dört renk, mühür, zarf numarası, jeton, zarf bağı, anahtar, gözlemci, başajan doğrulaması |
| ajanlar.py | Koşu 0'ın betikli ajanları (dil modeli yok) |
| olcum.py | yalnız kayıttan: iş, sızma (dış/iç), yakalama, TURUNCU, haksız durdurma, zarf bütünlüğü, kanarya |
| kosu0.py | 18 senaryo, beklenenler koşmadan önce yazılı · `kosular/` |
| test_v3.py | 11 kabul testi |
| KARAKTER_KARTLARI_v2_27eki.md | danışman kartları (özet 3243848274492ec2…) · `kartlar.py` özeti denetler, dağıtımı kurar |
| SISTEM_MESAJI_v3.md + .sha256 | model ajanının sistem mesajı ve üç öğretme kolu (O1 örnek, O2 anlam, O3 defter) · `sistem_yaz.py` üretir |
| suruculer.py | Ollama / OpenAI uyumlu / sahte taşıyıcı, model ajanı, öğretme kolları |
| kosu_model.py | Koşu 1 / 2 / 4 · `kosular/<klasör>/` içinde kayıt, kafa, ölçüm, ozet_tablo.jsonl, kosu_meta.json |
| oynatici_v3.html · oynatici3d_v3.html | kuşbakışı SVG ve 3B oynatıcı; kayıt yüklenir ya da `?kayit=kosular/...jsonl` (yerel sunucudan) |

Çalıştır: `python -I kosu0.py` · `python -I test_v3.py -v` · `python -I donuk_yaz.py`

Durum 27 Eki sabah · v3.1 (DEGISIKLIK_v3_1_27eki.md, özet 9d1499af…): çanta · kapı uyarısı · güçlü görev cümlesi · O3 çıktı, O2b geldi · Koşu 0 21/21 · donuk kurallar KAPI_KURALLARI_DONUK_v3_1.md (6f1e3594…) · sistem mesajı SISTEM_MESAJI_v3_1.md (e6ca869e…) · v3.0 kod ve donuk dosyalar `_arsiv_v3_0/` · v3.0 Koşu 1 kayıtları `kosular/kosu1_yerel_27eki/` · v3.1 Koşu 1 `kosular/kosu1_v31_yerel_27eki/`. Sırada: tahmin kilidi (Turan + danışman). Deneme koşusu yok; koşular yayın ve Unreal kapalıyken.

Durum 27 Eki öğleden sonra · v3.4 DONDU (dünya v3.3 + O2b v5, danışman): kurallar KAPI_KURALLARI_DONUK_v3_4.md (10a9257a…) · sistem mesajı SISTEM_MESAJI_v3_4.md (7cbe6a57…) · kartlar c1433457… · Koşu 0 25/25 · 15 test · KILIT_DEFTERI (yalnız ekle, zincirli; `python -I defter.py dogrula`), ilk kayıt 260c2b15…. Durdu: tahmin kilidini Turan ve danışman yazacak; kilit gelmeden sınav tohumları (6-15) koşulmaz. Kilit metni gelince `python -I defter.py kilit "<başlık>" <dosya.md>`.

