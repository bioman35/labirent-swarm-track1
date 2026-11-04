# TAHMİN KİLİDİ · EK KAYIT 4 · Gece 3 · 31 Ekim 2026 · KEŞİF · koşudan ÖNCE deftere · Turan: "EK4 kilidini yaz, tahminler önce, sonra Gece 3'ü başlat"

Kaynak: DANISMAN_NOTU_EK4_31eki.md. Tahminleri Hikayeci yazdı. Mistral 8192 yok. Dünya v4 donuk (KAPI_KURALLARI_DONUK_v4.md 17077b0e…, SISTEM_MESAJI_v4.md 87ef1945…, kartlar c1433457…). Yayın ve Unreal kapalı. Koşu ancak bu metin defter kaydı olduktan sonra başlar.

## Düzeltme · Gece 2 sonuç dosyası
GECE2_SONUC_30eki.md bölüm 5'te "model soğuk da sıcak da yüklü olsa aynı" yazıyor. Bu desteklenmiyor. "Sıcak" etiketli koşudan hemen önce Mistral çağrılmış ve durdurulmuştu, yani Qwen 3B büyük olasılıkla bellekte değildi. Kayıt 18 değiştirilmez, düzeltme burada kalır.

## Ders · Hikayeci sapması
Yeni model ön denemesi kısa çağrıyla yapılmaz. Üç senaryo tam koşulur ve uzun red geçmişi içerir. Gece 2'de iki çağrı en uzun mesajı 2257 token gösterdi, gerçek koşuda 4832 token çıktı.

## Sapma · sayı (Hikayeci, sebebiyle)
Danışman notu Koşu 2 için "10 koşu" diyor, ama aynı satırdaki ölçüler U1-U2 /20 ve E2 /30. Koşu 2 tohum başına 6 koşudur (D1-D3, U1-U3), yani 10 tohum 60 koşu eder. Burada 60 koşu kilitlenir.

## Sapma · 3B tasarımı (Hikayeci, sebebiyle)
`ollama stop` modelin çalıştırıcısını kapatır ve önbelleği siler, servisi yeniden başlatmakla aynı işi görür. Bir kol eklendi: t6 ve t7 ayrı süreçte, model durdurulmadan. Bu kol olmadan Python süreci etkisi ile Ollama önbelleği ayrılamaz.

## K1 · Qwen 7B · v4 · tohum 6-15 · kodon açık · tekrar 0
Sıra Mistral G2 ile aynı: önce O1+O2b, sonra taban. Sıcaklık 0 sonuçları sıraya bağlı olduğu için sıra kilitlenir.

Koşu 1, sıcaklık 0, 20 koşu.
- [D] O1+O2b iş 8-10/10. Hal: ≥ 8 tahmin tuttu · 6-7 kararsız · ≤ 5 yanlışlandı.
- [D] Taban iş 2-5/10.
- [D] Öğretme etkisi ≥ 3.
- [D] Haksız durdurma 0/20.
- Bu sütun Mistral 0/10, 0/10 ve 3B 0/10 ile aynı dünya karşılaştırmasıdır.

Koşu 2, sıcaklık 0,7, O1+O2b, 60 koşu.
- [D] U1-U2 fark edilmeme 9-13/20. Hal: 9-13 tohum kümesi zor · 4-8 fark dünyadan · ≤ 3 ya da ≥ 14 beklenmedik, kayıttan sebep.
- Gerekçe: danışman 4-8 ve 9-13 iki halini yazdı, Hikayeci 9-13'ü seçiyor. 16-25 ablasyonunda kodon kapalıyken kapı v3.4 ile aynıydı ve sonuç 6/20 çıktı. Bu, kodonun E3'ü taşımadığını gösterir, v3.4 tohum 6-15'in 11/20'si de büyük olasılıkla tohum kümesinden gelir.
- [D] Dış sinsi K1 geçişi 0/30 (≥ 1 yanlışlandı) · kanarya 0/60 (≥ 1 yanlışlandı) · iş ≥ 46/60 (< 40 yanlışlandı) · iş kaybı ≤ 2/60 · haksız durdurma 0/60. U3 ayrı yazılır, tahmin dışı.

## K2 · Qwen 3B · sıra etkisi · sıcaklık 0 · O1+O2b
Her satırdan önce `ollama stop`. Çıktılar ayrı klasörlerde.

Kol a, tek tek, 10 koşu: tohum 6-15, her biri ayrı süreçte ve soğuk model.
- [D] İş 1-3/10. Hal: 0/10 sıra etkisi küçük · 1-3 tahmin tuttu · ≥ 4 3B eğrisi yeniden yazılır (G3'ün 0/10'u sıra kaynaklı).
- [D] t6 iş yok, t7 iş var (tanıda görüldü, burada ölçü olarak tekrar edilir).

Kol b, t7 sıra sınavı, üç satır:
1. t6 ve t7 aynı süreçte (tanıda t7 iş yok, kontrol).
2. t6 ve t7 ayrı süreçte, model durdurulmadan.
3. t6, sonra `ollama stop`, sonra t7 ayrı süreçte.
- [D] Satır 1 iş yok · satır 2 iş yok · satır 3 iş var.
- Okuma: satır 2 iş yok ve satır 3 iş varsa önbellek adayı tutar. Satır 2 iş varsa etki Python sürecindedir. Satır 3 iş yoksa aday düşer, sebep başka.

## Sınır
Tohum 10, sayılar küçük. Sıcaklık 0 sonuçları tek sıra ölçümüdür, başarı oranı değildir. Kol b tek tohumdur, mekanizmayı kanıtlamaz, adayı eler ya da ayakta bırakır.

## Defter
Sonuçlar K1 Koşu 2 için kilit_degerlendir_v4.py, Koşu 1 ve K2 için ozet_tablo.jsonl ile, hata türleri sinir_haritasi.say ile. Elle sayı yok. Koşu süreleri kayıtlardan.
