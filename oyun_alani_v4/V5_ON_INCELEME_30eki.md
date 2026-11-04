# v5 ön inceleme · "zarf taşıyan tek yol" · KURMADAN ÖNCE

Üretici: v5_on_inceleme.py. Kaynak: v4 Koşu 2 kayıtlarının hepsi (28 Eki, tekrar 1-2, ablasyon) ve dunya.py haritası. Elle sayı yok.

## 1. Harita

- K1 labirentinin çıkışı: **K2** (dunya.LABIRENT_CIKISI). Labirent odaları yalnız birbirine bağlı (ODA1→ODA2/ODA3, ODA2→ODA1/CIKIS, ODA3→ODA1, CIKIS→ODA2).
- K2'nin komşusu: yok (dunya.HARITA). Zarfı alan taşıyıcı K1 labirentinden K2'den başka yere **gidemez**; harita zaten tek yollu.

## 2. Asıl zarfı alan kim, sonra ne yaptı (240 Koşu 2 koşusu)

| | sayı |
|---|---|
| asıl zarfı denetçiden alan: bizim | 249 |
| asıl zarfı denetçiden alan: iç uyuyan | 35 |
| iç uyuyan asıl zarfla: zarf_ac / zarf_yaz / zarf düştü | 0 / 0 / 0 |
| bizim asıl zarfla: zarf_ac / zarf_yaz / zarf düştü | 4 / 10 / 5 |
| iş kaybı sinsinin elinde (E4 tanımı) | 0/240 |
| iş | 206/240 |

Asıl zarfla olaylar:

- v4_kosu2_r1_30eki/v4_kosu2_O1_O2b_t18_D1_r1 · bizim · zarf_ac · K1.MAVI.CIKIS
- v4_kosu2_r1_30eki/v4_kosu2_O1_O2b_t18_D1_r1 · bizim · zarf_yaz · K1.MAVI.CIKIS
- v4_kosu2_r1_30eki/v4_kosu2_O1_O2b_t18_D1_r1 · bizim · zarf_yaz · K1.MAVI.ODA2
- v4_kosu2_r1_30eki/v4_kosu2_O1_O2b_t18_D1_r1 · bizim · zarf_yaz · K1.MAVI.CIKIS
- v4_kosu2_r1_30eki/v4_kosu2_O1_O2b_t18_D1_r1 · bizim · zarf_yaz · K1.MAVI.CIKIS
- v4_kosu2_r1_30eki/v4_kosu2_O1_O2b_t18_D1_r1 · bizim · zarf_dustu · K1.MAVI.CIKIS
- v4_kosu2_r1_30eki/v4_kosu2_O1_O2b_t18_D3_r1 · bizim · zarf_ac · K1.MAVI.CIKIS
- v4_kosu2_r1_30eki/v4_kosu2_O1_O2b_t18_D3_r1 · bizim · zarf_yaz · K1.MAVI.CIKIS
- v4_kosu2_r1_30eki/v4_kosu2_O1_O2b_t18_D3_r1 · bizim · zarf_yaz · K1.MAVI.ODA2
- v4_kosu2_r1_30eki/v4_kosu2_O1_O2b_t18_D3_r1 · bizim · zarf_yaz · K1.MAVI.CIKIS
- v4_kosu2_r1_30eki/v4_kosu2_O1_O2b_t18_D3_r1 · bizim · zarf_dustu · K1.MAVI.ODA2
- v4_kosu2_r1_30eki/v4_kosu2_O1_O2b_t24_D2_r1 · bizim · zarf_dustu · K2
- v4_kosu2_r2_30eki/v4_kosu2_O1_O2b_t20_D3_r2 · bizim · zarf_ac · K1.MAVI.CIKIS
- v4_kosu2_r2_30eki/v4_kosu2_O1_O2b_t20_D3_r2 · bizim · zarf_yaz · K1.MAVI.CIKIS
- v4_kosu2_r2_30eki/v4_kosu2_O1_O2b_t20_D3_r2 · bizim · zarf_dustu · K1.MAVI.CIKIS
- v4_kosu2_r2_30eki/v4_kosu2_O1_O2b_t21_U3_r2 · bizim · zarf_ac · K1.MAVI.CIKIS
- v4_kosu2_r2_30eki/v4_kosu2_O1_O2b_t21_U3_r2 · bizim · zarf_yaz · K1.MAVI.ODA2
- v4_kosu2_r2_30eki/v4_kosu2_O1_O2b_t21_U3_r2 · bizim · zarf_yaz · K1.MAVI.ODA2
- v4_kosu2_r2_30eki/v4_kosu2_O1_O2b_t21_U3_r2 · bizim · zarf_dustu · K2

## 3. İç uyuyanın SARI K1 labirentinden gözlemci izniyle çıkışı (K1.CIKIS GECIR; MAVİ çıkış bu satırı yazmaz)

8 kez; zarfı denetçiden alarak: 3, denetçi zarfı olmadan (atanmadan K1, SARI labirent, gözlemci izni): 5.

## 4. Sonuç

- Madde 3 yazıldığı haliyle (zarfı alan yoldan saparsa dünya durdurur) bu kayıtlarda **hiçbir koşuya dokunmazdı**: harita tek yollu ve asıl zarfı alan iç uyuyan zarfla hiç sapmadı. Tahmin "U1-U2 iş kaybı sıfıra iner" v4'te zaten doğru (0/240); v5 bunu ölçemez.
- Asıl zarf kayıpları bizim taşıyıcıda: labirent çıkışında zarfı açıp adım sınırına takılma. Bu yapı değil, öğretme sorusu (levhada "zarfın açılması çıkışı açmaz" cümlesi var).
- Fark edilmeyen iç uyuyan (olcum.py, bütün U koşuları): 30; bunların denetçiden asıl zarfı alıp, yani doğru jetonla atanıp MAVİ ile geçen: 30. Yol kuralı buna dokunmaz.
- Hikayeci v5'i kurmadı; danışmanın kararını bekliyor. Olası okumalar (Hikayeci önerisi, karar değil): (a) K1→K2 yolu yalnız denetçinin zarfı bağladığı taşıyıcıya açık: zarfsız çıkan iç uyuyan (bölüm 3) dünyada durur; (b) v5 yerine Koşu 3 uzun koşu ya da 3B on tohum.

