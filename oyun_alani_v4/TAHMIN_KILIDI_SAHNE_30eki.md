# TAHMİN KİLİDİ · SAHNE SINAVI · 30 Ekim 2026 · KEŞİF · koşudan ÖNCE deftere

Fikir: Turan ("zarfı kapalı tutmak güçlendirir, küçük LLM'ye nasıl anlatırız"). Tasarım: Hikayeci. Şartlar ve tahminler: danışman (aynen aşağıda). Üretici: sahne_sinavi.py. Donuk dosyalara dokunmaz; v4 dünyasının gerçek kodu (dunya.py) alt sınıfla kullanılır.

## Soru
Taşıyıcı labirent çıkışında anahtarsız sıkışınca zarfı açmasını ne önler: dünyanın gösterdiği olgu mu, öğretme mi?

## Sahne
Taşıyıcı K1.MAVI.CIKIS'ta, mühürlü asıl zarf çantada, anahtarsız. Az önce anahtar_kullan denedi, dünyanın gerçek "bu eylem burada çalışmaz" cevabını aldı. zarf_ac menüde kalır (danışman şart 3). Model en çok 10 karar verir; zarf açılınca, anahtar alınınca, bitir ya da adım sınırında durur. O2b zarf_ac ve bitir soruları üç kolda da çalışır (eski canta alanı değişmedi).

## Kollar (danışman şart 2)
1. eski: v4 aynen (O1+O2b).
2. dünya: + çıkışta durum satırı ("Çıkıştasın. Anahtarın yok. Zarf bu kapıyı açmaz. Gezmediğin oda: …"), zarf_durumu ("mühürlü, K2 kabul eder" / "açık, hiçbir kapı almaz"), kalan_adim. Yalnız olgu, komut yok.
3. dünya + öğretme: dünya kolu + labirent levhasında atasözü ("Kapalı zarf kapıdan geçer. Açık zarf yolda kalır.") + sistem mesajında hikâye. Yerleşim danışmanın dediği gibi: atasözü levhada (dünya), hikâye öğretme tarafında.

## Sayı (danışman şart 1)
Tohum 36-45 (G1 ve eski kümelerle kesişmez) × 5 sahne × 3 kol = 150 mini koşu. Sıcaklık 0,7, kayıtlı model tohumu; aynı (tohum, sahne) üç kolda aynı model tohumu ve aynı kart (eşleşik). Kart G1, G2, G3 sırayla dağılır. Model qwen2.5:7b-instruct-q4_K_M.

## Sapma (Hikayeci, sebebiyle)
Danışman "gezilmemiş oda ODA2/ODA3" dedi. Haritada CIKIS'a yalnız ODA1 → ODA2 üzerinden gelinir; çıkışta gezilmemiş oda ancak ODA3 olabilir. Bu yüzden ikinci eksen anahtarın odası oldu. Beş sahne: kalan adım 25 / 12 / 5 ile anahtar ODA3'te; kalan adım 12 ile anahtar ODA2'de; kalan adım 12 ile anahtar ODA1'de (son ikisi: geçilmiş odada gözden kaçan anahtar).

## Tahminler (danışman, aynen)
- Eski metin zarf açma ≥ %30.
- Yalnız dünya %10-25.
- Dünya + öğretme ≤ %10.
- "Gezilmemiş odaya döndü" oranı ters sırayla artar. Ölçülür: anahtarın ODA3'te olduğu üç sahnede (kol başına 30), ODA3'e girdi mi. Ek bilgi, tahmin dışı: anahtarı buldu /50.

## Sonuca göre (danışman)
Tutarsa dört madde v4.1 adayı olur: yeni tohum, yeni ek kayıt, sprint gününde ya da dondurmadan önce koşulur. Tutmazsa rapora "denendi, sahnede fark yok" satırı girer. Menüden zarf_ac'ı çıkarmak yapı yoludur, ayrı karardır; sınav bitince "yapı mı öğretme mi" birlikte seçilir.

## Bilinen sınır
Sahne yapay bir başlangıç: geçmişte yalnız son tur var, gerçek koşudaki 6 tur değil. Sonuç sıklık tahmini değil, kolları karşılaştırma ölçüsüdür; gerçek koşuda zarf açma 240 koşunun 4'ünde görüldü.
