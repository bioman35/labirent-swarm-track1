# Labirent Film

Gerçek koşu kayıtlarından kurulan gerçek zamanlı 3B film. Üç kısa film var, TR ve EN.

Açmak için `IZLE.bat` dosyasına çift tıkla. Küçük bir yerel sunucu açar ve tarayıcıyı başlatır, pencereyi kapatınca durur. `index.html` doğrudan açılmaz, tarayıcı yerel modül dosyasını engeller. İnternet gerekir: three.js ve yazı tipi ağdan yüklenir.

Klavye: boşluk oynat/duraklat, sol ve sağ ok 5 saniye geri ve ileri.

Doğruluk sınırı: olaylar, sıra, kapı kararları ve ajan cümleleri kayıttan birebir gelir. Görüntü, süre, kamera ve anlatım metni kurgudur. Anlatım kayıttaki olaylardan kuralla üretilir. Film süresi koşu süresi değildir, bekleme turları kısaltılır.

Yeni film eklemek: `film_veri.py` içindeki `FILM` listesine koşu yolunu ekle, `python -I film_veri.py` çalıştır. Koşu kaydına dokunulmaz.

Donuk dosya değildir. `oyun_alani_v4` ve `swarm/depo` içindeki dosyalara dokunmaz.
