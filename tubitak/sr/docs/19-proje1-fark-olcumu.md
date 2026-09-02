# WP20 — Proje 1'in iki depodaki kopyaları arasındaki fark: ölçüm

**Bu belgenin konusu Proje 1'dir, Proje 2 değil.** Bu klasörde durmasının tek sebebi,
depo taşınma serisinin (WP17–WP20) buraya yazıyor olmasıdır.

**Amaç.** `mvy0502/gencp-validation` (B) kurumun okuduğu depodur. `18-depo-tasima.md` §9
madde 6, B'deki Proje 1 kopyasının `mvy0502/GenCP` `tubitak-tr` (A) dalından geride
olduğunu kaydetmişti. Bunun önemli olup olmadığı bir insan kararıdır; bu belge o kararın
ihtiyaç duyduğu olguları verir, **başka bir şey yapmaz.** Bu iş paketinde iki depoda da
hiçbir Proje 1 dosyası değiştirilmemiş, kopyalanmamış, hazırlanmamıştır (G1: A'da 0 değişen
dosya, `18-depo-tasima.md` §12).

## 1. Ne, hangi commit'lerde karşılaştırıldı

| | depo | commit | izlenen dosya |
|---|---|---|---|
| A | `mvy0502/GenCP`, dal `tubitak-tr` | `e5a3d225f71c84d4105fe16c823c6b71b5545152` | 1272 |
| B | `mvy0502/gencp-validation`, dal `main` | `b47d4222373d86b08e1be9336f859dd3a37d7edf` | 1538 |

`tubitak/sr/` dışındaki her izlenen yol, iki deponun `HEAD` ağacındaki blob sağlamasıyla
karşılaştırılmıştır (`git ls-tree -r HEAD`). İki depoda da bulunan yol: **1189.** İçeriği
farklı olan: **12.** Yalnızca A'da: **4.** Yalnızca B'de: **269.** "Hangisi yeni" sorusu
içerikten tahmin edilmemiş, her yol için o yola son dokunan commit'in tarihinden okunmuştur
(`git log -1 -- <yol>`).

**Karara en çok yön veren tek olgu, önden:** kurumun kurduğu `plugin-v0.2.0` zip'i
(26 Ağustos 2026) içindeki beş Proje 1 dosyası — `plugin.py`, `__init__.py`, `strings.py`,
`metadata.txt`, `gencp_core/extent.py` — **B'nin ağacındakilerle bayt bayt aynıdır.** Zip
salt okunur olarak indirilip sağlamaları alınmıştır. Yani B, yayımlanmış Proje 1'in
kaynağıdır; **A, hem B'nin hem de yayımlanmış zip'in önündedir.** A'daki değişikliklerin
hiçbiri bir Proje 1 sürümüne girmemiştir.

## 2. İçeriği farklı olan 12 yol

Kova: **K** = kuruma önemli (B okuyucusunun uyguladığı ya da yanılabileceği bir şey);
**İ** = yalnızca iç (çalışma notu, ajan kuralı); **T** = tasarım gereği farklı (iki depo
farklı rol oynar). "Yeni taraf" son dokunan commit'in tarihiyle.

| yol | A son commit | B son commit | yeni taraf | fark, bir cümleyle | kova |
|---|---|---|---|---|---|
| `tubitak/gencp_core/extent.py` | 2026-08-31 `75332cb` | 2026-08-30 `f386da3` | A | Modül düzeyindeki `rasterio.crs` içe aktarması `_crs()` ile ilk kullanıma ertelenmiştir — QGIS 3.x'te `rasterio` yokken eklentinin hiç açılmamasına yol açan tek satır (WP12) | **K** |
| `tubitak/qgis_plugin/plugin.py` | 2026-08-31 `75332cb` | 2026-08-27 `6750978` | A | `REQUIRED_MODULES` / `missing_requirements()` eklenmiştir: `rasterio` ya da `onnxruntime` yoksa diyalog kurulmaz, kullanıcıya kütüphaneyi ve bu QGIS'in Python yolunu adlandıran bir uyarı gösterilir (WP12) | **K** |
| `tubitak/qgis_plugin/strings.py` | 2026-08-31 `75332cb` | 2026-08-30 `f386da3` | A | Yukarıdaki uyarının Türkçe metinleri (`err_no_rasterio`, `err_no_onnxruntime`, `err_missing_title`) eklenmiştir | **K** |
| `tubitak/qgis_plugin/__init__.py` | 2026-08-31 `94bf38c` | 2026-08-27 `6750978` | A | `_extend_path_for_vendored()` eklenmiştir: `_vendor/` varsa ve paket makinede yoksa `onnxruntime`/`osmium` oradan alınır (çevrimdışı Windows paketi, WP13); `_vendor/` yoksa etkisizdir | **K** |
| `tubitak/qgis_plugin/metadata.txt` | 2026-08-31 `216ab59` | 2026-08-27 `6750978` | A | `qgisMinimumVersion` 3.28 → 3.40 (doğrulanmış en eski sürüm) | **K** |
| `tubitak/qgis_plugin/QUICKSTART.md` | 2026-08-31 `f24fd9a` | 2026-08-30 `f386da3` | A | İndirme tablosu kaldırılıp yerine "tek yetkili kaynak A'nın kök `README.md`'sidir" notu ve iki sürüm etiketi (`plugin-v0.2.0`, `veri-turkiye-2026-08-31`) konmuştur; A sürümü okuyucuyu **A deposuna** yönlendirir | **K** (kayıtla) |
| `tubitak/DEVIR.md` | 2026-09-01 `f28342b` | 2026-08-31 `5c55b4f` | A | Proje 2 bölümleri büyümüştür: üç model tablosu ve kurulum (P2.7), indirme adresleri ve üç sürüm etiketinin gerekçesi (P2.8), açık maddeler 12–13 ve WP16 kapanışları (+88 −16 satır) | **K** |
| `tubitak/docs/open-items.md` | 2026-08-31 `216ab59` | 2026-08-31 `5c55b4f` | A | Proje 2 WP12 paket incelemesinden üç madde (27–29: `coverage_block.py` çalıştırılamıyor, Qt5 karanlık tema, `demo_dry_run`) eklenmiştir; tümü harness'a ilişkindir, eklentiyi etkilemez | İ |
| `.gitignore` | 2026-08-27 `361fa76` | 2026-08-27 `c41ca07` | eşit tarih | A `!tubitak/qgis_plugin/icon.png` ve `!tubitak/docs/evidence/plugin_screens/*.png` istisnalarını taşır; B `!docs/plugin/*.png` ve `!tubitak/docs/evidence/**` istisnalarını. **Sonuç:** B'de `*.png` kuralı `icon.png`'yi yutar (aşağıda §3) | T (kayıtla) |
| `README.md` | 2026-09-02 `dfcf59b` | 2026-09-02 `632d9bb` | eşit tarih | Tamamen farklı iki belge: A'nınki İngilizce fork README'si (indirme tablosu, Proje 1 ve 2 bölümleri, özgün pix2pix metni); B'ninki Türkçe doğrulama çalışması ön sayfası | T |
| `CLAUDE.md` | 2026-09-02 `e5a3d22` | 2026-09-02 `08fa009` | eşit tarih | A: 142 satırlık ajan kural dosyası; B: 19 satırlık "burası hedef, çalışma alanı değil" notu ve Proje 2 istisnası | İ / T |
| `claude/oturum-devri.md` | 2026-08-26 `d67588e` | 2026-08-25 `2a8305e` | A | A'da başa "Depo ayrımı — 26 Ağustos" tablosu eklenmiştir; oturum devri notudur | İ |

## 3. Yalnızca bir depoda bulunan yollar

**Yalnızca A'da (4):**

| yol | ne | B'den kim ister |
|---|---|---|
| `tubitak/qgis_plugin/icon.png` | Eklentinin araç çubuğu simgesi; `metadata.txt` adlandırır, zip derleme betiği kopyalar | B'nin `.gitignore`'u (`*.png`) bu dosyayı **yoksayar** — B'ye kopyalansa bile istisna eklenmeden izlenmez. B'den derlenecek bir zip'in düğmesi boş kalır; yayımlanmış zip'te simge **vardır**. B'deki `plugin-field-test.md` ve `sr/docs/00-recon.md` adını anar |
| `tubitak/tool/qgis_ortam_raporu.py` | Kurum makinelerinde QGIS ortamını raporlayan tek dosyalık teşhis betiği (Proje 2 WP12) | **B'deki `sr/docs/13-cevrimdisi-kurulum.md` bu dosyayı kullanmayı anlatır; dosya B'de yoktur** |
| `tubitak/docs/evidence/wp15/corpus_checks.json` | Proje 2 WP15 corpus denetimlerinin çıktı kaydı | **B'deki `sr/docs/15-kontroller.md` ve `03a-wald-corpus.md` bu dosyaya atıf yapar; dosya B'de yoktur** |
| `tubitak/scripts/build_plugin_zip_windows.py` | Çevrimdışı Windows paketini (`_vendor/` ile) derleyen betik (Proje 2 WP13) | B'de hiçbir belge anmaz |

Son üçü Proje 2 malzemesidir ve `tubitak/sr/` dışında durdukları için WP17'nin alt-ağaç
kopyasına girmemiştir; ikisi B'deki Proje 2 belgelerinden atıfla çağrılır. WP17'nin bağlantı
denetimi bunları yakalayamamıştır, çünkü atıflar markdown bağlantısı değil düz metindir.

**Yalnızca B'de (269):**

| yol | sayı | ne | neden yalnızca B'de |
|---|---|---|---|
| `tubitak/docs/evidence/rasters/**` | 260 | Proje 1 doğrulama çalışmasının kanıt rasterları (araştırma kaydı) | A'dan `b815b46` (26 Ağustos, depo ayrımı) ile bilerek çıkarılmıştır; B'nin varlık sebebidir |
| `tubitak/docs/figures/web/*.jpg` | 5 | B ön sayfasının görselleri (Ankara, Kapadokya, Tuz Gölü, ODTÜ paketi, üç kol) | B'nin README'sine aittir |
| `docs/plugin/QUICKSTART.md`, `dialog.png`, `confidence_layer.png` | 3 | B'nin kendi Proje 1 kurulum belgesi ve iki ekran görüntüsü (README "Kurulum" bunlara bağlanır) | B'nin ön sayfasına aittir; `tubitak/qgis_plugin/QUICKSTART.md`'den farklı bir dosyadır |
| `SNAPSHOT.md` | 1 | "Bu depo bir devir kopyasıdır" kaynak kaydı | B'nin rolüne aittir |

269'un tamamı **T** kovasındadır.

## 4. Kovaların özeti ve işin büyüklüğü

| kova | fark | yalnızca A'da | toplam |
|---|---|---|---|
| **K — kuruma önemli** | 7 (`extent.py`, `plugin.py`, `strings.py`, `__init__.py`, `metadata.txt`, `QUICKSTART.md`, `DEVIR.md`) | 2 atıfla çağrılan (`qgis_ortam_raporu.py`, `corpus_checks.json`) + 1 derleme için (`icon.png`) | **10** |
| **İ — yalnızca iç** | 3 (`open-items.md`, `CLAUDE.md`, `oturum-devri.md`) | 1 (`build_plugin_zip_windows.py`) | 4 |
| **T — tasarım gereği** | 2 (`README.md`, `.gitignore`) | — | 2 + 269 |

**Neden K'daki yedi dosyanın önemi düz bir "geride" olmaktan farklıdır.** Beş kod dosyası
WP12'nin düzelttiği kusuru taşır: kurumun bildirdiği "QGIS 3.40'ta eklenti çalışmıyor"
arızası. Ama kurum ağacı değil zip'i kurar, ve **zip B'nin ağacıyla aynıdır** — yani bugün
kurumun elindeki eklenti bu düzeltmeyi içermemektedir, ve B'nin ağacı yalnızca yenilenirse
bu durum değişmez. Ağaç yenilemek belgeleri günceller; kurumun kurduğu şeyi yalnızca yeni
bir sürüm değiştirir.

**K'yı yenilemenin içerdiği iş**, kararın yönünden bağımsız olarak:

1. Yedi dosyanın A `e5a3d22`'deki hâlinin B'ye kopyalanması (Proje 1 kodu için bu, A'da
   `75332cb` durumudur), artı `qgis_ortam_raporu.py` ve `corpus_checks.json`. Alt-ağaç
   kopyası; merge değil. WP17'deki G1 kapısının aynısı.
2. `icon.png` için B `.gitignore`'una bir `!tubitak/qgis_plugin/icon.png` istisnası — aksi
   hâlde dosya B'de izlenmez. Bu bir `.gitignore` değişikliğidir ve bu seride `.gitignore`
   dokunulmaz sayılmıştır.
3. `QUICKSTART.md`'nin A sürümü okuyucuyu A'nın README'sine gönderir; B'ye alınırsa bu
   bağlantının B'ye çevrilmesi gerekir, yoksa kurum okuyucusu yine A'ya yollanır.
4. `DEVIR.md`'nin A sürümü Proje 2 bölümlerinde `tubitak/sr/` içi yolları anar; B'de
   çözülürler (aynı yerleşim).
5. **Kurumun kurduğu eklentiyi değiştirmek isteniyorsa** ayrıca: yenilenmiş ağaçtan bir
   `plugin-v0.2.1` zip'i derlemek, WP12'de yapıldığı gibi QGIS 3.44 ve 4.2 üzerinde
   `rasterio` kaldırılarak sınamak, B README "Kurulum" tablosundaki 73 KB / `latest`
   bağlantısını ve sürüm notlarını güncellemek, `SHA256SUMS` yayımlamak.

## 5. Seçenekler

Ölçümün desteklediği seçenekler aşağıdadır. Hiçbiri önerilmemektedir; karar okuyanındır.

**S0 — Hiçbir şey yapmamak.**
*Bedel:* sıfır. *Risk:* B'nin ağacı yayımlanmış zip'le tutarlı kalır, ama kurumun elindeki
Proje 1 eklentisi QGIS 3.x'te `rasterio` yoksa açılmadan çöker (WP12'nin düzelttiği arıza)
ve B'deki iki Proje 2 belgesi B'de olmayan iki dosyayı anmaya devam eder. B'nin `DEVIR.md`'si
31 Ağustos'ta kalır.

**S1 — Yalnızca atıfla çağrılan iki Proje 2 dosyasını ve `DEVIR.md`'yi B'ye almak; Proje 1
koduna dokunmamak.**
*Bedel:* üç dosyalık alt-ağaç kopyası, bir G1. *Risk:* düşük; Proje 1 kodu ve zip
tutarlılığı olduğu gibi kalır. Kurumun eklentisindeki QGIS 3.x arızası çözülmez.

**S2 — K kovasının tamamını B'ye almak, sürüm yapmamak.**
*Bedel:* on dosya, bir `.gitignore` istisnası, `QUICKSTART.md`'de bir bağlantı çevirisi, G1.
*Risk:* B'nin ağacı artık yayımlanmış zip'ten **ileride** olur; B'den derleyen biri kurumun
kurduğundan farklı bir eklenti elde eder ve hiçbir belge bunu söylemez. Kurumun kurduğu
eklenti değişmez.

**S3 — S2 artı `plugin-v0.2.1` sürümü.**
*Bedel:* S2 + derleme, iki QGIS sürümünde sınama, sürüm notları, `SHA256SUMS`, B README
"Kurulum" tablosunun güncellenmesi, kuruma yeni bir dosya aktarımı. *Risk:* Proje 1 "bitmiş
ve teslim edilmiş" sayılmaktadır; yeni sürüm bu ifadeyi geçersiz kılar ve kurumda yeniden
kurulum gerektirir. Karşılığında kurum, kendi bildirdiği arızanın düzeltmesini alır.

**S4 — Yalnızca kaydetmek.** Bu belgeyi karar kaydı olarak bırakıp B README'sine ya da
`DEVIR.md`'ye tek satırla "B'deki Proje 1 kopyası 30 Ağustos durumundadır; sonraki
düzeltmeler A'da ve yayımlanmamıştır" yazmak. *Bedel:* bir satır. *Risk:* arıza çözülmez,
ama okuyucu artık yanılmaz.

K kovası boş **değildir**; dolayısıyla "hiçbir şey yapmamak" dürüst ama bedelsiz olmayan
bir seçenektir ve yukarıda öyle yazılmıştır.

## 6. Bu ölçümün sınırları

- Karşılaştırma blob düzeyindedir; iki dosyanın "aynı" olması bayt eşitliğidir.
- "Yeni taraf" commit tarihidir; aynı gün dokunulmuş dosyalarda ("eşit tarih") yön
  belirtilmemiştir.
- Zip karşılaştırması `plugin-v0.2.0`'ın `gencp_plugin.zip`'i içindir; `gencp_C2_fp32.onnx`
  modeli karşılaştırılmamıştır (iki ağaçta da yoktur, yalnızca sürümdedir).
- A'daki Proje 1 değişikliklerinin doğruluğu bu belgenin konusu değildir; WP12/WP13
  raporları onları anlatır.
