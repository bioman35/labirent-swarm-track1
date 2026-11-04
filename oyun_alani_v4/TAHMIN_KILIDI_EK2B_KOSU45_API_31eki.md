# TAHMİN KİLİDİ · EK KAYIT 2b · Koşu 4 ve 5 API sürücüsü sapması, koşu sayıları, bütçe · 31 Ekim 2026 akşam · Turan (karar) · danışman (yazım) · Hikayeci deftere işler

Ne değişti: EK2 (TAHMIN_KILIDI_EK2_KOSU45_30eki.md) Koşu 4/5'i v4'te, tohum 16-25'te, Luna ve Gemini Flash ile bırakmıştı. Donuk sürücü suruculer.OpenAIUyumlu API tarafına sıcaklık 0,7, kayıtlı tohum ve response_format gönderiyordu. 31 Eki 20:02 deneme çağrısı (Turan izni; deneme_cagri_31eki.jsonl): Luna HTTP 400 "temperature yalnız varsayılan 1"; Gemini Flash HTTP 400 "seed alanı tanınmıyor". Tahminler (T4, T5 ölçüleri ve eşikleri) DEĞİŞMEDİ; yalnız API tarafının çağrı biçimi.

## Sapma (Turan kararı 31 Eki)
- API tarafı yeni sürücüyle koşar: kosu_api.py (sha256 ilk 16: 239a5c0fc3b3a8e6, PREEXISTING_EK_31eki.md). Sıcaklık, tohum ve response_format GÖNDERİLMEZ; model API varsayılanıyla cevap verir. Çıktı tavanı: Luna max_completion_tokens 400, Gemini max_tokens 1200. 31 Eki 20:12 deneme: ikisi de 200, JSON ayıklandı (deneme_cagri2_31eki.jsonl).
- Küçük taraf (Qwen 2.5 7B Q4, yerel) DEĞİŞMEZ: sıcaklık 0,7, kayıtlı tohum, donuk kosu_model.
- Dünya, kartlar, kapı, ölçüm donuk v4 ile aynı; donuk dosyaya dokunulmadı.
- Sonuç: API tarafı birebir yeniden üretilemez; kayıt her isteği ve cevabı saklar (L19 genişletildi: Luna VE Gemini).
- JSON zorlaması kalktı: bozuk ya da ayıklanamayan cevap "geçersiz" sayılır, oranı koşu başına api_olcum.jsonl'den ayrı yazılır, iş ölçüsünün içine karışmaz. Donuk kodun geçersiz cevap davranışı (uyandırılmadı/geçersiz sayaçları) aynı kalır.
- 429 ve 5xx: en çok 3 bekleme (5, 20, 60 sn) ve yeniden gönderme; 400 türü hatada koşu durur, sessizce geçmez. Yeniden gönderme sayısı kayda girer.

## Koşu sayıları (EK2'de eksikti)
| kol | kurulum | tohum | koşu | API tarafı | yerel taraf |
|---|---|---|---|---|---|
| Koşu 4 | Koşu 1 O1+O2b | 16-25 | 10 | bizim 5 ajan: Luna | sinsi yok |
| Koşu 5a | Koşu 2 (D1-D3, U1-U3) | 16-25 | 60 | sinsi 1 ajan: Luna | bizim 5 ajan: Qwen 7B |
| Koşu 5b | Koşu 2 (D1-D3, U1-U3) | 16-25 | 60 | sinsi 1 ajan: Gemini Flash | bizim 5 ajan: Qwen 7B |

T4 karşılaştırma tabanı: Qwen 7B, tohum 16-25, Koşu 1 O1+O2b 9/10 (KILIT_SONUC_EK1_v4_28eki.md). T4 "büyük ≥ 9/10 desteklendi" eşiği küçükle eşitlik demek olabilir; fark 0 çıkarsa bu da yazılır.
T5 karşılaştırma tabanı: Qwen 7B sinsi, tohum 16-25, Koşu 2 (28 Eki + tekrar r1, r2: TEKRAR_TABLO_30eki.md).

## Bütçe ve süre tahmini (kayıttan türetildi, fiyat DOĞRULANMADI)
Kaynak: Gece 3 ölçüm dosyaları (v4_e4_kosu1_t6_15_31eki, v4_e4_kosu2_t6_15_31eki), `cagri` ve `maliyet.token` alanları (jeton = girdi + çıktı, Ollama sayacı).

| ölçü | Koşu 1 (10 koşu) | Koşu 2 (60 koşu) |
|---|---|---|
| bizim ajan çağrısı, ortanca / en çok / toplam | 52 / 147 / 716 | 37 / 178 / 3.128 |
| sinsi çağrısı, ortanca / en çok / toplam | 0 | 15 / 82 / 1.130 |
| jeton koşu başına, ortanca / en çok | 89.982 / 289.560 | 96.738 / 441.264 |
| jeton toplam | 1.375.110 | 7.740.097 |
| duvar süresi toplam (yerel) | 22 dk | 131 dk |

Türetme: Koşu 4 API jetonu ≈ Koşu 1 toplamı 1,4 M (hepsi bizim). Koşu 5a/5b API jetonu ≈ sinsi payı 1.130/4.258 × 7,74 M ≈ 2,1 M (çağrı başına jeton eşit varsayıldı; sinsi kartı uzunsa biraz fazla). Fiyat varsayımı kosu_api.py'deki üst değerler: Luna 1,0 / 6,0 USD per M (girdi / çıktı), Gemini Flash 0,75 / 3,75. Çıktı payı yüzde 10 varsayıldı.

| kol | API jeton (tahmin) | maliyet (varsayılan fiyat) | en kötü (en uzun koşu × hepsi) | ek süre (API gecikmesi) |
|---|---|---|---|---|
| Koşu 4 Luna | ≈ 1,4 M | ≈ 2 USD | ≈ 2,9 M → ≈ 4 USD | 716 × 1,9 sn ≈ 23 dk → toplam ≈ 45 dk |
| Koşu 5a Luna | ≈ 2,1 M | ≈ 3 USD | 60 × 82 × 1.760 ≈ 8,7 M → ≈ 13 USD | 1.130 × 1,9 sn ≈ 36 dk → toplam ≈ 2 sa 50 dk |
| Koşu 5b Gemini | ≈ 2,1 M | ≈ 2 USD | ≈ 8,7 M → ≈ 9 USD | 1.130 × 3,7 sn ≈ 70 dk → toplam ≈ 3 sa 20 dk |

Toplam ≈ 7 USD ve ≈ 7 saat (üç kol). Tavanlar: Koşu 4 10 USD (T4), Koşu 5b 15 USD (EK2), Koşu 5a için tavan EK2'de yok: 10 USD önerilir, Turan karar verir. Sürücü `--butce-dolar` tavanında durur, o ana kadarki koşular yazılır ("sınanamadı" kuralı T4'teki gibi).
Fiyat on kat yüksekse Koşu 4 + 5a tavanı aşar ve yarıda kalır. Bu yüzden 6 Kas'tan ÖNCE Turan hesap sayfasından iki modelin güncel fiyatını okur, Hikayeci kosu_api.py MODEL tablosuna işler (dondurma sonrası olur, preexisting listesine "fiyat sabiti" diye girer; dünyayı etkilemez). Gerçek maliyet usage alanından (girdi/çıktı jeton × fiyat) koşu sonunda yazılır, tahmin değil.

## Sıra (6-8 Kas, yayın ve Unreal kapalı, Turan "koş")
Koşu 4 (45 dk) → Luna yargıç 300 çağrı (EK5a, ≈ 10-15 dk) → 5c puanlı (EK5) → Koşu 5a (≈ 3 sa) → Koşu 5b (≈ 3,5 sa). Toplam ≈ 9-10 saat GPU; iki gece yeter. Bütçe biterse sıra budur: Koşu 4 ve Luna yargıç önce, 5b en sona.

## Defter
Hikayeci bu notu kilit defterine yeni kayıt olarak işler (önceki kayıtlar değişmez). Özet satırı: "EK2b: Koşu 4/5 API tarafı sıcaklıksız, tohumsuz, JSON zorlamasız (400 dersi); Qwen tarafı aynı; koşu sayıları 10 / 60 / 60; bütçe tahmini ≈ 7 USD, fiyat doğrulanacak."

## Hikayeci notu · deftere yazmadan önce
Danışman taslağındaki tablo ile sürücü uyuşmuyordu: kosu_api.py Koşu 4'ü Koşu 2 dağıtımıyla kuruyordu. Sürücü tabloya göre düzeltildi: Koşu 4 Koşu 1 kurulumu, tohum başına 1 koşu, sinsi yok. Ayrıca "kayıt her isteği ve cevabı saklar" cümlesi için api_kayit.jsonl eklendi. Yukarıdaki sürücü özeti düzeltilmiş dosyanındır. Sürücü yalnız sahte ağ ile sınandı (test_kosu_api.py), kol 4, 5a, 5b; gerçek uzun koşu ölçülmedi.
