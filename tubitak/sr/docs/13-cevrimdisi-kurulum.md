# Çevrimdışı kurulum kiti: internet erişimi olmayan Windows bilgisayarları için

Bu belge, internet erişimi olmayan bir Windows bilgisayarında QGIS eklentilerinin ihtiyaç
duyduğu Python paketlerinin nasıl kurulacağını anlatır. Komut satırı bilgisi gerektirmez;
her adım birebir uygulanacak biçimde yazılmıştır. Terimler [`sozluk.md`](sozluk.md)
dosyasında sabitlenmiştir.

**Kısaca.** Kit, sürüm sayfasından indirilen tek bir zip dosyasıdır. Bilgisayara kopyalanır,
açılır, önce ortam raporuyla hangi paketlerin eksik olduğu ölçülür (§2), sonra tek satırlık
bir komutla eksik paketler QGIS'in kendi Python ortamına kurulur (§3), QGIS yeniden başlatılır
ve rapor yeniden çalıştırılarak kurulum doğrulanır (§4).

## 1. Kitin içinde ne var

Zip dosyası açıldığında bir `MANIFEST.json` ve içinde **18 tekerlek (`.whl`)** bulunan bir
`wheels` klasörü elde edilir; toplam **64,7 MB**. 2 Eylül 2026'da Proje 2 için `Pillow` ve
`PyYAML` eklenmiştir; ilk 16 tekerlek değişmemiştir. Kit, bu deponun
`kit-win_amd64-py312-2026-08-31` sürümünde `gencp_kit_win_amd64_py312.zip` adıyla
yayımlanmıştır:
`https://github.com/mvy0502/gencp-validation/releases/tag/kit-win_amd64-py312-2026-08-31`. Sürüm
notları hangi paketin hangi eklenti için olduğunu ve kitin **neyi kapsamadığını** listeler. Her
tekerleğin sürümü ve SHA-256 sağlama toplamı `MANIFEST.json` içinde kayıtlıdır; kurulan
dosyaların sınanan dosyalarla aynı olduğu bu listeyle gösterilebilir.

| Paket | Sürüm | Boyut |
|---|---|---|
| `rasterio` | 1.5.1 | 29,2 MB |
| `onnxruntime` | 1.29.0 | 13,4 MB |
| `osmium` | 4.3.1 | 1,7 MB |
| `Pillow` (yalnızca Proje 2; her yöntem) | 12.3.0 | 6,9 MB |
| `PyYAML` (yalnızca Proje 2; `.yaml` künyeli modeller) | 6.0.3 | 0,15 MB |
| bağımlılıklar (numpy, protobuf, requests ve diğerleri) | 13 dosya | 13,3 MB |

Windows QGIS'in `rasterio`'yu zaten getiriyor olma ihtimaline rağmen bu paket bilerek kite
alınmıştır. `pip`, karşılanmış olan paketi atlar; 1,78 GB'lık veri yükünün yanında bu birkaç on
megabaytın maliyeti yoktur. Kit küçültülmeye çalışılmamıştır.

Hedef: **Windows 64 bit, Python 3.12 (cp312)**. Başka bir Python sürümü ya da başka bir
işletim sistemi için bu kit **kullanılamaz**.

## 2. Önce hangi paketlerin eksik olduğu ölçülmelidir

Kurulumdan önce `tubitak/sr/tools/qgis_ortam_raporu.py` dosyasının tamamı QGIS'in Python
konsoluna yapıştırılıp çalıştırılmalıdır (**Eklentiler > Python Konsolu**). Rapor iki şey
verir:

1. **Hangi paketlerin `YOK` olduğu**; yalnızca onlar kurulacaktır.
2. **QGIS'in kendi `site-packages` dizininin tam yolu**; kurulumun hedefi budur.

Rapordaki `abi tag` satırı `cp312` yazmalıdır. **Python sürümü 3.12 değilse bu kit
kullanılmamalıdır.**

## 3. Kurulum

Zip dosyası bilgisayara kopyalanıp açılmalıdır; örneğin `C:\gencp_kit\` klasörüne. Açıldığında
tekerlekler `C:\gencp_kit\wheels` altında durur.

### 3.1 Tercih edilen yol: OSGeo4W Shell

**OSGeo4W Shell**, QGIS ile birlikte gelen ve QGIS'in kendi Python ortamını doğru ayarlayan
komut penceresidir; Başlat menüsünde QGIS klasörünün altında bulunur. Açıldıktan sonra tek
satır çalıştırılır:

```
python -m pip install --no-index --find-links=C:\gencp_kit\wheels --target="<HEDEF>" rasterio onnxruntime osmium pillow pyyaml
```

`<HEDEF>`, §2'deki raporun gösterdiği QGIS `site-packages` dizinidir ve tırnak içinde
yazılmalıdır.

> **Hedef dizin neden açıkça yazılıyor?** `pip`'in öntanımlı hedefi, bilgisayardaki **her**
> Python 3.12 kurulumunun paylaştığı kullanıcı düzeyinde bir dizindir. Geliştirme bilgisayarında
> tam olarak bu durum ölçülmüştür: `onnxruntime` ve `osmium` oradan çözümleniyordu. Temiz bir
> kurum bilgisayarında bu karışma olmayacaktır; hedef yine de tahmine bırakılmamıştır.

Yazma izni hatası alınırsa OSGeo4W Shell **yönetici olarak** açılmalı (sağ tık > Yönetici
olarak çalıştır) ya da `--target` yerine `--user` kullanılmalıdır.

### 3.2 OSGeo4W Shell bulunamazsa: QGIS Python konsolu

**Eklentiler > Python Konsolu** açılıp tek satır çalıştırılır:

```python
import pip; pip.main(["install", "--no-index", "--find-links", r"C:\gencp_kit\wheels", "--target", r"<HEDEF>", "rasterio", "onnxruntime", "osmium", "pillow", "pyyaml"])
```

### 3.3 `pip` yoksa

Rapor `pip`'in bulunmadığını gösteriyorsa OSGeo4W Shell'de şu satır denenmelidir:

```
python -m ensurepip --default-pip
```

`ensurepip` de yoksa `get-pip.py` internet erişimi olan bir bilgisayardan indirilip kit
klasörüne konulmalı ve `python get-pip.py --no-index --find-links=C:\gencp_kit\wheels`
çalıştırılmalıdır.

## 4. Kurulumun doğrulanması

**QGIS yeniden başlatılmalıdır.** Ardından §2'deki rapor yeniden çalıştırılır. Kurulum,
şu iki koşul sağlanıyorsa başarılı sayılır:

- `rasterio`, `onnxruntime` ve `osmium` satırlarının üçü de **`VAR`** yazmalıdır;
- her birinin yolu, kurulum hedefi olarak verilen dizini göstermelidir.

Eklenti açıldığında eksik paket uyarısı **çıkmamalıdır**. Çıkıyorsa, uyarının gösterdiği dizin
ile kurulum hedefi aynı değildir; kurulum o dizine yeniden yapılmalıdır.

## 5. Bu kitin sınanmışlığı

**Sınanmıştır.** Kit iki kez, ağ bağlantısı kapalı biçimde (`--no-index`) kurulmuştur:

1. **Windows paket kümesi**, `--platform win_amd64 --python-version 3.12` seçenekleriyle
   ağsız çözümlenmiştir: 31 Ağustos 2026'da 16 tekerlek bir hedef dizine kurulmuş; 2 Eylül
   2026'da, `Pillow` ve `PyYAML` eklendikten sonra, beş paketlik istek kitteki 18 tekerleğin
   tamamını çözümlemiş, bağımlılık kümesi eksiksiz çıkmıştır.
2. **Aynı sürümler** temiz bir Python 3.12.12 sanal ortamına kurulmuş; `rasterio`,
   `onnxruntime` ve `osmium` **içe aktarılabilmiştir** (31 Ağustos 2026, ilk 16 tekerlek;
   `Pillow` ve `PyYAML` bu ortamda içe aktarılmamıştır).

**Sınanmamıştır:** Windows'un kendisi. Yukarıdaki iki çalıştırma paket kümesinin eksiksiz ve
komutun doğru olduğunu gösterir; **Windows'ta çalışacağını göstermez.** Windows QGIS 3.40'ın
`rasterio`'yu kendi içinde getirip getirmediği de bilinmemektedir; §2'deki rapor bunu ölçmek
içindir.

---

## Katman 2: `onnxruntime` ve `osmium` eklentinin içine gömülü

Bu bölüm Proje 1'in eklentisini (GenCP Synthetic Reference) ilgilendirir ve yayımlanmamış bir
yapıyı anlatır; sürüm sayfasındaki dosyalar bunlar değildir. Amaç, `rasterio`'su zaten olan bir
bilgisayarda kullanıcının yalnızca eklenti zip dosyasını kurmasıdır: `pip` gerekmez, internet
gerekmez, elle yapılacak adım yoktur.

## 6. İki ayrı dağıtım dosyası: bilinçli bir karar

Gömülen tekerlekler `win_amd64` / `cp312` ikilileridir. Tek dosyada dağıtılsalardı her macOS ve
Linux kurulumuna 44 MB kullanılamaz Windows ikilisi inecekti. Bu yüzden iki ayrı sürüm dosyası
vardır:

| Dosya | Boyut | İçerik | Kimin için |
|---|---|---|---|
| `gencp_plugin.zip` | **98.410 bayt** | `_vendor/` yok | macOS, Linux ve paketleri kendisi kuran Windows kullanıcıları |
| `gencp_plugin_win_amd64.zip` | **15.935.709 bayt** | `onnxruntime` ve `osmium` gömülü | internet erişimi olmayan Windows bilgisayarları |

Çapraz platform dosyası Windows'a özel hâle getirilmemiştir: iki dosya aynı kaynak koddan
üretilir ve `_vendor/` bulunmayan yapıda gömme kodu hiçbir şey yapmaz.

## 7. Kurulu kopya gömülü kopyadan önce gelir

`__init__.py` içindeki `_extend_path_for_vendored()` şöyle davranır:

- `importlib.util.find_spec` ile **önce paketin sistemde var olup olmadığına bakar**; yalnızca
  bulunamayan paketler için `_vendor` dizinini `sys.path` listesinin **sonuna ekler**, başına
  koymaz.
- `import` yerine `find_spec` kullanır: burada `onnxruntime`'ı içe aktarmak, WP12'de kurulan
  geciktirme düzenini bozardı.
- `find_spec` hata verdiğinde sonuç `False` olduğundan, bozuk bir kurulumu “yok” sayar.

Gerekçe: çalışan bir kurulumu sessizce ezen gömülü kopya yeni bir sessiz hata sınıfıdır ve bu
projenin varlık nedeni tam olarak o hata sınıfıdır.

**`rasterio` bilerek gömülmemiştir.** Kendi GDAL'ini taşır; QGIS aynı süreçte başka bir GDAL'i
çoktan yüklemiştir. Tek süreçte iki GDAL, bilinen bir çökme sebebidir. Kullanıcının elle kurduğu
bir bağımlılık, çöken bir QGIS'ten iyidir.

## 8. Üç durum da çalıştırılmıştır

| Durum | `ADDED_FOR` | İçe aktarma sonucu |
|---|---|---|
| **A** `_vendor` var, sistemde kopya yok | `['onnxruntime', 'osmium']` | ikisi de **`_vendor/`** dizininden gelmiştir |
| **B** `_vendor` yok, sistemde kopya yok | `[]` | `ModuleNotFoundError`; mevcut uyarı iletisi devreye girer |
| **C** `_vendor` var, sistemde kopya **var** | `[]` | ikisi de **sistemden** gelmiştir; gömülü kopya kullanılmamıştır |

B, denetimin eksikliği yakalayabildiğini gösterir; C, öncelik kuralının çalıştığını.

## 9. Doğrulanmamış olan ve bunun önemi

**Gömülü `onnxruntime`'ın Windows'ta yerel DLL dosyalarını yükleyip yükleyemediği
sınanmamıştır.** Python 3.8'den beri Windows, bir uzantının yanındaki DLL dosyalarını `sys.path`
üzerinden değil `os.add_dll_directory` listesi üzerinden çözümler. Kod bunu çağırır
(`onnxruntime/capi` ve `osmium.libs` için), **ancak hiçbir Windows bilgisayarında
çalıştırılmamıştır.** Katman 2'nin tamamı bu tek noktaya bağlıdır.

Bu yüzden Katman 1, yani çevrimdışı kurulum kiti, vazgeçilmezdir ve önce tamamlanmıştır.
Katman 2 çalışmasa da Katman 1 çalışır.
