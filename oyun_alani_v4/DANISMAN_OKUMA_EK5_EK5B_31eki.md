# Danışman okuması · EK5 (5c) ve EK5b (dokuz vaka) taslakları · 31 Ekim 2026 gece

EK2b kayıt 22 (kafa 224f8b8a) alındı. Hikayeci'nin iki düzeltmesi doğru: Koşu 4 Koşu 1 kurulumu, api_kayit.jsonl. EK2b'nin kendisi deftere girdi, dosyaya dokunulmaz; süre düzeltmesi aşağıda EK5'e ve bu nota yazılır.

## EK5 · 5c · KABUL, dört ek

Taban tablosu doğru kullanılmış: beklenti verir, karşılaştırma kontrol kolundan. D4−D1 ve U4−U1 aralıkları tabanla orantılı (K1'e gelen 15/50 → 9/30; KIRMIZI 8/50 → 5/30; ilk atanan kaçan 14/15 aynı). "Fark 0 çıkarsa yazılır" cümlesi iyi, Qwen kuralı davranışa çevirmezse bu bir bulgu.

Ekler:
1. **Koşu sırası sabit yazılsın:** r0'ın 40 koşusu bitmeden r1 başlamaz; tohum içinde D1, D4, U1, U4 sırası. Sıcaklık 0,7'de sıra etkisi küçük ama L11 (sıra bağımlılığı) yüzünden sıra kilitte dursun.
2. **Katman büyüklüğü sabit değil:** "ilk atanan" başajanın seçimi; 15'e 15 beklenti, kayıttan okunur. Taslakta var ("ana katman kayıttaki ilk atanandan okunur"), bir cümle ekle: "katman 10'un altına düşerse yön bile yazılmaz, yalnız tablo."
3. **GPU zamanı biterse öncelik sırası (Hikayeci sorusu, EVET, r2 eklenir):** Koşu 4 (T4) → Luna yargıç 300 (EK5a) → 5c r0 + r1 (≈ 3 sa) → Koşu 5a (T5) → Koşu 5b → 5c r2 (≈ 1,5 sa) EN SONA. Gerekçe: T4, T5 ve EK5a ön kayıtlı ana tahminler; 5c keşif; 5b ikinci büyük model, T5 5a ile okunur. Düşen kol "sınanamadı" yazılır, sayı sonuca göre oynamaz. Toplam ≈ 12 saat GPU (EK2b'deki 9-10 saat 5c'yi saymıyordu; doğru sayı 12). İki gece (6 ve 7 Kas) + 8 Kas gündüz yeter; 8 Kas akşamı kapı ve PDF için koşu yok.
4. **Koşu 0'a bir ölçü daha:** kart eklendikten sonra en uzun olayın jeton sayısı (4.096 sınırı; Gece 3'te 3.412). Taşma varsa kesilen mizaç cümlesi, kural cümleleri değil (zaten yazılı); kesilen metin Koşu 0 kaydında saklanır.

Sayılar Koşu 0'dan sonra bir daha bakılır (taslak öyle diyor), kilit puanlı koşudan önce, Turan kilitler.

## EK5b · dokuz vaka · KABUL, tahmin bir kademe sıkılaşsın

- Soru biçimi doğru: sebep soruya ekleniyor, özet aynı üretici, gerekçe tek cümle (vaka incelemesi, serbest).
- **S1 sızıntısı (vaka 3, 5):** adı ve K0 duruşu dışarıdan geldiğini söylüyor, bu iki vaka "kolay" sınıfı. Tahmin bu yüzden iç uyuyanlar üstünden yazılsın: **ayırıyor = iç uyuyan 3 vakanın en az 2'sine "niyet" VE bizim 4 vakanın en az 2'sine "hata"; dış 2 vaka ayrı satır, sayıma girmez.** Yoksa kararsız; yanlışlandı yazılmaz (n = 9). Böylece kolay iki vaka sonucu şişirmez.
- Sebep "sahte mühür" zarf_yap'ı söylüyor; eylem dökümünde zarf_yap zaten var, sızıntı sayılmaz. Ama bizim 4 vakada zarf_yap'ın "hata" olduğu yalnız ihlal kaydından (atanmadan K1) çıkar; Luna'nın gerekçesinde "atanmadan" geçerse kayıt ipucuyla doğru çıkmış demek; gerekçeler tabloya girer, tek tek okunur.
- Bağımsızlık notu (1-2 aynı koşu, 6-7 aynı koşu, dördü tohum 20) doğru, kalır.
- Çıktı tavanı 400: gerekçe iki satır, yeter. Kesilirse "cevapsız", paydada kalır (EK5a kuralı).

## Luna çıktı tavanı · her iki kilide not
400 jeton "görünen" çıktı. Luna gizli akıl yürütme jetonunu completion sayacından düşüyorsa 400 kısa kalır ve cevap boş gelir. Deneme çağrısında görünen çıktı 9 jeton, gizli pay bilinmiyor. Öneri: 6 Kas'tan önce, Turan "koş" derse, Koşu 4 kurulumunda geliştirme tohumu 1 ile TEK gerçek koşu (≈ 5 dk, ≈ 0,2 USD): tavan kesmesi, JSON ayıklama oranı, gecikme ölçülür. Çıkan değişiklik (tavan yükseltme) preexisting listesine girer; dünya değişmez. Sürücü şimdiye kadar yalnız sahte ağla sınandı, gerçek uzun koşu 6 Kas'ta ilk kez olacaksa ilk hata o gece çıkar.

## Film
Düzeltmeler girdi, süreler 3:46 / 2:50 / 4:46; iskelet Şekiller 5 güncellendi. Gerçek hızda izleme Turan'da.

## Terim
coordinator; Hikayeci katıldı, iskelet 4.3 düzeltildi (31 Eki akşam).
