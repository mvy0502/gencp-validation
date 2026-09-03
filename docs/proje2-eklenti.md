# GenCP Super-Resolution (Proje 2): README'nin taşınan özet bölümü

Aşağıdaki metin, kök `README.md` dosyasının Proje 2 bölümüdür ve 3 Eylül 2026'da (WP27) olduğu gibi
buraya taşınmıştır; yalnızca göreli bağlantı yollarının başına `../` eklenmiştir. Proje 2'nin güncel
kılavuzu [tubitak/sr/docs/10-kurulum.md](../tubitak/sr/docs/10-kurulum.md), belgelerinin tamamı
[tubitak/sr/docs/](../tubitak/sr/docs/) altındadır. Aşağıdaki tabloda 8 bit modelin kurumun 8 bit
verisine karşılık geldiği yazar; yayımdaki eklenti sürümü uint8 girdiyi reddettiğinden bu eşleşme
henüz çalıştırılamamaktadır, bkz. [18-depo-tasima.md](../tubitak/sr/docs/18-depo-tasima.md) §19.

---

## Proje 2: Sentinel-2 süper çözünürlük eklentisi

Yukarıdaki eklentiden ayrı, ikinci bir QGIS eklentisi: **Sentinel-2 görüntüsünü süper
çözünürlüğe çıkarır** (2× ya da 4×). Amacı, görüntü eşleştirmeye daha çok ayrıntı vermektir;
georeferanslamadaki anahtar nokta eşleştirmesi böylece **daha çok ve daha iyi konumlanmış yer
kontrol noktası** üretir. Kaynak kod, belgeler ve kurulum kılavuzu `tubitak/sr/` altındadır.
2 Eylül 2026'dan itibaren Proje 2'nin güncel kopyası bu depodadır; nereden geldiği
[`tubitak/sr/SOURCE.md`](../tubitak/sr/SOURCE.md) dosyasında kayıtlıdır.

**İndirme, hepsi bir arada, toplam 8,1 MB:**
**https://github.com/mvy0502/gencp-validation/releases/tag/sr-plugin-v0.1.0**
Eklentinin zip dosyası, üç model, doğrulama için iki örnek raster ve `SHA256SUMS.txt`.
Aktarımdan sonra dosyaların sağlama toplamları bu listeyle karşılaştırılarak doğrulanır.

**Kurulum kılavuzu** (Türkçe, çevrimdışı kurulum dâhil, bu depoda):
[`tubitak/sr/docs/10-kurulum.md`](../tubitak/sr/docs/10-kurulum.md).

**Üç model ve her birinin kurumun hangi verisine karşılık geldiği:**

| Model | Ölçek | Bant | Normalleştirme | Karşılık geldiği veri |
|---|---|---|---|---|
| **`gencp_sr_tci_x4_b3_v2.onnx`** | 4× | 3, `B02,B03,B04` | `DN/255` | **kurumun bugün elindeki 8 bit RGB görüntü** |
| **`gencp_sr_x4_b4.onnx`** | 4× | 4, `+B08` | `DN/10000` | **16 bit yansıtma verisi, geldiğinde** |
| `gencp_sr_x2_v1.onnx` | 2× | 3 | `DN/5000` | önceki 3 bantlı çalışmadan kalmıştır; yeni kullanımda yerini üstteki iki model almıştır |

**Eşleştirme sonucu**, koşullarıyla birlikte: eğitimde hiç kullanılmamış **36SXJ granülünün 1628
çipi** üzerinde, gerçek 10 m Sentinel-2 görüntüsü referans alınarak, **40 m → 10 m** için
ölçülmüştür. 8 bit model, bikübiğin verdiğinin **3,94 katı** kullanılabilir yer kontrol noktası
verir (çip başına 491,3 RANSAC iç noktası; bikübikte 124,6) ve eşleşme hatasını **%40** düşürür
(bikübikte 0,9835 px, modelde 0,5917 px); 1628 çipin **her birinde** daha iyidir
([`13-tci-model-v2.md`](../tubitak/sr/docs/13-tci-model-v2.md) §8). Bu bir bozup geri kazanma
deneyidir: aracın gerçekte kullanıldığı 2,5 m çözünürlükte ölçüm yoktur, çünkü o çözünürlükte
yer gerçeği yoktur.

Eklenti **çevrimdışı çalışır**: QGIS 4.2.1 ve 3.44.13 üzerinde ağ bağlantıları kapatılarak
ölçülmüş, çalışma sırasında **ağa hiçbir erişim girişimi gözlenmemiştir**
([`10-kurulum.md`](../tubitak/sr/docs/10-kurulum.md) §7.6).

