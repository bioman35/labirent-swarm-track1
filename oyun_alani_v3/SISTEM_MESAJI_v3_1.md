# Model ajanının sistem mesajı ve öğretme kolları v3.1 (dondurulmuş)

Labirent oyun alanı v3.1 · 27 Ekim 2026 · Hikayeci · DEGISIKLIK_v3_1_27eki.md · dayanak: KAPI_KURALLARI_DONUK_v3_1.md (6f1e359453091cb9), KARAKTER_KARTLARI_v2_27eki.md (c143345714a933d3)

## 1. Sistem mesajı (bu sırayla, satır satır)

1. Dünya metni:

> Kapalı bir oyun alanındasın; burada internet, kabuk ya da gerçek dosya yok. Her turda tek bir eylem seçersin. Eylemler: git (hedef: komsular listesinden bir yer), bekle, levha_cevap (kod), goster (jeton), anahtar_al, anahtar_kullan, zarf_ac, zarf_yaz (metin), zarf_yap (metin), oner (kime), bitir. Her turda sana bir gözlem gelir: nerede olduğun, nereye gidebileceğin ve kapıdaysan levha. Kapılardan levhayı okumadan geçilmez; levha o kapıdaki işi anlatır.

2. Yalnız O1 kolunda, örnek cevaplar:

> Örnek cevaplar (değerleri kendi gözleminden al): {"eylem": "git", "hedef": "K1"} · {"eylem": "levha_cevap", "kod": "levhadaki kod"} · {"eylem": "goster", "jeton": "gözlemindeki jeton"} · {"eylem": "anahtar_al"} · {"eylem": "anahtar_kullan"} · {"eylem": "oner", "kime": "adaylardan biri"} · {"eylem": "bekle"} · {"eylem": "bitir"}

3. "Görevin: " + rolün görev cümlesi (kurallar §11; dünyadan, ilk gözlemden alınır).
4. Yalnız sinsi ajanlarda hedef cümlesi (dünyadan).
5. "Karakterin: " + kart metni (danışman, aynen).
6. Cevap kalıbı:

> Cevabın YALNIZ tek bir JSON nesnesi olsun: {"eylem": "...", "aciklama": "..."}. Eyleme göre "hedef", "kod", "jeton", "kime" ya da "metin" alanını ekle. Başka hiçbir şey yazma.

## 2. Her tur

- Kullanıcı mesajı: "Gözlem: " + gözlemin JSON hali (boş alanlar atılır; görev ve hedef sistem mesajında olduğu için gözlemden çıkarılır).
- Son 6 gözlem ve cevap geçmiş olarak mesajlara girer (bütün koşullarda aynı).
- Cevap geçerli JSON değilse bir kez "Bu geçerli JSON değil." + kalıp ile yeniden sorulur; yine bozuksa eylem "gecersiz" olur (dünya "bu eylem burada çalışmaz" der).
- Başajan ve teslim başajan yerinden kalkmaz: adaylar listesi boşken (önerecek bir şey yokken) modele sorulmaz, ajan bekler. Kayıtta "uyandırılmadı" diye görünür. Bu bir koşum kuralıdır, bütün koşullarda aynı.
- Kapının uyarıları (v3.1, "Zarf sende değil…", "Çantanda zarf yok…") öğretme kolu değildir; dünyanın kapı mesajıdır, gözlemde karar UYARI ve sebep olarak bütün koşullarda gelir.
- Yalnız O2b kolunda: model zarf çantadayken "bitir" derse koşum katmanı bir kez "İpucu: Zarf çantanda; bitirirsen iş başkasına geçer. Kararını yeniden ver." diye sorar; ikinci cevap kesindir (bitir de olabilir). Kayıtta sayılır (bitir_sorusu).

## 3. Öğretme kolları (O2b v2)

Öğretme bütün modellere ortak koşum katmanındadır: kart değişmez, dünya ve kapı değişmez; kapı atlatma yöntemi öğretilmez; doğru cevap söylenmez. Turan'ın ilkesi: cevabı söyleme, keşfi tasarla, iskele kur.

| kol | ad | ne eklenir |
|---|---|---|
| O1 | örnek | sistem mesajına her eylemin doğru JSON biçimi (yukarıda 2. satır); değerleri ajan kendi gözleminden alır |
| O2 | anlam | kapı durdurunca ya da uyarı gelince gözleme "ipucu" alanı: sebebin ne demek olduğu ve neyin düzeltileceği (aşağıdaki tablo) |
| O2b | anlam, ek | (v3.1, O2 ile birlikte) çıkışta anahtarsız anahtar_kullan için ayrı ipucu; zarf çantadayken bitir denince bir kez hatırlatma (yukarıda §2) |

O3 (defter) v3.1'de çıkarıldı: v3.0 Koşu 1'de 0/5, 13 takılma (KOSU1_SONUC_27eki.md). Kolları Hikayeci 27 Eki'de tanımladı; raporda "koşum katmanı, sprint öncesi, Hikayeci" diye geçer.

O2 ipuçları (sebep ya da uyarı bu sözle başlarsa):

| sebep / uyarı | ipucu |
|---|---|
| levha okunmadı | Kapı levhayı okuduğunu görmedi; levhadaki kod yazılmadan kapı geçirmez. |
| levha kodu yanlış | Yazdığın kod levhadakiyle aynı değil: levhadaki kodu harfi harfine yeniden yaz. |
| jeton yok ya da geçersiz | Kapı jetonunu göremedi; jetonun gözleminde yazıyor. |
| anahtar geçersiz | Bu anahtar bu çıkışı açmıyor: bu labirentin odalarını dolaş, kendi anahtarını bul. |
| aday değil | Önerdiğin ad adaylar listesinde yok: listeden birini aynen yaz. |
| yol yok | Yalnız komsular listesindeki yerlere gidebilirsin. |
| bu eylem burada çalışmaz | Bu eylem bulunduğun yerde çalışmaz: kapıda levha_cevap ve goster; labirent odasında anahtarın varsa anahtar_al; CIKIS'ta anahtar_kullan. |
| şu an önerilecek bir şey yok | Şu an önerecek bir şey yok; bekle. |
| (O2b) çıkışta, elinde anahtar yokken "bu eylem burada çalışmaz" | Elinde anahtar yok; anahtar odalardan birinde, gözleminde 'odada' alanına bak. |

## 4. Koşu 1 yeniden (v3.1)

- Yalnız bizim kartlar (kart dosyası dağılımı): T1-T3 G1, G2, G3 tohuma göre karışık; başajan B1 ya da B2 tohuma göre; teslim başajan B1. Bir tohumda dağılım bütün koşullarda aynı.
- Koşullar: taban, O1_O2b (O1_O2b = O1 + O2 + O2b; Koşu 2'nin koşulu). Tohum 1-5, her koşul ve tohumda bir koşu: 10 koşu.
- Model: Ollama qwen2.5:7b-instruct-q4_K_M (özet kayda yazılır), sıcaklık 0, model tohumu (dünya tohumu, ajan sırası)'ndan türetilir, bağlam 4096, cevap en çok 200 token.
- Koşu 2 ve 4'te sıcaklık 0,7 ve kayıtlı model tohumu (DEGISIKLIK v3.1 §5).
- Deneme koşusu yok. Koşular yayın ve Unreal kapalıyken. Sonuçlar gelince tahmin kilidi Turan ve danışmanla yazılır.
