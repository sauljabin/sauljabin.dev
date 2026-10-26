#!/usr/bin/env python3
"""Generates the pixel-art SVGs used by the site.

Each sprite is a grid of characters; every character maps to a color in
PALETTE. "X" means currentColor, so mono sprites follow the page theme.

    python3 tools/pixelart.py

Writes assets/img/pixel.svg (a <symbol> sprite), favicon.svg,
apple-touch-icon.png and assets/img/og.png (the social preview image).
"""

import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PALETTE = {
    "X": "currentColor",
    "k": "#16171d",
    "w": "#ffffff",
    # ecuador
    "Y": "#ffd100",
    "B": "#034ea2",
    "R": "#ef3340",
    "c": "#6b4423",
    "g": "#2e8b57",
    "s": "#7fc8f8",
    "o": "#c9a227",
    # brands
    "L": "#0a66c2",
    "T": "#003d4f",
    "P": "#f2617a",
    # littlehorse knight
    "C": "#a0673a",
    "D": "#6b4423",
    # medal
    "G": "#f5c518",
    "O": "#b8860b",
    "b": "#1e50a0",
    "r": "#c62828",
    # heart
    "h": "#ef3340",
    "H": "#ff9a9a",
}

SPRITES = {
    "github": [
        ".....XXXXXX.....",
        "...XXXXXXXXXX...",
        "..XXXXXXXXXXXX..",
        ".XXX.XXXXXX.XXX.",
        ".XXX..XXXX..XXX.",
        "XXXX........XXXX",
        "XXX..........XXX",
        "XXX..........XXX",
        "XXX..........XXX",
        "XXXX........XXXX",
        ".XXXX......XXXX.",
        ".X..XX....XXXXX.",
        "..XX......XXXX..",
        "...XXX....XXX...",
        ".....X....X.....",
        "................",
    ],
    "linkedin": [
        ".LLLLLLLLLLLLLL.",
        "LLLLLLLLLLLLLLLL",
        "LLwwLLLLLLLLLLLL",
        "LLwwLLLLLLLLLLLL",
        "LLLLLLLLLLLLLLLL",
        "LLwwLLwwLwwwwLLL",
        "LLwwLLwwwwwwwwLL",
        "LLwwLLwwwLLLwwLL",
        "LLwwLLwwLLLLwwLL",
        "LLwwLLwwLLLLwwLL",
        "LLwwLLwwLLLLwwLL",
        "LLwwLLwwLLLLwwLL",
        "LLwwLLwwLLLLwwLL",
        "LLLLLLLLLLLLLLLL",
        "LLLLLLLLLLLLLLLL",
        ".LLLLLLLLLLLLLL.",
    ],
    "knight": [
        "......DD........",
        ".....DCCD.......",
        "....DCCCCDD.....",
        "...DCCkCCCCD....",
        "..DCCCCCCCCCD...",
        ".DCCCCCCCCCCCD..",
        "DCCCCCCCCCCCCD..",
        "DCCCDDCCCCCCCD..",
        ".DDD..DCCCCCCD..",
        "......DCCCCCCD..",
        ".....DCCCCCCCD..",
        ".....DCCCCCCCD..",
        "....DDDDDDDDDDD.",
        "...DCCCCCCCCCCCD",
        "...DCCCCCCCCCCCD",
        "...DDDDDDDDDDDDD",
    ],
    "tw": [
        ".TTTTTTTTTTTTTT.",
        "TTTTTTTTTTTTTTTT",
        "TTTTTTTTTTTTTTTT",
        "TTTTTTTTTTTTTTTT",
        "TTTTTPTTTTTTTTTT",
        "TTTTTPTwTTTTTTTT",
        "TTTTPTTwTTTTTTTT",
        "TTTTPTwwwTwTwTwT",
        "TTTPTTTwTTwTwTwT",
        "TTTPTTTwTTwTwTwT",
        "TTPTTTTwTTwTwTwT",
        "TTPTTTTTwTTwTwTT",
        "TTTTTTTTTTTTTTTT",
        "TTTTTTTTTTTTTTTT",
        "TTTTTTTTTTTTTTTT",
        ".TTTTTTTTTTTTTT.",
    ],
    "medal": [
        "...bbbb..rrrr...",
        "...bbbb..rrrr...",
        "....bbbbrrrr....",
        ".....bbbrrr.....",
        "......bbrr......",
        ".....OOOOOO.....",
        "....OGGGGGGO....",
        "...OGGGGGGGGO...",
        "...OGGGOOGGGO...",
        "...OGOOOOOOGO...",
        "...OGGOOOOGGO...",
        "...OGGOGGOGGO...",
        "...OGGGGGGGGO...",
        "....OGGGGGGO....",
        ".....OOOOOO.....",
        "................",
    ],
    "cap": [
        "................",
        "................",
        ".......XX.......",
        ".....XXXXXX.....",
        "...XXXXXXXXXX...",
        ".XXXXXXXXXXXXXX.",
        "...XXXXXXXXXX.Y.",
        ".....XXXXXX...Y.",
        "....X.XXXX.X..Y.",
        "....XX....XX..YY",
        "....XXXXXXXX..YY",
        "....XXXXXXXX....",
        ".....XXXXXX.....",
        "................",
        "................",
        "................",
    ],
    "star": [
        "....X....",
        "...XXX...",
        "XXXXXXXXX",
        ".XXXXXXX.",
        "..XXXXX..",
        ".XXXXXXX.",
        ".XX...XX.",
        "X.......X",
    ],
    "arrow": [
        "..XXXXX",
        "....XXX",
        "...XXXX",
        "..XXX.X",
        ".XXX..X",
        "XXX....",
        "XX.....",
    ],
    "sun": [
        ".....XX.....",
        ".X...XX...X.",
        "..X......X..",
        "....XXXX....",
        "...XXXXXX...",
        "XX.XXXXXX.XX",
        "XX.XXXXXX.XX",
        "...XXXXXX...",
        "....XXXX....",
        "..X......X..",
        ".X...XX...X.",
        ".....XX.....",
    ],
    "moon": [
        "...XXXX.....",
        ".XXXXX......",
        ".XXXX.......",
        "XXXX........",
        "XXXX........",
        "XXXX........",
        "XXXX........",
        "XXXXX......X",
        ".XXXXX....XX",
        ".XXXXXXXXXX.",
        "...XXXXXXX..",
        "............",
    ],
    "terminal": [
        "XXXXXXXXXXXXXXXX",
        "XXXXXXXXXXXXXXXX",
        "X..............X",
        "X.X............X",
        "X..X...........X",
        "X...X..........X",
        "X..X...........X",
        "X.X....XXXX....X",
        "X..............X",
        "XXXXXXXXXXXXXXXX",
    ],
    "heart": [
        ".hh...hh.",
        "hHhh.hhhh",
        "hHhhhhhhh",
        "hhhhhhhhh",
        ".hhhhhhh.",
        "..hhhhh..",
        "...hhh...",
        "....h....",
    ],
    "pin": [
        "..XXXX..",
        ".XXXXXX.",
        "XXX..XXX",
        "XXX..XXX",
        ".XXXXXX.",
        "..XXXX..",
        "...XX...",
        "...XX...",
    ],
}

FAVICON = [
    ".kkkkkkkkkkkkkk.",
    "kkkkkkkkkkkkkkkk",
    "kkkkkkkkkkkkkkkk",
    "kkYkkkkkkkkkkkkk",
    "kkYYkkkkkkkkkkkk",
    "kkkYYkkkkkkkkkkk",
    "kkkkYYkkkkkkkkkk",
    "kkkkkYYkkkkkkkkk",
    "kkkkYYkkkkkkkkkk",
    "kkkYYkkkkkkkkkkk",
    "kkYYkkkkkkkkkkkk",
    "kkYkkkkkkkkkkkkk",
    "kkkkkkkkYYYYYYkk",
    "kkkkkkkkkkkkkkkk",
    "kkkkkkkkkkkkkkkk",
    ".kkkkkkkkkkkkkk.",
]


def ecuador_flag():
    """A waving Ecuador flag: yellow (1/2), blue (1/4), red (1/4) and the arms."""
    w, h = 26, 18
    flag = [["k"] * w for _ in range(h)]
    for y in range(1, h - 1):
        band = "Y" if y <= 8 else "B" if y <= 12 else "R"
        for x in range(1, w - 1):
            flag[y][x] = band
    arms = {
        (10, 5): "c", (11, 5): "c", (14, 5): "c", (15, 5): "c",
        (11, 6): "c", (12, 6): "c", (13, 6): "c", (14, 6): "c",
        (12, 7): "o", (13, 7): "o",
        (11, 8): "o", (12, 8): "s", (13, 8): "s", (14, 8): "o",
        (11, 9): "o", (12, 9): "g", (13, 9): "s", (14, 9): "o",
        (11, 10): "o", (12, 10): "g", (13, 10): "g", (14, 10): "o",
        (12, 11): "o", (13, 11): "o",
    }
    for (x, y), c in arms.items():
        flag[y][x] = c
    # shift each column a little to make it wave
    out = [["."] * w for _ in range(h + 2)]
    for x in range(w):
        dy = round(1 + math.sin(x / w * 2 * math.pi))
        for y in range(h):
            out[y + dy][x] = flag[y][x]
    return ["".join(row) for row in out]


def landscape(w=560, h=36, peak=305, sun_x=245):
    """Cotopaxi and the Andes as mono layers, so each one can be tinted by CSS.

    The site draws it at a fixed pixel scale centered on the page, so it is
    wide enough for large screens and keeps the volcano and sun near the middle.
    """
    far, mountain, snow, sun = ([["."] * w for _ in range(h)] for _ in range(4))

    for x in range(w):
        ridge = 22 + 3 * math.sin(x / 9) + 2 * math.sin(x / 4.3 + 1) + 1.5 * math.sin(x / 2.1)
        for y in range(int(ridge), h):
            far[y][x] = "X"

    top, slope = 6, 1.45
    for x in range(w):
        d = max(0, abs(x - peak) - 3)
        base = top + d / slope
        base += 0.8 * math.sin(x * 1.7) if d > 0 else 0
        for y in range(max(top, round(base)), h):
            mountain[y][x] = "X"
            if y < 13 + (2 if x % 5 in (1, 2) else 0) - (1 if x % 7 == 3 else 0):
                snow[y][x] = "X"

    cx, cy, r = sun_x, 10, 5
    for y in range(h):
        for x in range(w):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r + 2:
                sun[y][x] = "X"

    join = lambda grid: ["".join(row) for row in grid]
    return {
        "scene-far": join(far),
        "scene-mountain": join(mountain),
        "scene-snow": join(snow),
        "scene-sun": join(sun),
    }


def paths(grid):
    """Merges horizontal runs of the same color into one <path> per color."""
    runs = {}
    for y, row in enumerate(grid):
        x = 0
        while x < len(row):
            c = row[x]
            if c == ".":
                x += 1
                continue
            end = x
            while end < len(row) and row[end] == c:
                end += 1
            runs.setdefault(c, []).append(f"M{x} {y}h{end - x}v1h-{end - x}z")
            x = end
    return "".join(f'<path fill="{PALETTE[c]}" d="{"".join(d)}"/>' for c, d in runs.items())


def size(grid):
    return len(grid[0]), len(grid)


def symbol(name, grid):
    w, h = size(grid)
    return f'<symbol id="{name}" viewBox="0 0 {w} {h}">{paths(grid)}</symbol>'


# 5x7 pixel font for the social image; accented letters get two extra rows
FONT = {
    "A": [".XXX.", "X...X", "X...X", "XXXXX", "X...X", "X...X", "X...X"],
    "B": ["XXXX.", "X...X", "X...X", "XXXX.", "X...X", "X...X", "XXXX."],
    "D": ["XXXX.", "X...X", "X...X", "X...X", "X...X", "X...X", "XXXX."],
    "E": ["XXXXX", "X....", "X....", "XXXX.", "X....", "X....", "XXXXX"],
    "F": ["XXXXX", "X....", "X....", "XXXX.", "X....", "X....", "X...."],
    "G": [".XXXX", "X....", "X....", "X..XX", "X...X", "X...X", ".XXXX"],
    "I": ["XXXXX", "..X..", "..X..", "..X..", "..X..", "..X..", "XXXXX"],
    "J": ["..XXX", "...X.", "...X.", "...X.", "...X.", "X..X.", ".XX.."],
    "L": ["X....", "X....", "X....", "X....", "X....", "X....", "XXXXX"],
    "N": ["X...X", "XX..X", "X.X.X", "X..XX", "X...X", "X...X", "X...X"],
    "O": [".XXX.", "X...X", "X...X", "X...X", "X...X", "X...X", ".XXX."],
    "P": ["XXXX.", "X...X", "X...X", "XXXX.", "X....", "X....", "X...."],
    "R": ["XXXX.", "X...X", "X...X", "XXXX.", "X.X..", "X..X.", "X...X"],
    "S": [".XXXX", "X....", "X....", ".XXX.", "....X", "....X", "XXXX."],
    "T": ["XXXXX", "..X..", "..X..", "..X..", "..X..", "..X..", "..X.."],
    "U": ["X...X", "X...X", "X...X", "X...X", "X...X", "X...X", ".XXX."],
    "V": ["X...X", "X...X", "X...X", "X...X", "X...X", ".X.X.", "..X.."],
    "W": ["X...X", "X...X", "X...X", "X.X.X", "X.X.X", "XX.XX", "X...X"],
    ".": [".....", ".....", ".....", ".....", ".....", ".....", "..X.."],
    ">": ["X....", ".X...", "..X..", "...X.", "..X..", ".X...", "X...."],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
}
ACCENTS = {"Ú": ("U", ["...X.", "..X.."]), "Ñ": ("N", [".XX.X", "X.XX."])}


def hex_rgb(color):
    return tuple(int(color[i : i + 2], 16) for i in (1, 3, 5))


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = [[hex_rgb(bg)] * w for _ in range(h)]

    def put(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = hex_rgb(color)

    def grid(self, grid, x0, y0, colors=None, scale=1):
        """Draws a sprite grid; colors overrides PALETTE (needed for "X")."""
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                if c == ".":
                    continue
                color = (colors or {}).get(c) or PALETTE[c]
                for dy in range(scale):
                    for dx in range(scale):
                        self.put(x0 + x * scale + dx, y0 + y * scale + dy, color)

    def text(self, text, x, y, color, scale=1):
        """Writes text with its baseline glyph top at y; accents go above it."""
        for ch in text:
            base, accent = ACCENTS.get(ch, (ch, []))
            self.grid(FONT[base], x, y, {"X": color}, scale)
            self.grid(accent, x, y - (len(accent) + 1) * scale, {"X": color}, scale)
            x += 6 * scale

    def png(self, path, scale=1):
        import struct
        import zlib

        rows = b"".join(
            b"\x00" + bytes(v for p in row for p in [p] * scale for v in p)
            for row in self.px
            for _ in range(scale)
        )
        chunk = lambda kind, data: (
            struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
        )
        header = struct.pack(">IIBBBBB", self.w * scale, self.h * scale, 8, 2, 0, 0, 0)
        path.write_bytes(
            b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(rows, 9))
            + chunk(b"IEND", b"")
        )


def social_image(path):
    """1200x630 Open Graph image: 240x126 pixels scaled by 5, in the dark theme."""
    c = Canvas(240, 126, "#0e0f13")
    scene = landscape(240, 36, peak=156, sun_x=50)
    for layer, color in [("sun", "#ffd100"), ("far", "#1b1e26"), ("mountain", "#262a35"), ("snow", "#d9dce4")]:
        c.grid(scene[f"scene-{layer}"], 0, 90, {"X": color})
    c.text(">", 16, 20, "#ffd100", 2)
    c.text("SAÚL PIÑA", 34, 20, "#e9e6dc", 2)
    c.grid(ecuador_flag(), 194, 16)
    c.text("STAFF SOFTWARE ENGINEER", 34, 44, "#e9e6dc")
    c.text("SAULJABIN.DEV", 34, 58, "#ffd100")
    c.png(path, scale=5)


def touch_icon(path):
    """180x180 icon for iOS home screens, from the favicon."""
    c = Canvas(18, 18, PALETTE["k"])
    c.grid(FAVICON, 1, 1)
    c.png(path, scale=10)


def main():
    sprites = {**SPRITES, "flag-ec": ecuador_flag(), **landscape()}
    for name, grid in sprites.items():
        assert len({len(row) for row in grid}) == 1, f"{name}: rows differ in width"

    symbols = "\n".join(symbol(n, g) for n, g in sprites.items())
    sprite = (
        '<svg xmlns="http://www.w3.org/2000/svg" shape-rendering="crispEdges">\n'
        f"{symbols}\n</svg>\n"
    )
    (ROOT / "assets/img").mkdir(parents=True, exist_ok=True)
    (ROOT / "assets/img/pixel.svg").write_text(sprite)

    w, h = size(FAVICON)
    favicon = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'shape-rendering="crispEdges">{paths(FAVICON)}</svg>\n'
    )
    (ROOT / "favicon.svg").write_text(favicon)
    social_image(ROOT / "assets/img/og.png")
    touch_icon(ROOT / "apple-touch-icon.png")

    for name, grid in sprites.items():
        print(f"{name:16} {'x'.join(map(str, size(grid)))}")


if __name__ == "__main__":
    main()
