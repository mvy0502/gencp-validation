# Snapshot provenance

This repository is a **handover copy**, not a workspace. See `CLAUDE.md`.

| | |
|---|---|
| **Source repository** | `mvy0502/GenCP`, branch `tubitak-tr` |
| **Reflects commit** | `4c1b666` — *fix: the link check passed on files no visitor can see* |
| **Snapshot taken** | 2026-08-27 |
| **Last verified** | 2026-08-27 |

## What this means

The `tubitak/` tree here was copied from the working repository at the commit above. Both
repositories share history from merge base `96503b7`, so commit SHAs cited across the study
record resolve in either.

**Refreshed 2026-08-27, at the plugin milestone.** The QGIS plugin package is complete, so
this snapshot now carries it: `tubitak/qgis_plugin/`, the confidence-score registrations and
results, the field-test record, and the evidence transcripts. Before this refresh the
handover repository's README linked to documents that did not exist here, and every one of
them bounced a visitor to `mvy0502/GenCP` — which defeats the point of a handover copy.
Those links now point at the local copies.

**Re-synced 2026-08-27, after the alpha-rendering fix.** The confidence alpha band was
making QGIS draw the plugin's output semi-transparently over whatever layer sat beneath it,
so a visual comparison of generated against real was silently comparing a blend of the two.
The file bytes were always correct and Gate ALPHA was unaffected; the fix is display-only.
This snapshot carries it, along with the regression check that would catch it returning.

**A snapshot still lags by construction.** Anything committed to `GenCP` `tubitak-tr` after
the commit named above is not here, and `mvy0502/GenCP`, branch `tubitak-tr`, remains the
live version.

## Refreshing

Refresh by **copying the curated `tubitak/` tree** from the working repository. Never by
merging `tubitak-tr` into this repository: commit `b815b46` there deletes 263 files, and
merging it would propagate those deletions and destroy the research record this repository
exists to preserve.

The 2026-08-27 refresh used:

```bash
rsync -a --delete \
  --exclude 'data/' --exclude 'outputs/' --exclude '__pycache__/' \
  --exclude '*.pyc' --exclude '.DS_Store' \
  --exclude 'docs/figures/web/' \
  ../GenCP/tubitak/ tubitak/
```

**`docs/figures/web/` is excluded on purpose, and the exclusion is load-bearing.** Those
five web-optimised JPGs exist only here — this repository's README displays them and the
working repository has no copy — so a plain mirror deletes them and silently breaks the
front page. The first attempt at this refresh did exactly that and it was caught by asking
the question `CLAUDE.md` requires: *does anything in this repository read this file?*

Two files were genuinely dropped, both unreferenced: `docs/corrections-entry-35-draft.md`
(a draft superseded upstream) and `docs/figures/odtu-package-visual.png`.

**Update the table above whenever the snapshot is refreshed** — a snapshot that does not name
the state it reflects cannot be checked against anything.
