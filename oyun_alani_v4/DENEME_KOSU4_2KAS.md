# Luna deneme koşusu · 2 Kasım 2026 · puanlı değil

İzin: Turan, 31 Eki gece (DANISMAN_CEVAP_7SORU_31eki.md, son ek). Başlatma: Turan 2 Kas, "ara koşu". EK2 ve EK2b sayılarına girmez.

Kurulum: `python -I kosu_api.py --kol 4 --tohumlar 1 --butce-dolar 0.5 --cikti kosular/v4_kosu4_deneme_2kas`. Koşu 4 kurulumu: Koşu 1, O1+O2b, bizim 5 ajan Luna (`gpt-5.6-luna`), sinsi yok, küçük taraf Qwen 7B yerel. Gönderilmeyen alanlar: temperature, seed, response_format. Çıktı tavanı `max_completion_tokens` 400. Yayın ve Unreal kapalıydı. Saat 22:33:24 - 22:34:17. Çevrimdışı sınama (`test_kosu_api.py`) koşudan önce TAMAM.

## Beş ölçü

| | ölçü | sonuç |
|---|---|---|
| 1 | 400 tavanında kesilen cevap (`bitis` = length) | 0/30. Bitişlerin 30'u da `stop`. En uzun cevap 77 çıktı jetonu. |
| 1b | Gizli akıl yürütme jetonu sayaca giriyor mu | Büyük olasılıkla evet, kesin değil. Çıktı jetonu ortancası 45, görünen metin ortancası 72 karakter. Karakter/4 kabaca 18 jeton eder, oran ortanca 2,4, en çok 3,9. Türkçe jeton başına karakter ölçülmedi, bu yüzden oran yaklaşık. |
| 2 | JSON ayıklanamayan cevap | 0/30 (`gecersiz` 0), boş cevap 0 |
| 3 | Çağrı gecikmesi | ortanca 1,75 sn · en çok 2,51 sn · en az 1,00 sn · hata ve yeniden deneme 0 |
| 4 | Koşu süresi ve iş (yalnız bilgi) | 51,4 sn, 9 tur, 70 adım, 30 çağrı, iş VAR, takılma 0, durdurma 0, haksız 0, zincir tamam |
| 5 | Kayıtta anahtar izi | yok. Anahtarın ilk 8 karakteri ve tamamı `api_kayit.jsonl`, `api_olcum.jsonl` ve koşu logunda aranmadı bulunmadı. Anahtarın kendisi bu belgeye ve ekrana yazılmadı. |

## Maliyet

Girdi 41.592, çıktı 1.416 jeton. Sürücüdeki fiyat sabitiyle (1 / 6 USD, milyon jeton başına, doğrulanmadı) ≈ 0,050 USD. Gerçek tutar koşuya özel anahtarın hesap sayfasından okunacak, ölçülmedi.

## Karar ve sonraki adım

Tavan kesmesi çıkmadı, `max_completion_tokens` değişmiyor, sürücüde değişiklik yok. Kayıtta dönen model adı `gpt-5.6-luna`. Koşu 4 (tohum 16-25) ve 5a için engel görülmedi. Bu tek koşudan 5a'nın uzun pencere davranışı okunmaz: en çok girdi 2.300 jeton.

Danışman izni gereği başka API çağrısı 6 Kas'a kadar yok.

Dosyalar: `kosular/v4_kosu4_deneme_2kas/` · api_kayit.jsonl f4af33017185f6b9… · api_olcum.jsonl cee6c483c2b21866… · olay kaydı 26181a2263d363f7… · kafa 492fa78c… satir=70 · log `kosular/v4_kosu4_deneme_2kas.log`.
