"""Gera os ícones do web app Planejamento TI a partir da logo em CSS.

Uso: python gerar_icones.py
Saída: a mesma pasta deste script (icons/).

Logo: caixa 22 x 18, polígono em frações (x, y) da caixa:
(0.5, 0), (1, 1), (0.72, 1), (0.5, 0.5), (0.28, 1), (0, 1)
Forma creme #f4f1ea sobre fundo #0a0a0b.
"""

from pathlib import Path

from PIL import Image, ImageDraw

BG_HEX = "#0a0a0b"
FG_HEX = "#f4f1ea"
BG = (0x0A, 0x0A, 0x0B)
FG = (0xF4, 0xF1, 0xEA)

BOX_W, BOX_H = 22, 18
FRACS = [(0.5, 0), (1, 1), (0.72, 1), (0.5, 0.5), (0.28, 1), (0, 1)]

SS = 8  # fator de supersampling
OUT = Path(__file__).resolve().parent


def shape_points(cx, cy, width):
    """Pontos do polígono com a largura dada, centralizados em (cx, cy)."""
    height = width * BOX_H / BOX_W
    x0 = cx - width / 2
    y0 = cy - height / 2
    return [(x0 + fx * width, y0 + fy * height) for fx, fy in FRACS]


def write_svg(path):
    width = 512 * 0.56
    pts = shape_points(256, 256, width)
    pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" '
        'width="512" height="512">\n'
        f'  <rect width="512" height="512" rx="112" ry="112" fill="{BG_HEX}"/>\n'
        f'  <polygon points="{pts_str}" fill="{FG_HEX}"/>\n'
        "</svg>\n"
    )
    path.write_text(svg, encoding="utf-8")
    return pts_str


def write_png(path, size, width_frac):
    big = size * SS
    img = Image.new("RGB", (big, big), BG)
    draw = ImageDraw.Draw(img)
    draw.polygon(shape_points(big / 2, big / 2, big * width_frac), fill=FG)
    img = img.resize((size, size), Image.LANCZOS)
    img.save(path, format="PNG", optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    pts_str = write_svg(OUT / "icon.svg")
    write_svg(OUT / "favicon.svg")
    print("icon.svg / favicon.svg: polygon points =", pts_str)

    specs = [
        ("icon-192.png", 192, 0.56),
        ("icon-512.png", 512, 0.56),
        ("icon-maskable-512.png", 512, 0.44),
        ("apple-touch-icon.png", 180, 0.56),
        ("favicon-32.png", 32, 0.70),
    ]
    for name, size, frac in specs:
        write_png(OUT / name, size, frac)
        print(f"{name}: {size}x{size}, largura {frac * 100:.0f}%")


if __name__ == "__main__":
    main()
