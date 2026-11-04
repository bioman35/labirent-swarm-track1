# TAHMİN KİLİDİ · EK KAYIT 2 · Koşu 4 ve 5 model kararı · 30 Ekim 2026 · Turan (karar, 29 Eki) · danışman (yazım) · KİLİTTEN SONRA DEĞİŞTİ

Ne değişti: Ana kilit T4-T5 (TAHMIN_KILIDI_27eki.md) ve Ek kayıt 1 "Sıra" 4. adımı (TAHMIN_KILIDI_EK1_v4_28eki.md) Koşu 5b için Grok yazıyordu. Grok DÜŞTÜ. Sebep: bütçe ve API limiti (Turan, 29 Eki: "limitimiz az"). Tahminlerin kendisi (T4, T5 ölçüleri ve eşikleri) DEĞİŞMEDİ; yalnız model ve zaman.

## Modeller
- Koşu 4 (bizim ajanlar büyük model, sinsi küçük): Luna. Bütçe tavanı 10 USD (T4'teki gibi).
- Koşu 5a (sinsi büyük: Luna; bizim ajanlar küçük Qwen 7B).
- Koşu 5b (sinsi büyük: Gemini Flash; Collusion'da hakem 2 olarak kullanılan sürüm; kesin model kimliği her koşunun meta dosyasına yazılır). Tavan 15 USD korunur; Turan değiştirebilir.
- Grok: koşulmaz. Raporda "planned, not run (budget)" diye yazılır; T5'in Grok ayağı için "sınanamadı".

## Zaman ve dünya
- Koşular sprint günlerinde (6-8 Kasım 2026), yayın ve Unreal kapalıyken.
- Dünya: v4 (KAPI_KURALLARI_DONUK_v4.md 17077b0e…, SISTEM_MESAJI_v4.md 87ef1945…), tohumlar 16-25, kartlar c1433457….
- Ek kayıt 1'deki cümle geçerli: "T4-T5 v4'te koşuldu, ölçüler aynı; v3.4 için sınanamadı (dünya değişti)."
- Koşu 4b (karma: role göre model) yalnız zaman ve bütçe kalırsa; ayrı ek kayıt ister.

## Bu gece (30 Eki) koşan zincir, bilgi
- Ablasyon (kodon kapalı, Koşu 2, tohum 16-25): danışman tahmini koşudan önce deftere girdi (Hikayeci işledi): U1-U2 fark edilmeme ≈ 5/20; dış sinsi K1 geçişi 0/30 kalır (uyarı merdiveniyle). Keşif etiketli.
- Tekrar ölçümü (Koşu 2 ×2 daha, Koşu 1 sıcaklık 0,7 ×3): her tohum için sonuçlar ayrı yazılır; rapordaki aralık oradan çıkar. Tahmin yok; yalnız varyans ölçümü.

## Defter
Hikayeci bu notu kilit defterine yeni kayıt olarak işler (önceki kayıtlar değişmez). Özet satırı: "EK2: Koşu 5b modeli Grok → Gemini Flash; Koşu 4/5 sprint günlerinde v4'te; tahmin ve eşikler aynı."
