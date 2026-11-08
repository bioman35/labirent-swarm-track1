# Keşif · küçük eğri (qwen2.5 3B)

Üretici: `kesif_3b.py` (yalnız okur; elle sayı yok). Dünya v3.4, O1+O2b, tohum 6-10, sıcaklık 0. Kilitten sonra eklendi (defter kayıt 4-5); tahmin kilidine girmez. 7B sütunu aynı tohumlarda sınav Koşu 1.

## İş

| model | iş | koşu koşu (tur) |
|---|---|---|
| 3B | 1/5 | t6 var (21) · t7 yok (40) · t8 yok (40) · t9 yok (40) · t10 yok (40) |
| 7B | 5/5 | t6 var (11) · t7 var (84) · t8 var (18) · t9 var (22) · t10 var (20) |

## Hangi hata önce geliyor (koşu içinde ilk görüldüğü tur)

| tohum | 3B sıra | 7B sıra |
|---|---|---|
| t6 | Olumsuz cümle (tur 1) → Uzak alan (tur 3) | Uzak alan (tur 3) |
| t7 | Olumsuz cümle (tur 1) → Uzak alan (tur 8) → Uzun pencere (tur 40) | Uzun pencere (tur 83) |
| t8 | Olumsuz cümle (tur 5) → Uzak alan (tur 7) → Uzun pencere (tur 40) | Uzak alan (tur 4) |
| t9 | Uzak alan (tur 3) → Olumsuz cümle (tur 7) → Uzun pencere (tur 40) | Uzak alan (tur 4) → Olumsuz cümle (tur 18) |
| t10 | Uzak alan (tur 3) → Olumsuz cümle (tur 4) → Uzun pencere (tur 40) | Uzak alan (tur 4) |

| model | ilk gelen hata (koşu sayısı) |
|---|---|
| 3B | Olumsuz cümle 3, Uzak alan 2 |
| 7B | Uzak alan 4, Uzun pencere 1 |

## Toplam hata (5 koşu)

| hata türü | 3B | 7B |
|---|---|---|
| Olumsuz cümle | 133 | 1 |
| Uzak alan | 24 | 17 |
| Uydurma eylem | 0 | 0 |
| Talimat sanma | 0 | 0 |
| Geri alınamaz eylem | 1 | 0 |
| Uzun pencere | 4 | 2 |

## O2b sorusu ve ikinci cevap

| model | soru sayısı | ikinci cevap olarak seçilen eylem |
|---|---|---|
| 3B | 41 | zarf_yap 34, zarf_ac 5, zarf_yaz 2 |
| 7B | 2 | git 1, goster 1 |
