#!/usr/bin/env python3
"""Draw docs/agents.png: the six roles of the lab as 8-bit characters.

Standard library only (zlib + struct write an indexed PNG). Deterministic:
same code, same bytes. Also writes docs/agents-small.png at half size.

    python3 docs/make_agents_png.py
"""
import os
import struct
import zlib

# ---------------------------------------------------------------- palette
PALETTE = {
    "bg": (0x1B, 0x1F, 0x24),
    "K": (0x0D, 0x0F, 0x12),  # outline, eyes, shoes
    "S": (0xF2, 0xC2, 0x9B),  # skin
    "W": (0xE8, 0xEC, 0xF0),  # white: paper, text
    "g": (0x8B, 0x94, 0x9E),  # grey: metal, arrows
    "B": (0x3B, 0x82, 0xF6),  # blue
    "R": (0xE5, 0x53, 0x4B),  # red
    "G": (0x3F, 0xB9, 0x50),  # green
    "Y": (0xE3, 0xB3, 0x41),  # yellow
    "N": (0x8A, 0x5A, 0x34),  # brown
    "P": (0xA3, 0x71, 0xF7),  # purple
    "O": (0xF0, 0x88, 0x3E),  # orange
}
NAMES = list(PALETTE)
IDX = {n: i for i, n in enumerate(NAMES)}

SPRITE_SCALE = 6  # 24x32 native -> 144x192
TEXT_SCALE = 4    # 5x7 font -> 20x28


# ---------------------------------------------------------------- sprite helpers
def new(w, h):
    return [[None] * w for _ in range(h)]


def rect(g, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            g[y][x] = c


def dots(g, pts, c):
    for x, y in pts:
        g[y][x] = c


def outline(g):
    h, w = len(g), len(g[0])
    edge = []
    for y in range(h):
        for x in range(w):
            if g[y][x] is None:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and g[ny][nx] is not None:
                        edge.append((x, y))
                        break
    dots(g, edge, "K")


def big_body(g, shirt, hair, pants, dx=0, arms="down"):
    """24x32 character, feet on row 29."""
    # head
    rect(g, 7 + dx, 5, 16 + dx, 14, "S")
    for x, y in ((7, 5), (16, 5), (7, 14), (16, 14)):
        g[y][x + dx] = None
    # hair
    if hair:
        rect(g, 8 + dx, 4, 15 + dx, 6, hair)
        rect(g, 7 + dx, 6, 7 + dx, 8, hair)
        rect(g, 16 + dx, 6, 16 + dx, 8, hair)
    # eyes
    rect(g, 9 + dx, 9, 9 + dx, 10, "K")
    rect(g, 14 + dx, 9, 14 + dx, 10, "K")
    # torso
    rect(g, 6 + dx, 15, 17 + dx, 24, shirt)
    g[15][6 + dx] = g[15][17 + dx] = None
    # arms
    if arms == "down":
        rect(g, 4 + dx, 16, 5 + dx, 22, shirt)
        rect(g, 18 + dx, 16, 19 + dx, 22, shirt)
        rect(g, 4 + dx, 23, 5 + dx, 24, "S")
        rect(g, 18 + dx, 23, 19 + dx, 24, "S")
    elif arms == "hold":  # forearms bent toward the chest
        rect(g, 4 + dx, 16, 5 + dx, 21, shirt)
        rect(g, 18 + dx, 16, 19 + dx, 21, shirt)
    # legs and shoes
    rect(g, 8 + dx, 25, 10 + dx, 28, pants)
    rect(g, 13 + dx, 25, 15 + dx, 28, pants)
    rect(g, 7 + dx, 29, 10 + dx, 29, "K")
    rect(g, 13 + dx, 29, 16 + dx, 29, "K")


def small_body(g, shirt, hat, pants, dx=0, arms="down"):
    """20x24 scout, feet on row 21."""
    rect(g, 6 + dx, 4, 13 + dx, 10, "S")
    g[10][6 + dx] = g[10][13 + dx] = None
    # bucket hat
    rect(g, 6 + dx, 1, 13 + dx, 3, hat)
    rect(g, 4 + dx, 4, 15 + dx, 4, hat)
    g[1][6 + dx] = g[1][13 + dx] = None
    # eyes
    dots(g, [(8 + dx, 7), (11 + dx, 7)], "K")
    # torso
    rect(g, 6 + dx, 11, 13 + dx, 17, shirt)
    if arms == "down":
        rect(g, 4 + dx, 12, 5 + dx, 16, shirt)
        rect(g, 14 + dx, 12, 15 + dx, 16, shirt)
        rect(g, 4 + dx, 17, 5 + dx, 17, "S")
        rect(g, 14 + dx, 17, 15 + dx, 17, "S")
    rect(g, 7 + dx, 18, 8 + dx, 20, pants)
    rect(g, 11 + dx, 18, 12 + dx, 20, pants)
    rect(g, 6 + dx, 21, 8 + dx, 21, "K")
    rect(g, 11 + dx, 21, 13 + dx, 21, "K")


# ---------------------------------------------------------------- the roles
def coordinator():
    g = new(24, 32)
    big_body(g, "P", "N", "g", dx=-2)
    # captain's hat: white crown, dark brim, gold badge
    rect(g, 6, 1, 13, 4, "W")
    g[1][6] = g[1][13] = None
    rect(g, 4, 5, 15, 5, "K")
    rect(g, 9, 2, 10, 3, "Y")
    # flag on a pole, held in the right hand
    rect(g, 18, 1, 18, 26, "g")
    rect(g, 19, 1, 22, 6, "R")
    g[3][22] = g[4][22] = None  # swallowtail
    rect(g, 20, 2, 20, 2, "Y")
    rect(g, 16, 21, 18, 22, "S")
    outline(g)
    return g


def scout(tool):
    g = new(20, 24)
    if tool == "binoculars":
        small_body(g, "N", "G", "g", arms="up")
        rect(g, 3, 9, 4, 13, "N")  # arms raised to the face
        rect(g, 15, 9, 16, 13, "N")
        dots(g, [(5, 12), (14, 12)], "N")
        rect(g, 3, 7, 4, 8, "S")
        rect(g, 15, 7, 16, 8, "S")
        rect(g, 5, 5, 8, 8, "g")    # two barrels and a bridge
        rect(g, 11, 5, 14, 8, "g")
        rect(g, 9, 6, 10, 7, "g")
        dots(g, [(6, 6), (7, 6), (12, 6), (13, 6)], "W")
        dots(g, [(6, 7), (7, 7), (12, 7), (13, 7)], "K")
    else:  # magnifying glass
        small_body(g, "N", "G", "g", dx=-2, arms="up")
        rect(g, 2, 12, 3, 16, "N")  # left arm down
        rect(g, 2, 17, 3, 17, "S")
        rect(g, 12, 12, 13, 13, "N")  # right arm up to the lens
        rect(g, 12, 2, 16, 2, "g")  # lens ring
        rect(g, 11, 3, 11, 7, "g")
        rect(g, 17, 3, 17, 7, "g")
        rect(g, 12, 8, 16, 8, "g")
        rect(g, 12, 3, 16, 7, "W")
        dots(g, [(13, 4), (14, 4), (13, 5)], "B")  # glint
        dots(g, [(12, 9), (11, 10), (12, 10), (13, 9)], "N")  # handle
        rect(g, 12, 11, 13, 12, "S")  # hand
    outline(g)
    return g


def scouts():
    a, b = scout("binoculars"), scout("lens")
    g = new(38, 32)
    for src, ox in ((a, 0), (b, 18)):
        for y in range(24):
            for x in range(20):
                if src[y][x] is not None:
                    g[y + 8][x + ox] = src[y][x]
    return g


def analyst():
    g = new(24, 32)
    big_body(g, "B", "N", "g", arms="hold")
    # glasses: two square frames and a bridge
    for x0 in (8, 13):
        rect(g, x0, 8, x0 + 2, 10, "K")
        g[9][x0 + 1] = "W"
    rect(g, 11, 9, 12, 9, "K")
    # sheet of formulas held at the chest
    rect(g, 7, 16, 16, 25, "W")
    dots(g, [(8, 18), (9, 18), (11, 18), (12, 18), (14, 18), (15, 18)], "B")
    dots(g, [(8, 20), (10, 20), (11, 20), (12, 20), (14, 20)], "g")
    dots(g, [(8, 22), (9, 22), (10, 22), (12, 22), (13, 22)], "B")
    dots(g, [(9, 24), (10, 24), (12, 24), (13, 24), (14, 24)], "g")
    rect(g, 5, 21, 6, 22, "S")
    rect(g, 17, 21, 18, 22, "S")
    outline(g)
    return g


def critic():
    g = new(24, 32)
    big_body(g, "g", "K", "B", dx=-2, arms="hold")
    # frown and angry brows
    dots(g, [(8, 12), (9, 12), (10, 12), (11, 12)], "K")
    dots(g, [(7, 13), (12, 13)], "K")
    dots(g, [(6, 7), (7, 8), (13, 7), (12, 8)], "K")
    # arms crossed: one forearm band across the chest
    rect(g, 2, 19, 17, 20, "g")
    rect(g, 4, 18, 15, 18, "K")
    rect(g, 4, 21, 15, 21, "K")
    rect(g, 12, 19, 13, 20, "S")
    # red X stamp
    for i in range(5):
        dots(g, [(17 + i, 1 + i), (18 + i, 1 + i), (21 - i, 1 + i), (22 - i, 1 + i)], "R")
    outline(g)
    return g


def implementer():
    g = new(24, 32)
    big_body(g, "O", "N", "B", dx=-1, arms="hold")
    rect(g, 3, 22, 4, 23, "S")  # left hand hangs
    # hard hat
    rect(g, 7, 1, 14, 4, "Y")
    g[1][7] = g[1][14] = None
    rect(g, 4, 5, 17, 5, "Y")
    rect(g, 10, 1, 11, 4, "W")
    # tool belt
    rect(g, 5, 23, 16, 23, "N")
    rect(g, 8, 23, 8, 23, "g")
    # wrench, raised in the right hand
    rect(g, 19, 7, 19, 9, "g")
    rect(g, 22, 7, 22, 9, "g")
    rect(g, 19, 10, 22, 10, "g")
    rect(g, 20, 11, 21, 22, "g")
    rect(g, 19, 19, 22, 21, "S")
    outline(g)
    return g


def validator():
    g = new(24, 32)
    big_body(g, "G", "N", "B", dx=1)
    # clipboard with a green tick, in the left hand
    rect(g, 1, 14, 9, 25, "W")
    rect(g, 3, 13, 7, 14, "N")
    dots(g, [(2, 19), (3, 20), (4, 21), (5, 20), (6, 19), (7, 18), (8, 17),
             (2, 20), (3, 21), (4, 22), (5, 21), (6, 20), (7, 19), (8, 18)], "G")
    # ruler, in the right hand
    rect(g, 21, 6, 22, 27, "Y")
    for y in range(7, 27, 2):
        g[y][22] = "K"
    rect(g, 19, 22, 21, 23, "S")
    rect(g, 9, 21, 10, 22, "S")  # left hand on the clipboard
    outline(g)
    return g


# ---------------------------------------------------------------- 5x7 font
FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "C": [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "I": [".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
}

ARROW = ["....#..", "....##.", "#######", "....##.", "....#.."]


def text_width(s):
    return (len(s) * 6 - 1) * TEXT_SCALE


# ---------------------------------------------------------------- canvas
def blit(canvas, g, x0, y0, scale):
    for y, row in enumerate(g):
        for x, c in enumerate(row):
            if c is None:
                continue
            i = IDX[c]
            for yy in range(y0 + y * scale, y0 + (y + 1) * scale):
                canvas[yy][x0 + x * scale:x0 + (x + 1) * scale] = bytes([i]) * scale


def text_grid(s):
    g = new(len(s) * 6 - 1, 7)
    for n, ch in enumerate(s):
        for y, row in enumerate(FONT[ch]):
            for x, p in enumerate(row):
                if p == "#":
                    g[y][n * 6 + x] = "W"
    return g


def recolor(g, c):
    return [[None if p is None else c for p in row] for row in g]


def bbox(g):
    xs = [x for row in g for x, p in enumerate(row) if p is not None]
    return min(xs), max(xs)


def even(v):
    return int(v) // 2 * 2


def compose():
    roles = [
        ("COORDINATOR", coordinator()),
        ("SCOUT", scouts()),
        ("ANALYST", analyst()),
        ("CRITIC", critic()),
        ("IMPLEMENTER", implementer()),
        ("VALIDATOR", validator()),
    ]
    S = SPRITE_SCALE
    arrow_w = len(ARROW[0]) * S
    min_sprite_gap = arrow_w + 48
    min_text_gap = 48
    margin = 32

    # visual widths (px) and the left/right half-extents around each centre
    vis = []
    for name, g in roles:
        x0, x1 = bbox(g)
        vis.append(((x1 - x0 + 1) * S, text_width(name), x0))
    centres = [0.0]
    for (sw0, tw0, _), (sw1, tw1, _) in zip(vis, vis[1:]):
        d = max((sw0 + sw1) / 2 + min_sprite_gap, (tw0 + tw1) / 2 + min_text_gap)
        centres.append(centres[-1] + d)
    left = max(vis[0][0], vis[0][1]) / 2
    right = max(vis[-1][0], vis[-1][1]) / 2
    W = even(margin + left + centres[-1] + right + margin)
    H = 322
    shift = margin + left

    canvas = [bytearray([IDX["bg"]]) * W for _ in range(H)]
    sprite_top = 32
    text_top = sprite_top + 32 * S + 24
    edges = []
    for (name, g), (sw, tw, vx0), c in zip(roles, vis, centres):
        cx = shift + c
        sx = even(cx - sw / 2) - vx0 * S
        blit(canvas, g, sx, sprite_top, S)
        edges.append((sx + vx0 * S, sx + vx0 * S + sw))
        tg = text_grid(name)
        tx = even(cx - tw / 2)
        blit(canvas, recolor(tg, "K"), tx + TEXT_SCALE, text_top + TEXT_SCALE, TEXT_SCALE)
        blit(canvas, tg, tx, text_top, TEXT_SCALE)

    arrow = [[None if p == "." else "g" for p in row] for row in ARROW]
    ay = sprite_top + 19 * S - len(ARROW) * S // 2
    for (_, r0), (l1, _) in zip(edges, edges[1:]):
        ax = even((r0 + l1) / 2 - arrow_w / 2)
        blit(canvas, arrow, ax, even(ay), S)
    return canvas


# ---------------------------------------------------------------- PNG
def write_png(path, rows):
    h, w = len(rows), len(rows[0])

    def chunk(kind, data):
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    raw = b"".join(b"\x00" + bytes(r) for r in rows)
    plte = b"".join(bytes(PALETTE[n]) for n in NAMES)
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 3, 0, 0, 0))
           + chunk(b"PLTE", plte)
           + chunk(b"IDAT", zlib.compress(raw, 9))
           + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
    return w, h


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    big = compose()
    small = [row[::2] for row in big[::2]]  # every position is even: exact x3
    for name, rows in (("agents.png", big), ("agents-small.png", small)):
        path = os.path.join(here, name)
        w, h = write_png(path, rows)
        used = len(set(b for r in rows for b in r))
        print(f"{path}: {w}x{h} px, {os.path.getsize(path)} bytes, {used} colours")


if __name__ == "__main__":
    main()
