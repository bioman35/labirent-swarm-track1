# Koşu 1 v3.2 · sonuç · 27 Ekim 2026 · Hikayeci

Turan ve danışman için, tahmin kilidinden önce. Hiçbir şey değiştirilmedi; yalnız ne olduğu.

## Kurulum
- Dünya v3.2: KAPI_KURALLARI_DONUK_v3_2.md (cc27300e…), madde 5 sade kurulum. Kartlar c1433457…. Sistem mesajı SISTEM_MESAJI_v3_2.md (b7fe44f8…), kollar O2b v3.
- Model: Ollama qwen2.5:7b-instruct-q4_K_M (845dbda0…), sıcaklık 0, tohum 1-5. Unreal ve yayın kapalıydı.
- Kayıtlar: `kosular/kosu1_v32_yerel_27eki/` (OZET.md dahil). Geçersiz JSON 0, haksız durdurma 0, maliyet 0 $.

## Tablo (iş = asıl zarf kapalı haliyle çıkış arşivinde)
| dünya | koşul | iş | tohum 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|---|
| v3.0 | taban | 1/5 | var | yok | yok | yok | yok |
| v3.1 | taban | 1/5 | var | yok | yok | yok | yok |
| v3.2 | taban | 2/5 | var | var | yok | yok | yok |
| v3.1 | O1+O2b v1 | 4/5 | var | yok | var | var | var |
| v3.1 | O1+O2b v2 | 2/5 | yok | yok | var | var | yok |
| v3.2 | O1+O2b v3 | **3/5** | var | yok | var | yok | var |

Beş tohumla farklar yine gürültü sınırında. O1+O2b'nin üç sürümü birlikte 9/15; tabanın üç dünyası birlikte 4/15.

## Ne değişti (v3.1'in 15 koşusu ile v3.2'nin 10 koşusu)
- "Bu eylem burada çalışmaz": 259'dan 36'ya (koşu başına yaklaşık 17'den 3,6'ya). Labirent levhası, gezilen odalar ve geçerli eylem listesi labirent takılmasını büyük ölçüde çözdü.
- Uydurma eylem ("böyle bir eylem yok"): 0.
- Başajan takılması yok: başajan ipucu hiç gerekmedi, 10 tur kuralı hiç tetiklenmedi.
- Bizim ajana renk: 1 (açık zarfla KIRMIZI). Haksız 0.

## Kalan tek büyük hata: zarf açma
İşin yapılmadığı 5 koşunun **5'inde de** taşıyıcı asıl zarfı açtı:
- 3 kez labirent çıkışında (anahtar_kullan çalışmayınca), 2 kez K2'de levhayı cevapladıktan hemen sonra ("K2'de duruyor ve zarfı açıyorum").
- Sonrası: 3'ünde taşıyıcı bitir dedi, açık zarf kutuya dönmediği için düştü (v3.1 kuralı); birinde K2'de KIRMIZI; birinde adım sınırında takıldı.
- Kartlardan dikkatli (G1) de açtı: G1 2, G2 1, G3 2.
- Görev cümlesinde "Zarfı açma… Açılan zarf bir daha kapanmaz ve hiçbir kapı kabul etmez" yazıyor; model yine açıyor. Açıklamalardan görünen: zarfı teslim için açmak gerektiğini sanıyor.

Küçük not: taban tohum 2 ve 5'te atanmamış iki taşıyıcı uyarıyı aldıktan sonra K1'de bekledi ve koşu 120 tura kadar uzadı; işi etkilemedi (tohum 2'de iş var), yalnız süreyi uzattı.

## Kilitten önce karar bekleyenler (Hikayeci önerisi, uygulanmadı)
1. DEGISIKLIK v3.2 §7 "zarf açmaya yeni cümle eklenmez" diyor. Sonuç bunu sınadı: kural cümlesi yetmiyor, başarısız koşuların hepsi bu. Danışman bu maddeyi yeniden açmak ister mi? Dünyaya uygun seçenekler (eylem söylemeden): K2 levhasına "Zarf kapalı haliyle kutuya alınır." · gözlemde çanta satırı "mühürlü zarf var (kapalı kalmalı)" · zarf_ac denince kapı mesajı gibi bir dünya cevabı yok (açma anında olur).
2. Kilide giren taban: O1+O2b v3, 3/5 (tohum 1-5). Danışmanın yazdığı gibi kilitte ölçü "sınav tohumlarında iş oranı" (6-15) olur.
3. Uyarıyı alıp K1'de bekleyen atanmamış taşıyıcı: kural gereği renk yok; koşuyu uzatıyor. Bir şey yapılsın mı, yoksa olduğu gibi mi kalsın?

Tez cümlesi (Turan): "Yapabilir demiyoruz; yapabilmesinin yolu vardır ve onu bulacağız." Bugün: labirentte kaybolma 259'dan 36'ya indi; kalan engel tek ve adı belli: zarfı açmak.

Program RMS: oyun_alani_v3 v3.2 · dunya.py (labirent levhası, gezilen odalar, geçerli eylem listesi, hareketsiz_tur, başajan) · suruculer.py (O2b v3) · kosu0.py (23 senaryo) · kayıtlar kosular/kosu1_v32_yerel_27eki/
