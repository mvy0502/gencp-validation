# WP17 — Proje 2'nin kurumun erişebildiği depoya taşınması

**Tarih** 2 Eylül 2026. **Kaynak** `mvy0502/GenCP`, dal `tubitak-tr`, commit
`f28342b8eb9739ef7cad838bf4474e18fb3873cd`. **Hedef** `mvy0502/gencp-validation`, öntanımlı
dal `main` (uzak `HEAD` sembolik referansından okunmuştur, varsayılmamıştır), taşınma öncesi
`5c55b4f`. Yerel klon bulunamadığından `~/Documents/gencp-validation` altına yeni klon
alınmıştır.

Eklenti, modeller, corpus'lar ve ölçümler değişmemiştir. `tubitak/sr/sr_plugin/` içeriğine
dokunulmamıştır. Bu bir alt-ağaç kopyası ve belge düzeltmesidir; tarih birleştirilmemiştir.

## 1. Öngörüler ve ölçümler

Üç sayı ölçümden önce dosyaya yazılmıştır (`predictions.txt`, 10:02:30 +03); ölçümden sonra
değiştirilmemiştir.

| | öngörü | ölçüm | yol |
|---|---|---|---|
| P1 — A'da `tubitak/sr/` altındaki dosya sayısı | 130 | **78** | `git ls-files tubitak/sr` |
| P2 — `tubitak/sr/` içindeki, ağacın dışına işaret eden markdown bağlantısı | 40 | **32** | 36 göreli bağlantı tarandı; 32'si `tubitak/sr/` dışına çözülüyor, **hepsi tek dosyada** (`docs/00-recon.md`) |
| P3 — B'de `5c55b4f` ile gelen `tubitak/sr/` dosya sayısı | 90 | **65** | `git ls-tree -r 5c55b4f -- tubitak/sr` |

Üçü de fazla öngörülmüştür. P2'nin öncülü — "kopyalanınca kırılacak" — **doğru çıkmamıştır**;
bkz. §4.

## 2. Kurallar: okunan, değiştirilen, değiştirilmeyen

B'de okunanlar: `CLAUDE.md` (`c7cdf2c`, ajanlar için rol ve sınır kuralları), `README.md`
"KURAL" bölümü (`34dae35`, iki yönde de merge yok), `tubitak/docs/standing-practices.md` ve
`tubitak/docs/open-items.md`'deki `34dae35` ekleri (kanıt commit'i doğrulaması ve ledger
maddesi; bu iş paketiyle çelişmezler). `claude/oturum-devri.md` bir oturum devri notudur,
kural dosyası değildir.

**Merge yasağı bu işle çelişmez** — hiçbir dal birleştirilmemiş, ortak commit eklenmemiş,
yalnızca izlenen dosyalar kopyalanmıştır. Çelişen, "çalışma GenCP'de olur" cümleleridir.

### 2.1 Değiştirilen: `CLAUDE.md` (tek değişiklik, yalnızca ekleme, +9 −0)

Eski metin, olduğu gibi korunmuştur:

> Work on this project happens in `mvy0502/GenCP`, branch `tubitak-tr`. … Do not develop
> here. Do not merge branches into here. If you were sent here to do work, you were sent to
> the wrong place — go to `mvy0502/GenCP`, `tubitak-tr`.

Eklenen bölüm:

> **Exception, from 2 September 2026: Project 2 lives here.** `tubitak/sr/` … has its
> **current** copy in this repository. It was brought in as a subtree copy of tracked files
> from `mvy0502/GenCP` at `f28342b`, not as a merge; `tubitak/sr/SOURCE.md` records the
> provenance. The copy left in GenCP is frozen. Documentation and installation fixes for
> Project 2 happen here. The no-merge rule above is unchanged.

Proje 1 hakkında söylenen hiçbir şey değişmemiştir.

### 2.2 Değiştirilmeyen ve karar bekleyen: `README.md` KURAL bölümündeki cümle

> Fork ve QGIS eklenti iş paketi [mvy0502/GenCP](https://github.com/mvy0502/GenCP)
> deposunda, `tubitak-tr` dalında devam eder.

Bu cümle Proje 2 için artık doğru değildir. Ancak fork'u ve Proje 1 eklentisini aynı cümlede
andığından, düzeltmek Proje 1 hakkındaki kural metnine dokunmak olurdu; brifing bunu
yasaklamıştır. **Cümle değiştirilmemiştir.** Bunun yerine yeni Proje 2 bölümünün içine, KURAL
bölümünün taşınmadan önce yazıldığı ve bu cümlenin Proje 1 için geçerli olduğu notu
eklenmiştir. Cümlenin kendisi için karar beklenmektedir.

## 3. Kopya

78 izlenen dosya, aynı göreli yollarla, `git ls-files` listesinden kopyalanmıştır.
`tubitak/sr/SOURCE.md` kaynak depo, dal, commit ve tarihi kaydeder.

- **1 MB üstü dosya:** yok. En büyüğü `docs/00-recon.md`, 54 KB. Modeller ağaçta değil,
  sürümdedir.
- **B'nin `.gitignore`'u (V3):** 78 yolun tamamı `git check-ignore --no-index` ile
  sınanmıştır; **0 yol yoksayılıyor.** `git add -f` kullanılmamıştır.
- **Eski kopyayla uzlaşma:** `5c55b4f`'in 65 dosyasının 65'i de A'da vardır (13'ü A'da
  değişmiş, 52'si aynı). **B'de olup A'da olmayan dosya: yok.** Dolayısıyla silinen
  bayat kopya **yoktur**; listelenmeyen hiçbir şey kaldırılmamıştır.

## 4. Bağlantılar

| | sayı |
|---|---|
| taranan göreli bağlantı (`tubitak/sr/**/*.md`) | **36** |
| `tubitak/sr/` dışına işaret eden | 32 |
| (a) B'deki yola yeniden yönlendirilen | **0** |
| (b) GenCP URL'sine çevrilen | **0** |
| B'de çözülmeyen (V2) | **0** |

Neden sıfır: 32 bağlantının hepsi `docs/00-recon.md`'de, hepsi
`../../gencp_core/…`, `../../qgis_plugin/…`, `../../tests/gate_g.py` biçimindedir. Bu
yollar `tubitak/` köküne görelidir ve **iki depo da `tubitak/` altında aynı yerleşimi
taşır** — B, Proje 1'in devir kopyasıdır. Kopyalandıklarında olduğu gibi çözülmüşlerdir;
değiştirilecek bir şey olmamıştır. Dış URL'ler çekilmemiştir; yalnızca dosya sistemi
üzerinde çözümleme yapılmıştır.

Bir uyarı: hedeflerden `tubitak/gencp_core/extent.py` A ve B'de **farklıdır** (WP12'nin
ertelenmiş `rasterio` içe aktarması A'ya B'nin son yenilenmesinden sonra girmiştir). Bu
bağlantılar satır çapaları (`#L16` vb.) taşır; çapalar WP0'da yazılmıştır ve zaten iki
depoda da tarihseldir. Dosyaya çözülürler; satıra çözülmeleri garanti değildir.

## 5. Ön sayfa ve sürüm notları

B `README.md`'ye `## Proje 2 — Sentinel-2 süper çözünürlük eklentisi` bölümü,
`## Araştırma kaydı`'ndan hemen önce eklenmiştir. **Yalnızca ekleme: +40 −0, değişen satır
0.** İçindeki her sayı dosyadan alınmıştır: üç model tablosu, 36SXJ / 1628 çip / 40 m → 10 m
koşulu, 3,94 kat (491,3'e karşı 124,6 iç nokta), %40 (0,5917'ye karşı 0,9835 px), 0/1628
(`13-tci-model-v2.md` §8); 8,1 MB (yedi varlığın ölçülen toplamı 8,1 MB); çevrimdışı ölçümü
(`10-kurulum.md` §7.6). Brifingdeki hiçbir rakam belgelerle çelişmemiştir.

Sürüm notları, `gh release edit` ile, yalnızca kılavuz bağlantısı:

```
59c59
< [`tubitak/sr/docs/10-kurulum.md`](https://github.com/mvy0502/GenCP/blob/tubitak-tr/tubitak/sr/docs/10-kurulum.md)
---
> [`tubitak/sr/docs/10-kurulum.md`](https://github.com/mvy0502/gencp-validation/blob/main/tubitak/sr/docs/10-kurulum.md)
```

Canlı gövde, düzenlemeden sonra çekilip özgün gövdeyle karşılaştırılmıştır; **tek fark bu
satırdır.** Yedi varlık dokunulmamıştır; `plugin-v0.2.0` dokunulmamıştır (26 Ağustos, 2
varlık). İlk uygulamada `--notes-file` gövdenin sonuna bir boş satır eklemişti; tam
baytlarla yeniden uygulanarak giderilmiştir.

## 6. Eski kopyanın işaretlenmesi (A)

Dal `README.md`'sinde Proje 2 başlığının hemen altına bir satır (+1 −0), ve yalnızca aynı
satırı içeren yeni `tubitak/sr/README.md`. A'da başka hiçbir şey değişmemiştir; hiçbir şey
silinmemiştir.

## 7. Doğrulama

**V1 — `diff -r` A/`tubitak/sr` ile B/`tubitak/sr`** (rapor yazılmadan önce; `__pycache__`
izlenmez, dışlanmıştır):

```
Only in .../GenCP-Generative-Goruntu-Uretimi-OpenStreetMap/tubitak/sr: README.md
Only in .../gencp-validation/tubitak/sr: SOURCE.md
```

İzin verilen ikisi dışında fark yoktur; (a)/(b) bağlantı düzenlemesi olmadığından ondan
kaynaklanan fark da yoktur. Bu rapor yazıldıktan sonra üçüncü bir satır eklenir — `Only in
…/gencp-validation/tubitak/sr/docs: 18-depo-tasima.md` — ki o da brifingin kendi
çıktısıdır.

**V2:** 36 bağlantı, **0 kırık**. README'nin 68 göreli bağlantısı da çözülmektedir.
**V3:** 78 yol, **0 yoksayılan**.

**V4 — ön sayfa, ilk kez gören gözle.** Sayfa "GenCP Doğrulama Çalışması" başlığı ve iki işi
anlatan bir giriş paragrafıyla açılır; giriş Proje 2'den söz etmez. Proje 1'in kurulum
bölümü ve eklenti ekran görüntüsü gelir; onun hemen ardından, araştırma kaydından önce,
"Proje 2" başlığı vardır. Oraya gelen bir kişi aracın ne olduğunu ve neden var olduğunu, tek
sayfalık 8,1 MB'lık indirme bağlantısını, `SHA256SUMS.txt`'nin ne işe yaradığını, üç modelin
hangisinin elindeki veriye uyduğunu, sonucun hangi koşulda ölçüldüğünü ve **bu depodaki**
kurulum kılavuzunu bulur; hiçbir adımda depodan çıkmaz. Eksik olan tek şey, giriş
paragrafının hâlâ "iki iş" demesidir: yalnızca ilk paragrafı okuyup bırakan biri Proje 2'yi
göremez. Bu paragraf var olan metin olduğundan ve düzenleme yalnızca ekleme olabildiğinden
değiştirilmemiştir; karar için §9'da listelenmiştir.

**G1 — birincil kapı.** Taban çizgisi: her iki depoda `tubitak/sr/` dışındaki her izlenen
dosyanın `HEAD`'deki blob sağlaması (`git ls-tree -r HEAD`); iki çalışma ağacı da başlangıçta
temizdi (A: 0 kirli giriş; B: yeni klon), bu yüzden `HEAD` iş paketinin hemen öncesindeki
durumdur. Sonra: aynı yolların çalışma ağacındaki `git hash-object` değeri. Manifestler
çalışma ağaçlarının dışında, oturum çalışma dizininde tutulmuştur.

| depo | karşılaştırılan dosya | yol kümesi | sağlaması değişen | izinli madde |
|---|---|---|---|---|
| A (GenCP) | **1193** | aynı; beliren/kaybolan/taşınan yok; `tubitak/sr/` dışında izlenmeyen dosya 0 | `README.md` | 4 — tek eklenen satır |
| B (gencp-validation) | **1458** | aynı; beliren/kaybolan/taşınan yok; `tubitak/sr/` dışında izlenmeyen dosya 0 | `CLAUDE.md` | 3 — tek kural değişikliği |
| | | | `README.md` | 2 — Proje 2 bölümü, yalnızca ekleme |

Listede beş izinli maddeden başka bir şey yoktur. `models/`, `docs/`, `datasets/`, `data/`,
`scripts/`, `options/`, `util/`, `imgs/`, `gencp_imgs/`, iki demo dizini, `tubitak/`'ın
`sr/` dışı, `train.py`, `test.py`, `requirements.txt`, `environment.yml`, defterler,
`LICENSE`, `SNAPSHOT.md`, `.gitignore` — hepsinin sağlaması aynıdır. **Kapı geçilmiştir;
Proje 1'in tek baytı değişmemiştir.** `10-kurulum.md`'nin Proje 1 bölümleri de aynen
durmaktadır (dosyada hiçbir bağlantı düzenlenmemiştir).

## 8. Commit'ler

Her depoda tek commit, açık yollarla (`git add -A` / `git add .` kullanılmamıştır).

- **A** (`tubitak-tr`): `dfcf59b4b81482db620c74859b29f03c9eb4064a` — iki uyarı satırı. İtildikten sonra `git ls-remote origin
  tubitak-tr` yerel `HEAD` ile eşleşmiştir.
- **B** (`main`): bu raporu içeren commit — 78 kopyalanan dosya, `SOURCE.md`, bu rapor,
  `README.md` bölümü, `CLAUDE.md` eki. SHA'sı kendi içinde yazılamaz; `git log` ile
  doğrulanır. İtme `git ls-remote origin main` ile doğrulanmıştır.

## 9. Brifingin öngörmediği bulgular ve karar bekleyenler

1. **P2'nin öncülü yanlıştı.** Ağacın dışına işaret eden 32 bağlantının hiçbiri kırılmamıştır,
   çünkü iki depo da `tubitak/` altında aynı yerleşimi taşır. (a) ve (b) sayıları bu yüzden
   sıfırdır.
2. **Sürüm notlarında ikinci bir GenCP bağlantısı var** (satır 160, `tubitak/sr/docs/`
   ağacına). Brifing "yalnızca kılavuz bağlantısı" dediğinden dokunulmamıştır. Aynı gerekçeyle
   onun da B'ye çevrilmesi kararı beklenmektedir.
3. **README giriş paragrafı "iki iş" der** (§7, V4). Yalnızca ekleme kuralı ve izinli
   değişiklik listesi gereği değiştirilmemiştir.
4. **README KURAL cümlesi** (§2.2) karar beklemektedir.
5. **A'nın `CLAUDE.md`'si** "`gencp-validation` bir hedeftir, asla kaynak değil. Orada asla
   çalışılmaz" der; Proje 2 için artık B'nin `CLAUDE.md`'siyle çelişir. A'da iki satırdan
   başka bir şey değişemeyeceğinden dokunulmamıştır; karar beklemektedir.
6. **`gencp_core/extent.py` A ve B'de farklıdır** (§4); B'nin Proje 1 devir kopyası A'nın
   `tubitak-tr` dalından geridedir. Bu iş paketinin kapsamı dışıdır ve öyle bırakılmıştır.
7. **Oturum çalışma dizininde 31 Ağustos'tan kalma bayat bir B klonu vardı**; kullanılmamış,
   yerine `~/Documents/gencp-validation` altına kalıcı klon alınmıştır.
8. **`gh release edit --notes-file` gövdenin sonuna boş satır ekler.** Fark edilmiş ve
   giderilmiştir (§5); "yalnızca bağlantı" iddiası canlı gövdeyle doğrulanmıştır.

---

## 10. WP18 — §9'da açık bırakılan beş maddenin kapatılması

**Tarih** 2 Eylül 2026. **Taban çizgisi** A `dfcf59b4b81482db620c74859b29f03c9eb4064a`,
B `08fa009b1923ba043b72f5419f57d3c6226f8b45`; iki ağaç da başlangıçta temizdi. Bu kez her
izlenen dosya — `tubitak/sr/` dahil — manifeste alınmıştır (A **1272**, B **1538** dosya,
`/tmp/wp18/` altında). §1–9 değiştirilmemiştir; bu bölüm onları çözer, yerine geçmez.
Değişen her satır aşağıda önce/sonra olarak aynen verilmiştir.

### 10.1 Madde 1 — README'nin açılış cümlesi (B `README.md`)

Önce (3. ve 5–7. satırlar):

> `Bu depoda iki iş bir arada duruyor. Biri, harita verisinden sentetik uydu görüntüsü üreten`
> `bağımsız ölçüm ve doğrulama çalışması — TÜBİTAK UZAY stajı, Ağustos 2026. Öteki, o`
> `çalışmadan çıkan **QGIS eklentisi**: seçilen bir alan için OpenStreetMap ve arazi örtüsü`
> `verisinden georeferanslı sentetik referans görüntü üretir, terminal gerektirmez.`

Sonra:

> `Bu depoda üç iş bir arada durmaktadır. Birincisi, harita verisinden sentetik uydu görüntüsü üreten`
> `bağımsız ölçüm ve doğrulama çalışması — TÜBİTAK UZAY stajı, Ağustos 2026. İkincisi, o`
> `çalışmadan çıkan **QGIS eklentisi** (Proje 1): seçilen bir alan için OpenStreetMap ve arazi örtüsü`
> `verisinden georeferanslı sentetik referans görüntü üretir, terminal gerektirmez. Üçüncüsü,`
> `Sentinel-2 görüntüsünü süper çözünürlüğe çıkaran ikinci bir **QGIS eklentisi** (Proje 2);`
> `kendi bölümü aşağıdadır.`

4. satır (GenCP bağlantısı) ve girişin geri kalanı değişmemiştir. Yalnızca sayının doğru
olması için değişmesi gereken cümleler değişmiştir: "iki/Biri/Öteki" üçlü sayıma
uymadığından, ve üçüncü iş bir cümleyle eklendiğinden.

### 10.2 Madde 2 — KURAL bölümündeki (b) cümlesi

**(a) Merge yasağı, bugün olduğu gibi, dokunulmamıştır** (`git diff -U0` ile doğrulanmış,
0 değişen satır):

> `**Hiçbir yönde merge yok, hiçbir zaman.** Bu bir uyarı değil, kuraldır.`

ve altındaki dört madde işareti (`tubitak-tr` birleştirilmez; ters yön kapalı; tek aktarım
`cherry-pick`; senkron kapanır).

**(b) önce** (153. ve 155. satırlar):

> `kanıt artefaktları ve düzeltme kaydı. Fork ve QGIS eklenti iş paketi`
> `[mvy0502/GenCP](https://github.com/mvy0502/GenCP) deposunda, `tubitak-tr` dalında`
> `devam eder. Makale çalışması `mvy0502/gencp-letter` deposundadır — **bu depo özeldir**, bağlantı`

**(b) sonra:**

> `kanıt artefaktları ve düzeltme kaydı. Fork ve **Proje 1** QGIS eklenti iş paketi`
> `[mvy0502/GenCP](https://github.com/mvy0502/GenCP) deposunda, `tubitak-tr` dalında`
> `devam eder, çünkü GenCP modelinden türemektedir. **Proje 2** (süper çözünürlük,`
> ``tubitak/sr/`) bu depoda bulunmaktadır; fork'taki kopyası dondurulmuştur. Makale çalışması`
> ``mvy0502/gencp-letter` deposundadır — **bu depo özeldir**, bağlantı`

WP17'nin Proje 2 bölümüne eklediği not artık doğru olmadığından **silinmiştir** (99–101.
satırlar). Silinen metin:

> `[`tubitak/sr/SOURCE.md`](tubitak/sr/SOURCE.md) dosyasında kayıtlıdır. (Aşağıdaki KURAL`
> `bölümü bu taşınmadan önce yazılmıştır; oradaki "QGIS eklenti iş paketi GenCP'de devam eder"`
> `cümlesi Proje 1 için geçerlidir.)`

Kalan satır: `[`tubitak/sr/SOURCE.md`](tubitak/sr/SOURCE.md) dosyasında kayıtlıdır.`
README toplamı: **+11 −9**.

### 10.3 Madde 3 — sürüm notlarındaki ikinci bağlantı

WP17 durumundaki gövde API'den tam baytlarıyla alınmış (uzunluk **8044**, sonda tam **1**
satır sonu — `gh --jq` çıktısı kendi satır sonunu eklediğinden bu ancak API üzerinden
ölçülebilmiştir), tek bağlantı değiştirilmiş, `gh release edit --notes-file` ile uygulanmış
ve **düzenlemeden sonra** API'den geri okunmuştur:

```
@@ -160 +160 @@
-[`tubitak/sr/docs/`](https://github.com/mvy0502/GenCP/tree/tubitak-tr/tubitak/sr/docs)
+[`tubitak/sr/docs/`](https://github.com/mvy0502/gencp-validation/tree/main/tubitak/sr/docs)
```

Canlı gövde == amaçlanan baytlar: **evet**; uzunluk 8049; sondaki satır sonu sayısı **1**
(değişmedi); gövdede kalan `github.com/mvy0502/GenCP` bağlantısı **0**. Varlıklar: 7,
dokunulmamış. `plugin-v0.2.0`: 26 Ağustos, 2 varlık, dokunulmamış.

### 10.4 Madde 4 — A'nın `CLAUDE.md`'si (kural 2)

Önce:

> `2. `gencp-validation` is a **destination, never a source.** Never work in it. Never`
> `   merge a branch into it. It is refreshed at milestones by copying the curated`
> `   `tubitak/` tree. Merging `tubitak-tr` into it would propagate deletions and destroy`
> `   the research record — this has already nearly happened once.`

Sonra:

> `2. `gencp-validation` is a **destination, never a source, for Project 1.** Never work in`
> `   it on Project 1. Never merge a branch into it. It is refreshed at milestones by copying`
> `   the curated `tubitak/` tree. Merging `tubitak-tr` into it would propagate deletions and`
> `   destroy the research record — this has already nearly happened once.`
> `   **Project 2 is the exception (WP17, 2 September 2026):** its canonical copy is`
> `   `tubitak/sr/` in `gencp-validation`. `tubitak/sr/` in this repository is a **frozen`
> `   mirror and must not be edited** — work done here on Project 2 is work that will be lost.`

Dosyadaki başka hiçbir kural değişmemiştir (+7 −4, tümü kural 2 içinde). A'da bu iş
paketinin tek değişikliği budur.

### 10.5 Madde 5 — `00-recon.md`'deki `extent.py` satır çapaları

Ölçüm: B'deki `tubitak/gencp_core/extent.py` blob'u `b5ebce46…`, A'nın `9141da2`
(29 Ağustos) sürümüyle **aynıdır** — yani `00-recon.md`'nin 30 Ağustos'ta okuduğu dosyanın
ta kendisi. B'de bu blob'u taşıyan commit `f386da375e78173ecb715167afe375a027b75ccb`'dir
(30 Ağustos). Çapalar B'de zaten doğru satıra çözülmekteydi; kayan, A'nın kopyasıdır
(`75332cb`, 31 Ağustos). §9 madde 6 bunu ters yönde anlamıştı.

Her çapa, iddia, ölçülen içerik ve sonuç:

| çapa | iddia | `f386da3`'te o satır | sonuç |
|---|---|---|---|
| `#L16` | modül sabitleri 16–27 | `SIZE = 257` (blok 16–27 sabitlerdir) | `f386da3`'e sabitlendi |
| `#L18` | `SUPERSAMPLE = 4` | `SUPERSAMPLE = 4` | sabitlendi |
| `#L21` | `SRC_PX = 257` | `SRC_PX = 257` | sabitlendi |
| `#L22` | `OUT_PX = 256` | `OUT_PX = 256` | sabitlendi |
| `#L23` | `NOMINAL = 10.0` | `NOMINAL = 10.0` | sabitlendi |
| `#L24` | `TRUE_GSD` = 257·10/256 | `TRUE_GSD = SRC_PX * NOMINAL / OUT_PX` | sabitlendi |
| `#L25` | `TILE_M` = 2570 | `TILE_M = SRC_PX * NOMINAL` | sabitlendi |
| `#L27` | `DEFAULT_OVERLAP_M = 640.0`, "seam ratio 1.008" yorumu | aynen | sabitlendi |
| `#L185` | `tile_grid`'in `align_origin` argümanı | `def tile_grid(extent, overlap_m=…, align_origin=None):` | sabitlendi |
| `#L200` | aralık denetimi 200–202 | `raise ExtentError("overlap must be in [0, TILE_M) …")` | sabitlendi |
| `#L228` | `SEC_PER_TILE = 0.48` | `SEC_PER_TILE = 0.48` | sabitlendi |
| `#L203` | `stride = TILE_M - overlap_m` | `tiles = []` | **çapa silindi** |

`#L203` için iki deponun tarihindeki her sürüm taranmıştır: `stride` satırı `f386da3` ve
`6750978`'de (B) **201**, A'da `9141da2`/`ef82289`'da 201, `75332cb`'de 213, `361fa76`'da
166, `f95ad61`'de 110'dadır. **Hiçbir commit'te 203. satırda değildir.** Satır numarası
uydurulmamış; çapa silinip düz dosya bağlantısı bırakılmıştır:

> önce `[extent.py:203](../../gencp_core/extent.py#L203)`
> sonra `[extent.py:203](../../gencp_core/extent.py)`

Bağlantı metnindeki "203" keşif sırasında yapılmış bir hatadır (içerik o sürümde 201.
satırdadır); izinli değişiklik yalnızca bağlantı hedefi olduğundan metin bırakılmıştır.

Sabitlenen 11 çapanın hedef biçimi:
`https://github.com/mvy0502/gencp-validation/blob/f386da375e78173ecb715167afe375a027b75ccb/tubitak/gencp_core/extent.py#L<n>`
— dal adına değil commit'e bağlıdır, bir daha kayamaz. `00-recon.md`: **+12 −12**, hepsi
bağlantı hedefi. A'daki kopya dondurulmuş hâliyle, bu kusur dahil, olduğu gibi durmaktadır.

### 10.6 Doğrulama

**V1 — yalnızca ilk paragraf.** İlk paragraf artık üç işi sayar ve üçüncüsünü "Sentinel-2
görüntüsünü süper çözünürlüğe çıkaran ikinci bir QGIS eklentisi (Proje 2)" olarak adlandırır.
Bu projeyi hiç görmemiş biri, yalnızca bu paragrafı okuyarak depoda üç ayrı işin
bulunduğunu ve birinin süper çözünürlük eklentisi olduğunu öğrenir. Madde 1 tamamdır.

**V2 — iç tutarlılık.** README'de Proje 2'nin yeri ya da eklenti çalışmasının nerede sürdüğü
hakkında kalan her cümle taranmıştır (`devam eder`, `dondurul`, `GenCP'de`, `güncel kopyası`,
`taşınmadan önce`, `iki iş`, `üç iş`):

- satır 3: "Bu depoda üç iş bir arada durmaktadır…" — taşınmayla uyumlu;
- satır 100: "…Proje 2'nin güncel kopyası bu depodadır…" — uyumlu;
- satır 155–156: "…Proje 1 QGIS eklenti iş paketi … GenCP deposunda … devam eder, çünkü GenCP
  modelinden türemektedir. Proje 2 … bu depoda bulunmaktadır; fork'taki kopyası
  dondurulmuştur." — uyumlu;
- satır 160: "`tubitak-tr` bu depoya birleştirilmez…" — merge kuralı, dokunulmamış.

Taşınmayla çelişen cümle **yoktur**; "KURAL bölümü taşınmadan önce yazılmıştır" notu
**kalmamıştır** (`taşınmadan önce` araması 0 sonuç).

**V3 — sürüm notları:** §10.3'te; tam olarak bir satır farklı, sondaki satır sonu sayısı
değişmemiş (1), GenCP bağlantısı kalmamış.

**V4 — B `tubitak/sr/` ağacında bağlantı çözümlemesi:** göreli bağlantı **25** taranmış,
**0 kırık**. WP17'deki 36'dan 25'e düşüş, 11 göreli çapanın mutlak (sabitlenmiş) URL'ye
dönüşmesindendir; mutlak URL'ler çekilmemiştir.

**G1 — birincil kapı, tüm düzenlemelerden sonra, commit'ten önce** (bu rapor dahil):

| depo | karşılaştırılan | yol kümesi | sağlaması değişen | izinli dosya |
|---|---|---|---|---|
| A | **1272** | aynı; beliren/kaybolan/taşınan yok; izlenmeyen 0 | `CLAUDE.md` | 4 |
| B | **1538** | aynı; beliren/kaybolan/taşınan yok; izlenmeyen 0 | `README.md` | 1 |
| | | | `tubitak/sr/docs/00-recon.md` | 2 |
| | | | `tubitak/sr/docs/18-depo-tasima.md` | 3 |

Listede dört izinli dosyadan başka bir şey yoktur; WP17'de kopyalanan 78 dosyanın
`00-recon.md` dışındaki 77'si, Proje 1'in tamamı ve her iki deponun geri kalanı sağlaması
aynı durmaktadır. **Kapı geçilmiştir.** (Rapor yazılmadan önceki ön koşuda liste aynıydı,
eksi bu dosyanın kendisi.)

### 10.7 Commit'ler

Her depoda tek commit, açık yollarla.

- **A** (`tubitak-tr`): `ef14cb475bb9632c615926678db6b10deee8fa5e` — yalnızca `CLAUDE.md`. `git ls-remote origin tubitak-tr` yerel
  `HEAD` ile eşleşmiştir.
- **B** (`main`): bu raporu içeren commit — `README.md`, `00-recon.md`, bu rapor. SHA'sı kendi
  içinde yazılamaz; `git log` ile doğrulanır. İtme `git ls-remote origin main` ile
  doğrulanmıştır.

### 10.8 Brifingin öngörmediği bulgular

1. **Çapa kayması B'de değil A'daydı.** B'nin `extent.py`'si keşfin okuduğu blob'un aynısıdır;
   §9 madde 6'nın "B geride" okuması doğru, "çapalar B'de güvenilmez" çıkarımı yanlıştı.
   Sabitleme yine de yapılmıştır, çünkü B'nin Proje 1 kopyası bir gün yenilenirse göreli
   çapalar kayacaktır.
2. **`#L203` metni keşif hatasıdır**, sürüm kayması değil (§10.5).
3. **Tarih taramasının ilk geçişi boş döndü**: zsh'de `"$c:tubitak/…"` ifadesindeki `:t`
   bir değiştirici (tail modifier) olarak yorumlanmakta, yol bozulmaktadır. `${c}:` ile
   yeniden koşulmuştur; ilk geçişin boş sonucu bir bulgu olarak alınmamıştır.
4. **Sondaki satır sonu, `gh --jq` ile ölçülemez**; jq kendi satır sonunu ekler. WP17'nin
   "tam bayt" iddiası bu yüzden API'den yeniden ölçülmüş ve doğru çıkmıştır (8044, 1).
5. **A'nın `CLAUDE.md`'sinde kural 2 dışında da eski durumu söyleyen yerler vardır**: tablo
   satırı ("Handover copy … Destination only") ve kural 1 ("All work happens here"). Brifing
   "yalnızca bu cümle" dediğinden dokunulmamıştır; karar beklemektedir.
6. **`00-recon.md`'deki diğer 20 çapa** (`infer.py`, `mosaic.py`, `dialog.py`, `gate_g.py`,
   `rasterize.py`, `task.py`; dosyalar A ve B'de aynı) örneklenmiş, iddia edilen içerik
   iddia edilen satırlarda bulunmuştur (ör. `infer.py:27 INPUT_PX = 256`,
   `mosaic.py:53 ov_px = int(round(overlap_m / TRUE_GSD))`, `task.py:22 STAGE_WEIGHTS`).
   Madde 5'in kapsamı dışında olduklarından göreli bırakılmışlardır; aynı kayma riskini
   taşırlar.
7. **G1 sarmalayıcısı, kapı geçmişken FAIL bildirdi.** Ölçüm doğruydu — dört dosya, başka
   hiçbir şey — ama koşulu birleştiren kabuk ifadesi (`a && b || c && d || FAIL=1`) soldan
   sağa bağlandığından, A'nın geçen sonucu B'nin karşılaştırmasına düşüp yanlış negatif
   üretti. Kapı zayıflatılmamış; yalnızca sarmalayıcının mantığı düzeltilip **aynı**
   karşılaştırma yeniden koşulmuştur. Bu projede alışılmış olanın tersi bir arıza —
   geçmesi gerekirken düşen bir denetim — ve yakalanması, listenin çıktıda görünür
   olmasındandır.

---

## 11. WP19 — WP18'den kalan iki madde

**Tarih** 2 Eylül 2026. **Taban çizgisi** A `ef14cb475bb9632c615926678db6b10deee8fa5e`,
B `632d9bbf29d815d570338de04c1248722db3c85f`; iki ağaç da temizdi; her izlenen dosya
manifeste alınmıştır (A **1272**, B **1538**, `/tmp/wp19/`). §1–10 değiştirilmemiştir.
Hiçbir sürüme dokunulmamıştır.

### 11.1 Madde 1 — A'nın `CLAUDE.md`'si kendi içinde tutarlı hâle getirildi

**(a) tablo satırı, önce:**

> `| `mvy0502/gencp-validation` | **Handover copy** for whoever takes the project over | Destination only — see below |`

**sonra:**

> `| `mvy0502/gencp-validation` | **The repository the institute has access to.** Holds both releases (`plugin-v0.2.0`, `sr-plugin-v0.1.0`) and the **canonical home of Project 2** (`tubitak/sr/`) | Project 2 work happens there; for Project 1 it is a destination only — see rule 2 |`

**(b) kural 1, önce:**

> `1. All work happens here, on `tubitak-tr`. This is where you push.`

**sonra:**

> `1. Project 1 work happens here, on `tubitak-tr`; this is where Project 1 is pushed. Project 2`
> `   work happens in `gencp-validation` (rule 2).`

**Brifingin saymadığı üçüncü satır — açıkça belirtilir.** GenCP satırının "Who writes"
hücresi de "All agent work happens here" demekteydi: kural 1'in tablo biçimi, aynı cümle.
Bırakılsaydı V1'in "Proje 2 işinin burada yapılacağını ima eden cümle kalmamalı" ölçütü
sağlanamazdı. Değiştirilmiştir:

> önce `| `mvy0502/GenCP` (this one), branch `tubitak-tr` | **Working repository.** Research record, gate registrations, results, code, QGIS plugin | All agent work happens here |`
> sonra `| `mvy0502/GenCP` (this one), branch `tubitak-tr` | **Working repository.** Research record, gate registrations, results, code, QGIS plugin | Project 1 agent work happens here |`

Dosyada başka hiçbir satır değişmemiştir (+4 −3, üçü de yukarıda). Kural 2 ve sonrası,
fork ilişkisi ve Proje 1'i bağlayan her şey aynen durmaktadır.

### 11.2 Madde 2 — `00-recon.md`'deki "203"

Doğrulama, bu prompt'tan aktarılarak değil ölçülerek yapılmıştır: diğer on bir çapanın
sabitlendiği `f386da375e78173ecb715167afe375a027b75ccb` commit'inde `extent.py`'nin 199–204.
satırları okunmuştur:

```
199     if not 0.0 <= overlap_m < TILE_M:
200         raise ExtentError(f"overlap must be in [0, {TILE_M}) m, got {overlap_m}")
201     stride = TILE_M - overlap_m
202     ox, oy = align_origin if align_origin else (xmin, ymax)
203     tiles = []
```

`stride = TILE_M - overlap_m` yalnızca **201.** satırdadır; B'nin `HEAD`'indeki blob
sabitlenen blob'la aynıdır. Metin 201 yapılmış, çapa `#L201` olarak, aynı commit'e
sabitlenerek geri konmuştur:

> önce `| stride | `TILE_M - overlap_m` = 1930 m at the default | [extent.py:203](../../gencp_core/extent.py) |`
> sonra `| stride | `TILE_M - overlap_m` = 1930 m at the default | [extent.py:201](https://github.com/mvy0502/gencp-validation/blob/f386da375e78173ecb715167afe375a027b75ccb/tubitak/gencp_core/extent.py#L201) |`

`00-recon.md`: +1 −1. On iki çapanın on ikisi de artık aynı commit'e bağlıdır.

**A'daki `00-recon.md` dondurulmuş bir aynadır ve bu kusuru — `#L203` çapası ve "203"
metniyle — bilerek korumaktadır; iki dosya arasındaki fark bir kopya hatası değildir.**

### 11.3 Doğrulama

**G1 — her izlenen dosya, tüm düzenlemelerden sonra, commit'ten önce** (bu bölüm dahil).
Karşılaştırma ifadesi bu kez depo başına tek `if/else`'tir; WP18'deki zincirlenmiş
`&& ||` kullanılmamıştır ve ifade koşulmadan önce okunmuştur.

| depo | karşılaştırılan | yol kümesi | sağlaması değişen | izinli |
|---|---|---|---|---|
| A | **1272** | aynı; beliren/kaybolan/taşınan yok; izlenmeyen 0 | `CLAUDE.md` | 1 |
| B | **1538** | aynı; beliren/kaybolan/taşınan yok; izlenmeyen 0 | `tubitak/sr/docs/00-recon.md` | 2 |
| | | | `tubitak/sr/docs/18-depo-tasima.md` | 3 |

Üç izinli dosyadan başkası yoktur. **Kapı geçilmiştir.**

**V1 — A'nın `CLAUDE.md`'si baştan sona, gelecekteki bir oturumun gözüyle.** "work",
"push", "here", "gencp-validation", "destination", "frozen" geçen her cümle okunmuştur:

- satır 9 (GenCP satırı): "Project 1 agent work happens here" — Proje 1'e sınırlı;
- satır 10 (gencp-validation satırı): "…canonical home of Project 2… Project 2 work happens
  there; for Project 1 it is a destination only" — taşınmayla uyumlu;
- satır 15–16 (kural 1): "Project 1 work happens here… Project 2 work happens in
  gencp-validation" — uyumlu;
- satır 17–22 (kural 2): "destination, never a source, for Project 1… Project 2 is the
  exception… frozen mirror and must not be edited" — uyumlu;
- kalan kurallar (3–12), sahiplik sınırı, eşzamanlılık ve commit politikası: hiçbiri Proje
  2'nin yerinden söz etmez.

Proje 2 işinin A'da yapılacağını ima eden cümle **kalmamıştır.**

**V2 — B'nin `CLAUDE.md`'si.** "Work on this project happens in `mvy0502/GenCP`… Do not
develop here" ve altındaki "Exception… Project 2 lives here… The copy left in GenCP is
frozen. Documentation and installation fixes for Project 2 happen here." A: Proje 1 burada,
Proje 2 orada. B: Proje 1 GenCP'de, Proje 2 burada. İki dosya artık iki projenin de yeri
konusunda **aynı şeyi söylemektedir.**

**V3 — B `tubitak/sr/` ağacında bağlantı çözümlemesi: 28 taranmış, 2 kırık. Sıfır değil.**
İkisi de bu raporun §10.2'sinde, WP18'in README'den **aynen** alıntıladığı satırların
içindedir: `[`tubitak/sr/SOURCE.md`](tubitak/sr/SOURCE.md)`. Yol README'ye görelidir;
`docs/` altından `tubitak/sr/docs/tubitak/sr/SOURCE.md`'ye çözülür ve GitHub bunu bağlantı
olarak işleyip 404 verir. **WP18'in V4'ü raporu yazılmadan önce koşulmuştu** ve rapor bu
iki bağlantıyı sonradan getirmiştir; WP18'in "0 kırık" sonucu kendi raporunu kapsamamıştır.
Düzeltmek §10'a dokunmayı gerektirir; bu brifing §1–10'u dondurduğundan **düzeltilmemiş,
karar için bırakılmıştır** (bkz. §11.5). Bu iş paketinin dokunduğu iki dosyada kırık
bağlantı yoktur.

**V4 — §9'daki maddelerin durumu:**

| §9 | madde | durum |
|---|---|---|
| 1 | P2'nin öncülü yanlıştı | bulgu; eylem gerektirmez — **kapalı** |
| 2 | sürüm notlarındaki ikinci GenCP bağlantısı | WP18 §10.3 — **kapalı** |
| 3 | README girişi "iki iş" | WP18 §10.1 — **kapalı** |
| 4 | README KURAL cümlesi | WP18 §10.2 — **kapalı** |
| 5 | A'nın `CLAUDE.md`'si | WP18 §10.4 kural 2; WP19 §11.1 tablo ve kural 1 — **kapalı** |
| 6 | `extent.py` A ve B'de farklı; çapalar | çapalar WP18/WP19 ile sabitlendi — o kısım **kapalı**. Altta yatan olgu — B'nin **Proje 1** kopyasının A'nın `tubitak-tr`'sinden (`75332cb`, 31 Ağustos) geride olması — **açıktır** ve bu seride kapsam dışıdır: Proje 1 dondurulmuştur, yenilemek ayrı bir devir kararıdır |
| 7 | bayat B klonu | kalıcı klon alındı — **kapalı** |
| 8 | `--notes-file` sondaki satır sonu | WP18 §10.3 ölçüldü — **kapalı** |

**Seri bitmiş ilan edilmemektedir.** Açık kalanlar §11.5'tedir.

### 11.4 Commit'ler

- **A** (`tubitak-tr`): `e5a3d225f71c84d4105fe16c823c6b71b5545152` — yalnızca `CLAUDE.md`; `git ls-remote origin tubitak-tr`
  yerel `HEAD` ile eşleşmiştir.
- **B** (`main`): bu raporu içeren commit — `00-recon.md` ve bu rapor; `git ls-remote origin
  main` ile doğrulanmıştır.

### 11.5 Brifingin öngörmediği bulgular ve karar bekleyenler

1. **§10.2'deki iki kırık bağlantı** (V3). Karar: ya §10.2'deki alıntı satırlarında bağlantı
   sözdizimi etkisizleştirilir (ör. kod bloğuna alınır — alıntı metni değişmez, yalnızca
   biçimi), ya da kabul edilip kayda geçirilir. İkisi de §10'a dokunur; burada yapılmamıştır.
2. **A `CLAUDE.md`'de üçüncü bir satır değiştirilmiştir** (§11.1): brifing iki yer saymıştı,
   V1 ölçütü üçüncüyü zorunlu kılmıştır. Değişiklik aynen alıntılanmıştır.
3. **B'nin Proje 1 kopyası A'dan geridedir** (§11.3 V4, madde 6). Bu seride bilerek
   dokunulmamıştır.
