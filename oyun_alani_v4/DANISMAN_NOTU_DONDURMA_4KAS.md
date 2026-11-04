# Danışman notu · dondurma günü · 4 Kasım 2026 · Turan kararları

## 1 · Film: saha preexisting, film sprint işi (Turan, 4 Kas sabah)
Gerçek durum ve rapora girecek cümle aynı: "Kendi koşu kayıtlarımız için bir 3B sahne kurmuştuk (31 Eki); sprint için bu sahnede ayrı bir film çektik (6-8 Kas)."
- `film_labirent/` olduğu gibi PREEXISTING listesine girer, bugünkü hash'iyle. Satır: "film_labirent/ · 3B tekrar sahnesi, kendi kayıtlarımız için, sprint öncesi · üç ham deneme klibi, anlatım ve kurgu yok · salt okunur, model çağrısı yok".
- Sprint filmi AYRI klasörde: `film_sprint/` (6 Kas'tan önce açılmaz, içine dosya konmaz). Appendix D'de "sprint-time" satırı: "film_sprint/ · sprint filmi, film_labirent sahnesinde, bu teslim için".
- 6 Kas'a kadar film_labirent/ koduna dokunulmaz. Sprint filminde sahne kodu kopyalanıp film_sprint/ içinde geliştirilir; film_labirent/ dondurulmuş kalır.
- Film işi GPU koşularıyla çakışmaz: render 8 Kas gündüz (5c r2'den sonra) ya da başka makinede. L11 (sıra bağımlılığı) yüzünden koşu sırasında aynı GPU'da render yok.

## 2 · Dondurma (bu akşam, Turan "dondur" deyince)
- Donuk v4 dosyalarının md5/sha256 listesi, KAPI_KURALLARI_DONUK_v4 ve SISTEM_MESAJI_v4 özetleri defterde zaten var; bugün bütün klasör için tek liste (DONDURMA_4KAS.sha256).
- PREEXISTING_EK listesi kapanır: 31 Eki satırları + 2 Kas (kosu_api düzeltmesi, api_kayit, DENEME_KOSU4) + film_labirent satırı. Kapanış hash'i deftere kayıt 24.
- Depoya yükleme (bioman35/labirent-swarm-track1): dünya kodu, kartlar, kayıtlar (kosular/), defter, kilitler, film_labirent/. luna/gizli/ GİRMEZ (8 Kas). Commit mesajı: "Freeze before sprint window: world v4, records, lock ledger, replay stage".
- Yükleme Kaptan'ın işi değil, Hikayeci yapar (depo GitHub, sunucu yok); anahtar dosyası (Desktop\api) depoya girmez, .gitignore'da.

## 3 · EK5b
Taslak hazır, danışman sıkılaştırması hazır (iç uyuyan üstünden; S1'li 2 vaka ayrı satır). Turan "kilitle" deyince kayıt 23. Luna çağrısı 6 Kas'ta, kilit 6'dan önce şart.

## Sırada
[T] cümleleri (Turan, bugün en az üç: abstract ana bulgu, iki katman hipotezi, dual-use). Künye kararı. Sprint filmi için 6 Kas'tan önce yalnız plan (anlatıcı, kurgu, kadraj, EN kartlar, rapor sayılarıyla birebir), kod yok.

## §4 · Apart maili (Kaptan W özeti, 4 Kas öğle) · takvime etkisi
- Son teslim: 8 Kas 23:59 AoE = **9 Kas Pazartesi 14:59 TRT**. İç hedef değişmez: 8 Kas akşamı kapı + PDF; Pazartesi sabahı yalnız yedek pay, yeni iş değil (Turan iştedir).
- Sprint açılışı: Kaptan W "6 Kas Cuma", açılış konuşması 7 Kas 00:30 TRT. **Puanlı ilk koşu (Koşu 4) resmi açılış saatinden önce başlamaz.** Collusion'da açılış 23 Eki 15:00 TRT idi ve "koştur" ondan sonra geldi; defterin UTC damgası kanıttı. Kaptan W Apart sayfasından saati tek sayıya bağlar; Hikayeci Koşu 4'ü o damgadan sonra başlatır. Açılış 7 Kas 00:30 ise plan 6 saat kayar, 12 saat GPU yine sığar: Cuma gecesi 00:30'dan Koşu 4 → Luna yargıç → 5c r0+r1 (≈ 06:00); Cumartesi 5a, 5b; Pazar 5c r2; Pazar akşamı kapı ve PDF.
- Kurallar Collusion ile aynı: 4-8 sayfa, Limitations + Dual-Use zorunlu (Appendix A var), preexisting işareti (bu gece dondurma + PREEXISTING listesi), uydurma sonuç/kaynak diskalifiye (kaynaksız sayı kuralı), kişi başı en çok iki proje (bizde bir), rapor jüri sonrası yayınlanır.
- Adaption kredisi (hesap açıldı, 1.000 kredi, kart yok): sprint planına GİRMEZ. KARAR 4 Kas öğleden sonra (Turan + Kaptan W + danışman): Swarm'da ne ana kol ne ek kol ne duman testi; "6 Kas'a kadar başka API çağrısı yok" aynen. 9 Kas'tan sonra Hikayeci'nin makinesinde: ayrı bayrak (varsayılan kapalı), geliştirme tohumu, üç ölçü (JSON ayıklama, gecikme, kesme), preexisting kaydı; Aralık sprintinin (4-6 Ara) ilk işi, ikinci model ailesi kolu olarak L1 ve L12'yi kapatır; hibe için "iki model ailesi, ucuz açık modelle tekrar" kanıtı. Önce API'den gerçek model listesi. Sürücü ve dünya donuk, yeni araç ya da ince ayar preexisting ve kilit düzenini bozar. Kredi alınabilir, bu sprintte kullanılmaz.
- Konuşmalar GPU koşusu sırasında PC'de izlenmez: Qwen 7B Q4 6 GB'ı dolduruyor, Chrome/Zoom video belleği taşma riski. Telefon ya da ikinci cihaz. Kemeklis (7 Kas 22:00, AI Control, içeriden tehdit) bizim kapı/gözlemci işine en yakın; Related Work'e yalnız kaynak makale okunursa girer, konuşma atıf değildir.

## TURAN: "dondur dostum" · 4 Kas 2026 ≈ 22:45 TRT (Hikayeci defter damgasını UTC yazar)
Dondurma sözü verildi. Hikayeci §2 adımlarını uygular: DONDURMA_4KAS.sha256 (dünya kodu, kartlar, kayıtlar, kilitler, luna_ozet*.py, film_labirent/) → PREEXISTING_EK listesi kapanır (film_labirent sahne satırı dahil; 4 Kas dosyaları: EK5b son metin, kilit metni, üretici, özetler, DANISMAN_* notları) → KILIT_DEFTERI.jsonl sıra 24, tür dondurma → depo bioman35/labirent-swarm-track1 (luna/gizli/ ve Desktop\api DIŞARIDA, .gitignore; commit "Freeze before sprint window: world v4, records, lock ledger, replay stage"). Dondurmadan sonra: donuk dosyalara dokunulmaz; 6 Kas'a kadar API çağrısı yok; Koşu 4 resmi açılış damgasından sonra. Danışman kontrolü: hash listesi ve depo ağacı (gizli ve anahtar yok, sahne var).
