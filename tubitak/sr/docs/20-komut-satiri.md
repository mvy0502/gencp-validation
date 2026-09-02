# Komut satırı aracı: `sr_cli.py`

Proje 2'nin süper çözünürlük işlemi QGIS olmadan, bir terminalden de çalıştırılabilir.
`tubitak/sr/tools/sr_cli.py` bir girdi GeoTIFF alır ve süper çözünürlüklü bir GeoTIFF yazar.
Araç yalnızca bir sarmalayıcıdır: eklentinin çalıştırdığı kodun aynısını
(`sr_core.run.superresolve` ve `sr_plugin.onnx_upsample`) içe aktarır ve çağırır; kendi içinde
süper çözünürlük aritmetiği yoktur. Bu yüzden çıktısı eklentininkiyle **piksel piksel aynıdır**.
Bu özdeşlik kod paylaşımından çıkarılmamış, ölçülmüştür (aşağıda). Terimler
[`sozluk.md`](sozluk.md) dosyasında sabitlenmiştir.

Gereksinimler eklentininkilerle aynıdır: Python 3, `numpy`, `Pillow`, `rasterio`; model
yöntemleri için `onnxruntime`; wsx4 için ayrıca `PyYAML`. Araç ağa hiçbir zaman erişmez;
yalnızca verilen yerel dosyaları okur ve yazar.

## Kullanım

Bikübik yöntem (model gerekmez; eklentinin bikübik ölçeği 4×):

```bash
python tubitak/sr/tools/sr_cli.py girdi.tif cikti.tif
```

Eğitilmiş model (ölçek, bant sayısı, normalleştirme ve karo düzeni modelin künyesinden
okunur):

```bash
python tubitak/sr/tools/sr_cli.py girdi.tif cikti.tif --method model --model gencp_sr_x4_b4.onnx
```

Yazmadan önce, yazılacak ızgarayı görmek için:

```bash
python tubitak/sr/tools/sr_cli.py girdi.tif cikti.tif --method model --model gencp_sr_x4_b4.onnx --dry-run
```

`--help` bütün seçenekleri ve çıkış kodlarını listeler. Her seçeneğin varsayılanı eklentinin
varsayılanıdır: karo 512 kaynak pikseli; bindirme 32 kaynak pikseli (model yolunda modelin
bildirdiği değer); birleştirme bikübik ve eğitilmiş modellerde yumuşak geçişli (`feather`),
wsx4'te kırpmalı (`crop`). `--overlap` metre cinsinden verilir ve kaynak pikselinin tam katı
olmalıdır. `--blend`, eklentinin kuralından ayrılmak içindir; ayrılınca uyarı basılır.

## Neyi reddeder, neden

Araç, çıktı ızgarasının kaynak ızgarasına **tam** oturmasını şart koşar: aynı KRS, piksel boyu
tam olarak kaynağınkinin ölçeğe bölümü, aynı başlangıç noktası, boyut tam olarak ölçek çarpı
kaynak (ızgara sözleşmesi, Gate S). Bu koşulu hem yazmadan önce hesaplayarak denetler hem de
yazdıktan sonra dosyada yeniden doğrular. Koşulu sağlayamayacak bir girdi yeniden projeksiyon ya
da yeniden örnekleme ile uydurulmaz; açık bir iletiyle ve ayrı bir çıkış koduyla reddedilir:

| Durum | Çıkış kodu |
|---|---|
| Girdi yok ya da raster olarak açılamıyor | 3 |
| Girdinin KRS'si yok | 4 |
| Girdi kuzeye dönük değil (döndürülmüş ya da eğilmiş) ya da piksel boyu sıfır | 5 |
| Bant sayısı modelin beklediği sayı değil | 6 |
| Veri tipi desteklenmiyor (model yolunda uint16 dışı; 8 bit TCI modele verilmez) | 7 |
| Model dosyası yok, okunamıyor ya da künyesiz | 8 |
| Çıktı zaten var ve `--overwrite` verilmemiş | 9 |
| Çıktı yolu girdiyle aynı | 10 |
| Bindirme kaynak pikselinin tam katı değil ya da kırpmalı birleştirme için yetersiz | 11 |
| `onnxruntime` yok / `rasterio` yok | 12 / 13 |
| Yazma başarısız ya da durduruldu | 14 |
| Ölçek ikinin kuvveti değil ya da modelinkiyle çelişiyor | 15 |
| Yazılan dosya ızgara sözleşmesini sağlamadı | 16 |

Çıktı önce aynı klasörde geçici bir dosyaya yazılır, sonra adı değiştirilir; durdurulan ya da
başarısız olan bir çalıştırma yarım dosya bırakmaz. Künye etiketi (`GENCP_SR_PROVENANCE`)
eklentininkiyle aynı mekanizmayla ve aynı içerikle yazılır.

## Eklentiyle özdeşlik

Araç, projenin kayıtlı her piksel özetinin girdisi üzerinde çalıştırılmış ve çıktısının piksel
özeti (SHA-256) kayıtlı değere **eşit** çıkmıştır; tolerans yoktur. Referanslar: bikübik 2× tam
granül (`ca3b4c41…`), bikübik 2× 1024 px kesit (`41b54b77…`), eğitilmiş 2× model (`5e3de3cf…`),
wsx4 (`6b71d037…`); ayrıca eklentinin 2 Eylül 2026'da QGIS içinde kendi görevinden ürettiği
bikübik 4× (`6cd62c38…`) ve `gencp_sr_x4_b4.onnx` (`c4794d79…`) çıktıları. Kanıt:
`tubitak/sr/tests/sr_cli_tests.py --all` (özdeşlik 12/12, bilinen-yanlış 17/17) ve
`18-depo-tasima.md` §16.
