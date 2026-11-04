# Oyun alanı v4 · okuma notu

Bu klasör labirentli kurye dünyasının v4 sürümüdür. Kilitler, tahminler ve sonuç özetleri `../oyun_alani_v3/KILIT_DEFTERI.jsonl` zincirindedir.

## Sıcaklık 0 kuralı

Sıcaklık 0 sonuçları aynı sırayla ve tek Ollama sürecinde tekrar edilir. Aynı sıra birebir aynı sonucu verir. Tohum tek başına koşulursa sonuç değişebilir: Qwen 3B tohum 7 tek başına işi bitirdi, tohum 6'dan sonra koşulunca bitiremedi.

Tek tohum "model yapamaz" kanıtı değildir.

Sıra etkisi Python sürecinde değildir: tohum 7 ayrı süreçte de, model durdurulmadıysa aynı kaldı. `ollama stop` sonrası soğuk sonuç birebir geri geldi (Gece 3, K2 kol b, tek tohum). Sebep ölçülmedi. Yeniden koşarken aynı sırayı ve aynı durdurma düzenini koruyun.
