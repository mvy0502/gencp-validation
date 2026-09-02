#!/usr/bin/env python
"""Names of files mentioned in prose must exist. Link checkers only see links.

WP20 found two files named in plain text - `qgis_ortam_raporu.py`, `corpus_checks.json` -
that every link check had passed over, because a backticked file name is not a markdown
link. A reader who follows the documentation and looks for a file we named must find it.

    check_named_files.py [--root=DIR] [--json=OUT]

Scans every *.md under ROOT/tubitak/sr for tokens that end in a known file extension,
and reports each distinct name that no file under ROOT/tubitak/sr carries. The report is
a LIST FOR TRIAGE, not a verdict: a name may be absent legitimately (a release asset, a
file the user creates, a gitignored data path, an example). The triage is a human's job
and is written in the report that cites this run; the check's job is to make sure no name
is invisible.

Known-false first, per standing practice 11: a planted name that cannot exist must be
reported before the real scan is trusted. Refuses arguments it does not understand
(practice 10, `_guard.strict_argv`).
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]                                    # <repo>/tubitak/sr/tools/x.py
sys.path.insert(0, str(ROOT / "tubitak" / "tests"))
from _guard import strict_argv                            # noqa: E402

strict_argv(known=("--root=", "--json="), positional=0,
            usage="check_named_files.py [--root=DIR] [--json=OUT]")

# File extensions that appear in this project's documents. A token is a candidate only if
# it ends in one of these, so `torch.save`, `sys.path`, `1.008` and `github.com` are not.
EXTS = ("py", "md", "json", "onnx", "tif", "tiff", "zip", "txt", "yml", "yaml", "qgz",
        "qml", "pbf", "csv", "npy", "pt", "png", "jpg", "xml", "jp2", "gz", "whl", "sh",
        "safe", "ipynb", "toml", "cfg", "log", "html")
TOKEN = re.compile(r"(?<![\w./-])([\w./-]*?[\w-]+\.(?:%s))(?![\w])" % "|".join(EXTS))
SELF_TEST_NAME = "this_file_cannot_exist_zz.py"


def scan(root: Path, extra_text: str = ""):
    tree = root / "tubitak" / "sr"
    mds = sorted(tree.rglob("*.md"))
    present = {p.name for p in tree.rglob("*") if p.is_file()}
    # names that resolve elsewhere in the repository (Project 1 code, demo project) are
    # reported with WHERE, so the triage can see them without a second search
    elsewhere = {}
    for p in root.rglob("*"):
        if p.is_file() and ".git" not in p.parts and "tubitak/sr" not in str(p.relative_to(root)):
            elsewhere.setdefault(p.name, str(p.relative_to(root)))
    names = {}                                            # name -> [(file, line)]
    def feed(text, label):
        for i, line in enumerate(text.split("\n"), 1):
            for m in TOKEN.finditer(line):
                tok = m.group(1).rstrip(".")
                base = tok.split("/")[-1]
                names.setdefault(base, []).append((label, i, tok))
    for p in mds:
        feed(p.read_text(encoding="utf-8"), str(p.relative_to(root)))
    if extra_text:
        feed(extra_text, "<planted>")
    missing = {}
    for base, where in names.items():
        exists = base in present
        if not exists:
            # a path given relative to the repository root also counts as resolving
            exists = any((root / w[2]).is_file() for w in where)
        if not exists:
            missing[base] = (where, elsewhere.get(base))
    return len(mds), names, missing


def main():
    root, out_json = ROOT, None
    for a in sys.argv[1:]:
        if a.startswith("--root="):
            root = Path(a.split("=", 1)[1]).resolve()
        elif a.startswith("--json="):
            out_json = a.split("=", 1)[1]
    if not (root / "tubitak" / "sr").is_dir():
        sys.stderr.write(f"check_named_files.py: no tubitak/sr under {root}\n")
        return 2

    # known-false FIRST: a planted name that cannot exist must be reported
    _, _, m = scan(root, extra_text=f"see `{SELF_TEST_NAME}` for details")
    if SELF_TEST_NAME not in m:
        print("self-test FAILED: a planted non-existent name was NOT reported; "
              "the check cannot be trusted and no real result is printed")
        return 3
    print(f"self-test PASSED: planted `{SELF_TEST_NAME}` was reported, so the scan below "
          f"demonstrably notices a missing name")

    n_md, names, missing = scan(root)
    n_ok = len(names) - len(missing)
    print(f"{n_md} markdown files under tubitak/sr; {len(names)} distinct file names; "
          f"{n_ok} resolve under tubitak/sr; {len(missing)} do not")
    print()
    print("names that do NOT resolve - a list for triage, not a verdict:")
    n_else = sum(1 for w, e in missing.values() if e)
    for base in sorted(missing):
        w, e = missing[base]
        first = ", ".join(f"{f}:{i}" for f, i, _ in w[:2]) + (" ..." if len(w) > 2 else "")
        tag = f"  [elsewhere: {e}]" if e else ""
        print(f"  {base:52s} {len(w):3d}x  {first}{tag}")
    print(f"\n{n_else} of the {len(missing)} resolve elsewhere in the repository; "
          f"{len(missing) - n_else} resolve nowhere in it")
    if out_json:
        Path(out_json).parent.mkdir(parents=True, exist_ok=True)
        Path(out_json).write_text(json.dumps(
            dict(markdown_files=n_md, names=len(names), resolving_under_sr=n_ok,
                 not_resolving={b: dict(where=[list(x) for x in w], elsewhere=e)
                                for b, (w, e) in missing.items()}),
            indent=1, ensure_ascii=False))
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
