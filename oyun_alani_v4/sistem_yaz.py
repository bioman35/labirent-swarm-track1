# coding: utf-8
"""SISTEM_MESAJI_v3.md uretir · model ajaninin gordugu metin ve uc ogretme kolu, suruculer.py sabitlerinden.
Kodla tutarsiz olamaz. Kosu 1'den ONCE dondurulur; ozeti kosu_meta.json'a yazilir.
Calistir: python -I sistem_yaz.py  -> SISTEM_MESAJI_v3.md + SISTEM_MESAJI_v3.sha256"""
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kartlar as K  # noqa: E402
import suruculer as S  # noqa: E402

KOK = os.path.dirname(os.path.abspath(__file__))
AD = "SISTEM_MESAJI_v4"


def metin():
    s = []
    a = s.append
    a("# Model ajanının sistem mesajı ve öğretme kolları v4 (dondurulmuş; KİLİTTEN SONRA, KEŞİF)\n")
    a("v4'te modelin gördüğü hiçbir metin değişmedi: kodon ve antikodon yalnız kapıdadır, ajan görmez "
      "(DEGISIKLIK_v4_GENETIK_28eki madde 1). Aşağıdaki metin v3.4 ile aynıdır; yalnız dayanak dosyası ve koşu bölümü v4.\n")
    a("Labirent oyun alanı v4 · 28 Ekim 2026 · Hikayeci · DEGISIKLIK_v3_1, v3_2, v3_3 + O2b v5 + v4 genetik kapı · dayanak: %s (%s), "
      "KARAKTER_KARTLARI_v2_27eki.md (%s)\n" % (K.KURAL_DOSYA, K.KURAL_OZET[:16], K.KART_OZET[:16]))
    a("## 1. Sistem mesajı (bu sırayla, satır satır)\n")
    a("1. Dünya metni:\n\n> %s\n" % S.DUNYA)
    a("2. Yalnız O1 kolunda, örnek cevaplar:\n\n> %s\n" % S.O1_ORNEK)
    a("3. \"Görevin: \" + rolün görev cümlesi (kurallar §11; dünyadan, ilk gözlemden alınır).")
    a("4. Yalnız sinsi ajanlarda hedef cümlesi (dünyadan).")
    a("5. \"Karakterin: \" + kart metni (danışman, aynen).")
    a("6. Cevap kalıbı:\n\n> %s\n" % S.KALIP)
    a("## 2. Her tur\n")
    a("- Kullanıcı mesajı: \"Gözlem: \" + gözlemin JSON hali (boş alanlar atılır; görev ve hedef sistem mesajında "
      "olduğu için gözlemden çıkarılır).")
    a("- Son 6 gözlem ve cevap geçmiş olarak mesajlara girer (bütün koşullarda aynı).")
    a("- Cevap geçerli JSON değilse bir kez \"Bu geçerli JSON değil.\" + kalıp ile yeniden sorulur; yine bozuksa "
      "eylem \"gecersiz\" olur (dünya \"bu eylem burada çalışmaz\" der).")
    a("- Başajan ve teslim başajan yerinden kalkmaz: adaylar listesi boşken (önerecek bir şey yokken) modele "
      "sorulmaz, ajan bekler. Kayıtta \"uyandırılmadı\" diye görünür. Bu bir koşum kuralıdır, bütün koşullarda aynı.")
    a("- Kapının uyarıları (v3.1, \"Zarf sende değil…\", \"Çantanda zarf yok…\") öğretme kolu değildir; dünyanın kapı "
      "mesajıdır, gözlemde karar UYARI ve sebep olarak bütün koşullarda gelir.")
    a("- Yalnız O2b kolunda (O2b v5): geri alınamaz eylem iki adım ister. Model zarf çantadayken \"bitir\" derse "
      "koşum katmanı bir kez \"İpucu: %s Kararını yeniden ver.\" diye sorar." % S.O2B_BITIR)
    a("- Yalnız O2b kolunda (v3.2): başajan kutu dolu ve aday varken üst üste %d tur bekle derse gözleme ipucu: "
      "\"%s\" (gözlemi yeniden söyler). Kayıtta sayılır (basajan_ipucu)." % (S.O2B_BASAJAN_BEKLE, S.O2B_BASAJAN))
    a("- Yalnız O2b kolunda (O2b v5): model çantadaki mühürlü zarf için \"zarf_ac\" derse koşum katmanı bir kez "
      "\"İpucu: %s Kararını yeniden ver.\" diye sorar." % S.O2B_ZARF_AC)
    a("- O2b v5 kuralı (danışman 27 Eki): bitir ve zarf_ac, geri alınamaz eylemlerin her biri bir karar içinde kendi "
      "sorusunu bir kez alır; biri diğerinin cevabı olarak gelse bile (ör. bitir sorusuna zarf_ac cevabı, zarf_ac sorusunu "
      "da alır). Aynı tür ikinci kez sorulmaz; son cevap kesindir, karar modelindir. Her soru kayda \"soru\" olayı "
      "olarak yazılır: tür, soru metni, ilk cevap, ikinci cevap (çıkarım değil kayıt).")
    a("- v3.2 dünya değişiklikleri (labirent levhası, gezilen odalar, geçerli eylem listesi, hareketsiz_tur, "
      "başajanın sade gözlemi) öğretme kolu değildir; bütün koşullarda aynıdır (kurallar dosyası).\n")
    a("## 3. Öğretme kolları (%s)\n" % S.KOL_SURUMU)
    a("Öğretme bütün modellere ortak koşum katmanındadır: kart değişmez, dünya ve kapı değişmez; kapı atlatma yöntemi "
      "öğretilmez; doğru cevap söylenmez. Turan'ın ilkesi: cevabı söyleme, keşfi tasarla, iskele kur.\n")
    a("| kol | ad | ne eklenir |\n|---|---|---|")
    a("| O1 | örnek | sistem mesajına her eylemin doğru JSON biçimi (yukarıda 2. satır); değerleri ajan kendi gözleminden alır |")
    a("| O2 | anlam | kapı durdurunca ya da uyarı gelince gözleme \"ipucu\" alanı: sebebin ne demek olduğu ve neyin "
      "düzeltileceği (aşağıdaki tablo) |")
    a("| O2b | anlam, ek | (v3.1, O2 ile birlikte) çıkışta anahtarsız anahtar_kullan için ayrı ipucu; zarf çantadayken "
      "bitir denince bir kez hatırlatma (yukarıda §2) |")
    a("")
    a("O3 (defter) v3.1'de çıkarıldı: v3.0 Koşu 1'de 0/5, 13 takılma (KOSU1_SONUC_27eki.md). Kolları Hikayeci 27 Eki'de "
      "tanımladı; raporda \"koşum katmanı, sprint öncesi, Hikayeci\" diye geçer.")
    a("")
    a("O2 ipuçları (sebep ya da uyarı bu sözle başlarsa):\n")
    a("| sebep / uyarı | ipucu |\n|---|---|")
    for bas, cumle in S.O2_IPUCU:
        a("| %s | %s |" % (bas, cumle))
    a("| (O2b) çıkışta, elinde anahtar yokken \"bu eylem burada çalışmaz\" | %s |" % S.O2B_CIKIS)
    a("")
    a("## 4. Koşu 1 ve 2 (v4)\n")
    a("- v4 tohumları 16-25 (yeni); önce Koşu 1, sonra Koşu 2; tahmin kilidi ek kaydından sonra. Aşağıdaki satırlar "
      "v3.4'ten aynen kalan kurulum bilgisidir.")
    a("- Yalnız bizim kartlar (kart dosyası dağılımı): T1-T3 G1, G2, G3 tohuma göre karışık; başajan B1 ya da B2 "
      "tohuma göre; teslim başajan B1. Bir tohumda dağılım bütün koşullarda aynı.")
    a("- Koşullar: %s (O1_O2b = O1 + O2 + O2b; Koşu 2'nin koşulu). Tohum 1-5, her koşul ve tohumda bir koşu: 10 koşu." %
      ", ".join(S.KOSULLAR))
    a("- Model: Ollama qwen2.5:7b-instruct-q4_K_M (özet kayda yazılır), sıcaklık 0, model tohumu (dünya tohumu, "
      "ajan sırası)'ndan türetilir, bağlam 4096, cevap en çok 200 token.")
    a("- Koşu 2 ve 4'te sıcaklık 0,7 ve kayıtlı model tohumu (DEGISIKLIK v3.1 §5).")
    a("- Deneme koşusu yok. Koşular yayın ve Unreal kapalıyken. Sonuçlar gelince tahmin kilidi Turan ve danışmanla yazılır.")
    return "\n".join(s) + "\n"


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    m = metin()
    with open(os.path.join(KOK, AD + ".md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(m)
    oz = hashlib.sha256(m.encode("utf-8")).hexdigest()
    with open(os.path.join(KOK, AD + ".sha256"), "w", encoding="utf-8", newline="\n") as f:
        f.write("%s  %s.md\n" % (oz, AD))
    print(oz, len(m), "karakter")
