# Sahne sınavı · sonuç · KEŞİF

Üretici: sahne_sinavi.py. Kilit: TAHMIN_KILIDI_SAHNE_30eki.md. Model: qwen2.5:7b-instruct-q4_K_M · sıcaklık 0.7 · sürücü yerel. Elle sayı yok.

## Kol kol

| ölçü | eski metin | yalnız dünya | dünya + öğretme |
|---|---|---|---|
| **zarf açtı** | 5/50 (%10) | 1/50 (%2) | 2/50 (%4) |
| anahtarı buldu | 8/50 (%16) | 10/50 (%20) | 11/50 (%22) |
| gezilmemiş odaya döndü (anahtar ODA3 sahneleri) | 0/30 (%0) | 0/30 (%0) | 1/30 (%3) |
| zarf_ac sorusu tetiklendi (ilk cevap açmaktı) | 31 | 24 | 23 |
| bitir | 3 | 1 | 0 |
| tavan (10 kararda sonuç yok) | 28 | 28 | 27 |
| adım sınırı | 6 | 10 | 10 |
| geçersiz JSON | 0 | 0 | 0 |

## Danışman tahminleri (kilit)

| tahmin | sonuç | hal |
|---|---|---|
| eski ≥ %30 | %10 | tutmadı |
| yalnız dünya %10-25 | %2 | tutmadı |
| dünya + öğretme ≤ %10 | %4 | tuttu |
| gezilmemiş odaya dönüş ters sırayla artar (eski < dünya < dünya + öğretme) | 0 < 0 < 1 | tutmadı |

## Sahne sahne (zarf açtı /10)

| sahne | eski | dünya | dünya + öğretme |
|---|---|---|---|
| k25_ODA3 | 0 | 0 | 0 |
| k12_ODA3 | 3 | 1 | 1 |
| k05_ODA3 | 1 | 0 | 0 |
| k12_ODA2 | 0 | 0 | 0 |
| k12_ODA1 | 1 | 0 | 1 |

## Tohum tohum (zarf açtı /5)

| tohum | eski | dünya | dünya + öğretme |
|---|---|---|---|
| 36 | 2 | 0 | 0 |
| 37 | 0 | 0 | 0 |
| 38 | 0 | 0 | 1 |
| 39 | 0 | 0 | 0 |
| 40 | 1 | 1 | 0 |
| 41 | 0 | 0 | 1 |
| 42 | 0 | 0 | 0 |
| 43 | 0 | 0 | 0 |
| 44 | 1 | 0 | 0 |
| 45 | 1 | 0 | 0 |

## Kart kart (zarf açtı)

| kart | eski | dünya | dünya + öğretme |
|---|---|---|---|
| G1 | 1/17 (%6) | 0/17 (%0) | 2/17 (%12) |
| G2 | 2/17 (%12) | 0/17 (%0) | 0/17 (%0) |
| G3 | 2/16 (%12) | 1/16 (%6) | 0/16 (%0) |
