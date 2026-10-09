#!/usr/bin/env python3

import sys
from pathlib import Path

try:
    import qrcode
    import qrcode.image.svg
except ImportError:
    print("Missing library. Install with:")
    print('  pip install "qrcode[pil]"')
    sys.exit(1)


def ask(prompt, default=None):
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "

    value = input(prompt).strip()
    return value if value else default


def ask_level():
    print("\nError correction level:")
    print("  1) L - 7%   (clean space)")
    print("  2) M - 15%  (normal)")
    print("  3) Q - 25%  (small print)")
    print("  4) H - 30%  (best for print)")

    choice = ask("Choose", "4")

    levels = {
        "1": qrcode.constants.ERROR_CORRECT_L,
        "2": qrcode.constants.ERROR_CORRECT_M,
        "3": qrcode.constants.ERROR_CORRECT_Q,
        "4": qrcode.constants.ERROR_CORRECT_H,
    }
    return levels.get(choice, qrcode.constants.ERROR_CORRECT_H)


def ask_format():
    print("\nFormat:")
    print("  1) PNG  (social media, screens)")
    print("  2) SVG  (print, stays sharp at any size)")
    print("  3) Both")

    choice = ask("Choose", "3")
    return choice


def build_qr(url, level):
    qr = qrcode.QRCode(
        version=None,
        error_correction=level,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr


def save_png(qr, path):
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(path)


def save_svg(url, level, path):
    factory = qrcode.image.svg.SvgPathImage
    qr = qrcode.QRCode(
        version=None,
        error_correction=level,
        box_size=10,
        border=4,
        image_factory=factory,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr.make_image().save(path)


def main():
    print("=" * 45)
    print("  QR Code Maker - offline")
    print("=" * 45)

    url = ask("\nURL")
    if not url:
        print("URL is required.")
        sys.exit(1)

    if not url.startswith(("http://", "https://")):
        url = "https://" + url
        print(f"  (prefixed https:// -> {url})")

    name = ask("File name (without extension)", "qr")
    name = Path(name).stem

    level = ask_level()
    fmt = ask_format()

    if fmt == "1":
        out = f"{name}.png"
        save_png(build_qr(url, level), out)
        print(f"\nOK {out}")

    elif fmt == "2":
        out = f"{name}.svg"
        save_svg(url, level, out)
        print(f"\nOK {out}")

    else:
        png = f"{name}.png"
        svg = f"{name}.svg"
        save_png(build_qr(url, level), png)
        save_svg(url, level, svg)
        print(f"\nOK {png}")
        print(f"OK {svg}")

    print("\nDone.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(0)
