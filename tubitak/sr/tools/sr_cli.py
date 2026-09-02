#!/usr/bin/env python
"""Command line front end for GenCP Super-Resolution — the same path the QGIS plugin runs.

    python tubitak/sr/tools/sr_cli.py GIRDI.tif CIKTI.tif                     bicubic
    python tubitak/sr/tools/sr_cli.py GIRDI.tif CIKTI.tif --method model --model M.onnx

WP24. This file is a THIN SHELL. It contains no super-resolution arithmetic: it imports
`sr_core.run.superresolve` (the pipeline) and `sr_plugin.onnx_upsample` (the model contract
and the ONNX upsampler), which are exactly the objects the plugin's `task.py` calls. Neither
imports QGIS or Qt at module level, which is what makes this construction possible (the
stage 1 trace in `docs/18-depo-tasima.md` §16). Equivalence to the plugin is therefore
structural for the pixels, and it is still MEASURED: `tubitak/sr/tests/sr_cli_tests.py`
compares this tool's outputs with every pixel hash the project has registered.

What the plugin's dialog contributes that is NOT in those two modules is parameter
selection, and that is restated here rather than imported, because `dialog.py` imports Qt:

  * the bicubic scale (`dialog.BICUBIC_SCALE`) and the model inference tile
    (`dialog.MODEL_INFER_TILE_PX`) are READ FROM dialog.py's source with `ast`, never
    imported and never copied as literals, so this tool cannot silently drift from the
    plugin when those constants change;
  * bicubic: tile `tiles.DEFAULT_TILE_PX`, overlap `tiles.DEFAULT_OVERLAP_PX`, feather;
  * model: scale, band count, normalisation, tiling and crop margin from the model's own
    contract (`read_provenance`); tile = the contract's `tile_src` when it crop-tiles,
    else `MODEL_INFER_TILE_PX`; overlap = the contract's `overlap_src`; the input is
    checked against the contract with `validate_input` before any tile runs;
  * `clip=True` on both paths, as `task.py` constructs the upsampler.

Nothing here reaches the network, by construction: the only I/O is rasterio on two local
paths and onnxruntime on one local file; a `/vsi` or URL-shaped path is refused before
GDAL sees it. The plugin package and `sr_core` are not modified by this work package.

User-facing text is Turkish, as the plugin's is (`strings.py`); code and comments stay
English, as everywhere else in the project.
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve()
SR = HERE.parents[1]                   # tubitak/sr
if str(SR) not in sys.path:
    sys.path.insert(0, str(SR))

TOOL = "sr_cli"

# ----------------------------------------------------------------------------- exit codes
# Distinct, documented, and asserted by sr_cli_tests.py. 0 is success, 2 is argparse's own
# usage error (kept so `--help`-style mistakes look like every other Python tool).
EXIT_OK = 0
EXIT_USAGE = 2
EXIT_INPUT_MISSING = 3
EXIT_INPUT_NO_CRS = 4
EXIT_GRID = 5                   # rotated/sheared, zero pixel size, or the Gate S contract
EXIT_BANDS = 6
EXIT_DTYPE = 7
EXIT_MODEL = 8                  # missing, unreadable, or without a usable contract
EXIT_OUTPUT_EXISTS = 9
EXIT_OUTPUT_IS_INPUT = 10
EXIT_OVERLAP = 11
EXIT_NO_ONNXRUNTIME = 12
EXIT_NO_RASTERIO = 13
EXIT_WRITE = 14
EXIT_SCALE = 15
EXIT_GATE_S = 16                # written output failed the tool's own Gate S re-check


class Refusal(Exception):
    """A refusal the user can act on: exit code plus a Turkish message."""

    def __init__(self, code, msg):
        super().__init__(msg)
        self.code = code


# --------------------------------------------------------------------- plugin constants
def _plugin_constants():
    """`BICUBIC_SCALE` and `MODEL_INFER_TILE_PX` read from dialog.py's SOURCE.

    dialog.py imports Qt at module level and cannot be imported here; parsing it keeps one
    definition of each constant, in the plugin, with this tool as a reader of it.
    """
    src = SR / "sr_plugin" / "dialog.py"
    tree = ast.parse(src.read_text(encoding="utf-8"), filename=str(src))
    want = {"BICUBIC_SCALE": None, "MODEL_INFER_TILE_PX": None}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in want \
                and isinstance(node.value, ast.Constant) \
                and isinstance(node.value.value, int):
            want[node.targets[0].id] = int(node.value.value)
    missing = [k for k, v in want.items() if v is None]
    if missing:
        raise RuntimeError(f"{src}: could not read {missing} as integer module constants")
    return want


def _plugin_version():
    meta = SR / "sr_plugin" / "metadata.txt"
    for line in meta.read_text(encoding="utf-8").splitlines():
        if line.startswith("version="):
            return line.split("=", 1)[1].strip()
    return "?"


# ------------------------------------------------------------------------------ helpers
def _tr(x):
    """Decimal comma for user-facing numbers (terimler.md)."""
    return str(x).replace(".", ",")


def _local_file(path, what, code):
    s = str(path)
    if "://" in s or s.startswith("/vsi"):
        raise Refusal(code, f"{what} yerel bir dosya olmalıdır; ağ ya da sanal yol "
                            f"kabul edilmez: {s}")
    p = Path(s)
    if not p.is_file():
        raise Refusal(code, f"{what} bulunamadı: {s}\n  Yolu ve dosya adını kontrol edin.")
    return p


def _open_source(path):
    try:
        import rasterio
    except ImportError as exc:
        raise Refusal(EXIT_NO_RASTERIO,
                      "rasterio paketi bu Python ortamında yok; araç raster okuyup yazmak "
                      f"için onu kullanır ve onsuz çalışamaz. ({exc})")
    try:
        d = rasterio.open(str(path))
    except Exception as exc:                                    # noqa: BLE001
        raise Refusal(EXIT_INPUT_MISSING, f"Girdi raster olarak açılamadı: {path}\n  {exc}")
    with d:
        T = d.transform
        info = dict(path=str(path), width=d.width, height=d.height, count=d.count,
                    dtype=d.dtypes[0], crs=d.crs, transform=T, nodata=d.nodata)
    if info["crs"] is None:
        raise Refusal(EXIT_INPUT_NO_CRS,
                      f"Girdinin koordinat referans sistemi (KRS) yok: {path}\n"
                      "  Çıktı ızgarası kaynağın KRS'sinden türetilir; KRS'siz bir raster "
                      "işlenmez. Dosyaya doğru KRS'yi atayın (yeniden örneklemeden, "
                      "örneğin gdal_edit.py -a_srs ile) ve tekrar deneyin.")
    if T.b != 0.0 or T.d != 0.0:
        raise Refusal(EXIT_GRID,
                      f"Girdi kuzeye dönük değil (döndürülmüş ya da eğilmiş: b={T.b!r}, "
                      f"d={T.d!r}): {path}\n  Araç yeniden projeksiyon ya da yeniden "
                      "örnekleme yapmaz; kaynağı önce kuzeye dönük bir ızgaraya alın.")
    if T.a == 0.0 or T.e == 0.0:
        raise Refusal(EXIT_GRID, f"Girdinin piksel boyu bir eksende sıfır "
                                 f"(a={T.a!r}, e={T.e!r}): {path}")
    if info["width"] < 1 or info["height"] < 1:
        raise Refusal(EXIT_GRID, f"Girdi boş: {info['width']} x {info['height']} piksel")
    return info


_BICUBIC_DTYPES = ("uint8", "int8", "uint16", "int16", "uint32", "int32",
                   "float32", "float64")


def _check_bicubic_dtype(info):
    if info["dtype"] not in _BICUBIC_DTYPES:
        raise Refusal(EXIT_DTYPE,
                      f"Veri tipi {info['dtype']} bikübik yöntemle desteklenmez. "
                      f"Desteklenenler: {', '.join(_BICUBIC_DTYPES)}.")


def _load_model(model_path):
    """The model's contract and a fresh session, exactly as `task.py` constructs them."""
    try:
        from sr_plugin.onnx_upsample import (read_provenance, validate_input,
                                             OnnxUpsampler, ModelInputError)
    except ImportError as exc:
        raise Refusal(EXIT_MODEL, f"Eklenti paketi içe aktarılamadı: {exc}")
    try:
        sess, prov = read_provenance(str(model_path))
    except ImportError as exc:
        raise Refusal(EXIT_NO_ONNXRUNTIME,
                      "onnxruntime paketi bu Python ortamında yok; eğitilmiş model bu "
                      "paketle çalışır. Bikübik yöntem onsuz da çalışır; model yolu için "
                      f"onnxruntime kurulmalıdır. ({exc})")
    except ModelInputError as exc:
        raise Refusal(EXIT_MODEL, f"Model dosyası kullanılabilir bir künye taşımıyor: "
                                  f"{model_path}\n  {exc.key}: {exc.fmt}")
    except Exception as exc:                                    # noqa: BLE001
        raise Refusal(EXIT_MODEL, f"Model dosyası okunamadı: {model_path}\n  {exc}")
    return sess, prov, validate_input, OnnxUpsampler, ModelInputError


def _validate_for_model(info, prov, validate_input, ModelInputError):
    """Same check the dialog runs before enabling the run button."""
    try:
        validate_input(info["path"], prov)
    except ModelInputError as exc:
        f = exc.fmt
        if exc.key == "err_bands":
            raise Refusal(EXIT_BANDS,
                          f"Model {f['want']} bant bekler ({f['order']}); girdide "
                          f"{f['got']} bant var.\n  Bu modele uygun bant sırasıyla "
                          "hazırlanmış yansıtma dosyasını seçin.")
        if exc.key == "err_dtype":
            raise Refusal(EXIT_DTYPE,
                          f"Model 16 bit tam sayı (uint16) yansıtma değerleri bekler; "
                          f"girdinin veri tipi {f['got']}.\n  8 bitlik TCI görseli modele "
                          "verilmez; onu bikübik yöntemle kullanabilirsiniz.")
        if exc.key == "err_range":
            raise Refusal(EXIT_DTYPE,
                          "Girdi 16 bit ama değerleri 8 bitlik bir görüntününki gibi "
                          f"(%99,9 dilimi {f['p999']:.0f}). Bu dosya büyük olasılıkla "
                          "dönüştürülmüş bir TCI; yansıtma dosyasını seçin.")
        raise Refusal(EXIT_DTYPE, f"Girdi modele uygun değil: {exc.key} {f}")


def _overlap_px(metres, default_px, info):
    """Plugin overlaps are SOURCE PIXELS. Metres are accepted only as an exact multiple."""
    if metres is None:
        return int(default_px)
    px = abs(info["transform"].a)
    q = metres / px
    if q < 0 or abs(q - round(q)) > 1e-9:
        raise Refusal(EXIT_OVERLAP,
                      f"Bindirme {_tr(metres)} m, {_tr(px)} m'lik kaynak pikselinin tam "
                      f"katı değil ({_tr(round(q, 4))} piksel).\n  Karo bindirmesi kaynak "
                      "pikseli cinsinden tam sayı olmalıdır; örneğin "
                      f"{_tr('%g' % (int(round(q)) * px))} m.")
    return int(round(q))


def _plan(args, consts):
    """Everything the run needs, decided the way the dialog decides it. No I/O writes."""
    src = _local_file(args.input, "Girdi", EXIT_INPUT_MISSING)
    info = _open_source(src)
    out = Path(args.output)
    try:
        if out.resolve() == src.resolve():
            raise Refusal(EXIT_OUTPUT_IS_INPUT, "Çıktı yolu girdiyle aynı olamaz.")
    except OSError:
        pass
    if out.exists() and not args.overwrite:
        raise Refusal(EXIT_OUTPUT_EXISTS,
                      f"Çıktı dosyası zaten var: {out}\n  Üzerine yazmak için --overwrite "
                      "verin ya da başka bir ad seçin.")

    from sr_core import tiles as _tiles
    plan = dict(src=info, out=str(out))
    method = args.method
    if method == "bicubic":
        if args.model:
            raise Refusal(EXIT_USAGE, "--model yalnızca model yöntemleriyle kullanılır.")
        _check_bicubic_dtype(info)
        scale = consts["BICUBIC_SCALE"] if args.scale is None else int(args.scale)
        if scale < 1 or (scale & (scale - 1)):
            raise Refusal(EXIT_SCALE, f"Ölçek ikinin kuvveti olmalıdır (1, 2, 4, 8 …); "
                                      f"verilen: {scale}")
        plan.update(method="bicubic", scale=scale, tile_px=_tiles.DEFAULT_TILE_PX,
                    overlap_px=_overlap_px(args.overlap, _tiles.DEFAULT_OVERLAP_PX, info),
                    tiling="feather", margin_out=0, model=None, upsampler=None,
                    blend_default="feather")
    else:
        if not args.model:
            raise Refusal(EXIT_USAGE, f"--method {method} bir model dosyası gerektirir: "
                                      "--model DOSYA.onnx")
        model = _local_file(args.model, "Model dosyası", EXIT_MODEL)
        sess, prov, validate_input, OnnxUpsampler, ModelInputError = _load_model(model)
        _validate_for_model(info, prov, validate_input, ModelInputError)
        scale = int(prov["scale"])
        if args.scale is not None and int(args.scale) != scale:
            raise Refusal(EXIT_SCALE,
                          f"--scale {args.scale} verildi ama model {scale}x; model yolunda "
                          "ölçek modelin künyesinden okunur ve değiştirilemez.")
        tile_px = int(prov["tile_src"]) if prov["tiling"] == "crop" \
            else consts["MODEL_INFER_TILE_PX"]
        plan.update(method=method, scale=scale, tile_px=tile_px,
                    overlap_px=_overlap_px(args.overlap, prov["overlap_src"], info),
                    tiling=prov["tiling"], margin_out=int(prov["margin_out"]),
                    model=str(model), prov=prov, blend_default=prov["tiling"],
                    upsampler=lambda: OnnxUpsampler(str(model), clip=True))
    # --blend: the plugin offers no choice; its rule is "what the contract declares".
    if args.blend != "auto" and args.blend != plan["tiling"]:
        print(f"{TOOL}: uyarı: --blend {args.blend} istendi; eklenti bu yöntem için "
              f"{plan['tiling']} kullanır. Çıktı eklentininkiyle aynı olmayacaktır.",
              file=sys.stderr)
        plan["tiling"] = args.blend
    if plan["tiling"] == "crop":
        from sr_core.mosaic import min_overlap_for_margin
        need = min_overlap_for_margin(plan["margin_out"], plan["scale"])
        if plan["overlap_px"] < need:
            raise Refusal(EXIT_OVERLAP,
                          f"Kırpmalı birleştirme için bindirme en az {need} kaynak "
                          f"pikseli olmalıdır (kenar {plan['margin_out']} çıktı pikseli, "
                          f"ölçek {plan['scale']}); verilen {plan['overlap_px']}.")

    from sr_core import grid as _grid
    ow, oh, oT = _grid.output_grid(info["transform"], info["width"], info["height"],
                                   plan["scale"])
    tlist, _stride = _tiles.tile_grid(info["width"], info["height"],
                                      plan["tile_px"], plan["overlap_px"])
    plan.update(out_w=ow, out_h=oh, out_T=oT, n_tiles=len(tlist))
    return plan


def _grid_lines(plan):
    """The output grid in the terms Gate S is stated in. Exact reprs, not rounded."""
    s, i, T = plan["scale"], plan["src"], plan["out_T"]
    st = i["transform"]
    px = abs(st.a)
    return [
        f"S1 KRS                : {i['crs'].to_string()}  (kaynakla aynı)",
        f"S2 piksel boyu        : {T.a!r} x {T.e!r}  (= {st.a!r} / {s}, {st.e!r} / {s}; tam)",
        f"S3 başlangıç noktası  : ({T.c!r}, {T.f!r})  (kaynakla aynı)",
        f"S4 boyut              : {plan['out_w']} x {plan['out_h']} piksel  "
        f"(= {s} x {i['width']} x {i['height']})",
        f"yöntem                : {plan['method']}, ölçek {s}"
        + (f", model {Path(plan['model']).name}" if plan.get("model") else ""),
        f"bant / veri tipi      : {i['count']} bant, {i['dtype']}"
        + (f", nodata {i['nodata']!r}" if i["nodata"] is not None else ""),
        f"karo                  : {plan['tile_px']} px, bindirme {plan['overlap_px']} px "
        f"({_tr('%g' % (plan['overlap_px'] * px))} m), {plan['n_tiles']} karo, "
        f"birleştirme {plan['tiling']}"
        + (f" (kenar {plan['margin_out']} çıktı px)" if plan["tiling"] == "crop" else ""),
    ]


def _gate_s_recheck(plan):
    """Re-open the written file and assert Gate S S1–S4 exactly. S5 follows from S1–S4."""
    import rasterio
    i, s = plan["src"], plan["scale"]
    with rasterio.open(plan["out"]) as d:
        T, crs, w, h = d.transform, d.crs, d.width, d.height
    st = i["transform"]
    checks = [
        ("S1 KRS", crs == i["crs"], f"{crs} != {i['crs']}"),
        ("S2 piksel boyu", T.a == st.a / s and T.e == st.e / s,
         f"{T.a!r},{T.e!r} != {st.a / s!r},{st.e / s!r}"),
        ("S3 başlangıç noktası", T.c == st.c and T.f == st.f,
         f"({T.c!r},{T.f!r}) != ({st.c!r},{st.f!r})"),
        ("S4 boyut", w == i["width"] * s and h == i["height"] * s,
         f"{w}x{h} != {i['width'] * s}x{i['height'] * s}"),
    ]
    bad = [(n, d) for n, ok, d in checks if not ok]
    if bad:
        raise Refusal(EXIT_GATE_S, "Yazılan çıktı ızgara sözleşmesini (Gate S) sağlamıyor: "
                      + "; ".join(f"{n}: {d}" for n, d in bad)
                      + f"\n  Dosya yerinde bırakıldı: {plan['out']}")
    return [n for n, _ok, _d in checks]


# --------------------------------------------------------------------------------- main
def build_parser(consts, version):
    p = argparse.ArgumentParser(
        prog=TOOL,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "GenCP Süper Çözünürlük — komut satırı. Bir GeoTIFF'i, kendi ızgarasının tam "
            "tamsayı incelmesi üzerine süper çözünürlükle yazar. QGIS eklentisiyle aynı "
            "kodu çalıştırır ve aynı pikselleri üretir; çıktı ızgarası kaynağın KRS'sini, "
            "başlangıç noktasını ve kapsamını olduğu gibi korur (Gate S)."),
        epilog=(
            "Örnekler:\n"
            f"  {TOOL} girdi.tif cikti.tif\n"
            f"      bikübik, ölçek {consts['BICUBIC_SCALE']} (eklentinin bikübik varsayılanı)\n"
            f"  {TOOL} girdi.tif cikti.tif --method model --model gencp_sr_x4_b4.onnx\n"
            "      eğitilmiş model; ölçek, bant sayısı ve karo düzeni modelin künyesinden okunur\n"
            f"  {TOOL} girdi.tif cikti.tif --method model --model M.onnx --dry-run\n"
            "      hiçbir şey yazmadan, yazılacak ızgarayı Gate S terimleriyle basar\n\n"
            "Çıkış kodları: 0 başarı; 2 kullanım hatası; 3 girdi yok/okunamıyor; 4 girdinin "
            "KRS'si yok;\n  5 girdi kuzeye dönük değil ya da ızgara sözleşmesi sağlanamıyor; "
            "6 bant sayısı modele uymuyor;\n  7 veri tipi desteklenmiyor; 8 model dosyası "
            "yok/okunamıyor; 9 çıktı var, --overwrite yok;\n  10 çıktı girdiyle aynı; "
            "11 bindirme piksel katı değil ya da yetersiz; 12 onnxruntime yok;\n  13 rasterio "
            "yok; 14 yazma hatası; 15 ölçek geçersiz; 16 yazılan çıktı Gate S'i sağlamadı.\n"
            "Ağ erişimi yoktur: yalnızca verilen yerel dosyalar okunur ve yazılır."))
    p.add_argument("input", help="girdi GeoTIFF (kuzeye dönük, KRS'li)")
    p.add_argument("output", help="yazılacak GeoTIFF; önce geçici dosyaya yazılır, sonra "
                                  "adı değiştirilir (yarım dosya kalmaz)")
    p.add_argument("--method", choices=("bicubic", "model", "wsx4"), default="bicubic",
                   help="eklentideki yöntemler: bicubic (varsayılan; model gerekmez), "
                        "model (GenCP eğitilmiş model), wsx4 (referans model). model ve "
                        "wsx4 aynı yolu izler; ikisi de --model ister")
    p.add_argument("--model", metavar="DOSYA.onnx",
                   help="ONNX model dosyası; --method model/wsx4 için zorunlu. wsx4 için "
                        "aynı adlı .yaml dosyası modelin yanında olmalıdır")
    p.add_argument("--scale", type=int, metavar="N",
                   help=f"yalnızca bicubic: ölçek katsayısı, ikinin kuvveti (varsayılan "
                        f"{consts['BICUBIC_SCALE']}, eklentinin bikübik ölçeği). Model "
                        "yolunda modelin künyesinden okunur; verilirse ona eşit olmalıdır")
    p.add_argument("--overlap", type=float, metavar="METRE",
                   help="karo bindirmesi, metre; kaynak pikselinin tam katı olmalıdır. "
                        "Varsayılan eklentininkidir: bicubic 32 kaynak pikseli, model "
                        "yolunda modelin künyesindeki değer")
    p.add_argument("--blend", choices=("auto", "feather", "crop"), default="auto",
                   help="karo birleştirme. auto (varsayılan) eklentinin kuralıdır: bicubic "
                        "feather, model yolunda modelin bildirdiği düzen. Başka bir seçim "
                        "çıktıyı eklentininkinden ayırır ve uyarı basılır")
    p.add_argument("--overwrite", action="store_true",
                   help="var olan çıktının üzerine yaz (varsayılan: var olan çıktı reddedilir)")
    p.add_argument("--dry-run", action="store_true",
                   help="hiçbir şey yazma; yazılacak ızgarayı Gate S terimleriyle bas ve çık")
    p.add_argument("--version", action="version",
                   version=f"{TOOL} {version} (GenCP Super-Resolution eklentisi "
                           f"{version} ile aynı sr_core ve model çekirdeği)")
    return p


def main(argv=None):
    consts = _plugin_constants()
    parser = build_parser(consts, _plugin_version())
    if not (sys.argv[1:] if argv is None else argv):
        parser.print_usage(sys.stderr)
        print(f"{TOOL}: girdi ve çıktı dosyası verilmelidir. Yardım için --help.",
              file=sys.stderr)
        return EXIT_USAGE
    args = parser.parse_args(argv)
    try:
        plan = _plan(args, consts)
        lines = _grid_lines(plan)
        if args.dry_run:
            print("Kuru çalıştırma — yazılacak ızgara (Gate S terimleriyle):")
            for ln in lines:
                print("  " + ln)
            print("Hiçbir şey yazılmadı.")
            return EXIT_OK

        from sr_core.run import superresolve
        print(f"{TOOL}: {plan['src']['width']} x {plan['src']['height']} -> "
              f"{plan['out_w']} x {plan['out_h']}, {plan['n_tiles']} karo, "
              f"{plan['method']} x{plan['scale']}", file=sys.stderr)
        t0 = time.perf_counter()

        def prog(k, n):
            if k == n or k % 25 == 0:
                print(f"  karo {k}/{n}", file=sys.stderr, flush=True)

        up = plan["upsampler"]() if plan["upsampler"] else None
        try:
            rec = superresolve(plan["src"]["path"], plan["out"], scale=plan["scale"],
                               method=plan["method"] if up is None else "bicubic",
                               tile_px=plan["tile_px"], overlap_px=plan["overlap_px"],
                               clip=True, progress=prog, upsampler=up,
                               tiling=plan["tiling"], margin_out=plan["margin_out"])
        except KeyboardInterrupt:
            # atomic_path has already unlinked the .part; the destination is untouched.
            raise Refusal(EXIT_WRITE, "Durduruldu. Diske eksik dosya yazılmadı.")
        except Exception as exc:                                # noqa: BLE001
            raise Refusal(EXIT_WRITE, f"Yazma başarısız: {type(exc).__name__}: {exc}")
        secs = time.perf_counter() - t0
        passed = _gate_s_recheck(plan)
        print(f"Bitti: {rec['output']}")
        for ln in lines:
            print("  " + ln)
        print(f"  Gate S           : {', '.join(passed)} yazılan dosyada tam eşitlikle "
              "doğrulandı")
        print(f"  süre             : {_tr(f'{secs:.1f}')} sn, {rec['n_tiles']} karo, "
              f"{rec['output_size_bytes'] / 1e6:.0f} MB")
        return EXIT_OK
    except Refusal as r:
        print(f"{TOOL}: {r}", file=sys.stderr)
        return r.code


if __name__ == "__main__":
    sys.exit(main())
