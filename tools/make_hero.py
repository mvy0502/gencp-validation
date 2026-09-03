#!/usr/bin/env python3
"""Build docs/kapak.png, the front-page composite of the README, from figures that already exist.

No inference is run. Four panels, 2 x 2:

  top left      tubitak/docs/evidence/plugin_screens/06_canvas_output_only.png
                GenCP Synthetic Reference output for the Ankara demo tile ank_0_30
                (2570 x 2570 m, EPSG:32636), rendered by QGIS's own renderer
  top right     tubitak/docs/evidence/plugin_screens/12_canvas_confidence_layer.png
                the confidence layer of the same tile (red do not use, orange use with care,
                green usable)
  bottom left   panel 1 of 03_ODTU_Ankara.png, the 10 m EOxCloudless s2cloudless-2024 input
                over the ODTU campus, Ankara, 2.56 x 2.56 km, replicated 4x by nearest neighbour
  bottom right  panel 3 of the same figure, the input through gencp_sr_tci_x4_b3_v2.onnx, 4x,
                2.5 m

03_ODTU_Ankara.png is one of the six figures tubitak/sr/tools/make_slides_v2.py produced on
2026-09-01 (3100 x 1218; three 1024 x 1024 panels at columns 0, 1038 and 2076, rows 120 to
1143). It is not in the repository: pass its path as the only argument. The EOxCloudless
attribution is drawn on the output because the licence (CC BY-NC-SA 4.0) requires it.

    python tools/make_hero.py /path/to/03_ODTU_Ankara.png
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "kapak.png")
P1_OUT = os.path.join(ROOT, "tubitak/docs/evidence/plugin_screens/06_canvas_output_only.png")
P1_CONF = os.path.join(ROOT, "tubitak/docs/evidence/plugin_screens/12_canvas_confidence_layer.png")
PANEL = 512
GAP = 10
LABEL_H = 30
ATTR = ("Alt sıra: EOxCloudless https://cloudless.eox.at, EOX IT Services GmbH, CC BY-NC-SA 4.0 "
        "(Copernicus Sentinel verisi 2024 içerir). Üst sıra: OpenStreetMap katkıcıları (ODbL), "
        "CLC+ Backbone (Copernicus).")


def font(size):
    for p in ("/System/Library/Fonts/Helvetica.ttc", "/Library/Fonts/Arial.ttf",
              "/System/Library/Fonts/Supplemental/Arial.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def main(argv):
    if len(argv) != 2 or argv[1].startswith("-"):
        sys.exit("usage: python tools/make_hero.py /path/to/03_ODTU_Ankara.png")
    slide = Image.open(argv[1]).convert("RGB")
    if slide.size != (3100, 1218):
        sys.exit(f"unexpected slide size {slide.size}; expected 3100 x 1218")
    p2_in = slide.crop((0, 120, 1024, 1144))
    p2_out = slide.crop((2076, 120, 3100, 1144))
    p1_out = Image.open(P1_OUT).convert("RGB")
    p1_conf = Image.open(P1_CONF).convert("RGB")
    panels = [
        (p1_out, "GenCP Synthetic Reference: sentetik referans (Ankara, ank_0_30)"),
        (p1_conf, "GenCP Synthetic Reference: güven katmanı (aynı karo)"),
        (p2_in, "GenCP Super-Resolution: girdi 10 m (ODTÜ, Ankara, EOxCloudless)"),
        (p2_out, "GenCP Super-Resolution: çıktı 2,5 m (8 bit TCI modeli, 4x)"),
    ]
    W = 2 * PANEL + 3 * GAP
    H = 2 * (LABEL_H + PANEL) + 3 * GAP + 24
    im = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(im)
    f = font(15)
    fa = font(11)
    for i, (p, label) in enumerate(panels):
        r, c = divmod(i, 2)
        x = GAP + c * (PANEL + GAP)
        y = GAP + r * (LABEL_H + PANEL + GAP)
        d.text((x, y + 6), label, fill=(20, 20, 20), font=f)
        im.paste(p.resize((PANEL, PANEL), Image.LANCZOS), (x, y + LABEL_H))
    d.text((GAP, H - 20), ATTR, fill=(90, 90, 90), font=fa)
    im.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    if size >= 1_000_000:
        im.convert("P", palette=Image.ADAPTIVE, colors=256).save(OUT, optimize=True)
        size = os.path.getsize(OUT)
    print(f"{OUT}: {im.size[0]} x {im.size[1]}, {size} bytes")


if __name__ == "__main__":
    main(sys.argv)
