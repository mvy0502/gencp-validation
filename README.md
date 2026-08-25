# GenCP Doğrulama Çalışması

ESA'nın **GenCP** projesi ([telespazio-tim/GenCP](https://github.com/telespazio-tim/GenCP)),
OpenStreetMap rasterlarından pix2pix (koşullu GAN) ile sentetik uydu görüntüsü — GCP
(Ground Control Point) referans chipleri — üretir. Bu repo, o yayınlanmış pipeline'ın
**bağımsız ölçüm ve doğrulama çalışmasıdır**: TÜBİTAK UZAY stajı kapsamında yürütüldü
(Ağustos 2026, staj devam ediyor).

Upstream kod bu repoda değiştirilmeden durur; çalışmanın tamamı [`tubitak/`](tubitak/)
altındadır. 660+ commitlik geçmiş, kayıtların (registration) zaman damgası olduğu için
aynen korunmuştur. Upstream'in kendi dokümantasyonu (eğitim/test seçenekleri, orijinal
README) upstream reposundadır; burada tekrarlanmaz.

**Projeyi devralacaksanız buradan başlayın: [`tubitak/DEVIR.md`](tubitak/DEVIR.md)**

## Ne bulundu — ana bulgular

Her bulgu ölçülmüş, yöntemi/sayıları/falsifikasyon ölçütüyle yazılmıştır
(ayrıntılı tablo: [`tubitak/README.md`](tubitak/README.md)):

1. **Georeferanslama ölçek hatası (+1/256).** Yayınlanan `gencp_georeferencing.py`,
   256 piksellik ızgarayı 257 piksellik kaynak transformuyla eşliyor: gerçek GSD
   10.039 m, beyan 10.0 m; karo köşesinde **14.1 m** hata. Dört bağımsız yöntemle,
   KARIOS'ta 9.9σ ile doğrulandı — [geometry-finding.md](tubitak/docs/geometry-finding.md)
2. **Ağ hizalaması temiz.** Ekivaryans 0.008 px'e sertifikalı; analitik ofset tam 0.
3. **Eğitim/çıkarım ölçek uyuşmazlığı** gerçek ama görev metriğinde fark yaratmıyor —
   ölçüldü ve reddedildi.
4. **Üreteç yapı uyduruyor.** OSM girdisinin **2.1×** kenar yoğunluğu üretiyor; girdi ne
   derse desin gerçek uydunun "yoğunluğunu" tutturuyor — eşik yok, siteler sıralanmalı —
   [hallucinated-structure.md](tubitak/docs/hallucinated-structure.md)
5. **Seyrek OSM chipi konum doğruluğu kaybediyor ve bu GenCP'ye özgü** (kısmi rho = −0.61;
   gerçek görüntüde tavan kontrolü null) — [karios-validation.md](tubitak/docs/karios-validation.md)
6. **Veri seti kusurları:** 9 sızmış test chipi, 25 demo/eğitim çakışması, 566 çiftin
   323'ünde OSM yarısı georeferanslı rasteriyle bayt-özdeş değil.

KARIOS üç-kol koşusunun sonucu: upstream'in kendi istatistiğinde **4.5× daha iyiyiz**
(0.155 px vs 0.70 px global sistematik kayma); affine düzeltmesi sistematik kaymayı
**%40.3** azaltıyor; ~2 px'lik taban gürültüsü lokal eşleştirmeden geliyor (varyansın
~%95'i chip-içi).

## Nereye gelindi (25 Ağustos 2026)

* **Teslimat aracı:** [`tubitak/tool/gencp_ref.py`](tubitak/tool/gencp_ref.py) —
  deterministik GenCP referans üreteci; düzeltilmiş transform gömülü (düzeltmesiz kod
  yolu yok), bayt-özdeş yeniden koşu doğrulanmış, provenance çıktıya işleniyor —
  [tool-results.md](tubitak/docs/tool-results.md)
* **Faz C — 2×2 kayıp fonksiyonu faktöriyeli** sıfırdan eğitildi ve kayıtlara karşı
  skorlandı: [phase-c-results.md](tubitak/docs/phase-c-results.md),
  [phase-c-lpips-results.md](tubitak/docs/phase-c-lpips-results.md); başlık ölçümleri
  B1–B3: [headline-results.md](tubitak/docs/headline-results.md)
* **Gerçek görüntüye karşı kıyas:** T1 — gerçek görüntü, var olduğu yerde sentetik
  referansı belirgin biçimde geçiyor ([T1-benchmark-results.md](tubitak/docs/T1-benchmark-results.md));
  T3 — güvenilirlik katmanı öneri olarak paketlendi
  ([T3-reliability-results.md](tubitak/docs/T3-reliability-results.md))
* **Konumlandırma (E1–E3):** sentetik referans gerekçesinin üç ölçülü öncülü de yazıldığı
  haliyle düşüyor ([positioning-results.md](tubitak/docs/positioning-results.md)).
  Önemli kapsam notu: hedef ortam **uyduda offline kullanım** (gerçek referansa erişim
  yok) — bu, öncüllerin geçerli olmadığı, sentetik referansın gerekçesinin ayakta
  kaldığı senaryodur; sonuçlar bu caveat'la okunmalı.
* **Türkiye hattı:** Ankara veri edinimi tamam ve doğrulanmış
  ([ankara-acquisition.md](tubitak/docs/ankara-acquisition.md)); OSM rasterizer'ı palete
  oturtuldu ama KARIOS kabul kapısını geçemedi — tanımlı çözüm land-cover taban katmanı,
  karar bekliyor ([renderer-tolerance.md](tubitak/docs/renderer-tolerance.md))
* **Seed-düzeyi replikasyon:** faktöriyelin tüm çıkarımı seed düzeyine taşındı
  ([seed-replication-registration.md](tubitak/docs/seed-replication-registration.md));
  SEED-b kapısı Modal A10G üzerinde **koşuyor**
* **Yayın:** IEEE GRSL letter, kayıp fonksiyonu sonucuna daraltılmış kapsamla planlı —
  [paper-roadmap.md](tubitak/docs/paper-roadmap.md)
* **Türkçe raporlar:** ilerleme raporu [`tubitak/rapor2/`](tubitak/rapor2/), sonuç
  raporu [`tubitak/rapor3/`](tubitak/rapor3/) (kaynaklar sürümlü; PDF'ler
  `rapor3/build_pdf.py` ile üretilir, git'te tutulmaz)

## Kullanılan veri

| Veri | Kaynak | Not |
|---|---|---|
| HR eğitim korpusu (`GenCP_HR_DB.zip`, 1.6 GB) | [Zenodo 15044428](https://zenodo.org/records/15044428) | S2 yaması + OSM raster çiftleri (566 çift, 10 m GSD, 256/257 px); kusur envanteri bulgu 6'da |
| Yayınlanmış HR model ağırlıkları (208 MB) | Zenodo 15044428 | MD5'ler [data-sources.md](tubitak/docs/data-sources.md)'de |
| CLC backbone 10 m | Copernicus | OSM rasterlarındaki boşlukları doldurmada kullanılmış |
| Ankara/Türkiye | Sentinel-2 + OSM | Edinim ve doğrulama: [ankara-acquisition.md](tubitak/docs/ankara-acquisition.md) |

Tüm indirme kaynakları, sürümler ve sağlamalar tek yerde:
[data-sources.md](tubitak/docs/data-sources.md). `tubitak/data/` ve `tubitak/outputs/`
git dışıdır; her şey oradaki kayıtlardan yeniden üretilebilir.

## Eğitimler nerede, nasıl yapıldı

* **Kaggle (2× T4):** faktöriyel kollar — C1 (GAN+L1, upstream varsayılanları; yayınlanan
  D olmadığı için kayıtlı warm-up protokolü), C2 (yalnız L1; Kaggle kopyasına 3 satırlık
  yama), C4/C5 (LPIPS yarıları). Kol başına 20 epoch, 1394 iterasyon/epoch. Kernel'ler
  tek script'ten üretilir: [`tubitak/kaggle/build_kernels.py`](tubitak/kaggle/build_kernels.py);
  eğitim: [`tubitak/kaggle/train_c1_c2.py`](tubitak/kaggle/train_c1_c2.py); protokol ve
  sapmalar: [phase-c-config.md](tubitak/docs/phase-c-config.md)
* **Modal (A10G):** seed replikasyonu — [`tubitak/modal/gencp_modal.py`](tubitak/modal/gencp_modal.py).
  Ortam Kaggle imajına pinli (Python 3.12.13, pip freeze preflight'ta), veri tek tar ile
  stage edilir, dosya-sayısı guard'ı ve enumeration-order yaması vardır (neden gerektiği:
  [corrections-log.md](tubitak/docs/corrections-log.md) girdi 29)
* **Lokal (MacBook M4 Max, CPU):** tüm çıkarım ve ölçümler; KARIOS ayrı conda ortamında
  koşar ve tek iş parçacıklıdır (8-geniş paralel koşturmak 25 dk'lık partiyi ~3 dk'ya indirir)

## Nasıl çalıştırılır

1. Ortam kurulumu ve bilinen tuzaklar (OpenMP, visdom):
   [`tubitak/README.md`](tubitak/README.md) → "Environment setup" / "Known issues"
2. Referans üretimi: `tool/gencp_ref.py` — kullanım ve doğrulama adımları
   [`tubitak/README.md`](tubitak/README.md) → "Running the pipeline"
3. Ölçüm scriptleri: her scriptin başında ne ölçtüğü yazar; açıklamalı liste
   [`tubitak/README.md`](tubitak/README.md)'deki dizin ağacında

## Çalışma disiplini

Her deney önce **kayıt** (tahminler, falsifikasyon bantları), sonra koşu, sonra kayda
karşı skorlanmış sonuç dosyası. Hatalar silinmez;
[corrections-log.md](tubitak/docs/corrections-log.md)'a numaralı girdi olarak işlenir.
Açık işler [open-items.md](tubitak/docs/open-items.md)'de tutulur ve her paket sonunda
baştan okunur. Git geçmişi kayıtların zaman damgasıdır; history rewrite yapılmaz.

## Lisans ve atıf

Upstream kod **BSD 3-Clause** lisanslıdır ([LICENSE](LICENSE)); telif bildirimleri
korunmuştur. Temel mimari: [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)
(Isola vd. 2017, Zhu vd. 2017). GenCP projesi: [telespazio-tim/GenCP](https://github.com/telespazio-tim/GenCP).
