# WP17 — Proje 2'nin kurumun erişebildiği depoya taşınması

**Tarih** 2 Eylül 2026. **Kaynak** `mvy0502/GenCP`, dal `tubitak-tr`, commit
`f28342b8eb9739ef7cad838bf4474e18fb3873cd`. **Hedef** `mvy0502/gencp-validation`, öntanımlı
dal `main` (uzak `HEAD` sembolik referansından okunmuştur, varsayılmamıştır), taşınma öncesi
`5c55b4f`. Yerel klon bulunamadığından `~/Documents/gencp-validation` altına yeni klon
alınmıştır.

Eklenti, modeller, corpus'lar ve ölçümler değişmemiştir. `tubitak/sr/sr_plugin/` içeriğine
dokunulmamıştır. Bu bir alt-ağaç kopyası ve belge düzeltmesidir; tarih birleştirilmemiştir.

## 1. Öngörüler ve ölçümler

Üç sayı ölçümden önce dosyaya yazılmıştır (`predictions.txt`, 10:02:30 +03; dosya depoya
alınmamıştır, içeriği §14.4'te aynen verilmiştir); ölçümden sonra
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

```text
[`tubitak/sr/SOURCE.md`](tubitak/sr/SOURCE.md) dosyasında kayıtlıdır. (Aşağıdaki KURAL
bölümü bu taşınmadan önce yazılmıştır; oradaki "QGIS eklenti iş paketi GenCP'de devam eder"
cümlesi Proje 1 için geçerlidir.)
```

Kalan satır:

```text
[`tubitak/sr/SOURCE.md`](tubitak/sr/SOURCE.md) dosyasında kayıtlıdır.
```
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

---

## 12. WP20 — alıntı bağlantıları ve Proje 1 fark ölçümü

**Tarih** 2 Eylül 2026. **Taban çizgisi** A `e5a3d225f71c84d4105fe16c823c6b71b5545152`,
B `b47d4222373d86b08e1be9336f859dd3a37d7edf`; iki ağaç da temizdi; her izlenen dosya
manifeste alınmıştır (A **1272**, B **1538**, `/tmp/wp20/`). §1–11, §10.2'deki iki alıntının
sınırlayıcıları dışında değiştirilmemiştir. **A'da hiçbir şey değişmemiş, hazırlanmamış,
commit'lenmemiştir.** Hiçbir sürüme dokunulmamıştır.

### 12.1 Bölüm A — §10.2'deki iki alıntı

İki alıntı bölgesi (silinen üç README satırı, ve "Kalan satır") `> `…`` blok-alıntı
biçiminden ```` ```text ```` çitli kod bloğuna alınmıştır. Alıntının içindeki hiçbir bayt
değişmemiştir; yalnızca sınırlayıcılar.

**V1 — bayt karşılaştırması.** Düzenlemeden önce her bölgenin alıntı baytları (satır başındaki
"> `" ve sonundaki "`" sınırlayıcıları çıkarılarak) `/tmp/wp20/quote_before_{1,2}.txt`'ye,
düzenlemeden sonra çitin içindekiler `quote_after_{1,2}.txt`'ye yazılmış ve `cmp` ile
karşılaştırılmıştır:

| bölge | önce | sonra | sha256 (ilk 16) | sonuç |
|---|---|---|---|---|
| 1 — silinen üç satır | 233 bayt | 233 bayt | `5d1b0a7b655c5007` = `5d1b0a7b655c5007` | **aynı** |
| 2 — "Kalan satır" | 73 bayt | 73 bayt | `861cbcbcdc4e210c` = `861cbcbcdc4e210c` | **aynı** |

Rapor: +10 −4, tümü sınırlayıcı.

**Brifingin öncülü ölçülmüş ve doğru çıkmamıştır.** Brifing (ve WP19 §11.3) bu alıntıların
GitHub'da canlı 404 bağlantısı olarak işlendiğini söylüyordu. Bu iddia WP19'da kod
aralıklarını (`` `…` ``) tanımayan bir düzenli ifadeden gelmişti, işlemeden değil. Bu kez
GitHub'ın kendi işleyicisine (`POST /markdown`, `gfm`) tam kalıplar verilmiştir:

| kalıp | `<a>` etiketi |
|---|---|
| §10.2 özgün 268. satır (blok-alıntı + ters tırnak) | **0** |
| §10.2 özgün 272. satır (satır içi ters tırnak) | **0** |
| §11.3'teki kalan anma (satır içi ters tırnak) | **0** |
| kontrol: çıplak README-göreli bağlantı | 1 (`href="tubitak/sr/SOURCE.md"`) |
| kontrol: yeni çit | 0 |

CommonMark kod aralıklarını bağlantılardan önce çözdüğünden `` `[` `` bir kod aralığıdır ve
bağlantı hiç oluşmaz. Alıntılar hiçbir zaman gezinme olarak işlenmemiştir; kusur, WP19'un
denetleyicisindeydi. Çit yine de doğru biçimdir — aynen alıntı metin olarak durmalıdır — ve
brifingin istediği gibi yapılmıştır.

**V2 — bağlantı denetimi.** Denetleyici artık işleyiciyi modellemektedir: çitli kod blokları
**ve** satır içi kod aralıkları bağlantı taramasından çıkarılır; bu davranış yukarıdaki
işleyici tablosuyla doğrulanmıştır, varsayılmamıştır. B `tubitak/sr/**/*.md`: **24 göreli
bağlantı taranmış, 0 kırık.** (Yalnızca çitleri çıkaran ara koşu 28/1 vermişti; o "1",
§11.3'teki kod aralığıydı — işleyiciye göre bağlantı değil.)

### 12.2 Bölüm B — ölçüm, ayrı belgede

Proje 1 fark ölçümü [`19-proje1-fark-olcumu.md`](19-proje1-fark-olcumu.md)'dedir:
karşılaştırılan commit'ler, 12 farklı yolun tablosu (tarih, tek cümle, kova), tek taraflı
dosya listeleri (A'da 4, B'de 269), işin büyüklüğü ve seçenekler. Hiçbir Proje 1 dosyası
değiştirilmemiştir. Ölçümün en belirleyici bulgusu buraya bir cümleyle alınır: **kurumun
kurduğu `plugin-v0.2.0` zip'i B'nin ağacıyla bayt bayt aynıdır; A hem ağacın hem sürümün
önündedir ve WP12'nin QGIS 3.x düzeltmesi hiçbir Proje 1 sürümüne girmemiştir.**

### 12.3 G1

İfade depo başına tek `if/else`'tir ve koşulmadan önce okunmuştur.

| depo | karşılaştırılan | yol kümesi | sağlaması değişen | izinli |
|---|---|---|---|---|
| A | **1272** | aynı; izlenmeyen 0 | **hiçbiri** | — (V3) |
| B | **1538** | aynı; beliren/kaybolan/taşınan yok; izlenmeyen 1 (yeni belge) | `tubitak/sr/docs/18-depo-tasima.md` | 1 |
| | | | `tubitak/sr/docs/19-proje1-fark-olcumu.md` (yeni) | 2 |

**V3:** A'nın manifesti taban çizgisiyle aynıdır, 0 değişen dosya. Kapı geçilmiştir.

### 12.4 V4 — `19-proje1-fark-olcumu.md`, hiç görmemiş gözle

Belge kendi başına şunları verir: neyin hangi commit'lerde karşılaştırıldığı; 12 farklı
yolun her biri için hangi tarafın yeni olduğu (commit tarihiyle), farkın tek cümlelik
anlatımı ve kovası; tek taraflı dosyaların ne olduğu; K kovasının 10 dosya olduğu ve
yenilemenin beş adımı; beş seçenek, her birinin bedeli ve riskiyle, önerisiz. Karar için
yeterli görünen olgu, kurumun kurduğu zip'in B ile aynı olmasıdır — belge bunu önden verir.

Okuyucunun yine de sormak zorunda kalacağı iki şey vardır ve belge bunları
**yanıtlamaz**: (1) WP12'nin QGIS 3.x düzeltmesinin kurum için gerçekten gerekli olup
olmadığı — yani kurumun makinelerinde `rasterio`'nun QGIS'in Python'unda bulunup
bulunmadığı; bu, `12-qt5-uyumluluk.md`'de kurumun bildirdiği arızadan çıkarılır ama bu
belgede ölçülmemiştir. (2) Proje 1'in "bitmiş ve teslim edilmiş" statüsünün yeni bir sürümü
dışlayıp dışlamadığı — bu bir sözleşme/teslim sorusudur, ölçüm sorusu değil. Bu iki soru
dışında belge karar için yeterlidir.

### 12.5 Commit

- **B** (`main`): bu raporu ve yeni belgeyi içeren commit; `git ls-remote origin main` ile
  doğrulanmıştır. **A'ya commit yapılmamıştır.**

### 12.6 Brifingin öngörmediği bulgular

1. **"Canlı 404 bağlantısı" öncülü yanlıştı** (§12.1); WP19'un V3 bulgusu denetleyici
   hatasıydı. Düzeltme yine de doğru biçim olduğundan yapılmıştır.
2. **B'deki iki Proje 2 belgesi, B'de olmayan iki dosyayı anmaktadır**
   (`13-cevrimdisi-kurulum.md` → `tubitak/tool/qgis_ortam_raporu.py`;
   `15-kontroller.md` ve `03a-wald-corpus.md` → `tubitak/docs/evidence/wp15/corpus_checks.json`).
   İkisi de `tubitak/sr/` dışında durduğu için WP17'nin alt-ağaç kopyasına girmemiştir;
   atıflar düz metin olduğundan bağlantı denetimi görmemiştir. Düzeltilmemiş, `19`'un K
   kovasına yazılmıştır.
3. **B'nin `.gitignore`'u `icon.png`'yi yutar**; Proje 1 ağacı B'ye yenilense bile simge
   izlenmez. `19` §3'te kayıtlıdır.
4. Kurumun kurduğu zip'in kaynağının B olduğu (§12.2) bu brifingin sorduğu bir şey değildi;
   karar için en belirleyici olgu olduğu için ölçülmüştür.

---

## 13. WP21 — Proje 2'nin kurumun okuduğu depoda kendine yeterli olması

**Tarih** 2 Eylül 2026. **Taban çizgisi** A `e5a3d225f71c84d4105fe16c823c6b71b5545152`,
B `41dd36af3a5d21953c502e4707fc4b5e38cc16a1`; iki ağaç da temizdi; her izlenen dosya manifeste
alınmıştır (A **1272**, B **1539**, `/tmp/wp21/`). §1–12 değiştirilmemiştir. **A'da hiçbir
şey değişmemiş, hazırlanmamış, commit'lenmemiştir.** Hiçbir Proje 1 dosyasına, hiçbir sürüme
dokunulmamıştır.

### 13.1 Adım 1 — iki dosya, dosya başına karar

**`qgis_ortam_raporu.py`.** B'de anıldığı tek yer, okuyucuyu yönlendiren bir cümledir
(`13-cevrimdisi-kurulum.md:29`):

> Kurulumdan önce `tubitak/tool/qgis_ortam_raporu.py` dosyasının tamamı QGIS'in Python
> Konsolu'na yapıştırılıp çalıştırılır…

Dosyanın kendisi (A `tubitak/tool/`, 85 satır) kurum makinesinde QGIS'in Python ortamını
raporlayan, hiçbir şey kurmayan, internet gerektirmeyen tek dosyalık bir betiktir; başlığı
"bu dosyanın TAMAMINI kopyalayıp konsola yapıştırın" der. **Kurumdaki okuyucu bu dosyayı
bizzat kullanır ve belge onu burada bekletir.** Karar: **(a)**, kopyalanmıştır —
`tubitak/sr/tools/qgis_ortam_raporu.py` (`tools/` zaten `make_slides_v2.py`'yi barındırır).
Kopyalama yapılmadan önce hedef yol `git check-ignore` ile sınanmış, yoksayılmadığı
görülmüştür. Blob A'dakiyle aynıdır (`ebcbba28820f`). Atıf düzeltilmiştir:

> önce `Kurulumdan önce `tubitak/tool/qgis_ortam_raporu.py` dosyasının tamamı QGIS'in Python`
> sonra `Kurulumdan önce `tubitak/sr/tools/qgis_ortam_raporu.py` dosyasının tamamı QGIS'in Python`

**`corpus_checks.json`.** B'de iki ayrı dosya adı bu adı taşır. (1) `15-kontroller.md:6`:
"**Evidence** `tubitak/docs/evidence/wp15/corpus_checks.json`" — WP15'in 11/11 sonucunun
kanıt kaydı, 2,7 KB, bir koşunun dondurulmuş çıktısı. (2) `03a-wald-corpus.md:568`:
"`tubitak/data/sr_wald_corpus/evidence/corpus_checks.json`. Exit 0, 9 of 9 cases…" — WP3A'nın
**başka** bir koşusunun, `tubitak/data/` altındaki, politika gereği hiçbir depoya girmemiş
çıktı yolu. Kurumdaki okuyucu (1)'i kullanmaz ama raporun dayandığı kanıt olarak orada
bekler; kaydın kendisi değişmeyeceğinden ikinci kopyanın kayma riski yoktur ve kendine
yeterlilik taşınmanın amacıdır. Karar: **(a)** —
`tubitak/sr/docs/evidence/wp15/corpus_checks.json` (yoksayılmıyor; blob `8209aaa79abb`).
(2) dosya yolu olarak doğru bir tarihsel ifadedir, düzeltilmemiştir. Atıf:

> önce `**Evidence** `tubitak/docs/evidence/wp15/corpus_checks.json`.`
> sonra `**Evidence** `tubitak/sr/docs/evidence/wp15/corpus_checks.json`.`

Kaynak kaydı `tubitak/sr/SOURCE.md`'ye ek olarak yazılmıştır: depo, A'daki yol, A'daki son
commit, blob. §12.6/2 ve `19` §3'teki "dosya B'de yoktur" cümleleri WP20 anındaki ölçümün
kaydıdır ve değiştirilmemiştir; bu bölüm onları geçersiz kılar. **A'daki `tubitak/sr/`
aynası dondurulmuştur ve bu iki dosyayı taşımaz; A–B farkı kopya hatası değil, bu ekin
sonucudur.**

### 13.2 Adım 2 — kök neden: düz metindeki dosya adları

`tubitak/sr/tools/check_named_files.py` yazılmıştır: `tubitak/sr/**/*.md` içinde bilinen
bir uzantıyla biten her belirteci toplar, `tubitak/sr/` altında o adı taşıyan dosya var mı
bakar, olmayanları **ayıklama listesi** olarak basar (karar değil), her birinin depoda başka
yerde bulunup bulunmadığını da yazar. Bilinen-yanlış önce: var olamayacak bir ad ekilir, o
bildirilmeden gerçek tarama basılmaz. Anlamadığı argümanı reddeder (`--overlap=2560`,
fazladan konumsal, olmayan `--root` → çıkış 2). Çıktısı
`tubitak/sr/docs/evidence/wp21/named_files.json`'dadır.

**Sayımlar:** 31 markdown dosyası; **193** ayrı ad; **103** `tubitak/sr/` altında çözülüyor;
**90** çözülmüyor. Doksanın ayıklaması, her ad için cümlesi okunarak:

| sınıf | adet | örnekler | neden meşru |
|---|---|---|---|
| Sürüm varlığı (ağaçta değil, sürümde) | 10 | `SAMPLE_*.tif`, `SHA256SUMS.txt`, `gencp_sr_x4_b4.onnx`, `gencp_sr_tci_x4_b3_v2.onnx`, `gencp_C2_fp32.onnx`, `gencp_plugin.zip`, `clcplus_2021_turkey_10m.tif`, `turkey-2026-08-19.osm.pbf` | B'nin üç sürümünden indirilir |
| `tubitak/data/` altı koşu çıktısı ya da girdi (politika gereği depoda değil; belgeler yolu `tubitak/data/…` diye yazar) | 44 | `best.pt`, `last.pt`, `train_record.json`, `chips_*.npy`, `manifest.csv`, `corpus.json`, `leakage.json`, `eval_x4.FIRSTRUN.json`, `SCL.tif`, `TCI_36TVK_20260430.tif`, `eox_*.tif/.png`, `three_panel_36SXJ.png`, `fixture_1024.tif`, `gencp_sr_tci_x4_b3.onnx` (aşılmış v1) … | Ölçümün kaydı raporlardadır; ham çıktı depoya girmez (CLAUDE.md 4) |
| Depoda `tubitak/sr/` dışında mevcut (Proje 1 kodu, demo, kaggle) | 14 | `infer.py`, `rasterize.py`, `vectors.py`, `download_task.py`, `coverage_block.py`, `plugin-field-test.md`, `dialog.png`, `confidence_layer.png`, `gencp_demo.qgz`, `phase-c-config.md`, `train_c1_c2.py`, `prepare_dataset.sh`, `setup_kaggle_cli.sh`, `dataset-metadata.json` | Denetim "başka yerde" sütununda gösterir; B'de vardır |
| Üçüncü taraf / araç ortamı | 8 | `sentinel2.py`, `setup.cfg` (sensorsio/aracın), `serialization.py`, `storage.py`, `torch.onnx` (torch), `get-pip.py`, `WMTSCapabilities.xml` (EOX sunucusu), `sentinel.py` | Bizim dosyamız değildir |
| Ad kalıbı / örnek / uzantı anması | 11 | `_sr_x2.tif`, `_sr_x4.tif`, `_2m5_sisr.tif`, `..._2m5_sisr.tif`, `_2m5_bicubic.tif`, `some.tif`, `.osm.pbf`, `B02.tif`, `.cancel_target.tif`, `cancel_target.tif`, `36SVJ_TCI_bicubic_x2.tif` | Dosya adı değil, biçim |
| Yazarın makinesindeki yapılandırma, keşifte envanter olarak anılmış | 2 | `kaggle.json`, `.modal.toml` | Kimlik dosyaları; depoya girmez |
| Yalnızca A'da, Proje 1 / derleme (bilerek dokunulmadı) | 2 | `icon.png`, `build_plugin_zip_windows.py` | `19` §3'te kayıtlı; Proje 1 sürüm işine ait |
| **Yazarın makinesindeki betik / kayıt, rapor tarafından anılmış** | 4 | `norm_probe.py` ("scratchpad/" diye açıkça), `wp16_repro.py` (yığın izinde), `host_wsx4.py` ("depo ağacının dışında" diye açıkça), `predictions.txt` | Kurum okuyucusuna verilmiş söz değil; **ama araştırmacı için yeniden üretilebilirlik açığı** — `make_slides_v2.py` ile kapatılan arıza şeklinin aynısı. Düzeltilmemiştir: A'da yoktur, kopyalanacak bir kaynak yoktur; izinli liste dışıdır. Karar bekler |
| **Okuyucuya verilmiş ve B'den tutulamayan söz** | 3 | `MANIFEST.json` (tekerlek kiti), `gencp_plugin_win_amd64.zip`, `gencp_plugin.zip` (98.410 baytlık WP13 yapısı) | **Aşağıda, V5** |

Toplam 90 = 10 + 44 + 14 + 8 + 11 + 2 + 2 + 4 + 3 — biri geçmiş iki üst satırla çakışan
`gencp_plugin.zip`, sürüm varlığı olarak da (73 KB, `plugin-v0.2.0`) sayılmıştır; sözü
tutulmayan olan 98.410 baytlık **yeni** yapıdır. **Bu iş paketinde düzeltilebilen gerçek
kusur: 2** (Adım 1'in iki dosyası; ikisi de düzeltilmiştir). **Düzeltilemeyen gerçek kusur: 3**
(V5).

### 13.3 G1

İfade depo başına tek `if/else`'tir ve koşulmadan önce okunmuştur.

| depo | karşılaştırılan | yol kümesi | değişen / eklenen | sınıf |
|---|---|---|---|---|
| A | **1272** | aynı; izlenmeyen 0 | **hiçbiri** (V4) | — |
| B | **1539** | aynı; beliren/kaybolan/taşınan yok | `tubitak/sr/docs/13-cevrimdisi-kurulum.md`, `tubitak/sr/docs/15-kontroller.md`, `tubitak/sr/SOURCE.md` (değişen) | 2 / 1 |
| | | | `tubitak/sr/tools/qgis_ortam_raporu.py`, `tubitak/sr/docs/evidence/wp15/corpus_checks.json` (eklenen) | 1 |
| | | | `tubitak/sr/tools/check_named_files.py`, `tubitak/sr/docs/evidence/wp21/named_files.json` (eklenen) | 3 |
| | | | `tubitak/sr/docs/18-depo-tasima.md` (bu bölüm) | 4 |

Sekiz yolun sekizi de `tubitak/sr/` altındadır ve dört sınıftan birine girer. Kapı
geçilmiştir.

### 13.4 V1–V4

**V1.** İki atıf yeni biçimleriyle §13.1'de aynen verilmiştir; ikisi de B'deki bir yola
çözülür (`ls` ile doğrulanmıştır). `18` §12.6 ve `19` §3'teki anmalar WP20 kaydıdır, A yolunu
adlandırır ve o yol A'da hâlâ vardır.

**V2.** Denetim temiz çıkmaz — tasarımı gereği: 90 ad çözülmez ve çıkış kodu 1'dir. Doksanın
her biri §13.2'de sınıflandırılmıştır; meşru olmayan 3'ü V5'tedir.

**V3.** Bağlantı denetimi (çitler ve kod aralıkları hariç, WP20'de GitHub işleyicisiyle
doğrulanan model): B `tubitak/sr/**/*.md` — **25 göreli bağlantı, 0 kırık.**

**V4.** A'nın manifesti taban çizgisiyle aynıdır: **0 değişen dosya**; A'da hiçbir şey
hazırlanmamıştır.

### 13.5 V5 — kurumdaki bir okuyucu gibi belgeleri izlemek

`10-kurulum.md` baştan sona, ve adı geçen dosyaları anan belgeler (`13-cevrimdisi-kurulum.md`,
`15-kontroller.md`), yalnızca B ve B'nin sürümleri elde varken izlenmiştir.

**Çevrimiçi ya da `onnxruntime`'ı hazır makine — EVET.** Süper çözünürlük eklentisi
(`gencp_super_resolution.zip`), üç model, iki örnek raster, `SHA256SUMS.txt`: hepsi
`sr-plugin-v0.1.0`'da. Proje 1 eklentisi (`gencp_plugin.zip`, `gencp_C2_fp32.onnx`):
`plugin-v0.2.0`'da. Veri: `veri-turkiye-2026-08-31`'de. Ortam raporu betiği: artık
`tubitak/sr/tools/`'da. Kurulum kılavuzu: bu depoda. Okuyucu A'ya hiç gitmez.

**İnternetsiz makine, `onnxruntime` yok — HAYIR.** `10-kurulum.md` §7.5 adım 2 okuyucuyu
"§3'teki çevrimdışı tekerlek kiti"ne gönderir; §3 ve `13-cevrimdisi-kurulum.md` §1 kiti
"`kit/` klasörü, 16 `.whl` + `MANIFEST.json`, 57,6 MB" diye anlatır. **Kit hiçbir sürümde
yoktur;** yalnızca A'nın yoksayılan `tubitak/data/kit/`'inde durmaktadır. Aynı belge iki
Proje 1 yapısını "iki ayrı sürüm dosyası" diye sunar: `gencp_plugin.zip` **98.410 bayt** ve
`gencp_plugin_win_amd64.zip` **15.935.709 bayt** (`_vendor/` gömülü). **İkisi de
yayımlanmamıştır;** `plugin-v0.2.0`'daki `gencp_plugin.zip` 26 Ağustos'un 73 KB'lık,
WP12/WP13 öncesi yapısıdır; Windows yapısı yalnızca A'nın `tubitak/data/dist/`'indedir.
Dolayısıyla internetsiz bir Windows makinesinde, `onnxruntime` yoksa, belgelerin anlattığı
yolun **hiçbiri** B'den yürütülemez.

Eksik olan, tam olarak: (1) tekerlek kiti (`kit/`, 57,6 MB) bir sürüm varlığı olarak;
(2) `gencp_plugin_win_amd64.zip` bir sürüm varlığı olarak; (3) 98.410 baytlık `gencp_plugin.zip`
ya bir sürüm olarak ya da belgede "yayımlanmadı" notuyla. Üçü de Proje 1 eklentisinin sürüm
işidir (`19` §5, S3) ve bu iş paketinin kapsamı dışında bırakılmıştır; burada hiçbiri
yapılmamıştır. **İş bitmiş ilan edilmemektedir.**

### 13.6 Brifingin öngörmediği bulgular

1. **Çevrimdışı kurulum yolu B'den yürütülemez** (V5). Bu, iki dosyanın eksikliğinden daha
   büyük bir açıktır ve ancak adları tek tek okuyunca görülmüştür; bağlantı denetimi de,
   Adım 2'nin denetimi de tek başına bunu "kusur" diye işaretleyemez — üçü de meşru görünen
   "sürüm varlığı" sınıfına benzer.
2. **Raporlar dört yazar-makinesi betiğini/kaydını anmaktadır** (`norm_probe.py`,
   `wp16_repro.py`, `host_wsx4.py`, `predictions.txt`). İkisi (`norm_probe.py`,
   `wp16_repro.py`) hâlâ oturum çalışma dizinindedir ve depoya alınabilir; karar bekler.
3. **`SOURCE.md` eki ilk denemede bozuk yazılmıştır**: tırnaksız bir heredoc'ta zsh, ters
   tırnaklı yolları komut olarak çalıştırdı. Fark edilmiş, `HEAD` sürümü geri alınıp ek
   Python ile yazılmıştır (+15 −0).
4. **`icon.png`, gözlem:** yalnızca A'dadır; B'nin `.gitignore`'u (`*.png`) onu yoksayar; sürüm
   zip'inde vardır. Proje 1'e aittir; dokunulmamıştır.
5. `03a-wald-corpus.md:568` ile `15-kontroller.md:6` aynı adı taşıyan **iki farklı**
   dosyayı anar (9 vakalık WP3A koşusu, 11 vakalık WP15 koşusu); ilki veri yolu olarak
   doğrudur ve WP15 kaydı onu aşar.


---

## 14. WP22 — çevrimdışı tekerlek kitinin yayımlanması, ve depoda olmayan dosyaların anılmaması

**Tarih** 2 Eylül 2026. **Taban çizgisi** A `e5a3d225f71c84d4105fe16c823c6b71b5545152`,
B `7b9e975d7ad12ea7d62ebb6d2852d2147bf14fce`; iki ağaç da temizdi; her izlenen dosya manifeste
alınmıştır (A **1272**, B **1543**, `/tmp/wp22/`). §1–13 değiştirilmemiştir — tek istisna, §1'de
`predictions.txt`'yi anan cümledir; Adım 4 her anan cümlenin düzeltilmesini istediğinden,
o cümleye "dosya depoya alınmamıştır, içeriği §14.4'te" eklenmiştir (+2 −1, aşağıda). **A'da
hiçbir şey değişmemiş, hazırlanmamış, commit'lenmemiştir.** Var olan hiçbir sürüme
dokunulmamıştır; bir sürüm **oluşturulmuştur**. Dosya içerikleri Python ile yazılmıştır;
tırnaksız heredoc kullanılmamıştır.

### 14.1 Adım 1 — kit, yayımlanmadan önce (V1, V2)

**Kaynak:** A `tubitak/data/kit/` (yoksayılan yol), 31 Ağustos 2026'da macOS üzerinde
`pip download --only-binary=:all: --platform win_amd64 --python-version 3.12 --implementation cp`
ile `rasterio onnxruntime osmium` için indirilmiştir. Her tekerleğin sağlaması **diskteki
dosyadan** hesaplanmış, manifestle karşılaştırılmıştır: **16/16 aynı, 0 uyuşmazlık**; toplam
60.446.086 bayt (57,6 MiB), manifestle aynı.

| dosya | dağıtım | sürüm | py | abi | platform | bayt | sha256 (ilk 16) | lisans |
|---|---|---|---|---|---|---|---|---|
| affine-3.0.1-py3-none-any.whl | affine | 3.0.1 | py3 | none | any | 10.887 | `cda3b303325e7bf2` | BSD-3 |
| attrs-26.1.0-py3-none-any.whl | attrs | 26.1.0 | py3 | none | any | 67.548 | `c647aa4a12dfbad9` | MIT |
| certifi-2026.7.22-py3-none-any.whl | certifi | 2026.7.22 | py3 | none | any | 136.983 | `62f22742b58a1a33` | MPL-2.0 |
| charset_normalizer-3.5.1-cp312-cp312-win_amd64.whl | charset_normalizer | 3.5.1 | cp312 | cp312 | win_amd64 | 200.551 | `3617ac3cfd8b9888` | MIT |
| click-8.5.0-py3-none-any.whl | click | 8.5.0 | py3 | none | any | 125.251 | `255bc9599cf7748b` | BSD-3 |
| flatbuffers-25.12.19-py2.py3-none-any.whl | flatbuffers | 25.12.19 | py2.py3 | none | any | 26.661 | `7634f50c427838bb` | Apache-2.0 |
| idna-3.19-py3-none-any.whl | idna | 3.19 | py3 | none | any | 68.550 | `815e7be7a7806d54` | BSD-3 |
| numpy-2.5.2-cp312-cp312-win_amd64.whl | numpy | 2.5.2 | cp312 | cp312 | win_amd64 | 12.464.674 | `28ac63476ec76514` | BSD-3 (+0BSD, MIT, Zlib) |
| onnxruntime-1.29.0-cp312-cp312-win_amd64.whl | onnxruntime | 1.29.0 | cp312 | cp312 | win_amd64 | 14.001.407 | `4acf2b4948b7ede8` | MIT |
| osmium-4.3.1-cp312-cp312-win_amd64.whl | osmium | 4.3.1 | cp312 | cp312 | win_amd64 | 1.811.488 | `0604b866d4e875fa` | BSD-2 |
| packaging-26.3-py3-none-any.whl | packaging | 26.3 | py3 | none | any | 129.956 | `d7193f7c8e4e93f4` | Apache-2.0 / BSD-2 |
| protobuf-7.36.0-cp310-abi3-win_amd64.whl | protobuf | 7.36.0 | cp310 | abi3 | win_amd64 | 453.731 | `1781cc1de61249b7` | BSD-3 |
| pyparsing-3.3.2-py3-none-any.whl | pyparsing | 3.3.2 | py3 | none | any | 122.781 | `850ba148bd908d7e` | MIT |
| rasterio-1.5.1-cp312-cp312-win_amd64.whl | rasterio | 1.5.1 | cp312 | cp312 | win_amd64 | 30.621.456 | `6fbafe970d44ec06` | BSD-3 |
| requests-2.34.2-py3-none-any.whl | requests | 2.34.2 | py3 | none | any | 73.075 | `2a0d60c172f83ac6` | Apache-2.0 |
| urllib3-2.7.0-py3-none-any.whl | urllib3 | 2.7.0 | py3 | none | any | 131.087 | `9fb4c81ebbb1ce95` | MIT |

Lisanslar tekerleklerin `METADATA`'sından okunmuştur; on altısı da yeniden dağıtıma izin
verir, hiçbiri dışarıda bırakılmamıştır.

**Platform ve Python.** Etiketler `win_amd64` + `cp312` (`protobuf` `abi3`, saf-Python olanlar
`any`); hedef **Windows 64 bit, CPython 3.12**. Kılavuz bunu söyler mi? `10-kurulum.md`
söylemez; delege ettiği `13-cevrimdisi-kurulum.md` 24. satırda **"Windows 64 bit, Python 3.12
(cp312)"** der ve 36. satırda "Python sürümü 3.12 değilse bu kit kullanılmamalıdır; rapordaki
`abi tag` `cp312` yazmalıdır" diye ölçmeyi şart koşar. Etiketlerle uyuşur; çözülecek bir
çelişki bulunmamıştır.

**Kapanış (V2), iki yolla.** (i) Her tekerleğin `Requires-Dist` beyanı, `sys_platform=win32`
/ `python_version=3.12` işaretleyicileri değerlendirilerek çözülmüş: **kit kendi beyan ettiği
bağımlılıklar altında kapalıdır**, eksik yoktur. (ii) `pip download --no-index
--find-links=<kit> --platform win_amd64 --python-version 3.12` ağ olmadan çözmüştür:
`rasterio onnxruntime osmium` → **16 tekerlek**; `rasterio onnxruntime` → **11 tekerlek**.

**Kapanış, eklenti başına — Adım 1B.** Her eklentinin kodundan (B'deki), üçüncü taraf içe
aktarmaları dosya ve düzey (modül / işlev içi) ayrımıyla çıkarılmıştır:

| eklenti | çalışma zamanı ihtiyacı | kitte | kitte **değil** |
|---|---|---|---|
| **Proje 2** (`sr_plugin`, `sr_core`) | `rasterio`, `onnxruntime` (yalnızca model yöntemleri), `numpy`, `PIL` (`upsample.py`, `mosaic.py` — bikübik dahil **her yöntem**), `yaml` (yalnızca `.yaml` künyeli model) | rasterio, onnxruntime, numpy | **Pillow**, **PyYAML** |
| **Proje 1** (`qgis_plugin`, `gencp_core`) | `rasterio`, `onnxruntime`, `numpy`, `PIL`, `scipy` (`confidence`, `mosaic`, `rasterize`), `shapely` (`rasterize`, `index_cache`, `_pbf_rows`), `osmium` (`.pbf`), **`geopandas`** (`PbfIndex`, `fetch_pbf` — yani çevrimdışı `.pbf` yolunun kendisi), `osmnx`+`geopandas` (yalnızca çevrimiçi `fetch`) | rasterio, onnxruntime, osmium, numpy, requests | **Pillow, scipy, shapely, geopandas, osmnx** |

Verdikt, ikiye ayrılarak: **Proje 2 için kit, `rasterio`/`onnxruntime` eksiğini kapatır; `Pillow`
QGIS Windows kurulumuyla geliyorsa yeterlidir** — bu bir varsayımdır ve ortam raporu betiği
`Pillow`'u ölçmemektedir (ölçtükleri: rasterio, onnxruntime, osmium, numpy, shapely, pyproj).
**Proje 1 için kit yeterli değildir:** çevrimdışı `.osm.pbf` yolu `geopandas` ister; `geopandas`
kitte yoktur ve QGIS'in Windows kurulumuyla gelmez. Bu, kağıt üstünde kapatılmamış, sürüm
notlarına ve buraya olduğu gibi yazılmıştır; Proje 1 sürüm işinin açık maddesidir.

**Doğrulamanın sınırı.** Bu makine macOS'tur. Manifest, etiketler, lisanslar ve kapanış
doğrulanmıştır; **kurulum Windows'ta çalıştırılmamıştır.** Sürüm notları bunu aynen söyler.

### 14.2 Adım 2 — sürüm (V3)

Adı ne olduğuna göre konmuştur, projeye göre değil (Adım 1B): etiket
**`kit-win_amd64-py312-2026-08-31`**, başlık "Çevrimdışı kurulum kiti — Windows 64 bit,
Python 3.12 tekerlekleri, iki QGIS eklentisi için (2026-08-31)". Var olan etiket biçimini izler
(`veri-turkiye-2026-08-31`), platformu ve Python sürümünü adında taşır; başka bir platform için
ikinci bir kit yan yana durabilir. `latest` **değildir** (`plugin-v0.2.0` kalmıştır).

Zip yalnızca `wheels/` (16) ve `MANIFEST.json` içerir. Kit klasöründeki `KURULUM.md` ve
`qgis_ortam_raporu.py` kopyaları **alınmamıştır**: ikincisi B'dekiyle aynıdır, ilki
`13-cevrimdisi-kurulum.md`'nin 29. satırda geride kalmış bir sürümüdür — yayımlanmış ikinci bir
kopya kayar. Zip içindeki 16 tekerlek `MANIFEST.json`'a karşı yeniden sağlanmıştır: 16/16.

Notlar Türkçedir: ne olduğu, hedef, **paket-paket hangi eklentinin ihtiyaç duyduğu**, neyi
kapsamadığı (iki eklenti için ayrı ayrı), `certutil` ile aktarım doğrulaması,
`13-cevrimdisi-kurulum.md` ve `10-kurulum.md` §7.5'e işaret, Windows'ta çalıştırılmadığı
cümlesi, lisanslar.

**API'den geri okuma:** üç varlık indirilmiş ve yeniden sağlanmıştır.

| varlık | API boyut | indirilen sha256 | yerel sha256 | |
|---|---|---|---|---|
| `gencp_kit_win_amd64_py312.zip` | 59.959.899 | `c9fabbebed86…` | `c9fabbebed86…` | **aynı** |
| `MANIFEST.json` | 3.274 | `bb2658bf6818…` | `bb2658bf6818…` | **aynı** |
| `SHA256SUMS.txt` | 176 | `88fe7271d2f6…` | `88fe7271d2f6…` | **aynı** |

`sha256sum -c SHA256SUMS.txt` indirilen dosyalarda: ikisi de OK. `sr-plugin-v0.1.0` 7 varlık,
`plugin-v0.2.0` 2 varlık, dokunulmamış.

### 14.3 Adım 3 — kılavuz

Kiti anan yerler aranmıştır (`kit/`, `tekerlek kiti`, `.whl`, `MANIFEST.json`, `wheel`):
`10-kurulum.md` §7.5 ve §3, `13-cevrimdisi-kurulum.md` §1 ve komutlar (`C:\gencp_kit\wheels`
— makinedeki klasör, değişmez), `09-release-notes-draft.md:20` (taslak kayıt, değişmez),
`00-recon.md:268` ("wheel" genel anlamda). Üç düzenleme:

- `10-kurulum.md` §3 tablosuna bir satır **eklenmiştir** (§7.5 "§3'teki kit" diyordu, §3'te kit
  **yoktu** — sarkık bir çapraz atıf; brifing bunu öngörmemişti):
  `| **Her ikisi — çevrimdışı Python paketleri** … | gencp_kit_win_amd64_py312.zip … | <sürüm URL'si> … |`
- `10-kurulum.md` §7.5 adım 2, önce: `2. YOK ise §3'teki çevrimdışı tekerlek kiti ile kurulur ve **QGIS yeniden başlatılır.**`
  sonra: `2. YOK ise §3'teki çevrimdışı tekerlek kiti (kit-win_amd64-py312-2026-08-31 sürümündeki gencp_kit_win_amd64_py312.zip) ile kurulur ve **QGIS yeniden başlatılır.**`
- `13-cevrimdisi-kurulum.md` §1, "toplam 57,6 MB." cümlesinden sonra üç cümle **eklenmiştir**:
  kitin hangi sürümde hangi dosya olarak yayımlandığı, açılınca bu klasörün elde edildiği,
  notların kapsamı listelediği.

İki Proje 1 zip'ini anlatan cümlelere dokunulmamıştır.

### 14.4 Adım 4 — dört betik

| betik | durum | yapılan |
|---|---|---|
| `norm_probe.py` | oturum çalışma dizininde duruyordu (2.393 bayt, 30 Ağu 21:06) | `tubitak/sr/tools/`'a alındı (yoksayılmıyor); `07-x4-model.md:37` yolu adlandırır |
| `wp16_repro.py` | duruyordu (5.359 bayt, 1 Eyl 16:42) | `tubitak/sr/tools/`'a alındı; `16-checkpoint.md` yığın izinin altına yolu adlandıran bir cümle eklendi (iz aynen kaldı) |
| `host_wsx4.py` | yalnızca yazarın makinesinde | `05-referans-arac.md:234` ve `17-wsx4-hizalama.md:137` "korunmamıştır" diyecek biçimde düzeltildi |
| `predictions.txt` | **brifing "yok" demişti; oturum çalışma dizininde duruyor** (221 bayt) | betik değil, izinli listede yok; depoya alınmadı. §1'deki cümle düzeltildi; içeriği aşağıda aynen |

`predictions.txt`, aynen:

```text
WP17 predictions, written before measurement
P1 files under tubitak/sr/ in A            : 130
P2 md links in tubitak/sr/ leaving the tree : 40
P3 files under tubitak/sr/ in B @5c55b4f    : 90
Wed Sep  2 10:02:30 +03 2026
```

Düzeltilen cümleler, önce/sonra:

- `07-x4-model.md`: `Path: scratchpad/norm_probe.py, written for this question;` →
  `Path: tubitak/sr/tools/norm_probe.py (preserved in WP22; it lived only in a session scratchpad until then), written for this question;`
- `05-referans-arac.md`: `…host_wsx4.py, outside the repository tree — presenting…` →
  `…host_wsx4.py, outside the repository tree, and **not preserved**: it exists only on the author's machine — presenting…`
- `17-wsx4-hizalama.md`: `host_wsx4.py and our seam are exonerated;` →
  `host_wsx4.py (WP5's adapter, not preserved in the repository) and our seam are exonerated;`
- `18-depo-tasima.md` §1: `(predictions.txt, 10:02:30 +03); ölçümden sonra` →
  `(predictions.txt, 10:02:30 +03; dosya depoya alınmamıştır, içeriği §14.4'te aynen verilmiştir); ölçümden sonra`

Kaynak kaydı `SOURCE.md`'ye ek olarak yazılmıştır (blob'lar, tarihler, "A'da commit yok").

### 14.5 Adım 5 — denetimler (V4)

| | WP21 | WP22 |
|---|---|---|
| ayrı ad | 193 | **197** |
| `tubitak/sr/` altında çözülen | 103 | **108** |
| çözülmeyen | 90 | **89** |
| okuyucuya verilmiş, B'den tutulamayan söz | 3 (kit, iki Proje 1 zip'i) | **1 grup: iki Proje 1 zip'i** (`gencp_plugin.zip` 98.410 B, `gencp_plugin_win_amd64.zip`) — kapsam dışı |

Yeni adlar: `gencp_kit_win_amd64_py312.zip`, `SHA256SUMS.txt`, `MANIFEST.json` artık **sürüm
varlığı** sınıfındadır; `norm_probe.py` ve `wp16_repro.py` çözülür; `host_wsx4.py` ve
`predictions.txt` "korunmadı/alınmadı" diye etiketlidir. Bağlantı denetimi: **25 göreli
bağlantı, 0 kırık.**

### 14.6 G1 ve V6

İfade depo başına tek `if/else`'tir ve koşulmadan önce okunmuştur.

| depo | karşılaştırılan | yol kümesi | değişen / eklenen | sınıf |
|---|---|---|---|---|
| A | **1272** | aynı; izlenmeyen 0 | **hiçbiri** (V6) | — |
| B | **1543** | aynı; beliren/kaybolan/taşınan yok | değişen: `SOURCE.md`; `docs/05-referans-arac.md`, `07-x4-model.md`, `10-kurulum.md`, `13-cevrimdisi-kurulum.md`, `16-checkpoint.md`, `17-wsx4-hizalama.md`, `18-depo-tasima.md` | 3 / 2 / 4 |
| | | | eklenen: `tools/norm_probe.py`, `tools/wp16_repro.py` | 1 |

Hepsi `tubitak/sr/` altındadır; 60 MB'lık zip hazırlanmamıştır (staged listede yalnızca metin
dosyaları vardır). Kapı geçilmiştir.

### 14.7 V5 — okuyucu sınaması, düşen durum için

Yalnızca B ve B'nin sürümleri elde, internetsiz bir Windows makinesi, `onnxruntime` yok:
`10-kurulum.md` baştan sona izlenmiştir.

- §2: ortam raporu betiği `tubitak/sr/tools/`'da — bulunur. Python 3.12 / `cp312` ölçülür.
- §3 tablosu: kit satırı var; `kit-win_amd64-py312-2026-08-31` sürümü, üç varlık — indirilir,
  `SHA256SUMS.txt` ile doğrulanır.
- §7.5 adım 2 → `13-cevrimdisi-kurulum.md` §3.1: `pip install --no-index --find-links=C:\gencp_kit\wheels
  … rasterio onnxruntime osmium` — kit kapalıdır, `pip` ağ istemez (V2).
- `gencp_super_resolution.zip`, üç model, örnekler: `sr-plugin-v0.1.0`'da.

**Cevap: EVET — bir varsayımla.** `rasterio` ve `onnxruntime` artık B'den kurulabilir; belgelerin
anlattığı yol baştan sona B'den yürütülebilir. Varsayım: **`Pillow`, QGIS'in Windows kurulumuyla
gelir.** Kitte yoktur, kılavuzun §2 tablosunda ölçülmez, ortam raporu betiği ölçmez. Gelmiyorsa
Proje 2'nin bikübik yolu dahil hiçbir yöntemi çalışmaz ve okuyucunun bunu makinede öğrenmesi
dışında yolu yoktur. Bu varsayım kapatılmadan "sınanmış" denemez; kapatmanın yolu, betiğe
`PIL` (ve `yaml`) satırı eklemek ya da kite Pillow tekerleğini katmaktır — ikisi de bu iş
paketinin izinli listesinde değildir, açık madde olarak yazılmıştır.

**Proje 1 için cevap HAYIR, iki sebeple:** iki zip yayımlanmamıştır (bilinen, kapsam dışı), ve
kit `geopandas`'ı kapsamaz (yeni bulgu, §14.1). İkisi de Proje 1 sürüm işine aittir.

### 14.8 Brifingin öngörmediği bulgular

1. **Proje 1'in çevrimdışı `.pbf` yolu `geopandas` ister** ve kit onu içermez; QGIS de getirmez.
   Kit Proje 1 için yeterli değildir — sürüm notlarında ve burada açıkça yazılmıştır.
2. **Proje 2 `Pillow`'a bağımlıdır** (bikübik dahil) ve ne kit ne ortam raporu bunu görür. Açık
   madde: ortam raporu betiğine `PIL` ve `yaml` satırları.
3. **`10-kurulum.md` §7.5 "§3'teki kit" diyordu, §3'te kit yoktu.** Satır eklenerek giderilmiştir.
4. **`predictions.txt` duruyordu**; brifing yok saymıştı. İçeriği §14.4'te korunmuştur.
5. Kit klasöründeki `KURULUM.md`, `13-cevrimdisi-kurulum.md`'nin **eski** bir kopyasıdır (29.
   satırda hâlâ `tubitak/tool/…` der); zip'e alınmamıştır.
6. `pip download` ilk denemede "geçersiz gereksinim" verdi: zsh, `$set` değişkenini kelimelere
   bölmez; `${=set}` ile yeniden koşulmuştur. İlk başarısızlık bulgu sayılmamıştır.
