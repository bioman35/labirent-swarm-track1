# Sapma kaydı · EK5a tekrar · çıktı tavanı 400 → 2000 · 7 Kasım 2026 · defter 26

EK5a sapma sonrası tekrar, çıktı tavanı 400 → 2000. Turan kararı 7 Kas öğleden sonra (danışmana): "ek5a 2000 tekrar yaparız dostum".

EK5a kilitli sonucu (tavan 400, 230/300 cevapsız, DANISMAN_EK5A_SONUC_7KAS.md) DEĞİŞMEZ ve raporda kalır; bu tekrar "sapma sonrası tekrar" etiketiyle yanına yazılır. Aynı 300 özet (luna/ozet), aynı soru (luna/soru.txt), aynı sıra k0001 → k0300, tek çağrı, tekrar yok; kilitli tahminler (defter, TAHMIN_KILIDI_EK5A_LUNA_31eki.md) bilgi olarak aynı ölçülerle uygulanır. Değişen yalnız max_completion_tokens 400 → 2000. Tavan 10 USD. Defter 26.

Bu kayıt EK5a-2'ye hiç çağrı gitmeden önce yazıldı.

Uygulama: luna_yargic.py (779da09455ed534a) değişmedi, kosu_api.py (239a5c0f…) değişmedi. Komut: `python -I luna_yargic.py --asama ek5a --tavan 2000 --klasor cevap_ek5a_2000`, çıktı luna/cevap_ek5a_2000/. luna/cevap_ek5a (kilitli geçiş) dokunulmaz.
