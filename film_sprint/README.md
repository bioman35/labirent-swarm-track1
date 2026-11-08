# Sprint filmi · Gates Below, a Judge Above

Beş gerçek sprint koşusu (6-8 Kasım), tek kurgu. Sahne film_labirent/ sahnesinin kopyasıdır (8 Kas); film_labirent/ dondurulmuş kalır.

Doğruluk sınırı: olaylar, sıra, kapı kararları ve ajan cümleleri kayıttan birebir gelir. Görüntü, süre, kamera ve anlatım kurgudur. Film süresi koşu süresi değildir. 3. ve 4. bölümde sinsinin K0 girişi (2. bölümdekinin aynısı) hızlı geçilir; kayıt sırası bozulmaz. Film model çağırmaz, kayda dokunmaz. Kodla ses yok: tek ses, Yaprak'ın anlatım kaydı.

Dosyalar
- FILM_METNI_8KAS.md: metin, kartlar, sayıların kaynakları. Filmdeki her yazı buradan gelir.
- ANLATIM_EN_8KAS.txt: anlatım, 8 paragraf, ses programına verilen metin.
- film_veri.py → veri/filmler.js: beş koşu kaydı (sha256 dosyada).
- metin.py → veri/sprint.js: yazılar ve anlatım süreleri.
- film.js, index.html: sahne ve kurgu (?sprint=1). IZLE.bat tarayıcıda oynatır (sessiz).
- cik.py: kare kare çekim (Playwright, GPU). karis.py: anlatım sesini bölme ve birleştirme.

Yapım sırası: ses/anlatim_tam.* (ya da ses/anlatim_0..7.wav) → `python -I karis.py bol` → `python -I metin.py` → `python -I cik.py tam` → `python -I karis.py birlestir` → SPRINT_FILMI.mp4
