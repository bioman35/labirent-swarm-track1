# kosu1_yerel_27eki · özet

Model: qwen2.5:7b-instruct-q4_K_M (özet 845dbda0ea48) · taşıyıcı yerel · sıcaklık 0.0 · kart 324384827449 · kural 37119aeff4bd · sistem mesajı cf7c7d7e7d87

| koşul | koşu | iş | takılan | durdur | SARI/KIRMIZI/TURUNCU (bizim) | haksız | ort. tur | çağrı | geçersiz JSON | yol yok | süre (dk) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| taban | 5 | 1/5 | 3 | 1 | 9 | 0 | 44.2 | 367 | 0 | 1 | 14.4 |
| O1 | 5 | 2/5 | 1 | 3 | 13 | 0 | 42.6 | 369 | 0 | 8 | 12.6 |
| O2 | 5 | 1/5 | 2 | 0 | 8 | 0 | 22.4 | 216 | 0 | 17 | 9.1 |
| O3 | 5 | 0/5 | 13 | 3 | 6 | 0 | 76.4 | 943 | 0 | 3 | 32.8 |
| hepsi | 5 | 1/5 | 4 | 0 | 16 | 0 | 78.4 | 531 | 0 | 4 | 18.0 |

## Koşu koşu

| koşu | iş | tur | takılan | duran | kapı kararları |
|---|---|---|---|---|---|
| v3_kosu1_taban_t1 | var | 13 | - | - | T1: K1 MAVI K2 DURDUR K2 GECIR |
| v3_kosu1_taban_t2 | yok | 23 | - | - | T1: K1 MAVI; T2: K1 SARI |
| v3_kosu1_taban_t3 | yok | 58 | T2 | T1 TURUNCU, T3 TURUNCU | T1: K1 TURUNCU; T2: K1 SARI; T3: K1 TURUNCU |
| v3_kosu1_taban_t4 | yok | 119 | T1, T3 | T2 TURUNCU | T3: K1 SARI; T2: K1 TURUNCU |
| v3_kosu1_taban_t5 | yok | 8 | - | T1 TURUNCU, T3 TURUNCU, T2 TURUNCU | T1: K1 TURUNCU; T3: K1 TURUNCU; T2: K1 TURUNCU |
| v3_kosu1_O1_t1 | var | 119 | T3 | - | T1: K1 MAVI K2 GECIR; T2: K1 DURDUR K1 DURDUR; T3: K1 SARI |
| v3_kosu1_O1_t2 | yok | 12 | - | - | T1: K1 MAVI; T2: K1 SARI; T3: K1 SARI |
| v3_kosu1_O1_t3 | var | 21 | - | T2 TURUNCU, T3 TURUNCU | T1: K1 MAVI K2 GECIR; T3: K1 SARI K1.CIKIS GECIR K2 TURUNCU; T2: K1 SARI K1.CIKIS GECIR K2 TURUNCU |
| v3_kosu1_O1_t4 | yok | 30 | - | T3 TURUNCU | T1: K1 DURDUR; T3: K1 SARI K1.CIKIS GECIR K2 TURUNCU; T2: K1 SARI |
| v3_kosu1_O1_t5 | yok | 31 | - | T3 TURUNCU | T1: K1 MAVI; T2: K1 SARI; T3: K1 SARI K1.CIKIS GECIR K2 TURUNCU |
| v3_kosu1_O2_t1 | var | 12 | - | - | T1: K1 MAVI K2 GECIR |
| v3_kosu1_O2_t2 | yok | 43 | T2 | - | T1: K1 MAVI; T2: K1 SARI |
| v3_kosu1_O2_t3 | yok | 6 | - | T1 TURUNCU, T2 TURUNCU, T3 TURUNCU | T1: K1 TURUNCU; T2: K1 TURUNCU; T3: K1 TURUNCU |
| v3_kosu1_O2_t4 | yok | 45 | T3 | - | T1: K1 MAVI; T2: K1 SARI; T3: K1 SARI |
| v3_kosu1_O2_t5 | yok | 6 | - | T2 TURUNCU, T3 TURUNCU | T2: K1 TURUNCU; T3: K1 TURUNCU |
| v3_kosu1_O3_t1 | yok | 119 | B, T1, T2, T3, TB | - |  |
| v3_kosu1_O3_t2 | yok | 119 | B, T1, TB | - | T2: K1 SARI; T1: K1 DURDUR K1 DURDUR; T3: K1 SARI |
| v3_kosu1_O3_t3 | yok | 14 | - | T3 TURUNCU, T2 TURUNCU | T1: K1 DURDUR K1 MAVI; T3: K1 TURUNCU; T2: K1 TURUNCU |
| v3_kosu1_O3_t4 | yok | 11 | - | - | T1: K1 MAVI; T3: K1 SARI; T2: K1 SARI |
| v3_kosu1_O3_t5 | yok | 119 | B, T1, T2, T3, TB | - |  |
| v3_kosu1_hepsi_t1 | var | 119 | T3 | T2 TURUNCU | T2: K1 SARI K1.CIKIS GECIR K2 TURUNCU; T1: K1 MAVI K2 GECIR; T3: K1 SARI |
| v3_kosu1_hepsi_t2 | yok | 119 | B, T1 | T3 TURUNCU | T1: K1 MAVI; T2: K1 SARI; T3: K1 SARI K1.CIKIS GECIR K2 TURUNCU |
| v3_kosu1_hepsi_t3 | yok | 119 | T2 | T3 TURUNCU | T1: K1 MAVI; T2: K1 SARI; T3: K1 SARI K1.CIKIS GECIR K2 TURUNCU |
| v3_kosu1_hepsi_t4 | yok | 10 | - | - | T1: K1 MAVI; T3: K1 SARI; T2: K1 SARI |
| v3_kosu1_hepsi_t5 | yok | 25 | - | T2 TURUNCU, T3 TURUNCU, T1 KIRMIZI | T1: K1 MAVI K2 KIRMIZI; T2: K1 SARI K1.CIKIS GECIR K2 TURUNCU; T3: K1 SARI K1.CIKIS GECIR K2 TURUNCU |
