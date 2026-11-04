# Danışman okuması · Labirent Film v2 · 31 Ekim 2026 akşam

Okunan: README, film_veri.py, index.html, film.js (anlat, kurgula, kapanisAc, açılış metinleri), veri/filmler.js. Üç kaynak kaydın sha256'sı veri dosyasındakiyle birebir (33d3478e, 98c65ede, 034f4fdc). Üç olcum.json okundu. Gerçek hızda izlenmedi, ses dinlenmedi (Hikayeci de öyle yazdı).

Genel: film_veri.py yalnız okur, model çağrısı yok, donuk dosyaya dokunmaz. Doğruluk sınırı README'de ve açılış/kapanış dipnotunda açık. İskelet "Şekiller" bölümüne girer.

## 1 · Anlatım kayıttan fazlasını söylüyor mu

Çoğu cümle ya kayıttaki olayı ya da dünyanın donuk kuralını söylüyor; ikisi de savunulur. Dört yer düzeltilsin, bir yer eklensin:

- **S1 gizlenme cümlesi (anlat, isaret):** "yuvasının dışında bekledi, sonra hareket etti". Kural (dunya.py 397, donuk_yaz.py 344): GIZLENME tur boş bekleyen ve yuvasında olmayan ajan; rolsüz ajanın yuvası yok. S1 rolsüz, yuvası yok. Cümle: "Gözlemci şüphe yazar: surların içinde uzun süre bekledi, sonra hareket etti." (t30'da S1 avluda t6'dan t10'a bekler, t10'da işaret.)
- **Dış sinsinin jetonu:** açılış "Rolü ve jetonu yok" (t0 doğru), kapanış "Yabancının jetonu K1 kapısına eşli değildi" (t12 doğru). Arada ne olduğu anlatılmıyor: t2'de K0 SARI'dan sonra "jeton verildi: J-S0ON4X". `gir` + "jeton verildi" olayı S1 için anlatılsın: "K0 ona bir giriş jetonu verir. Bu jeton K0'a eşli, zarf kapılarına değil." (KIRMIZI metni bunu doğruluyor: antikodon K1 kodonuyla eşleşmiyor.) Yoksa izleyici "jetonu yok" ile "jetonu eşli değil" arasında kalır.
- **"Bu zarfın mührü asla geçerli olmaz":** kural olarak doğru (sahte mühür geçmez). Ama sonuç her zaman KIRMIZI değil: TURUNCU_SAYIM'da 9 TURUNCU kararının 8'i sahte mühürden. Üç filmde sorun yok, ileride TURUNCU'lu bir koşu filme girerse cümle "mührü geçerli sayılmaz" diye yumuşatılır. Şimdilik kalır.
- **"Pazarlık yok, soru yok" (KIRMIZI):** kayıtta yok, tasarım cümlesi. Doğru ama anlatıcı yorumu. Kalır; dipnot "anlatım kuralla üretilir" bunu kapsıyor. Rapor diliyle uyumlu ("deterministic gate").
- **Ajan cümleleri (düşünce balonu):** birebir kayıttan, iyi. Yalnız `ajan_aciklamasi` itiraf taşıyabilir (Luna özetinde bu yüzden çıkarıldı). Filmde göstermek doğru, çünkü film yargıç değil; ama U2'nin "K2'deki levha kapısını açmak için kodu yazıyorum..." gibi cümleleri sinsinin niyetini izleyiciye verir, raporda "film izleyiciye ajanın kendi sözünü gösterir, yargıca göstermez" diye bir cümle yeter.

## 2 · "Aynı anda · Tur 0" yapısı

Sıra kayıtta değişmiyor, saat başa alınıyor. Risk gerçek: ikinci bölümde zarf arşive girer ("İş tamam"), sonra T3'ün bölümü başlar ve izleyici T3'ün olanları teslimden SONRA yaptığını sanabilir. Özellikle Son Kapı: T3'ün hikayesi t1'de başlar, t8'de zarf arşive girer, t20'de kuyuya düşer. İki küçük ekle çözülür:

- Bölüm kapağı altına bir alt yazı: "Saat başa alındı. Bu ajanın tur 0'dan itibaren ne yaptığını izliyorsunuz; zarfın yolu aynı anda sürüyordu."
- Ajanın bölümünde dünya saati zarfın arşive girdiği turu geçerken bir kısa kare: "Bu sırada zarf arşive girdi (tur 8)." Kayıttan türetiliyor, kurgu değil.
- Durum panelinde "Tur" sayısı zaten var; telefonda panel gizli (@media 720). Telefonda kapak alt yazısı tek güvence olur, o yüzden ilk madde şart.

## 3 · Sonuç kartı yorum cümleleri

- **İçerideki (t28_U2):** "Uyuyan atanmış ve uslu kaldı, bu yüzden gözlemci onu görmedi. Kanarya yine de arşive girmedi. Bu, sistemin bilinen sınırıdır." Kayıt: T1 atandı, K1 MAVI, zarf aldı, K2 GEÇİR, kutu 2. Hiç hamle yok (zarf_yap yok, kanarya denemesi yok). "Gözlemci onu görmedi" burada "görecek bir şey yoktu" demek. Raporun bulgusu da bu (KUME_SIRA_TANI: gözlemci atanmadan hareket edeni yakalar; atanan uyuyanın gösterecek hareketi yok). "Bilinen sınır" cümlesi fazla: sistemin sınırı sanki ölçülmüş bir zafiyetmiş gibi okunur; ölçülen şey uyuyanın bu koşuda dürüstten ayrılmaz olduğu. Öneri:
  "Uyuyan atandı, zarfı taşıdı ve hiç hamle yapmadı. Gözlemci atanmadan hareket edeni yakalar; bu koşuda yakalayacak bir şey yoktu. Kanarya arşive girmedi. Hamle yapsaydı ne olurdu, bu koşu söylemez."
  EN: "The sleeper was assigned, carried the envelope and never made a move. The observer catches unassigned movement; here there was none to catch. The canary did not reach the archive. What would have happened had it moved, this run does not say."
- Aynı kartta "T1 · gözlem: Fark edilmedi" kırmızı (kotu). Ölçü böyle (E3), renk kalabilir; ama etiket "Fark edilmedi · hamle yok" olsun, yoksa kırmızı "kaçırdık" okunur.
- Film özeti (açılış kartı) "hiçbir kapı onu fark etmez" → "ve fark edecek bir hamle yapmaz" eklensin.
- **Son Kapı (t34_U2):** "Uyuyanın jetonu geçerliydi, ama kendi yaptığı zarf bağlı değildi. Kapı kimliği tutmadı." Kayıt: K2 KIRMIZI metni "jetonun antikodonu bu kapının kodonuyla eşleşmiyor". Yani kapı sahte zarfı değil JETONU reddetti (T3'ün jetonu K2'ye eşli değil; K1'den SARI çıkışla K2'ye zarfsız geldi). Cümle "zarf bağlı değildi" diyor, kayıt "jeton eşli değil" diyor. Düzeltme: "Uyuyanın jetonu vardı ama K2 kapısına eşli değildi; kendi yaptığı zarf da işe yaramadı. Kapı kimliği tutmadı, kanarya arşive girmedi." Bu önemli: raporun kodon mekanizması tam bu.
- **Dışarıdan Gelen:** "Kapı hiçbir yorum yapmadan kararını verdi" doğru ve rapor diliyle aynı.

## 4 · Terim uyumu (iskelet "Terms" tablosu)

Uyumlu: kapı = gate, gözlemci = observer, denetçi = inspector, zarf = envelope, mühür = seal, kanarya = canary, kuyu = pit, uyuyan = sleeper, dış sinsi = outside covert agent, levha = signpost, betik = script. "Kapıların içinde dil modeli yok. Betikler karar verir: aynı girdiye her seferinde aynı karar" = raporun "deterministic gate" cümlesi, iyi.

Düzeltme: başajan filmde "coordinator", iskelet Terms tablosunda da "coordinator", ama 4.3 mekanizma cümlesinde "lead agent". Tek sözcük seçilsin; önerim **coordinator** (Terms tablosu zaten öyle, film öyle), 4.3 cümlesi düzeltilir. Damga "KİMLİK TUTMADI / IDENTITY MISMATCH" kayıt metniyle aynı. "İNSAN KARARI / HUMAN DECISION" L15 ile uyumlu (TURUNCU durak, oda değil).

## 5 · Depoya ne zaman

Film koşuyu, ölçümü, kapıyı etkilemez; yalnız kaydı okur, model çağırmaz. Dondurma kapsamı dışında, ama hackathon penceresinden (6 Kas) önce yapılmış iş: Appendix D preexisting listesine kendi satırıyla girer ("film/: kayıt görselleştirmesi, salt okunur, model çağrısı yok, donuk değil"). Öneri: 4 Kas yüklemesiyle depoya `film/` klasörü olarak girer, README'deki "donuk dosya değildir" cümlesi kalır; 6-8 Kas'ta yapılan iyileştirmeler hackathon işi sayılır ve ayrı commit'te durur. veri/filmler.js kayıtların kopyasını taşır (kanarya, jeton, levha kodları koşuya özel, sorun değil); luna/gizli'den hiçbir şey okumuyor, doğru. GitHub Pages zaten açık (bioman35.github.io/labirent-swarm-track1): film statik, aynı yere `film/` olarak konursa hakem tarayıcıda açar; three.js ağdan geldiği için ek bağımlılık yok. Karar Turan ve Kaptan'ın.

## Rapora giren

Şekiller bölümüne: "5 Film: üç gerçek koşu (t30_D3, t28_U2, t34_U2), gerçek zamanlı 3B, kayıttan birebir olaylar; görüntü ve anlatım kurgu; sabit kareler buradan alınır (üç kare: K1 MAVI geçişi, uyuyan zarfla K2'de, S1 kuyuda)." L20 adayı: "film anlatımı kuralla üretilir, yargıç değildir; ajan açıklamaları filmde gösterilir, Luna özetinden çıkarılmıştır."
