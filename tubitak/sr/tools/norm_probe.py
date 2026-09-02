"""Why is the scale-4 control ABOVE the scale-2 control, when the task is harder?

Two candidates, separated by a 2x2 on the same chips and the same code path:
  bands  {B02,B03,B04}  vs  {B02,B03,B04,B08}
  divisor      5000     vs        10000
Everything else - degradation, upsampler, metric functions, chip membership - is held fixed.
The scale-2 control is 3 bands at divisor 5000, so cell (3, 5000) is the like-for-like cell.
"""
import json, sys, time
from pathlib import Path
import numpy as np
SR = Path("tubitak/sr").resolve(); ROOT = SR.parents[1]
for p in (str(SR), str(ROOT / "tubitak" / "tests")):
    sys.path.insert(0, p)
import warnings; warnings.filterwarnings("ignore")
from sr_core.upsample import BicubicUpsampler
from sr_data.degrade import degrade_chip
from sr_data.metrics import mae_chip, psnr_chip, ssim_chip, summarise
from sr_train import config as C, data as D

assert C.VARIANT == "x4" and C.SCALE == 4 and C.N_BANDS == 4, C.VARIANT

def cell(chips, nb, div):
    up = BicubicUpsampler(scale=4)
    ps, ss, ma = [], [], []
    for i in range(chips.shape[0]):
        lo, hi = degrade_chip(chips[i][:nb], np.float32(div), scale=4)
        pred = np.moveaxis(up.upsample(np.moveaxis(lo, 0, -1)), -1, 0)
        ps.append(psnr_chip(pred, hi, 1.0)); ss.append(ssim_chip(pred, hi, 1.0))
        ma.append(mae_chip(pred, hi))
    assert up.n_clipped == 0, f"upsampler clipped {up.n_clipped}/{up.n_total} - path is NOT linear"
    return np.asarray(ps), np.asarray(ss), np.asarray(ma)

out = {}
for split in ("heldout", "test"):
    chips, _ = D.load_split(split)
    print(f"\n=== {split}  n={chips.shape[0]} ===")
    print(f"{'bands':>6} {'divisor':>8} | {'PSNR dB':>9} {'SSIM':>9} {'MAE':>12}")
    out[split] = {}
    for nb in (3, 4):
        for div in (5000.0, 10000.0):
            t = time.perf_counter()
            ps, ss, ma = cell(chips, nb, div)
            out[split][f"b{nb}_d{div:.0f}"] = dict(
                n=len(ps), psnr=float(ps.mean()), ssim=float(ss.mean()), mae=float(ma.mean()),
                psnr_per_chip=[float(v) for v in ps])
            print(f"{nb:>6} {div:>8.0f} | {ps.mean():9.4f} {ss.mean():9.6f} {ma.mean():12.8f}"
                  f"   ({time.perf_counter()-t:.0f}s)")
Path("tubitak/data/sr_wald_corpus_x4/norm_probe.json").write_text(json.dumps(out, indent=2))
print("\nwrote tubitak/data/sr_wald_corpus_x4/norm_probe.json")
