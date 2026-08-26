# Standing practices

Rules of general force, collected where future work will see them. Each carries its origin.

## Registrations are frozen. Standing practices are living.

*Written 2026-08-26, because it was unwritten and a session hesitated in exactly this
place.*

A **registration** binds a specific analysis and **must not move once numbers exist**. A
**standing practice** is a working rule and **improves as the project learns**.

A practice's **FORWARD-ONLY** marker governs whether past *registrations* get repaired
under it. It **never** governs whether the practice's own text may be improved.

Improving a practice is recorded as a **dated broadening with the original preserved
verbatim**. It is never a silent edit, and it never reopens a disposal already made.

The test that keeps the two apart: **a rule can only have been adjusted to pass if it
changes a verdict.** A broadening that changes no verdict is a broadening. One that
changes a verdict is a re-registration, and re-registration after seeing which way a
rule cuts is exactly what practice 4 forbids.


1. **Invariance section in every gate registration** (2026-08-21). Three ill-posed gate
   elements failed the same way — an unstated invariance assumption (same OSM source: false;
   same render path: false; deterministic inference: false). Every gate registration now
   lists explicitly what it assumes identical on both sides: data source, render path, code
   path, determinism. A gate that does not state its invariances does not know what it is
   measuring. Origin: [tool-gate-registration-2.md](tool-gate-registration-2.md) family,
   corrections-log entries 13–15.

2. **K-draw averaging on small subsets** (2026-08-21). Any comparison on roughly n < 60
   chips generates K seeded dropout draws and averages before scoring. Test-time dropout
   noise (~0.1–0.4 px per chip median) is a large relative contributor at small n — it sits
   inside the CI on R, the salt and badlands subsets, and the Cappadocia per-stratum
   numbers. It is removable noise and unaveraged small-n results have been paying it.
   Origin: corrections-log entry 14; Task-3 determinism probe.

3. **No retraining on production-provenance inputs for now** (2026-08-21). The train/serve
   skew is real (training = pre-fix simple-strategy extracts; production = post-fix smart),
   its cost is measured (~0.6 px on forest-heavy chips), and it lands on precisely the class
   the institution intends to mask out — which is fortunate, not designed. Mitigation: the
   reliability layer is weighted against forest; retraining on post-fix inputs is Phase F
   future work, not undertaken now. Origin: phase-c-results Limitations;
   [phase-f-backlog.md](phase-f-backlog.md).

4. **Registrations before numbers; failed gates reported, never adjusted; mis-specified
   gates re-registered with the original preserved** (standing since Phase B, restated here
   for completeness).

5. **Every reported number states its inference path** (2026-08-21). All C-phase and tool
   evaluation numbers were measured on the stochastic (dropout-active) path; the delivered
   tool defaults to the deterministic path (measured agreement |Δ| ≤ 0.05 px at n = 30
   resolution). The invariance rule applied to our own reporting: a reader must see the
   gap, not discover it. Origin: tool-results.md §A; Task 1 decision.

6. **One sign convention, document-wide** (2026-08-21). Δ = candidate − baseline; negative
   = candidate better. "Gain" is defined at point of use as −Δ. Stated at the top of each
   results document. Origin: the regC/+phase-D sign divergence.

7. **Long detached runs checkpoint intermediate results** (2026-08-21). Any run expected to
   outlive a session writes per-item artifacts so a respawn resumes rather than restarts
   (registration B had to be respawned from zero after a session limit). Origin: regB.

8. **Review the open items; do not only append to them** (2026-08-21). At the end of every
   package, [open-items.md](open-items.md) is read from the top; each item is closed or
   explicitly deferred with a written reason. Origin: three headline-deciding findings (the
   cold-D risk, the small-n rule lapse, the unexplained baseline shift) were all items we
   wrote down ourselves and stopped watching. The corrections log records what went wrong;
   nothing before this rule forced revisiting what we flagged as pending.

9. **Registration audits get a fourth leg: does the design support the inference?**
   (2026-08-24). The audit method used on T1, B2/B3 and the phase-C pair has three legs —
   timeline (commit times vs artifact mtimes), recomputation (every reported cell rebuilt from
   raw), and configuration (run configs diffed against the registration text). All three ask
   **whether the numbers are what we say they are**. None asks **what the numbers are evidence
   about**. The fourth leg does: *at what level was the treatment applied, at what level is the
   error bar computed, and are they the same level?* — and, more generally, whether the design
   can support the claim the document draws from it. Origin: the C4/C5 package passed all three
   existing legs on 2026-08-24 and was found the same day, by an adversarial review pass and
   not by us, to rest on a treatment applied once per cell with every standard error computed
   at chip level — 130 chips replicating the evaluation, not the intervention, and an
   interaction term with no run-level error bar at all. The audit that had just cleared it
   would never have caught that, because no leg was pointed at it.
   [seed-replication-registration.md](seed-replication-registration.md) is the correction; this
   practice is so the class is caught next time rather than the instance.

10. **Numerical artifacts that a published number depends on live under `docs/` and are
    tracked** (2026-08-26). `.gitignore` excludes `tubitak/data/*` and `tubitak/outputs/*`
    wholesale, so **no per-chip CSV, summary JSON or analysis script under those paths has
    ever been under version control**. Any such file that a published number rests on is
    committed to `tubitak/docs/evidence/`, with its sha256 recorded in
    [evidence/MANIFEST.md](evidence/MANIFEST.md) and verified against any value already
    published for it. **The scripts that produce those files are committed too** — an output
    without its producer is not reproducible, only re-implementable, and re-implementation
    yields new numbers rather than the published ones. Origin: **Phase D**
    ([phase-d-audit.md](phase-d-audit.md) §C). Six of its seven registered checks and its veto
    rule have no surviving artifact of any kind; `eu_per_chip.csv`,
    `blur_control_per_chip.csv`, `eu_decomposition_per_chip.csv`, `veto_features.csv` and
    `veto_rule.py` do not exist anywhere in the repository; and the sentence that justified not
    committing them — "regenerable end-to-end from committed scripts and registrations" — was
    **false**, because none of those scripts was committed either. Two Table II rows rest on
    numbers nothing in this repository can re-derive. **The rule is not "hash your artifacts".
    A hash proves identity if the file survives; it does not preserve the file.** At the moment
    the Phase D audit was written, the six-seed Modal block — 26 arm-units, one night, $23 of
    GPU — was protected by nothing but sha256 strings in a markdown file. The corrective is
    this practice, and entry 22 (B3's harness deleted, four registered matcher parameters
    permanently unverifiable) is the earlier instance of the same class that this practice
    exists to stop recurring for a third time.

    **Amended 2026-08-26, after the practice failed on its second day.** The required
    final step: **after an evidence commit, verify from a fresh clone that the files are
    actually there.** Not `git status`, which is silent about ignored paths, and not
    `git log`, which reports what was committed rather than what was intended: clone the
    pushed remote into a scratch directory and re-run the manifest check against that
    tree. **A file is evidence when a stranger can obtain it, not when the committing
    session believes it was added.** If that check cannot be run, the artifacts are not
    committed yet and the manifest rows must not be written.

    Why the clause was needed, stated so it is not read as carelessness: **`git add`
    exits zero when it adds nothing.** `4e4fb05` was told to commit 260 evidence
    rasters; `.gitignore`'s `*.tif` rule refused every one of them silently; the commit
    then succeeded on the two files that remained, and `MANIFEST.md` went on asserting
    the sha256 and byte size of all 260. **Every local signal reported success.** The
    only signal that would have contradicted it was one nobody was asked to look for —
    which is why this amendment specifies an *observation of the resulting state* rather
    than one more action. The practice as first written said "commit the artifacts"; it
    did not say "check that the commit succeeded", and that gap is the whole failure.
    Type rules are fixed at the class level too: `.gitignore` now ends with
    `!tubitak/docs/evidence/**`, so no future extension rule can swallow an evidence
    artifact. Instance: **corrections entry 35**.

11. **A rule states the class it governs, not the instance that prompted it**
    (2026-08-26; **BROADENED 2026-08-26** — original text preserved verbatim below).
    **FORWARD-ONLY.**

    A rule states the class it governs, not the instance that prompted it. When an
    exception, a budget or a threshold is written against the case in hand, write the
    membership test instead, and write it down — **an intended class that is not stated
    is not checkable**. Where the class lives in code, quoting the implementing code
    inside the registration is how this is done.

    ### Original text, preserved verbatim (2026-08-26, before the broadening)

    > 11. **A registration that names a set, a threshold or a condition QUOTES the implementing
    > code's expression of it** (2026-08-26). **FORWARD-ONLY.** When a registration fixes a
    > reading in prose, the line of code that implements it is quoted in the registration
    > itself, so prose and implementation sit in one place and can be checked against each
    > other by reading rather than by remembering to compare two files. Origin: **three findings
    > that looked like unrelated slips and share one cause — a registration written in prose,
    > implemented in code, and the two drifting.**
    >
    > - **The warm-up de-confound's branch text** said "as C1 and C4 did", presuming both
    >   adversarial arms rise at the first main-stage transition. True at seed 42, false at
    >   seed 43, where C4 falls. The branch fired on its antecedent so nothing changed, but the
    >   clause had no determinate referent
    >   ([warmup-deconfound-results.md](warmup-deconfound-results.md) §5).
    > - **The hardware gate's acceptance rule** was written as a single global verdict while
    >   scaling each quantity to its own spread, so the most reproducibly-measured quantity
    >   governed the package and one quantity vetoed ten
    >   ([hardware-gate-results.md](hardware-gate-results.md)).
    > - **AMENDMENT SEED-c (d)** reads "C5's edge mean the highest of **the four arms**", while
    >   `seed_analysis.py:212` implements the tie rule as `("pre", "C1", "C2", "C4")` —
    >   **five arms, including pretrained** ([phase-d-closeout.md](phase-d-closeout.md) §C).
    >   The harness was stricter than the registration, which is the safe direction, and the
    >   reading held either way.
    >
    > **Not applied retroactively.** The existing registrations stand exactly as written, with
    > their mismatches disclosed where they were found and not repaired — the same disposal the
    > hardware gate's own flaw received, and for the same reason: a rule rewritten after seeing
    > which way it cuts is indistinguishable from a rule adjusted to pass. **When
    > corrections-log entries 30–34 are applied, these three are grouped under one heading in
    > the tiering**, so a reader sees one class with three instances rather than three
    > unrelated slips.

    ### Why it was broadened

    The original's mechanism — quote the implementing code — requires a registration,
    implementing code, and two artifacts that can drift. Two further instances arrived
    the same day with none of those three: a boundary exception written in a README and
    a word budget written in a drafting skeleton. Each is a single artifact with no code
    to quote, so the practice as first written had no purchase on either, **while both
    failed in precisely the way its three founding cases had failed**. Quoting the code
    is not the principle; it is how the principle is applied in the one setting where
    the class happens to be written in code.

    ### The broadening changes no past disposal

    Stated explicitly, because it is what removes any suspicion that the rule was
    adjusted to pass. **All five instances below stay disclosed and not repaired**, and
    every one would have been disposed of identically had this practice been written
    broadly from the start. The broadening changes **no verdict**: not a gate, not a
    reading, not a number, not a retraction condition. A rule can only have been
    adjusted to pass if it changes a verdict; this changes none. The non-retroactivity
    of the original stands unaltered — a rule rewritten after seeing which way it cuts
    is indistinguishable from a rule adjusted to pass, which is why the five are
    disclosed where they were found rather than repaired.

    ### Instances — one class, five cases

    1. **"as C1 and C4 did"** — the warm-up de-confound's branch text presumed both
       adversarial arms rise at the first main-stage transition. True at seed 42, false
       at seed 43, where C4 falls. The branch fired on its antecedent so nothing
       changed, but the clause had no determinate referent
       ([warmup-deconfound-results.md](warmup-deconfound-results.md) §5).
    2. **"the four arms"** — AMENDMENT SEED-c (d) reads "C5's edge mean the highest of
       the four arms", while `seed_analysis.py:212` implements the tie rule as
       `("pre", "C1", "C2", "C4")` — five arms, including pretrained
       ([phase-d-closeout.md](phase-d-closeout.md) §C). The harness was stricter than
       the registration, the safe direction, and the reading held either way.
    3. **The hardware gate's acceptance rule** — written as a single global verdict
       while scaling each quantity to its own spread, so the most
       reproducibly-measured quantity governed the package and one quantity vetoed ten
       ([hardware-gate-results.md](hardware-gate-results.md)).
    4. **The interaction disclosure's 120-word budget** — set by what the deleted
       paragraph happened to vacate rather than by what the disclosure requires. The
       budget described the hole left behind, not the class of text that had to fill it.
    5. **The split boundary's exception** — written as one file,
       `plugin-gate-registrations.md`, rather than as the class it meant: the plugin
       work package's registrations **and results**. The deletion commit `b815b46`
       consequently removed `plugin-results.md` while a parallel session was writing
       it; in-flight work was destroyed and recovered by rewriting (`21054d7`). Nothing
       published was affected and no registered claim moved, so it is recorded as
       repository hygiene in the handover guides rather than in the corrections log.

    **Cases 4 and 5 were both specified by the supervising session, within one day of
    each other.** That is recorded because it locates the class correctly: this is not
    a failure of care by whoever drafted a given line, and it is not confined to
    registrations or to any one author. It is a failure mode of rule-writing itself —
    the instance in front of you is the cheapest thing to describe, and it is almost
    never what you mean.

    **When corrections-log entries 30–34 are applied, the first three are grouped under
    one heading in the tiering**, so a reader sees one class with instances rather than
    unrelated slips. Cases 4 and 5 are not corrections-log material: neither moved a
    published number.
