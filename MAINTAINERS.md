# Bakım kuralları

Bu dosya deponun bakımını yapan kişiler içindir. Aşağıdaki kural, kök `README.md` dosyasından 3 Eylül
2026'da (WP27) olduğu gibi taşınmıştır; ajanlar aynı kuralı `CLAUDE.md` dosyasında okur. Kuralın
gerekçesi ve tarihçesi [tubitak/sr/docs/18-depo-tasima.md](tubitak/sr/docs/18-depo-tasima.md)
dosyasındadır.

---

## KURAL: BU DEPO VE GenCP KALICI OLARAK AYRILDI

**Hiçbir yönde, hiçbir zaman birleştirme yapılmaz.** Bu bir uyarı değil, kuraldır.

Bu depo (**gencp-validation**) araştırma kaydıdır: ön kayıtlar, sonuçlar, denetimler, kanıt
dosyaları ve düzeltme kaydı. Fork ve **Proje 1** QGIS eklenti iş paketi, GenCP modelinden
türedikleri için [mvy0502/GenCP](https://github.com/mvy0502/GenCP) deposunda `tubitak-tr`
dalında devam eder. **Proje 2** (süper çözünürlük, `tubitak/sr/`) bu depodadır; fork'taki
kopyası dondurulmuştur. Makale çalışması `mvy0502/gencp-letter` deposundadır; **o depo özeldir**
ve dışarıdan bir ziyaretçiye 404 döndürdüğü için bağlantı verilmemiştir.

- **`tubitak-tr` bu depoya birleştirilmez.** GenCP'deki `b815b46` commit'i 263 dosyayı siler;
  o dal buraya birleştirilirse silme buraya yayılır ve **araştırma kaydını yok eder**.
- **Ters yön de kapalıdır.** Bu deponun `main` dalı GenCP'ye birleştirilmez.
- **Bekleyen tek tamamlayıcı aktarım `cherry-pick` ile yapılır**, birleştirmeyle değil. Eşitleme
  noktası `844dbec`; oraya kadar her şey buradadır (birleştirme `f9e0de6`, ardından kanıt
  rasterları `284571b`).
- **O aktarımdan sonra eşitleme KAPANIR.** İki depo bir daha birleşmez.

Geçmiş yeniden yazılmamıştır ve yazılmayacaktır: iki depo `96503b7` birleşme tabanından itibaren
aynı geçmişi paylaşır; bu yüzden araştırma kaydında anılan 49 commit SHA'sının hepsi iki depoda
da çözümlenir. `filter-repo` hiç kullanılmamıştır ve kullanılmayacaktır.

