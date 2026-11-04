# Preexisting eki · 31 Ekim 2026 · Hikayeci · Appendix D için

Dondurma 4 Kasım akşamından önce yazılan yeni dosyalar. Donuk v4 dosyaları değişmedi. Özetler dosyanın bu andaki halidir.

| dosya | ne | SHA256 ilk 16 |
|---|---|---|
| kosu_api.py | Koşu 4, 5a, 5b API sürücüsü; temperature, seed, response_format göndermez | 239a5c0fc3b3a8e6 |
| test_kosu_api.py | sürücü sınaması, ağ yok | 3a13ac3d98f2ea26 |
| deneme_cagri.py | iki deneme çağrısının betiği | d2db16875d59aad8 |
| deneme_cagri_31eki.jsonl | deneme sonucu: Luna 400 temperature, Gemini 400 seed | 14081fb154f38760 |
| kosu_5c.py | 5c sürücüsü | 87b2d2586e551bba |
| test_5c.py | 5c sınaması, sahte taşıyıcı | 09cdf189af10ed3c |
| kart/5c_kartlar_taslak_31eki.md | D4, U4 kartları | 2672ced738da5d4c |
| kart/TAHMIN_NOTU_5C_31eki.md | U4−U1 koşullu ölçü | 94016f43a31ddf2a |
| luna_ozet.py | Luna özet üreticisi | 9eb433bf0cfe2bbe |
| turuncu_vaka.py | dokuz vaka tablosu | d2dabc848e76bdc4 |
| turuncu_sayim.py | TURUNCU sayımı | 0efa4d96f5534185 |
| kume_sira_tani.py | ilk atanan tanısı | 0d0283c9b643a57e |
| luna_sizinti_olc.py | sızıntı ölçümü | 22d4e3b44cd00098 |
| deneme_cagri2.py | yeni sürücüyle deneme betiği | 0d831f2f4898193d |
| deneme_cagri2_31eki.jsonl | sonuç: Luna 200, Gemini 200 | 24465625797f15eb |
| kart/taban_5c.py | D1 ve U1 taban ölçümü | dca17a86eeb4376b |
| TAHMIN_TASLAK_EK5_5C_31eki.md | 5c tahmin taslağı, kilit değil | 09f897c5f8ce5e04 |
| TAHMIN_TASLAK_EK5B_VAKA_31eki.md | dokuz vaka taslağı, kilit değil | d38bb3667e0ae4d7 |
| luna_ozet_ek5b.py | EK5b özet üreticisi (4 Kas), luna_ozet.py'den türetildi, model çağrısı yok | 031b2332c48a7bf5 |
| luna/EK5B_OZET_HASH_4kas.md | dokuz özet ve soru SHA256 (4 Kas) | a9fe1acefdc6af6e |
| luna/gizli/yer_gercegi_ek5b.json | EK5b kimlik eşlemesi, Luna'ya gitmez (4 Kas) | 880953adb4a674d6 |
| TAHMIN_EK5B_VAKA_SON_4kas.md | EK5b son metin, kilit değil (4 Kas) | dfb19386b4f22260 |
| TAHMIN_KILIDI_EK5B_VAKA_4kas.md | EK5b kilit metni, defter sira 23 (4 Kas, Turan kilitledi) | b24479b00840e96b |

## Kilitten sapma · Koşu 4 ve 5 · Turan kararı 31 Eki

T4 ve T5 kurulumu API modeline sıcaklık 0,7 ve kayıtlı tohum gönderiyordu. Deneme çağrısı bunun çalışmadığını gösterdi. Yeni sürücüde büyük model API varsayılanıyla, tohumsuz ve JSON zorlaması olmadan çalışır. Küçük taraf Qwen 7B sıcaklık 0,7 ile kalır. Sonuç birebir yeniden üretilemez, kayıt her cevabı saklar. JSON zorlaması kalktığı için bozuk cevap oranı kayıttan ayrı yazılır.

## 2-4 Kasım satırları · kapanışta eklendi

| dosya | ne | SHA256 ilk 16 |
|---|---|---|
| DENEME_KOSU4_2KAS.md | Koşu 4 deneme notu (2 Kas) | 2de5f18cbc910f4a |
| kosular/v4_kosu4_deneme_2kas/ | Koşu 4 deneme koşusu, 8 dosya; api_kayit.jsonl ve api_olcum.jsonl dahil (2 Kas) | af33a83c86ca2a29 |
| kosular/v4_kosu4_deneme_2kas.log | deneme koşusu günlüğü (2 Kas) | 5458c5f1d5f1e1aa |
| TAHMIN_KILIDI_EK5_5C_2kas.md | EK5 kilit metni, defter sira 22 (2 Kas) | 851f7da547835b41 |
| ../film_labirent/ | 3B tekrar sahnesi, kendi kayıtlarımız için, sprint öncesi · üç ham deneme klibi, anlatım ve kurgu yok · salt okunur, model çağrısı yok · 7 dosya | 9cd1faceb9f8f0b0 |
| luna/ozet_ek5b/ | EK5b dokuz özet (4 Kas), 9 dosya | addb231d4e338de7 |
| luna/soru_ek5b/ | EK5b dokuz soru (4 Kas), 9 dosya | 64c2752a9a6e7a8b |
| dondurma_4kas.py | bu dondurmanın betiği (4 Kas) | c88377531f5f1f36 |
| DANISMAN_CEVAP_7SORU_31eki.md | danışman notu | dbef01fb451f061d |
| DANISMAN_EK5B_KILIT_ONCESI_4KAS.md | danışman notu | 9f0e895d7ea9114d |
| DANISMAN_NOTU_DONDURMA_4KAS.md | danışman notu | ead97d726512fb18 |
| DANISMAN_NOTU_EK4_31eki.md | danışman notu | b1d736e620110f10 |
| DANISMAN_NOTU_IS_1KAS.md | danışman notu | c1ea539769aed9ec |
| DANISMAN_OKUMA_5C_LUNA_31eki.md | danışman notu | 770c8fee8710bdc1 |
| DANISMAN_OKUMA_EK5_EK5B_31eki.md | danışman notu | 72fcf4096b59fe7f |
| TAHMIN_TASLAK_EK5_5C_31eki.md | 5c taslağının bugünkü hali; 31 Eki satırındaki özet ilk haline aitti, taslak aynı gün 21:54'te güncellendi, kilit metni ayrı (EK5) | 1c1c7728afaca7cf |
| TAHMIN_TASLAK_EK5B_VAKA_31eki.md | EK5b taslağının bugünkü hali; 31 Eki satırındaki özet ilk haline aitti, taslak aynı gün 21:54'te güncellendi, kilit metni ayrı (EK5b) | b07420d4f9669925 |

## Kapanış · 4 Kasım 2026 · Turan "dondur dostum"

Liste bu satırla kapandı. Bundan sonra yazılan dosyalar sprint işidir (sprint-time) ve bu listeye girmez. Klasör satırlarının özeti, sıralanmış "sha256  göreli_yol" satırlarının SHA256'sıdır. Bütün klasörün dosya dosya listesi DONDURMA_4KAS.sha256'dadır; o dosyanın ve bu listenin özeti kilit defterinde dondurma kaydındadır. Danışman notları dondurmadan sonra da ek alabilir; buradaki özet bu anın halidir.
