"""Bisect what makes the end-of-training torch.save hang.

Runs real optimiser steps on the real device, then saves a dict whose contents --case
chooses. A watchdog dumps every thread's stack and aborts if the save does not return, so
a hang is reported as a stack rather than inferred from a CPU percentage.
"""
import argparse, faulthandler, json, os, sys, time
from pathlib import Path
sys.path.insert(0, "tubitak/sr"); sys.path.insert(0, "tubitak/sr/sr_train")
import numpy as np, torch
import config as C
from model import SRNet


def versions_objects():
    """Exactly what train.versions() returns - torch.__version__ is a TorchVersion."""
    import numpy
    return dict(torch=torch.__version__, numpy=numpy.__version__,
                python=sys.version.split()[0], mps=True)


def versions_strings():
    import numpy
    return dict(torch=str(torch.__version__), numpy=str(numpy.__version__),
                python=sys.version.split()[0], mps=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True)
    ap.add_argument("--device", default="mps")
    ap.add_argument("--steps", type=int, default=12)
    ap.add_argument("--timeout", type=float, default=90.0)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sync", type=int, default=0)
    ap.add_argument("--drop-stray", dest="drop_stray", type=int, default=0)
    ap.add_argument("--stray", type=int, default=1,
                    help="leave a non-blocking device transfer alive, as the real loop does")
    a = ap.parse_args()

    dev = torch.device(a.device)
    torch.manual_seed(C.TRAIN_SEED)
    model = SRNet(ch=C.WIDTH, n_blocks=C.N_BLOCKS, scale=C.SCALE, bands=C.N_BANDS).to(dev)
    opt = torch.optim.Adam(model.parameters(), lr=1e-4)
    rng = np.random.default_rng(0)
    px = C.CHIP_PX if hasattr(C, "CHIP_PX") else 256
    lo_px = px // C.SCALE

    t0 = time.perf_counter()
    for i in range(a.steps):
        lo = torch.from_numpy(rng.random((4, C.N_BANDS, lo_px, lo_px), np.float32)).to(dev)
        hi = torch.from_numpy(rng.random((4, C.N_BANDS, px, px), np.float32)).to(dev)
        loss = torch.nn.functional.l1_loss(model(lo), hi)
        opt.zero_grad(set_to_none=True); loss.backward(); opt.step()
    print(f"  {a.steps} steps in {time.perf_counter()-t0:.1f}s on {dev}", flush=True)

    stray = None
    if a.stray == 2:
        # a live MPS tensor, but transferred BLOCKING - is it the transfer or the tensor?
        stray = (torch.from_numpy(rng.random((4, C.N_BANDS, lo_px, lo_px), np.float32)).to(dev),
                 torch.from_numpy(rng.random((4, C.N_BANDS, px, px), np.float32)).to(dev))
        print("  a BLOCKING device transfer is alive and unconsumed", flush=True)
    elif a.stray:
        # what the real loop leaves alive: one more batch fetched non-blocking, then break
        stray = (torch.from_numpy(rng.random((4, C.N_BANDS, lo_px, lo_px), np.float32))
                 .to(dev, non_blocking=True),
                 torch.from_numpy(rng.random((4, C.N_BANDS, px, px), np.float32))
                 .to(dev, non_blocking=True))
        print("  a non-blocking device transfer is alive and unconsumed", flush=True)

    cases = {
        "full":        lambda: dict(model=model.state_dict(), opt=opt.state_dict(),
                                    step=1, best=0.1),
        "model_only":  lambda: dict(model=model.state_dict()),
        "opt_only":    lambda: dict(opt=opt.state_dict()),
        "scalars":     lambda: dict(step=1, best=0.1),
        "tiny":        lambda: dict(t=torch.zeros(4, device=dev)),
        "tiny_cpu":    lambda: dict(t=torch.zeros(4)),
        "cpu_state":   lambda: dict(model={k: v.detach().to("cpu")
                                           for k, v in model.state_dict().items()},
                                    opt=opt.state_dict(), step=1, best=0.1),
        "versions_obj":  lambda: dict(step=1, versions=versions_objects()),
        "versions_str":  lambda: dict(step=1, versions=versions_strings()),
        "fix":         lambda: dict(model={k: v.detach().to("cpu")
                                           for k, v in model.state_dict().items()},
                                    opt=cpu_opt(opt.state_dict()), step=1, best=0.1,
                                    versions=versions_strings()),
    }
    payload = cases[a.case]()
    if a.sync:
        torch.mps.synchronize()
        print("  torch.mps.synchronize() called before save", flush=True)
    if a.drop_stray:
        stray = None
        print("  the stray transfer was dropped before save", flush=True)

    faulthandler.dump_traceback_later(a.timeout, exit=True,
                                      file=open(a.out + ".stack", "w"))
    t1 = time.perf_counter()
    torch.save(payload, a.out)
    faulthandler.cancel_dump_traceback_later()
    dt = time.perf_counter() - t1
    print(f"  SAVED case={a.case} in {dt:.2f}s, {os.path.getsize(a.out)} bytes", flush=True)
    return 0


def cpu_opt(sd):
    """Adam state moved to CPU, structure preserved."""
    out = {"param_groups": sd["param_groups"], "state": {}}
    for k, st in sd["state"].items():
        out["state"][k] = {kk: (vv.detach().to("cpu") if torch.is_tensor(vv) else vv)
                           for kk, vv in st.items()}
    return out


if __name__ == "__main__":
    sys.exit(main())
