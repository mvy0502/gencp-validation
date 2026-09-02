# Sözlük

Proje 2'nin kurum için yazılan her belgesinde her kavram tek bir terimle anılır. Bu liste o
terimleri sabitler. Sol sütundaki terim kullanılır; “yerine geçtiği biçimler” sütunundakiler
eski belgelerde görülen ve artık kullanılmayan karşılıklardır. İngilizce sütunu yalnızca bir
geliştiricinin kodla eşleştirmesi içindir. Dosya adları, etiketler, komut seçenekleri ve
QGIS menü adları terim değildir; oldukları gibi yazılır.

Seçim kuralı: belgelerde zaten baskın olan terim korunmuştur. Baskın terim yanlış ya da
kararsızsa değiştirilmiş ve nedeni son sütunda verilmiştir.

| Terim | Yerine geçtiği biçimler | İngilizce | Not |
|---|---|---|---|
| eklenti | plugin | plugin | Ürün adları (`GenCP Super-Resolution`, `GenCP Synthetic Reference`) QGIS menüsünde göründükleri gibi kalır |
| süper çözünürlük | super-resolution, süper-çözünürlük | super-resolution | Ürün adı dışında her yerde |
| sürüm, sürüm sayfası, sürüm notları | release, release sayfası | release, release page, release notes | |
| sağlama toplamı | sağlama, checksum, özet (dosya için) | checksum | Algoritma adı `SHA-256` olduğu gibi yazılır |
| piksel özeti | pixel hash, piksel SHA | pixel hash | Dosyanın değil piksel içeriğinin SHA-256'sı; sağlama toplamından ayrı tutulur |
| tekerlek | wheel, `.whl` dosyası | wheel | Dosya uzantısı olarak `.whl` kalır |
| çevrimdışı kurulum kiti, kit | tekerlek kiti, offline kit | offline kit | |
| çevrimdışı | internetsiz, ağsız, offline | offline | “İnternet erişimi olmayan makine” yalnızca kavram ilk açıklanırken |
| QGIS'in kendi Python ortamı | QGIS Python'u, QGIS'in yorumlayıcısı | QGIS's own Python | Dizin adı `site-packages` olduğu gibi |
| Python konsolu | Python Console | Python console | QGIS menü adı İngilizce arayüzde `Python Console` |
| ortam raporu | environment report | environment report | `qgis_ortam_raporu.py` betiğinin çıktısı |
| deneysel eklenti | experimental plugin | experimental plugin | QGIS kutusunun adı: **Deneysel eklentileri de göster** |
| profil | profile | QGIS profile | |
| künye | provenance, metadata, üstveri | model provenance / metadata | Modelin kendi içinde taşıdığı bilgi: ölçek, bant sırası, normalleştirme |
| yan dosya | sidecar | sidecar (`.yaml`) | wsx4'ün künyesini taşıyan `.yaml` |
| yöntem | method | method | Eklentideki üç seçenek: bikübik, eğitilmiş model, referans model (wsx4) |
| bikübik | bicubic | bicubic | |
| eğitilmiş model | GenCP SR, GenCP modeli, model yöntemi | trained model | Eklentideki kutu adı `Eğitilmiş model` |
| referans model (wsx4) | wsx4 modeli, Evoland modeli | reference model | |
| ölçek katsayısı, ölçek | ölçek faktörü, kat | scale factor | Sayı biçimi: `4×`, `2×` |
| ızgara sözleşmesi (Gate S) | grid contract, Gate S | grid contract | `Gate S` kapının adıdır, çevrilmez |
| KRS | CRS, koordinat sistemi | coordinate reference system | QGIS'in Türkçe arayüzündeki kısaltma |
| başlangıç noktası | origin, orijin | origin | Rasterın sol üst köşesinin koordinatı |
| piksel boyu | piksel boyutu, GSD, çözünürlük (piksel için) | pixel size | “Çözünürlük” genel anlamda kalır |
| bant | band, kanal | band | |
| veri tipi | dtype | data type | Değerler olduğu gibi: `uint8`, `uint16` |
| yansıtma verisi | yansıtım, reflectance | reflectance | 16 bit DN cinsinden Sentinel-2 bantları |
| normalleştirme | normalizasyon, normalisation | normalisation | Bölen olduğu gibi: `DN/10000` |
| karo | tile | tile | |
| karo bindirmesi, bindirme | overlap | overlap | Kaynak pikseli cinsinden |
| karo birleştirme | blend, harmanlama | blending | İki düzen: yumuşak geçişli, kırpmalı |
| yumuşak geçişli birleştirme | feather | feather blending | Komut satırında seçenek adı `feather` kalır |
| kırpmalı birleştirme | crop | crop tiling | Seçenek adı `crop` kalır |
| kırpma kenarı | kenar payı, kenar, margin | crop margin | Çıktı pikseli cinsinden |
| kuru çalıştırma | dry run | dry run | Seçenek adı `--dry-run` |
| çalıştırma | koşu, run | run | “Koşu” yalnızca araştırma kayıtlarında |
| doğrulama | verification | verification | Kurulumun ya da aktarımın doğru olduğunun gösterilmesi |
| sınanmıştır / sınanmamıştır | test edilmiştir, denenmiştir | tested / untested | Belgelerdeki “ne ölçüldü” ayrımı |
| aktarım | transfer | transfer | Kurumun dosya aktarım sistemi üzerinden taşıma |
| indirme | download | download | |
| örnek raster | sample raster, SAMPLE dosyası | sample raster | `SAMPLE_*.tif` dosyaları |
| model dosyası | ağırlık dosyası, `.onnx` | model file | |
| yer kontrol noktası | kontrol noktası, GCP | ground control point | |
| granül | granule, sahne | granule | Sentinel-2 karesi, örneğin `36SXJ` |
| çip | chip | chip | Ölçüm için kesilmiş küçük görüntü parçası |
| iç nokta | inlier | inlier | RANSAC sayımlarında |
| uçtan uca | end-to-end | end-to-end | |
| bilinen-yanlış, bilinen-doğru | known-false, known-true | known-false, known-true | Sınama düzeninin iki ucu |
| komut satırı aracı | CLI, komut satırı arayüzü | command line tool | Dosya adı `sr_cli.py` |
| çıkış kodu | exit code, dönüş kodu | exit code | |
| kapsam | extent | extent | |
| geçerli veri | valid data | valid data | |

Yazım kuralları, terimlerden bağımsız olarak: ondalık ayırıcı virgüldür (2,5 m), binlik
ayırıcı noktadır (49.379 bayt); özel adlara ve tanımlayıcılara gelen ekler kesme imiyle
ayrılır (QGIS'in, `rasterio`'nun); tırnak olarak “ ” kullanılır; uzun çizgi (U+2014) ve emoji
kullanılmaz; tanımlayıcılar ve komutlar kendi biçimlerini korur.
