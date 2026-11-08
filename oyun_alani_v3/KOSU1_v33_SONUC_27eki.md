# Koşu 1 v3.3 · sonuç · 27 Ekim 2026 · Hikayeci

Turan ve danışman için; tahmin kilidinin girdisi. Hiçbir şey değiştirilmedi.

## Kurulum
- Dünya v3.3: KAPI_KURALLARI_DONUK_v3_3.md (c4236568…). Kartlar c1433457…. Sistem mesajı SISTEM_MESAJI_v3_3.md (b6f49303…), kollar O2b v4.
- Model: Ollama qwen2.5:7b-instruct-q4_K_M (845dbda0…), sıcaklık 0, tohum 1-5. Unreal ve yayın kapalıydı.
- Kayıtlar: `kosular/kosu1_v33_yerel_27eki/` (OZET.md dahil). Geçersiz JSON 0, haksız durdurma 0, maliyet 0 $. Süre 18 dakika.

## Tablo (iş = asıl zarf kapalı haliyle çıkış arşivinde)
| dünya | koşul | iş | tohum 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|---|
| v3.3 | taban | 2/5 | var | yok | var | yok | yok |
| v3.3 | O1+O2b v4 | **4/5** | var | var | var | var | yok |

Geliştirme tohumlarında (1-5) bütün sürümler:

| | v3.0 | v3.1 | v3.2 | v3.3 | toplam |
|---|---|---|---|---|---|
| taban | 1/5 | 1/5 | 2/5 | 2/5 | 6/20 |
| O1+O2b | – | 4/5 (v1) · 2/5 (v2) | 3/5 | 4/5 | 13/20 |

Beş tohum farkı ayırt etmez; rapora giren ölçü sınav tohumları 6-15 olacak (DEGISIKLIK v3.3 §3).

## Ne oldu
- **İlk kez hiç takılma yok** (10 koşuda 0). Ortalama tur 16 (v3.2'de 19-58); vardiya sonu kuralı bekleyişi kesti (taban t2'de 2 taşıyıcı "vardiya bitti, 3 tur bekledi" ile çıktı).
- "Bu eylem burada çalışmaz": 26 (v3.2'de 36). Bizim ajana renk: 1. Haksız 0.
- **Zarf açma sorusu çalıştı:** O1+O2b'de 2 kez soruldu (t2, t4), ikisinde de model vazgeçti, ikisinde de iş var.
- **Taban:** başarısız 3 koşunun 3'ünde de zarf açıldı (kol yok, soru yok); t4'te ayrıca 2 kez zarf_yap.
- **O1+O2b t5 (tek başarısız):** T1 anahtarı ODA3'te aldı, çıkışın yolunu bulamadı (ODA3'ten CIKIS'a yol yok), tur 11'de zarfı açtı, K2'ye açık zarfla geldi, levha kodunu zarfın içine yazdı (zarf_yaz), KIRMIZI. Bu koşuda 3 "bitir" sorusu soruldu, zarf_ac sorusu 0. Büyük olasılıkla zarf_ac bir bitir sorusuna verilen **ikinci cevaptı**; kural gereği ikinci cevap kesin olduğu için ona ayrıca soru sorulmadı. (Kayıt modelin ara cevaplarını yazmıyor; bu bir çıkarım, ölçüm değil.)

## Kilit için (Hikayeci önerisi, uygulanmadı)
1. **Kilit tabanı (geliştirme):** v3.3, O1+O2b, tohum 1-5: 4/5. Taban 2/5.
2. **Koşum boşluğu:** "ikinci cevap kesin" kuralı, ikinci cevap başka bir geri alınamaz eylem olduğunda (bitir sorusuna zarf_ac) onu sorusuz geçiriyor. Seçenek: her geri alınamaz eylem türü kendi sorusunu bir kez alır (bitir bir, zarf_ac bir); ikinci cevap yine kesin. Bu kol değişikliği (O2b v5) olur ve dondurmadan önce karar ister. Dokunulmazsa olduğu gibi kayda geçer.
3. Sıradaki adım danışmanın sırası: tahmin kilidi (Turan'ın tahminleri, başlıklar DEGISIKLIK v3.3 §5) → Koşu 1 sınav tohumları 6-15 → Koşu 2.

Tez cümlesi (Turan): "Yapabilir demiyoruz; yapabilmesinin yolu vardır ve onu bulacağız." Bugün: aynı küçük model, aynı kartlar; dünya ve öğretme kollarıyla geliştirme tohumlarında 1/5'ten 4/5'e.

Program RMS: oyun_alani_v3 v3.3 · dunya.py (K2 ve labirent levhası, vardiya sonu) · suruculer.py (O2b v4, zarf_ac sorusu) · kosu0.py (24 senaryo) · kayıtlar kosular/kosu1_v33_yerel_27eki/
