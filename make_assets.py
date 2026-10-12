"""Regenerate the page's image assets: a web-sized logo and the QR code that points at the page.

Run after changing the logo or moving the page:  python make_assets.py [page-url]
Needs Pillow and segno (pip install --user pillow segno).
"""
import sys
from pathlib import Path

import segno
from PIL import Image

HERE = Path(__file__).parent
URL = sys.argv[1] if len(sys.argv) > 1 else "https://johnsawesome.github.io/tfg-marketplace/"

# Logo: trim the transparent margin, scale to 2x the largest size the header shows it at.
src = Image.open(HERE / "Together_For_Good_2026_Logo.png")
src = src.crop(src.getchannel("A").getbbox())
src.thumbnail((320, 320), Image.LANCZOS)
src.save(HERE / "logo.png", optimize=True)

# QR: navy on transparent, medium error correction, 2-module quiet zone (the header supplies white).
segno.make(URL, error="m").save(HERE / "qr.svg", border=2, dark="#00355F", light=None, svgclass=None, lineclass=None, omitsize=True)

print("logo.png", (HERE / "logo.png").stat().st_size, "bytes; qr.svg ->", URL)
