# Corrections log — entry 35, DRAFT

**Status: drafted, awaiting review.** Not yet merged into
[corrections-log.md](corrections-log.md), which stands at entry 29 in git; entries 30-34 are
drafted and under the same review. Tier 2 (unrecoverable artifacts) is the wrong home — nothing
was lost — so this is filed for **Tier 3, reporting errors**, with the standing-practice
amendment in section 4 below.

## The correction

| # | Date | What was asserted | What was true |
|---|---|---|---|
| 35 | 26 Aug | [evidence/MANIFEST.md](evidence/MANIFEST.md) listed 260 raster files under `input_render_warped/` and `real_chip_bt601/`, each with a sha256 and a byte size, and [evidence/rasters/README.md](evidence/rasters/README.md) stated they were "**committed 2026-08-26 as insurance**" so that "the informative-mask test can be run in any later session even if this disk does not survive" | `4e4fb05` committed **only** `MANIFEST.md` and `rasters/README.md`. Every one of the 260 `.tif` files was silently refused by `.gitignore:49` (`*.tif`), whose three negations covered neither path. The files existed in one working tree, on one disk, and in no repository. The rows also carried the wrong path: they omitted the `rasters/` prefix the files actually live under, so a verifier walking the manifest would have failed to find them even had they been tracked |

**How it was found.** During the GenCP to gencp-validation sync, the manifest was verified
row by row against the working tree rather than read. 83 of 343 rows resolved; 260 did not.
Follow-up with `git check-ignore -v` and `git show --stat 4e4fb05` established the cause.

**Scope of the damage: none, and that is luck rather than discipline.** The disk survived.
Had it not, the informative-mask test would have been unreproducible, and that test is the
one that replaced the lost Phase D blur control. The failure mode was therefore pointed
directly at the repair for the previous failure of the same kind.

## Why this is worse than a missing manifest

A manifest that vouches for untracked files **reads as verified**. Its sha256 column is an
assertion of identity that a reader is invited to check, and the invitation is what makes it
persuasive; the reader who does not run the check comes away with more confidence than the
evidence supports, and the reader who does run it discovers the files are absent. An absent
manifest claims nothing and misleads no one. This entry belongs with the class named in
entry 32, not with the artifact losses of Tier 2: the artifacts were fine. The record about
them was false.

## Why standing practice 10 did not prevent it

Practice 10 was written on **2026-08-26**, two days before this entry and out of the Phase D
audit — that is, it was written for this exact failure, and it was in force at the moment the
failure occurred. It did not prevent it, and the reason is worth stating plainly rather than
treating as an anomaly:

> The practice said **commit the artifacts**. Nobody checked that the commit succeeded.

The practice specified an action and an accompanying record. It did not specify an
observation of the resulting state. `git commit` reported success — it had two files to
commit and it committed them — and `git add` had exited zero after adding nothing, because
adding an ignored path is not an error. Every local signal said the work was done. The only
signal that would have contradicted it was one nobody was asked to look for.

This is the same structure as the sentence practice 10 itself was written to retire
("regenerable end-to-end from committed scripts" — false, because the scripts were not
committed either). Both are **claims about repository state, made without reading repository
state**. The class is not "someone forgot"; it is "the practice ended one step before the
step that would have caught it."

## Proposed amendment to standing practice 10

Add, as a required final clause:

> **After an evidence commit, verify from a fresh clone that the files are actually there.**
> Not `git status`, which is silent about ignored paths, and not `git log`, which reports
> what was committed rather than what was intended: clone the pushed remote into a scratch
> directory and re-run the manifest check against that tree. A file is evidence when a
> stranger can obtain it, not when the committing session believes it was added. If the
> check cannot be run, the artifacts are not committed yet and the manifest rows must not
> be written.

**Type rules are also fixed at the class level, not per incident.** `.gitignore` now carries
`!tubitak/docs/evidence/**` as its last rule, so no future extension-based exclusion can
swallow an evidence artifact. `git add -f` was considered and rejected: it would have fixed
26 August and left 27 August exposed.

## Remediation performed

| Action | Result |
|---|---|
| `.gitignore` negation `!tubitak/docs/evidence/**`, appended last so it wins | rasters no longer ignored |
| 260 `.tif` files committed to gencp-validation | 130 `input_render_warped/` + 130 `real_chip_bt601/` |
| 260 manifest rows re-prefixed to `rasters/...` | paths now resolve as written |
| 7 unlisted `informative_mask/` outputs given rows | manifest and tree agree in both directions |
| Fresh-clone verification | see the commit message for the counts |

**What this entry does not claim.** The per-seed arm warps remain uncommitted by design
(650 files x 6 seeds); `rasters/README.md` already discloses that re-inferring them is a
stochastic path and therefore a replication rather than a reproduction. That disclosure was
accurate and is unchanged.
