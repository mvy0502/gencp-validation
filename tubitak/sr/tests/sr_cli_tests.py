#!/usr/bin/env python
"""WP24 — does `tools/sr_cli.py` produce exactly what the plugin produced?

Three kinds of test, all three required by the work package:

  --equivalence   The gate. The tool is run on the input behind every pixel hash this
                  project has registered, and the pixel hash of its output is compared for
                  EQUALITY — no tolerance, no visual similarity. On a mismatch the first
                  differing pixel (band, row, col, both values) is reported. Each real run
                  is also preceded by a --dry-run of the same invocation, and the grid the
                  dry run printed is compared with the grid the file carries (test kind 3).
  --self-test     Known-false: a raster with no CRS, a band count the model refuses, a
                  model path that does not exist, an output that exists without
                  --overwrite, a rotated raster, and the degenerate no-argument call. Each
                  must be REFUSED with the documented exit code and leave no output on disk;
                  the test fails if the tool succeeds. Also the pixel-hash comparison's own
                  known-false: a one-pixel perturbation must be reported at its coordinates.
  --all           Both.

The pixel hash is `pixhash` from WP2B (`docs/02b-plugin.md` §7.1): SHA-256 over
`"{count}|{height}|{width}|{dtype}"` followed by each band's rows in order. It is restated
here because WP2B kept it in a scratch directory; every registered value below reproduces
under this definition (verified in WP24 before this file was written).

Data: the registered inputs live under the gitignored `tubitak/data/` tree. On this machine
that is repository A's; pass `--data-root=DIR` if it is elsewhere. A missing input is
reported as NOT RUN and the verdict is withheld (exit 2) — a gate that cannot see its
inputs does not pass.

Standing practice 10: unknown arguments are refused via `tubitak/tests/_guard.py`.
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import tempfile
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

HERE = Path(__file__).resolve()
SR = HERE.parents[1]                 # tubitak/sr
ROOT = HERE.parents[3]               # repository root
sys.path.insert(0, str(SR))
sys.path.insert(0, str(ROOT / "tubitak" / "tests"))
from _guard import strict_argv                                          # noqa: E402

strict_argv(known=("--equivalence", "--self-test", "--all", "--data-root=", "--keep"),
            positional=0,
            usage="sr_cli_tests.py --equivalence | --self-test | --all [--data-root=DIR]")

import numpy as np                                                      # noqa: E402
import rasterio                                                         # noqa: E402
from rasterio.transform import Affine                                   # noqa: E402

TOOL = SR / "tools" / "sr_cli.py"
PY = sys.executable

# ------------------------------------------------------------------ registered hashes
# Each entry: where the hash is recorded, the input that produced it, and the exact
# invocation the plugin's parameters translate to. `expect` is the full digest; the two
# recorded only as prefixes in the documents (`41b54b77…`, `6b71d037…`) were completed from
# the WP2B/WP6 session record and re-verified on the surviving output files in WP24.
REGISTERED = [
    dict(key="bicubic_x2_fixture_1024",
         recorded="02b-plugin.md §7.1 (prefix); WP2B session record (full)",
         produced_by="plugin QgsTask, bicubic x2, sr_wp2b/fixture_1024.tif "
                     "(36SVJ TCI window 4096,4096,1024,1024)",
         input="sr_wp2b/fixture_1024.tif", args=["--scale", "2"],
         expect="41b54b778f07c98974d63cf38969e25aadf089c2a40e82aa3ddaebe0108f72ee"),
    dict(key="bicubic_x2_36SVJ_full",
         recorded="02b-plugin.md §7.1; 04-model-in-plugin.md §2.1; 06-wsx4-eklentide.md §0",
         produced_by="plugin QgsTask and CLI, bicubic x2, tiles36SVJ/TCI.tif (10980 x 10980)",
         input="tiles36SVJ/TCI.tif", args=["--scale", "2"],
         expect="ca3b4c41b6661aed8cc3c771d0cdd5a44dd1f70684f18932f1644beba55ad03c"),
    dict(key="model_x2_v1_DEMO_4096",
         recorded="04-model-in-plugin.md §4",
         produced_by="plugin dialog, gencp_sr_x2_v1.onnx, DEMO_INPUT_36SXJ_4096px, "
                     "tile 512 / overlap 32 / feather",
         input="sr_model_input/DEMO_INPUT_36SXJ_4096px_B02-B03-B04_uint16DN_10m.tif",
         args=["--method", "model", "--model", "sr_models/gencp_sr_x2_v1.onnx"],
         expect="5e3de3cfcf4cf60910d6763712350fbfe42a1116abe4767fc77542bc0f374cd2"),
    dict(key="wsx4_x4_DEMO_WSX4_1024",
         recorded="06-wsx4-eklentide.md §0 (prefix); WP6 session record (full)",
         produced_by="plugin dialog and CLI, wsx4_spatrad.onnx (+ .yaml), "
                     "DEMO_INPUT_WSX4 1024px, tile 256 / overlap 65 / crop margin 130",
         input="sr_model_input/DEMO_INPUT_WSX4_36SXJ_1024px_B2-B3-B4-B8_uint16DN_10m.tif",
         args=["--method", "wsx4", "--model", "wp5_reference/models/wsx4_spatrad.onnx"],
         expect="6b71d0370642b56617eee715b5ceb24b62f5139542b3fed2aa1fd498e1675835"),
    # Not in a document before WP24: the plugin's own bicubic 4x output, run through the
    # real QgsTask inside QGIS 4.2.1 on 2 September 2026 (the scale-fix work package's
    # evidence, docs/evidence/wp22/scale_fix_known_false_known_true.json), hashed in WP24.
    # It is the only plugin-produced reference at the tool's DEFAULT scale.
    dict(key="bicubic_x4_DEMO_WSX4_1024_plugin_2sep",
         recorded="18-depo-tasima.md §16 (WP24); plugin run of 2 Sep 2026",
         produced_by="plugin QgsTask, bicubic x4 (BICUBIC_SCALE), DEMO_INPUT_WSX4 1024px",
         input="sr_model_input/DEMO_INPUT_WSX4_36SXJ_1024px_B2-B3-B4-B8_uint16DN_10m.tif",
         args=[],
         expect="6cd62c3859d920d1e1d5b8d6cea17d878f3b8c33a8974d8d92805a24591dd767"),
    # Also new in WP24: the SHIPPED demo model, gencp_sr_x4_b4.onnx, had no registered
    # pixel hash. The plugin was driven headlessly inside QGIS 4.2.1 (run_in_qgis.sh) and
    # ran the model through its real QgsTask on the 4-band demo input; that output is
    # hashed here. It is the reference that matters for the presentation.
    dict(key="model_x4_b4_DEMO_WSX4_1024_plugin_2sep",
         recorded="18-depo-tasima.md §16 (WP24); plugin QgsTask run of 2 Sep 2026",
         produced_by="plugin QgsTask, gencp_sr_x4_b4.onnx, DEMO_INPUT_WSX4 1024px, "
                     "tile 512 / overlap 32 / feather",
         input="sr_model_input/DEMO_INPUT_WSX4_36SXJ_1024px_B2-B3-B4-B8_uint16DN_10m.tif",
         args=["--method", "model", "--model", "plugin_models/gencp_sr_x4_b4.onnx"],
         expect="c4794d792c156e14c687093fa1cb9de3aec541d31102ad9d537e93b31061a2ac"),
]


def pixhash(path, block=2048):
    h = hashlib.sha256()
    with rasterio.open(str(path)) as d:
        h.update(f"{d.count}|{d.height}|{d.width}|{d.dtypes[0]}".encode())
        for b in range(1, d.count + 1):
            for r0 in range(0, d.height, block):
                nr = min(block, d.height - r0)
                a = d.read(b, window=rasterio.windows.Window(0, r0, d.width, nr))
                h.update(np.ascontiguousarray(a).tobytes())
    return h.hexdigest()


def first_diff(a_path, b_path, block=1024):
    """(band, row, col, a_value, b_value) of the first differing pixel, or None."""
    with rasterio.open(str(a_path)) as A, rasterio.open(str(b_path)) as B:
        if (A.count, A.height, A.width) != (B.count, B.height, B.width):
            return ("shape", (A.count, A.height, A.width), (B.count, B.height, B.width),
                    None, None)
        for b in range(1, A.count + 1):
            for r0 in range(0, A.height, block):
                nr = min(block, A.height - r0)
                w = rasterio.windows.Window(0, r0, A.width, nr)
                x, y = A.read(b, window=w), B.read(b, window=w)
                if x.dtype != y.dtype or not np.array_equal(x, y):
                    idx = np.argwhere(x != y)
                    if len(idx) == 0:
                        return (b, None, None, str(x.dtype), str(y.dtype))
                    r, c = idx[0]
                    return (b, int(r0 + r), int(c), x[r, c].item(), y[r, c].item())
    return None


def run_tool(args, timeout=1800):
    p = subprocess.run([PY, str(TOOL)] + [str(a) for a in args],
                       capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


DRY_RE = {
    "crs": re.compile(r"S1 KRS\s*:\s*(\S+)"),
    "pixel": re.compile(r"S2 piksel boyu\s*:\s*(\S+) x (\S+)"),
    "origin": re.compile(r"S3 başlangıç noktası\s*:\s*\((\S+), (\S+)\)"),
    "size": re.compile(r"S4 boyut\s*:\s*(\d+) x (\d+) piksel"),
}


def parse_dry(stdout):
    g = {k: rx.search(stdout) for k, rx in DRY_RE.items()}
    missing = [k for k, m in g.items() if m is None]
    if missing:
        raise AssertionError(f"dry-run output lacks {missing}:\n{stdout}")
    return dict(crs=g["crs"].group(1),
                pixel=(float(g["pixel"].group(1)), float(g["pixel"].group(2))),
                origin=(float(g["origin"].group(1)), float(g["origin"].group(2))),
                size=(int(g["size"].group(1)), int(g["size"].group(2))))


def grid_of(path):
    with rasterio.open(str(path)) as d:
        T = d.transform
        return dict(crs=d.crs.to_string(), pixel=(T.a, T.e), origin=(T.c, T.f),
                    size=(d.width, d.height))


# ------------------------------------------------------------------------- reporting
def report(title, rows):
    print(title)
    n_fail = 0
    for ok, name, detail in rows:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        if detail:
            for ln in str(detail).splitlines():
                print(f"         {ln}")
        n_fail += (not ok)
    return n_fail


# ---------------------------------------------------------------------- equivalence
def find_data_root(explicit):
    cands = [Path(explicit)] if explicit else [
        ROOT / "tubitak" / "data",
        Path.home() / "Documents" / "GenCP-Generative-Goruntu-Uretimi-OpenStreetMap"
        / "tubitak" / "data"]
    for c in cands:
        if (c / "tiles36SVJ" / "TCI.tif").is_file():
            return c
    return None


def equivalence(data_root, keep):
    out_dir = data_root / "sr_wp24"
    out_dir.mkdir(parents=True, exist_ok=True)
    rows, timings, not_run = [], {}, []
    for reg in REGISTERED:
        src = data_root / reg["input"]
        args = [(str(data_root / a) if a.endswith(".onnx") else a) for a in reg["args"]]
        model = next((a for a in args if a.endswith(".onnx")), None)
        if not src.is_file() or (model and not Path(model).is_file()):
            not_run.append(reg["key"])
            rows.append((False, f"{reg['key']}: NOT RUN — input or model missing",
                         f"{src}\n{model or ''}"))
            continue
        out = out_dir / f"{reg['key']}.tif"
        if out.exists():
            out.unlink()
        # (3) dry run first, on the same invocation
        rc, dry_out, dry_err = run_tool([src, out] + args + ["--dry-run"])
        if rc != 0:
            rows.append((False, f"{reg['key']}: --dry-run exited {rc}", dry_err))
            continue
        dry = parse_dry(dry_out)
        if out.exists():
            rows.append((False, f"{reg['key']}: --dry-run wrote a file", str(out)))
            continue
        # the real run, timed
        t0 = time.perf_counter()
        rc, so, se = run_tool([src, out] + args)
        secs = time.perf_counter() - t0
        timings[reg["key"]] = secs
        if rc != 0 or not out.is_file():
            rows.append((False, f"{reg['key']}: run exited {rc}", se[-800:]))
            continue
        real = grid_of(out)
        dry_ok = (dry["crs"] == real["crs"] and dry["pixel"] == real["pixel"]
                  and dry["origin"] == real["origin"] and dry["size"] == real["size"])
        rows.append((dry_ok, f"{reg['key']}: --dry-run grid == written grid",
                     f"dry {dry}\nreal {real}" if not dry_ok else
                     f"{real['size'][0]} x {real['size'][1]}, px {real['pixel']}, "
                     f"origin {real['origin']}, {real['crs']}"))
        # (1) the gate: pixel hash equality
        got = pixhash(out)
        same = got == reg["expect"]
        detail = (f"registered {reg['expect']}\n     tool     {got}\n"
                  f"     recorded in: {reg['recorded']}\n"
                  f"     produced by: {reg['produced_by']}\n"
                  f"     wall clock {secs:.1f} s")
        if not same:
            ref = _reference_file(data_root, reg["key"])
            if ref is not None:
                d = first_diff(ref, out)
                detail += f"\n     first differing pixel (band,row,col,plugin,tool): {d}"
            else:
                detail += "\n     no surviving plugin output to locate the first pixel"
        rows.append((same, f"{reg['key']}: pixel SHA-256 equals the registered value",
                     detail))
        if not keep and same:
            out.unlink()
    n_fail = report("WP24 equivalence — tool output vs registered plugin pixel hashes",
                    rows)
    if not_run:
        print(f"NOT RUN: {not_run} — verdict withheld")
        return 2
    print(f"timings: " + ", ".join(f"{k} {v:.1f} s" for k, v in timings.items()))
    print(f"EQUIVALENCE: {'PASS' if n_fail == 0 else 'FAIL'} "
          f"({len(rows) - n_fail}/{len(rows)} checks)")
    return 1 if n_fail else 0


def _reference_file(data_root, key):
    """A surviving plugin/CLI output with the registered hash, if one is still on disk."""
    cands = {
        "bicubic_x2_fixture_1024": ["sr_wp2b/plugin_fixture_x2.tif"],
        "bicubic_x2_36SVJ_full": ["sr_wp2b/plugin_36SVJ_x2.tif", "tiles36SVJ/TCI_sr_x2.tif"],
        "model_x2_v1_DEMO_4096": [
            "sr_model_input/DEMO_INPUT_36SXJ_4096px_B02-B03-B04_uint16DN_10m_sr_x2.tif"],
        "wsx4_x4_DEMO_WSX4_1024": [
            "sr_model_input/DEMO_INPUT_WSX4_36SXJ_1024px_B2-B3-B4-B8_uint16DN_10m_sr_x4.tif"],
        "bicubic_x4_DEMO_WSX4_1024_plugin_2sep": ["sr_wp24/reference_plugin_bicubic_x4_2sep.tif"],
        "model_x4_b4_DEMO_WSX4_1024_plugin_2sep": ["sr_wp24/reference_plugin_x4_b4_2sep.tif"],
    }.get(key, [])
    for c in cands:
        p = data_root / c
        if p.is_file():
            return p
    return None


# ------------------------------------------------------------------------ self-test
def _write(path, arr, crs="EPSG:32636", transform=Affine(10.0, 0.0, 400000.0, 0.0, -10.0,
                                                        4400000.0), nodata=None):
    arr = np.asarray(arr)
    if arr.ndim == 2:
        arr = arr[None]
    prof = dict(driver="GTiff", height=arr.shape[1], width=arr.shape[2], count=arr.shape[0],
                dtype=arr.dtype, crs=crs, transform=transform)
    if nodata is not None:
        prof["nodata"] = nodata
    with rasterio.open(str(path), "w", **prof) as d:
        d.write(arr)
    return path


def self_test(data_root, keep):
    rng = np.random.default_rng(20260902)
    tmp = Path(tempfile.mkdtemp(prefix="sr_cli_selftest_"))
    rows = []
    a3 = rng.integers(0, 255, (3, 64, 64), dtype=np.uint8)
    good = _write(tmp / "good.tif", a3)
    model = data_root / "plugin_models" / "gencp_sr_x4_b4.onnx" if data_root else None

    def refused(name, args, code, out=None):
        rc, so, se = run_tool(args)
        left = out is not None and Path(out).exists()
        ok = (rc == code) and not left
        rows.append((ok, f"{name} -> exit {rc} (expected {code})"
                     + (", output left on disk" if left else ""),
                     se.strip().splitlines()[-1] if se.strip() else so.strip()[-200:]))

    # KF1 no CRS
    nocrs = _write(tmp / "nocrs.tif", a3, crs=None)
    refused("KF1 raster with no CRS", [nocrs, tmp / "kf1.tif"], 4, tmp / "kf1.tif")
    # KF2 band count the model does not accept (3-band uint16 to a 4-band model)
    if model and model.is_file():
        u16 = _write(tmp / "u16_3band.tif", rng.integers(300, 5000, (3, 64, 64),
                                                         dtype=np.uint16))
        refused("KF2 band count the model refuses (3 bands to a 4-band model)",
                [u16, tmp / "kf2.tif", "--method", "model", "--model", model], 6,
                tmp / "kf2.tif")
    else:
        rows.append((False, "KF2 NOT RUN — gencp_sr_x4_b4.onnx not found", str(model)))
    # KF3 model path that does not exist
    refused("KF3 model path that does not exist",
            [good, tmp / "kf3.tif", "--method", "model", "--model", tmp / "nope.onnx"], 8,
            tmp / "kf3.tif")
    # KF4 output exists without --overwrite: the sentinel must be byte-identical afterwards
    sentinel = tmp / "exists.tif"
    sentinel.write_bytes(b"sentinel-not-a-tif")
    before = hashlib.sha256(sentinel.read_bytes()).hexdigest()
    refused("KF4 output exists, no --overwrite", [good, sentinel], 9)
    after = hashlib.sha256(sentinel.read_bytes()).hexdigest()
    rows.append((before == after, "KF4 the existing output was left byte-identical", ""))
    # KF5 rotated raster
    rot = _write(tmp / "rot.tif", a3,
                 transform=Affine(10.0, 0.5, 400000.0, 0.5, -10.0, 4400000.0))
    refused("KF5 rotated/sheared raster", [rot, tmp / "kf5.tif"], 5, tmp / "kf5.tif")
    # KF6 input missing
    refused("KF6 input that does not exist", [tmp / "missing.tif", tmp / "kf6.tif"], 3,
            tmp / "kf6.tif")
    # KF7 overlap not a whole number of source pixels
    refused("KF7 overlap 325 m on a 10 m raster (32.5 px)",
            [good, tmp / "kf7.tif", "--overlap", "325"], 11, tmp / "kf7.tif")
    # DG degenerate: no arguments at all
    rc, so, se = run_tool([])
    rows.append((rc != 0 and "usage" in (se + so).lower(),
                 f"DG no arguments -> exit {rc}, usage printed", se.strip()[:120]))
    # DG2 unknown argument
    rc, so, se = run_tool([good, tmp / "dg2.tif", "--scalee", "2"])
    rows.append((rc == 2 and not (tmp / "dg2.tif").exists(),
                 f"DG2 unrecognised argument --scalee -> exit {rc}", ""))

    # KT: the known-true control — the same synthetic raster IS accepted (exit 0)
    rc, so, se = run_tool([good, tmp / "kt.tif", "--scale", "2"])
    rows.append((rc == 0 and (tmp / "kt.tif").is_file(),
                 f"KT the accepting case runs -> exit {rc}", se.strip()[-200:]))
    # --overwrite accepted on the second run
    rc, so, se = run_tool([good, tmp / "kt.tif", "--scale", "2", "--overwrite"])
    rows.append((rc == 0, f"KT --overwrite on an existing output -> exit {rc}", ""))

    # (3) dry-run vs real on the synthetic raster, default scale
    rc, dry_out, _ = run_tool([good, tmp / "dry.tif", "--dry-run"])
    dry = parse_dry(dry_out)
    rows.append((not (tmp / "dry.tif").exists(), "dry-run wrote nothing", ""))
    rc, _, _ = run_tool([good, tmp / "dry.tif"])
    real = grid_of(tmp / "dry.tif")
    same = (dry["crs"] == real["crs"] and dry["pixel"] == real["pixel"]
            and dry["origin"] == real["origin"] and dry["size"] == real["size"])
    rows.append((same, "dry-run grid == written grid (synthetic, default scale)",
                 f"dry {dry}\nreal {real}"))

    # the comparison's own known-false: perturb one pixel, the hash must differ and the
    # first differing pixel must be reported at exactly that coordinate
    src_out = tmp / "dry.tif"
    pert = tmp / "perturbed.tif"
    with rasterio.open(str(src_out)) as d:
        arr, prof = d.read(), d.profile
    b, r, c = 1, 37, 91
    arr[b, r, c] = (int(arr[b, r, c]) + 1) % 256
    with rasterio.open(str(pert), "w", **prof) as d:
        d.write(arr)
    h0, h1 = pixhash(src_out), pixhash(pert)
    fd = first_diff(src_out, pert)
    rows.append((h0 != h1, "KF-hash one perturbed pixel changes the pixel hash",
                 f"{h0[:16]} vs {h1[:16]}"))
    rows.append((fd is not None and fd[:3] == (b + 1, r, c),
                 "KF-hash first differing pixel reported at the perturbed coordinate",
                 f"reported {fd}, planted band {b + 1} row {r} col {c}"))
    # KT-hash: identical files hash identically and report no difference
    rows.append((pixhash(src_out) == h0 and first_diff(src_out, src_out) is None,
                 "KT-hash identical file -> same hash, no differing pixel", ""))

    n_fail = report("WP24 self-test — known-false refusals, degenerate calls, dry-run", rows)
    not_run = [r for r in rows if "NOT RUN" in r[1]]
    if not keep:
        for p in tmp.iterdir():
            p.unlink()
        tmp.rmdir()
    else:
        print(f"kept: {tmp}")
    if not_run:
        print("NOT RUN present — verdict withheld")
        return 2
    print(f"SELF-TEST: {'PASS' if n_fail == 0 else 'FAIL'} "
          f"({len(rows) - n_fail}/{len(rows)} checks)")
    return 1 if n_fail else 0


def main():
    args = sys.argv[1:]
    keep = "--keep" in args
    explicit = next((a.split("=", 1)[1] for a in args if a.startswith("--data-root=")), None)
    data_root = find_data_root(explicit)
    want_eq = "--equivalence" in args or "--all" in args
    want_st = "--self-test" in args or "--all" in args
    if not (want_eq or want_st):
        sys.stderr.write("sr_cli_tests.py: nothing to check.\n"
                         "  Usage: sr_cli_tests.py --equivalence | --self-test | --all "
                         "[--data-root=DIR] [--keep]\n")
        return 2
    if data_root is None:
        sys.stderr.write("sr_cli_tests.py: data root with tiles36SVJ/TCI.tif not found; "
                         "pass --data-root=DIR\n")
        return 2
    print(f"data root: {data_root}")
    rc = 0
    if want_st:
        rc = max(rc, self_test(data_root, keep))
    if want_eq:
        rc = max(rc, equivalence(data_root, keep))
    return rc


if __name__ == "__main__":
    sys.exit(main())
