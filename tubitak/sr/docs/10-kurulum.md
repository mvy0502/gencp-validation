# Kurulum kılavuzu: iki QGIS eklentisi

Bu kılavuz, eklentileri başka bir bilgisayara kuracak kişi için yazılmıştır. Anlatılan her adım,
31 Ağustos 2026'da yayımlanmış zip dosyaları indirilerek, hiçbir şeyin kurulu olmadığı yeni bir
QGIS profilinde sınanmıştır. Sınanmamış her şey, sınanmadığı belirtilerek yazılmıştır.

**Kısaca.** İki eklenti vardır, birbirinden bağımsızdır ve ikisi de aynı yoldan kurulur:
zip dosyası indirilir, QGIS'te **Deneysel eklentileri de göster** kutusu işaretlenir,
**ZIP'ten Kur** ile kurulur. Proje 2 için gereken her dosya tek sürüm sayfasındadır ve toplamı
8,1 MB'tır (§7.1). İnternet erişimi olmayan bir bilgisayara kurulacaksa doğrudan §7'ye
geçilmelidir.

| Eklenti | Ne yapar | Sürüm |
|---|---|---|
| **GenCP Synthetic Reference** (Proje 1) | OpenStreetMap ve arazi örtüsü verisinden sentetik uydu görüntüsü üretir | 0.2.0 |
| **GenCP Super-Resolution** (Proje 2) | Sentinel-2 görüntüsünün çözünürlüğünü artırır | 0.1.0 |

Proje 2, QGIS olmadan komut satırından da çalıştırılabilir ve eklentiyle piksel piksel aynı
çıktıyı üretir: [`20-komut-satiri.md`](20-komut-satiri.md). Bu belgedeki terimler
[`sozluk.md`](sozluk.md) dosyasında sabitlenmiştir.

---

## 1. Ön koşullar

### 1.1 QGIS ve işletim sistemi

| | Sınanan | Durum |
|---|---|---|
| QGIS | **4.2.1 (Belém do Pará)** | Sınanmıştır |
| İşletim sistemi | **macOS** | Sınanmıştır |
| QGIS 3.28 ile 3.x arası | yok | **Sınanmamıştır.** Eklentilerin `metadata.txt` dosyaları en düşük sürüm olarak 3.28 belirtir; bu sürümlerde hiç çalıştırılmamıştır |
| Windows, Linux | yok | **Sınanmamıştır** |

Sınanmamış bir yapılandırmanın çalışacağı taahhüt edilmez. Bu, desteklenmediği anlamına da
gelmez; yalnızca sınanmamıştır.

### 1.2 Python paketleri

Eklentiler QGIS'in **kendi** Python ortamını kullanır. Bilgisayarda ayrıca kurulu bir Python'un
paketleri işe yaramaz; paketlerin QGIS'in içinden içe aktarılabilmesi gerekir.

**Python konsolu**, QGIS'in içinde komut yazılan penceredir; **Eklentiler > Python Konsolu**
menüsünden açılır (İngilizce arayüzde **Plugins > Python Console**). Aşağıdaki satırlar bu
konsola tek tek yapıştırılıp Enter'a basılarak denenmelidir.

| Paket | Hangi eklenti, hangi yöntem için | Kontrol satırı |
|---|---|---|
| `rasterio` | **İki eklentinin her yöntemi için zorunludur** | `import rasterio; print(rasterio.__version__)` |
| `onnxruntime` | Proje 1'in tamamı; Proje 2'de yalnızca model yöntemleri | `import onnxruntime; print(onnxruntime.__version__)` |
| `PyYAML` | Yalnızca Proje 2'nin wsx4 yöntemi | `import yaml; print(yaml.__version__)` |

Bir sürüm numarası yazdırılıyorsa paket vardır; `ModuleNotFoundError` alınıyorsa yoktur.

**Paket eksikken ne olduğu ölçülmüştür.** Aşağıdaki tablo, paketler sınama sırasında QGIS'in
Python ortamından kaldırılarak elde edilmiştir; kaynak kod okunarak değil.

| Eksik paket | Eklenti | Gözlenen sonuç |
|---|---|---|
| `rasterio` | Proje 2 | Eklenti açılırken uyarı verir ve çalışmaz |
| `rasterio` | Proje 1 | Üretim başlarken **Python'un kendi hata iletisi**: `ImportError`, `gencp_core/extent.py` satır 65 |
| `onnxruntime` | Proje 2 | **Eklenti sorunsuz yüklenir; bikübik yöntem çalışır.** Yalnızca model yöntemleri kullanılamaz |
| `onnxruntime` | Proje 1 | Üretim, çıkarım aşamasında **Python'un kendi hata iletisini** verir: `ImportError`, `gencp_core/infer.py` satır 54 |

Proje 1, eksik paket için Türkçe bir ileti üretmez; kullanıcı Python'un kendi hata iletisini
görür. Bu bir bulgudur ve düzeltilmemiştir: eklenti kodu dondurulmuştur.

Proje 2'nin gösterdiği Türkçe iletiler, eklentiden birebir alınmıştır.

`rasterio` eksikken (bu ileti sınama sırasında ekranda görülmüştür):

> **rasterio** paketi bu QGIS kurulumunda yok. Eklenti raster okuyup yazmak için onu kullanır ve onsuz çalışamaz.
>
> QGIS'in Python ortamına `rasterio` kurulmalıdır.

`onnxruntime` eksikken (metin eklentiden alınmıştır; iletinin ekranda belirdiği sınanmamıştır):

> **onnxruntime** paketi bu QGIS kurulumunda yok. Eğitilmiş model bu paketle çalışır.
>
> **Bikübik** yöntemi onsuz da çalışır; model yolu için QGIS'in Python ortamına `onnxruntime` kurulmalıdır.

`PyYAML` eksikken (metin eklentiden alınmıştır; iletinin ekranda belirdiği sınanmamıştır):

> **PyYAML** paketi bu QGIS kurulumunda yok. Eklenti, künye taşımayan modellerin (wsx4 gibi) yapılandırmasını yanındaki .yaml dosyasından okur ve onsuz okuyamaz.
>
> QGIS'in Python ortamına `PyYAML` kurulmalıdır.

---

## 2. Kurulum adımları

**Profil**, QGIS'in ayarlarını ve kurulu eklentilerini sakladığı klasördür. Aşağıdaki adımlar
kullanılan profili değiştirmez; eklenti o sırada açık olan profile kurulur.

### 2.1 İki eklenti için ortak ve atlanamaz adım

İki eklenti de “deneysel” (experimental) olarak işaretlidir. Aşağıdaki kutu işaretlenmeden
eklenti kurulur, fakat listede görünmez; kullanıcı kurulumun başarısız olduğunu sanır.

1. **Eklentiler > Eklentileri Yönet ve Kur** penceresi açılmalıdır (İngilizce arayüzde
   **Plugins > Manage and Install Plugins**).
2. Soldaki **Ayarlar** (**Settings**) sekmesine geçilmelidir.
3. **Deneysel eklentileri de göster** (**Show also experimental plugins**) kutusu
   işaretlenmelidir.

### 2.2 Proje 2: GenCP Super-Resolution

1. Zip dosyası indirilmelidir:
   `https://github.com/mvy0502/gencp-validation/releases/download/sr-plugin-v0.1.0/gencp_super_resolution.zip`
   (49.379 bayt)
2. **Eklentiler > Eklentileri Yönet ve Kur** penceresinde **ZIP'ten Kur** (**Install from
   ZIP**) sekmesine geçilmelidir.
3. **…** düğmesiyle indirilen `gencp_super_resolution.zip` seçilmelidir.
4. **Eklentiyi Kur** (**Install Plugin**) düğmesine basılmalıdır.
5. Eklenti **Raster** menüsünde **GenCP Super-Resolution** adıyla görünmelidir.

### 2.3 Proje 1: GenCP Synthetic Reference

1. Zip dosyası indirilmelidir:
   `https://github.com/mvy0502/gencp-validation/releases/download/plugin-v0.2.0/gencp_plugin.zip`
   (94.987 bayt)
2. Aynı **ZIP'ten Kur** sekmesinden bu dosya seçilip kurulmalıdır.
3. Eklenti **Raster > GenCP > GenCP Synthetic Reference** altında ve araç çubuğunda
   görünmelidir.

> Eklentinin kendi `QUICKSTART.md` dosyasında zip boyutu 73 KB olarak yazılıdır. Yayımlanmış
> dosya 94.987 bayttır; bu belgedeki sayı ölçülmüştür.

---

## 3. Dosyalar tablosu

> İndirme adreslerinin tek doğru kaynağı deponun kök `README.md` dosyasındaki tablodur.
> Aşağıdaki satırlar oradan alınmıştır; bir çelişki olursa `README.md` geçerlidir.

Eklentiler kurulduktan sonra, kullanılacak yönteme göre ek dosyalar gerekir. Hiçbiri zip
dosyasının içinde gelmez.

| Yöntem | Gereken dosya | Nereden indirilir | Nereye konulur |
|---|---|---|---|
| **P2, bikübik** | ek dosya gerekmez | | |
| **P2, eğitilmiş model 2×** | `gencp_sr_x2_v1.onnx` (1.964.122 bayt) | `https://github.com/mvy0502/gencp-validation/releases/download/sr-plugin-v0.1.0/gencp_sr_x2_v1.onnx` | Herhangi bir klasöre; yol eklentinin **Model dosyası** alanından seçilir |
| **P2, eğitilmiş model 4×** | `gencp_sr_x4_b4.onnx` (2.086.466 bayt) | `https://github.com/mvy0502/gencp-validation/releases/download/sr-plugin-v0.1.0/gencp_sr_x4_b4.onnx` | Aynı şekilde |
| **P2, wsx4** | `wsx4_spatrad.onnx` **ve** `wsx4_spatrad.yaml` | `https://github.com/Evoland-Land-Monitoring-Evolution/sentinel2_superresolution` (bu projenin ürünü değildir; sürüm sayfasına eklenmemiştir) | **İkisi aynı klasörde, yan yana.** Eklenti `.yaml` dosyasını modelin yanında arar; ölçek, normalleştirme ve kırpma kenarı oradan okunur |
| **P2, girdi** | Sentinel-2 rasteri, uint16 DN, 10 m | Kullanıcının kendi verisi | Herhangi bir klasör |
| **P1, model** | `gencp_C2_fp32.onnx` (217.678.087 bayt) | `https://github.com/mvy0502/gencp-validation/releases/download/plugin-v0.2.0/gencp_C2_fp32.onnx` | Herhangi bir klasöre; yol eklentinin model alanından seçilir |
| **P1, arazi örtüsü** | `clcplus_2021_turkey_10m.tif` (916.422.550 bayt) | `https://github.com/mvy0502/gencp-validation/releases/download/veri-turkiye-2026-08-31/clcplus_2021_turkey_10m.tif` | Yolu `GENCP_CLC_PATH` ortam değişkeniyle ya da eklentinin ilgili alanından verilir |
| **İkisi için, çevrimdışı Python paketleri** (yalnızca internet erişimi olmayan Windows, Python 3.12) | `gencp_kit_win_amd64_py312.zip` (67.325.080 bayt; 18 tekerlek, Pillow ve PyYAML dâhil), `MANIFEST.json`, `SHA256SUMS.txt` | `https://github.com/mvy0502/gencp-validation/releases/tag/kit-win_amd64-py312-2026-08-31` (hangi paketin hangi eklenti için olduğu sürüm notlarında yazılıdır) | Herhangi bir klasöre açılır; kurulum [`13-cevrimdisi-kurulum.md`](13-cevrimdisi-kurulum.md) |
| **P1, OSM** | `turkey-2026-08-19.osm.pbf` (642.343.710 bayt) | `https://github.com/mvy0502/gencp-validation/releases/download/veri-turkiye-2026-08-31/turkey-2026-08-19.osm.pbf` ya da eklentinin kendi indirme düğmesi | Herhangi bir klasör |

---

## 4. Doğrulama

### 4.1 Eklentiler görünüyor mu

**Eklentiler > Eklentileri Yönet ve Kur > Kurulu** listesinde şu iki satır bulunmalıdır:

- `GenCP Super-Resolution`
- `GenCP Synthetic Reference`

Görünmüyorlarsa §2.1'deki deneysel eklenti kutusu işaretlenmemiştir.

### 4.2 Proje 2: kısa çalıştırma

Ek dosya gerektirmediği için doğrulama **bikübik** yöntemle yapılmalıdır.

1. Bir Sentinel-2 rasteri QGIS'e eklenmelidir.
2. **Raster > GenCP Super-Resolution** açılmalıdır.
3. Yöntem olarak **Bikübik** seçilmelidir. Ölçek seçilmez: **Ölçek katsayısı** satırı bikübik
   yöntemde **4 ×** yazar; bikübik, karşılaştırıldığı 4× modellerle aynı çıktı ızgarasını
   üretmek için 4× çalışır.
4. Bir çıktı yolu verilip **Çalıştır** düğmesine basılmalıdır.

**Beklenen sonuç, sınamada ölçülmüştür.** 256 × 256 piksellik, 3 bantlı, EPSG:32636, 10 m
piksel boylu bir girdiyle:

| | Girdi | Çıktı |
|---|---|---|
| Boyut | 256 × 256 | **1024 × 1024** |
| KRS | EPSG:32636 | **EPSG:32636, değişmez** |
| Piksel boyu | 10 m | **2,5 m** |
| Başlangıç noktası | | **değişmez** |

Kırpılan değer sayısı **0**, kapsanmayan piksel sayısı **0** olmalıdır.

### 4.3 Proje 1: kısa çalıştırma

Model, arazi örtüsü ve OSM dosyaları hazırsa küçük bir alan için üretim çalıştırılmalıdır.

**Sınamada ölçülen:** İstanbul'da yaklaşık 2,6 km × 2,3 km'lik bir alan, tek çekirdek,
**21,7 saniye**; çıktı 258 × 228 piksel, 3 bant, uint8, EPSG:32635; geçerli veri oranı
0,9999; uyarı üretilmemiştir.

---

## 5. Sorun giderme

| Belirti | Olası sebep | Yapılacak işlem |
|---|---|---|
| Eklenti kurulduğu hâlde listede görünmüyor | İki eklenti de deneysel işaretlidir | **Ayarlar** sekmesinde **Deneysel eklentileri de göster** kutusu işaretlenmelidir (§2.1) |
| Eklenti listede görünüyor, fakat açılmıyor | `rasterio` eksiktir (Proje 2) ya da zip dosyası bozuk inmiştir | Python konsolunda `import rasterio` denenmelidir. İndirilen dosyanın boyutu §2'deki bayt sayısıyla karşılaştırılmalıdır |
| `rasterio` bulunamadı | Paket QGIS'in Python ortamında yok | QGIS'in kendi Python ortamına `rasterio` kurulmalıdır. Bilgisayardaki başka bir Python'a kurmak sonucu değiştirmez |
| `onnxruntime` bulunamadı | Paket yok | Proje 2'de bikübik yöntem çalışmaya devam eder; model yöntemleri için paket kurulmalıdır. Proje 1'in tamamı bu pakete bağlıdır ve onsuz üretim yapamaz |
| `PyYAML` bulunamadı | Paket yok | Yalnızca wsx4 için gerekir. Projenin kendi modelleri künyelerini kendi içlerinde taşır ve `PyYAML` olmadan çalışır |
| Model dosyası seçilmemiş | Yöntem model gerektiriyor, alan boş | **Model dosyası** alanından `.onnx` dosyası seçilmelidir. Yeni kurulmuş eklentide bu alan boş gelir; bu beklenen davranıştır |
| Yanlış dosya yanlış yöntemle verilmiş | Örneğin 3 bantlı eski model (`gencp_sr_x2_v1.onnx`), 4 bant bekleyen wsx4 yerine seçilmiş | Girdi ile model eşleştirilmelidir. Beklenen bant sayısı ve ölçek modelin künyesinden okunur; uyuşmazlığı eklenti reddeder. Dağıtılan model `gencp_sr_x4_b4.onnx` (4×) ve wsx4 (4×) 4 bant (B02,B03,B04,B08) ister; eski `gencp_sr_x2_v1.onnx` (2×) 3 bant (B02,B03,B04) ister |
| wsx4 seçildi, fakat çalışmıyor | `.yaml` dosyası modelin yanında değil | `wsx4_spatrad.yaml`, `wsx4_spatrad.onnx` ile **aynı klasöre** konulmalıdır |
| Çıktı yazılamıyor | Hedef klasör yok, yazma izni yok ya da disk dolu | Yazma izni olan bir klasör seçilmelidir. Ağ sürücüleri yerine yerel disk tercih edilmelidir |

---

## 6. Sınanmış ve sınanmamış olanlar

**Ne kadar sürer.** İndirme ve üretim süreleri, ölçüldükleri bilgisayar, ağ ve girdilerle
birlikte [`11-zamanlama.md`](11-zamanlama.md) belgesinde kayıtlıdır. Özet: dört dosyanın
indirilmesi, 1,78 GB için **1,6 dakika** (20 MB/s bağlantıda ölçülmüştür; ağa bağlıdır);
10 × 10 km'lik bir sahnenin **ilk** üretimi, ülke geneli OSM dosyasıyla ve önbellek boşken
**16,6 dakika**; aynı sahnenin yeniden üretimi **1,3 saniye**.

**Sınanmıştır** (31 Ağustos 2026, QGIS 4.2.1 Belém do Pará, macOS):

- İki eklenti de **yayımlanmış zip dosyalarından** indirilmiş ve çalışma ağacına erişimi
  olmayan, yeni oluşturulmuş bir profile kurulmuştur.
- QGIS ikisini de **görmüş, yüklemiş ve başlatmıştır**.
- Proje 2'nin bikübik yöntemi uçtan uca çalışmış, ızgara sözleşmesi tam olarak korunmuştur.
- Proje 1 uçtan uca çalışmış, 21,7 saniyede çıktı üretmiştir.
- `rasterio` ve `onnxruntime` Python ortamından kaldırılarak iki eklentinin davranışı
  ölçülmüştür.

**Sınanmamıştır:**

- QGIS 3.28 ve diğer 3.x sürümleri.
- Windows ve Linux.
- Proje 2'nin **eğitilmiş model** ve **wsx4** yöntemlerinin bu yeni profilde uçtan uca
  çalıştırılması; yalnızca bikübik çalıştırılmıştır.
- `PyYAML` ve `onnxruntime` eksikken Türkçe iletilerin ekranda belirmesi; metinler eklentiden
  birebir alınmıştır, ekrana geldikleri gözlenmemiştir.
- Bu belgedeki adımların Türkçe arayüzlü bir QGIS'te sınanması; sınama İngilizce arayüzde
  yapılmıştır. Menü adlarının İngilizce karşılıkları parantez içinde verilmiştir.

---

## 7. İnternet erişimi olmayan bilgisayarlara kurulum

Kurum bilgisayarlarında internet yoktur. Dosyalar internet erişimi olan başka bir
bilgisayara indirilir, aktarım sistemi üzerinden taşınır ve orada kurulur. Bu bölüm o yolu
anlatır.

### 7.1 Nereden indirilir

Tek adres, sürüm sayfasıdır:
<https://github.com/mvy0502/gencp-validation/releases/tag/sr-plugin-v0.1.0>

**Toplam 8,1 MB.** Aktarım sisteminin boyut sınırı bunun altındaysa dosyalar tek tek
taşınmalıdır; her dosyanın boyutu aşağıda ayrıca verilmiştir.

| Dosya | Boyut | Ne için |
|---|---:|---|
| `gencp_super_resolution.zip` | 49.379 bayt | Eklentinin kendisi |
| `gencp_sr_tci_x4_b3_v2.onnx` | 2.047.228 bayt | 8 bit RGB görüntü için model (4×) |
| `gencp_sr_x4_b4.onnx` | 2.086.466 bayt | 16 bit, dört bantlı görüntü için model (4×) |
| `gencp_sr_x2_v1.onnx` | 1.964.122 bayt | 16 bit, üç bantlı görüntü için model (2×) |
| `SAMPLE_3band_TCI_uint8_10m_512px.tif` | 732.623 bayt | Kurulum doğrulaması için örnek girdi, 8 bit |
| `SAMPLE_4band_B02-B03-B04-B08_uint16_10m_512px.tif` | 1.636.956 bayt | Kurulum doğrulaması için örnek girdi, 16 bit |
| `SHA256SUMS.txt` | 577 bayt | Sağlama toplamları |

**wsx4 model dosyaları bu sürüme dâhil değildir**; bu çalışmanın ürünü değildir. Gerekiyorsa
`wsx4_spatrad.onnx` ve `wsx4_spatrad.yaml` üst kaynaktan birlikte indirilmeli ve **aynı klasöre
yan yana** konulmalıdır. Eklenti `.yaml` dosyasını modelin yanında arar;
ölçek, normalleştirme ve kırpma kenarı oradan okunur. Kaynak:
<https://github.com/Evoland-Land-Monitoring-Evolution/sentinel2_superresolution>

### 7.2 Aktarımdan sonra, kurulumdan önce: sağlama toplamı doğrulanmalıdır

**Bu adım atlanmamalıdır.** Aktarım sisteminden geçen bir dosya bozuk gelebilir; bozuk bir
`.onnx` dosyasının verdiği hata ise aktarım hatasına değil model hatasına benzer. Kaybedilecek
zaman, bu kontrolün süresinin kat kat üstündedir.

`SHA256SUMS.txt` diğer dosyalarla aynı klasöre konulur ve şu satır çalıştırılır:

- **Windows**, her dosya için ayrı ayrı:
  ```
  certutil -hashfile gencp_super_resolution.zip SHA256
  ```
  Çıkan değer, `SHA256SUMS.txt` içindeki satırla karşılaştırılmalıdır.
- **macOS / Linux**, hepsi birden:
  ```
  shasum -a 256 -c SHA256SUMS.txt
  ```

Her satırda **`OK`** yazmalıdır. Bir satırda `FAILED` yazıyorsa o dosya yeniden aktarılmalıdır;
kurulmamalıdır.

### 7.3 Hangi dosya nereye konulur

| Dosya | Nereye |
|---|---|
| `gencp_super_resolution.zip` | Herhangi bir klasöre; QGIS'in **ZIP'ten Kur** penceresinden seçilir. Kurulumdan sonra dosya silinebilir |
| `.onnx` model dosyaları | Kalıcı bir klasöre, örneğin `C:\gencp\models\`. Yol eklentinin **Model dosyası** alanından seçilir; dosya taşınırsa yol yeniden verilmelidir |
| `SAMPLE_*.tif` örnek girdiler | Herhangi bir klasöre; yalnızca doğrulama içindir |
| `wsx4_spatrad.onnx` ve `.yaml` | **İkisi aynı klasörde**, yan yana |

Kurulum adımları §2'de anlatılmıştır. **Deneysel eklentileri de göster** kutusu §2.1'de
anlatıldığı gibi işaretlenmeden eklenti listede görünmez.

### 7.4 Kurulum yalnızca örnek dosyalarla doğrulanır

Kurumun kendi verisine ihtiyaç yoktur; örnek rasterler bunun içindir.

1. `SAMPLE_3band_TCI_uint8_10m_512px.tif` QGIS'e eklenir.
2. **Raster > GenCP Super-Resolution** açılır.
3. Yöntem olarak **Bikübik** seçilir (ölçek seçilmez; satır **4 ×** yazar), bir çıktı yolu
   verilir ve **Çalıştır** düğmesine basılır.

**Beklenen sonuç:** 512 × 512 girdiden **2048 × 2048** çıktı; KRS **EPSG:32636, değişmeden**;
piksel boyu 10 m'den **2,5 m**'ye; başlangıç noktası **değişmeden**. Bu dördü sağlanıyorsa
eklenti çalışıyordur.

Model yolu da sınanacaksa aynı dosyayla yöntem olarak **Eğitilmiş model** (GenCP), model
dosyası olarak `gencp_sr_tci_x4_b3_v2.onnx` seçilir; ölçek satırı modelden okunan **4×** değerini gösterir.
Çıktı **2048 × 2048**, piksel boyu **2,5 m** olmalıdır.

Dört bantlı model ve wsx4 için `SAMPLE_4band_B02-B03-B04-B08_uint16_10m_512px.tif`
kullanılmalıdır.

### 7.5 Yalnızca bikübik çalışıyorsa

**Bu beklenen bir durumdur, arıza değildir.** Bikübik yöntem `onnxruntime` paketini bilerek içe
aktarmaz; böylece o paketin olmadığı bir bilgisayarda eklenti yüklenir ve çalışır. Model
yöntemleri ise o pakete bağlıdır.

Yapılacak işlem, sırasıyla:

1. Ortam raporu çalıştırılır ([`13-cevrimdisi-kurulum.md`](13-cevrimdisi-kurulum.md) §2) ve
   `onnxruntime` satırının **`YOK`** olduğu doğrulanır.
2. `YOK` ise paket, §3'teki çevrimdışı kurulum kitiyle (`kit-win_amd64-py312-2026-08-31`
   sürümündeki `gencp_kit_win_amd64_py312.zip`) kurulur ve **QGIS yeniden başlatılır**.
3. `VAR` görünmesine rağmen model yöntemi çalışmıyorsa, raporun gösterdiği dizin ile
   eklentinin uyarısında adı geçen dizin karşılaştırılmalıdır: paket **yanlış Python ortamına**
   kurulmuş olabilir. Bilgisayarda birden çok QGIS varsa her birinin Python ortamı ayrıdır.
4. Model dosyasının sağlama toplamı §7.2'ye göre yeniden doğrulanmalıdır; bozuk bir model
   dosyası model hatası gibi görünür.

### 7.6 Çalışma sırasında internet gerekmez

Ölçülmüştür: QGIS 4.2.1 ve QGIS 3.44.13 üzerinde, Python düzeyindeki ağ bağlantıları kapatılarak
bikübik yöntem, model çıkarımı ve bir koordinat dönüşümü çalıştırılmış; **ağa hiçbir erişim
girişimi gözlenmemiştir**.

PROJ'un CDN üzerinden datum ızgarası indirme özelliği iki sürümde de öntanımlı olarak
kapalıdır: `PROJ_NETWORK` ortam değişkeni tanımsız, `osr.GetPROJEnableNetwork()` ve
`pyproj.network.is_network_enabled()` **False**.

Eklenti ayrıca hiçbir zaman yeniden projeksiyon yapmaz; ızgara sözleşmesi (Gate S) çıktının
KRS'sinin girdininkine eşit olmasını şart koşar. Bu yüzden olağan bir çalıştırmada datum
ızgarasına zaten gerek yoktur.

Kurum politikası kesinlik istiyorsa, QGIS başlatılmadan önce `PROJ_NETWORK=OFF` ortam
değişkeni tanımlanmalı ya da Python konsolunda şu satır çalıştırılmalıdır:

```python
from osgeo import gdal; gdal.SetConfigOption("PROJ_NETWORK", "NO")
```

`PROJ_NETWORK=ON` iken ağ erişimi olmasa da dönüşümler tamamlanmıştır: PROJ, QGIS ile gelen
yerel ızgaraları kullanır; hata vermez.
