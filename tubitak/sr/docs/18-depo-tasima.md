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
