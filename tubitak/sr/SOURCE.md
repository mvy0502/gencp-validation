# Kaynak

Bu ağaç (`tubitak/sr/`) **mvy0502/GenCP** deposunun `tubitak-tr` dalından, `f28342b8eb9739ef7cad838bf4474e18fb3873cd`
commit'inden (`f28342b`, "fix: the checkpoint hang was an abandoned async copy, and the wsx4 shift is theirs"), **2 Eylül 2026** tarihinde alt-ağaç
kopyası olarak alınmıştır. Birleştirme (merge) yapılmamıştır; yalnızca izlenen dosyalar aynı
göreli yollarla kopyalanmıştır (WP17, `docs/18-depo-tasima.md`). Bu tarihten itibaren
Proje 2'nin güncel kopyası bu depodadır; GenCP'deki kopya dondurulmuştur.

## Ek — `tubitak/sr/` dışından alınan iki dosya (WP21, 2 Eylül 2026)

WP17 kopyası yalnızca `tubitak/sr/` alt-ağacını taşımıştı; bu klasördeki belgelerin adıyla
andığı iki dosya A'da o ağacın dışında durduğu için gelmemişti. İkisi de A
`e5a3d225f71c84d4105fe16c823c6b71b5545152` durumundan bayt bayt alınmıştır (blob sağlamaları
A'dakiyle aynıdır):

| burada | A'daki yol | A'da son commit | blob |
|---|---|---|---|
| `tubitak/sr/tools/qgis_ortam_raporu.py` | `tubitak/tool/qgis_ortam_raporu.py` | `277f19e` (31 Ağustos 2026) | `ebcbba28820f` |
| `tubitak/sr/docs/evidence/wp15/corpus_checks.json` | `tubitak/docs/evidence/wp15/corpus_checks.json` | `0caf201` (1 Eylül 2026) | `8209aaa79abb` |

A'daki `tubitak/sr/` aynası dondurulmuştur ve bu iki dosyayı **içermez**; A ile B arasındaki
bu fark bir kopya hatası değil, bu ekin sonucudur.
