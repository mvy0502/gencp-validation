# Komut satırı aracı — `sr_cli.py`

Proje 2'nin süper çözünürlük işlemi QGIS olmadan, bir terminalden de çalıştırılabilir.
`tubitak/sr/tools/sr_cli.py` bir girdi GeoTIFF alır ve süper çözünürlüklü GeoTIFF yazar.
Araç ince bir kabuktur: eklentinin çalıştırdığı kodun aynısını (`sr_core.run.superresolve`
ve `sr_plugin.onnx_upsample`) içe aktarır ve çağırır; kendi içinde süper çözünürlük
aritmetiği yoktur. Bu yüzden çıktısı eklentininkiyle **piksel piksel aynıdır**; bu, kod
paylaşımından çıkarılmamış, ölçülmüştür (aşağıda).

Gereksinimler eklentininkilerle aynıdır: Python 3, `numpy`, `Pillow`, `rasterio`; model
yolu için `onnxruntime`; wsx4 için ayrıca `PyYAML`. Araç ağa hiçbir zaman erişmez: yalnızca
verilen yerel dosyaları okur ve yazar.

## Kullanım

Bikübik (model gerekmez; eklentinin bikübik ölçeği 4×):

```bash
python tubitak/sr/tools/sr_cli.py girdi.tif cikti.tif
```

Eğitilmiş model (ölçek, bant sayısı, normalleştirme ve karo düzeni modelin kendi
künyesinden okunur):

```bash
python tubitak/sr/tools/sr_cli.py girdi.tif cikti.tif --method model --model gencp_sr_x4_b4.onnx
```

Yazmadan önce, yazılacak ızgarayı görmek için:

```bash
python tubitak/sr/tools/sr_cli.py girdi.tif cikti.tif --method model --model gencp_sr_x4_b4.onnx --dry-run
```

`--help` bütün seçenekleri ve çıkış kodlarını listeler. Varsayılanların her biri eklentinin
varsayılanıdır: karo 512 kaynak pikseli, bindirme 32 kaynak pikseli (model yolunda modelin
bildirdiği değer), birleştirme bikübik ve GenCP modellerinde yumuşak geçişli (feather),
wsx4'te kırpmalı (crop). `--overlap` metre alır ve kaynak pikselinin tam katı olmalıdır;
`--blend` eklentinin kuralından ayrılmak içindir ve ayrılınca uyarı basılır.

## Neyi reddeder ve neden

Araç, çıktının kaynağın ızgarasının **tam** incelmesi olmasını (Gate S: aynı KRS, piksel boyu
tam olarak kaynak/ölçek, aynı başlangıç noktası, boyut tam olarak ölçek × kaynak) hem yazmadan
önce öngörür hem de yazdıktan sonra dosyada yeniden doğrular. Bunu sağlayamayacak bir girdi
yeniden projeksiyon ya da yeniden örnekleme ile uydurulmaz; açık bir mesaj ve ayrı bir çıkış
koduyla reddedilir:

| Durum | Çıkış kodu |
|---|---|
| Girdi yok ya da raster olarak açılamıyor | 3 |
| Girdinin KRS'si yok | 4 |
| Girdi kuzeye dönük değil (döndürülmüş/eğilmiş) ya da piksel boyu sıfır | 5 |
| Bant sayısı modelin beklediği değil | 6 |
| Veri tipi desteklenmiyor (model yolunda uint16 dışı; 8 bit TCI modele verilmez) | 7 |
| Model dosyası yok, okunamıyor ya da künyesiz | 8 |
| Çıktı zaten var ve `--overwrite` verilmemiş | 9 |
| Çıktı yolu girdiyle aynı | 10 |
| Bindirme kaynak pikselinin tam katı değil ya da kırpmalı birleştirme için yetersiz | 11 |
| `onnxruntime` / `rasterio` yok | 12 / 13 |
| Yazma başarısız ya da durduruldu | 14 |
| Ölçek ikinin kuvveti değil ya da modelinkiyle çelişiyor | 15 |
| Yazılan dosya Gate S'i sağlamadı | 16 |

Çıktı önce aynı klasörde geçici bir dosyaya yazılır, sonra adı değiştirilir; durdurulan ya
da başarısız olan bir çalıştırma yarım dosya bırakmaz. Provenance etiketi
(`GENCP_SR_PROVENANCE`) eklentininkiyle aynı mekanizmayla, aynı içerikle yazılır.

## Eklentiyle özdeşlik

Araç, projenin kayıtlı her piksel özetinin girdisi üzerinde çalıştırılmış ve çıktısının
piksel SHA-256'sı kayıtlı değere **eşit** çıkmıştır (tolerans yok): bikübik 2× tam granül
(`ca3b4c41…`), bikübik 2× 1024 px kesit (`41b54b77…`), GenCP 2× modeli (`5e3de3cf…`), wsx4
(`6b71d037…`); ayrıca eklentinin 2 Eylül 2026'da QGIS içinde kendi görevinden ürettiği
bikübik 4× (`6cd62c38…`) ve `gencp_sr_x4_b4.onnx` (`c4794d79…`) çıktılarıyla. Kanıt:
`tubitak/sr/tests/sr_cli_tests.py --all` (12/12 özdeşlik, 17/17 bilinen-yanlış) ve
`18-depo-tasima.md` §16.
