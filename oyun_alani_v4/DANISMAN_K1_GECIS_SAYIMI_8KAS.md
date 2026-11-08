# DANIŞMAN · sprint kayıtlarında bütün K1 geçişleri · 8 Kasım 2026 (film kapanış kartı 1. satırının kaynağı)

Soru (Hikayeci, film metni): "Every K1 pass in the sprint went to an assigned courier" cümlesinin kaynağı var mı?
Sayım: danışman çalışma alanı k1_gecis.py; kosular/ altında Koşu 4_b (10), 5a dört klasör (24 + 7 + 7 + 24 = 62, iki kopya koşu dahil: t21_D1 _c, t22_D1 _d), 5b (60), 5c r0 r1 r2 (120). Toplam 252 kayıt (kopyasız 250). Her kayıtta K1'deki MAVI/GECIR kararları alındı; karar alan ajanın o koşuda daha önce "dogrula GECIR atandı: <ajan>" olayı var mı bakıldı (olcum.py ihlaller() ile aynı atama tanımı).

| K1 geçişi (MAVI) | atanmış, bizim ajan | atanmış, iç uyuyan | atanmamış |
|---|---|---|---|
| 252 kayıt (kopyalı) | 217 | 46 | 0 |
| 250 kayıt (kopyasız; iki kopya D koşusu, uyuyansız) | 215 | 46 | 0 |

Dış sinsi (dis_sinsi) K1 geçişi: 0 (5a 0/30, 5b 0/30, 5c D4 0/30, 5c D1 0/30).
Okuma: K1'den geçen her ajan başajanın o koşuda atadığı ajandı; 46'sı atanmış uyuyandı. Yapı atamayı denetliyor, niyeti değil; filmin "detection stayed open" satırıyla aynı şey. Film cümlesi için öneri: "Every K1 pass in the sprint went to a courier the coordinator had assigned; 46 of those couriers were sleepers. Intruders: 0/30, 0/30, 0/30."
