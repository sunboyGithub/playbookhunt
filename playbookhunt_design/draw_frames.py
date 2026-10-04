"""Draw Playbook Hunt design frames (v2) as PNGs with Pillow (no browser needed).
Run: /usr/bin/python3 draw_frames.py  -> writes png/*.png
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 2  # supersampling factor
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "png")
os.makedirs(OUT, exist_ok=True)

BG = "#FAF9F6"; CARD = "#FFFFFF"; BORDER = "#E7E5E0"; TEXT = "#1C1B19"; MUTED = "#6B6862"
ACCENT = "#FF5A1F"; ACCENT_SOFT = "#FFF1EB"; WORKED = "#16A34A"; PARTLY = "#F59E0B"; DIDNT = "#DC2626"
WORKED_SOFT = "#DCFCE7"; PARTLY_SOFT = "#FEF3C7"; DIDNT_SOFT = "#FEE2E2"; SOFT = "#F3F2EE"
MUSE = "#2A66DE"; MUSE_SOFT = "#E8EFFC"; MUSE_DARK = "#1D4FB8"; MUSE_SUB = "#3F64A8"; MUSE_LINE = "#C3D4F5"; GREYED = "#A8A59E"; META_BLUE = "#0081FB"; FB_BLUE = "#1877F2"

FONT = "/System/Library/Fonts/HelveticaNeue.ttc"
MONO = "/System/Library/Fonts/Menlo.ttc"
WEIGHTS = {"regular": 0, "bold": 1, "medium": 10, "light": 7}
_cache = {}


def font(size, weight="regular", mono=False):
    key = (size, weight, mono)
    if key not in _cache:
        if mono:
            _cache[key] = ImageFont.truetype(MONO, int(size * S), index=0)
        else:
            _cache[key] = ImageFont.truetype(FONT, int(size * S), index=WEIGHTS[weight])
    return _cache[key]


SYMBOLS = set("✓▶→←▾↗⌘☎✈✕☰▦‹›☆★")
SYMFONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"


def symfont(size):
    key = ("sym", size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(SYMFONT, int(size * S))
    return _cache[key]


MUSE_AVATAR = Image.open(os.path.join(HERE, "assets", "muse_avatar.png")).convert("RGBA")


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


class Canvas:
    def __init__(self, w, h, bg=BG):
        self.w, self.h = w, h
        self.img = Image.new("RGB", (w * S, h * S), bg)
        self.d = ImageDraw.Draw(self.img)

    def _refresh(self):
        self.d = ImageDraw.Draw(self.img)

    # primitives -----------------------------------------------------------
    def rect(self, x, y, w, h, fill=None, outline=None, r=0, width=1):
        self.d.rounded_rectangle([x * S, y * S, (x + w) * S, (y + h) * S], radius=r * S,
                                 fill=fill, outline=outline, width=int(width * S))

    def shadow(self, x, y, w, h, r=14, spread=10, alpha=18):
        layer = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        for i in range(spread, 0, -1):
            a = int(alpha * (1 - i / spread) ** 2) + 1
            ld.rounded_rectangle([(x - i) * S, (y - i + 6) * S, (x + w + i) * S, (y + h + i + 6) * S],
                                 radius=(r + i) * S, fill=(0, 0, 0, a))
        self.img.paste(layer, (0, 0), layer)
        self._refresh()

    def gradient_rect(self, x, y, w, h, c1, c2, r=12, streak=True):
        W, H = int(w * S), int(h * S)
        D = int(1.6 * (W + H))
        g = Image.linear_gradient("L").resize((D, D)).rotate(-40)
        g = g.crop(((D - W) // 2, (D - H) // 2, (D - W) // 2 + W, (D - H) // 2 + H))
        grad = Image.composite(Image.new("RGB", (W, H), c2), Image.new("RGB", (W, H), c1), g)
        if streak:
            band = Image.new("L", (W, H), 0)
            bd = ImageDraw.Draw(band)
            bd.line([(int(W * 0.55), H + 20), (int(W * 0.85), -20)], fill=90, width=int(H * 0.35))
            band = band.filter(ImageFilter.GaussianBlur(H * 0.18))
            grad = Image.composite(Image.new("RGB", (W, H), (255, 255, 255)), grad, band)
        mask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 1, H - 1], radius=int(r * S), fill=255)
        self.img.paste(grad, (int(x * S), int(y * S)), mask)
        self._refresh()

    def fade_right(self, x, y, w, h, color=BG):
        W, H = int(w * S), int(h * S)
        m = Image.linear_gradient("L").rotate(90).resize((W, H)).transpose(Image.FLIP_LEFT_RIGHT)
        self.img.paste(Image.new("RGB", (W, H), color), (int(x * S), int(y * S)), m)
        self._refresh()

    def scene(self, x, y, w, h, fn, r=14, round_left=False):
        W, H = int(w * S), int(h * S)
        im = Image.new("RGB", (W, H), "#FFFFFF")
        fn(im, ImageDraw.Draw(im), W, H)
        mask = Image.new("L", (W, H), 0)
        md = ImageDraw.Draw(mask)
        md.rounded_rectangle([0, 0, W - 1, H - 1], radius=int(r * S), fill=255)
        if not round_left:
            md.rectangle([0, 0, int(r * S) + 2, H - 1], fill=255)
        self.img.paste(im, (int(x * S), int(y * S)), mask)
        self._refresh()

    def line(self, x1, y1, x2, y2, color=BORDER, width=1):
        self.d.line([x1 * S, y1 * S, x2 * S, y2 * S], fill=color, width=int(width * S))

    def circle(self, cx, cy, r, fill, outline=None, width=0):
        self.d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=fill,
                       outline=outline, width=int(width * S))

    @staticmethod
    def _runs(s, size, weight, mono):
        runs, cur, cur_sym = [], "", None
        for ch in s:
            sym = ch in SYMBOLS
            if cur and sym != cur_sym:
                runs.append((cur, cur_sym))
                cur = ""
            cur += ch
            cur_sym = sym
        if cur:
            runs.append((cur, cur_sym))
        return [(t, symfont(size) if sym else font(size, weight, mono)) for t, sym in runs]

    def tw(self, s, size=14, weight="regular", mono=False):
        return sum(self.d.textlength(t, font=f) for t, f in self._runs(s, size, weight, mono)) / S

    def text(self, x, y, s, size=14, weight="regular", color=TEXT, anchor="la", mono=False):
        total = self.tw(s, size, weight, mono)
        h, v = anchor[0], anchor[1]
        if h == "m":
            x -= total / 2
        elif h == "r":
            x -= total
        cx = x
        for t, f in self._runs(s, size, weight, mono):
            self.d.text((cx * S, y * S), t, font=f, fill=color, anchor="l" + v)
            cx += self.d.textlength(t, font=f) / S
        return total

    def wrap(self, x, y, s, maxw, size=14, weight="regular", color=TEXT, lh=None, mono=False, max_lines=99):
        lh = lh or size * 1.45
        lines = []
        for para in s.split("\n"):
            words, cur = para.split(" "), ""
            for wd in words:
                t = (cur + " " + wd).strip()
                if self.tw(t, size, weight, mono) <= maxw:
                    cur = t
                else:
                    lines.append(cur)
                    cur = wd
            lines.append(cur)
        lines = lines[:max_lines]
        for i, ln in enumerate(lines):
            self.text(x, y + i * lh, ln, size, weight, color, mono=mono)
        return len(lines) * lh

    # components -----------------------------------------------------------
    def card(self, x, y, w, h, r=14, fill=CARD, shadow=False, outline=BORDER):
        if shadow:
            self.shadow(x, y, w, h, r)
        self.rect(x, y, w, h, fill=fill, outline=outline, r=r)

    def chip(self, x, y, label, size=13, fill=CARD, color=TEXT, outline=BORDER, h=30, pad=13, weight="regular"):
        w = self.tw(label, size, weight) + pad * 2
        self.rect(x, y, w, h, fill=fill, outline=outline, r=h / 2)
        self.text(x + pad, y + h / 2, label, size, weight, color, anchor="lm")
        return w

    def badge(self, x, y, label, kind="verified", size=11.5):
        fills = {"verified": (WORKED_SOFT, "#166534"), "new": (ACCENT_SOFT, "#C2410C"),
                 "early": (SOFT, MUTED), "partly": (PARTLY_SOFT, "#92400E"), "didnt": (DIDNT_SOFT, "#991B1B"),
                 "dark": ("#2A2926", "#FFFFFF"), "muse": (MUSE_SOFT, MUSE_DARK), "soon": ("#EFEEEA", GREYED)}
        bg, fg = fills[kind]
        return self.chip(x, y, label, size, bg, fg, None, h=22, pad=9, weight="bold")

    def tag(self, x, y, label):
        w = self.tw(label, 11, "bold") + 16
        self.rect(x, y, w, 21, fill="#2A2926", r=6)
        self.text(x + 8, y + 10.5, label, 11, "bold", "#FFFFFF", anchor="lm")
        return w

    def button(self, x, y, w, h, label, kind="secondary", size=14, icon=None):
        styles = {"primary": (ACCENT, ACCENT, "#FFFFFF"), "dark": (TEXT, TEXT, "#FFFFFF"),
                  "secondary": (CARD, BORDER, TEXT), "ghost": (SOFT, SOFT, TEXT),
                  "muse": (MUSE, MUSE, "#FFFFFF"), "success": (WORKED_SOFT, WORKED, "#166534")}
        fill, ol, fg = styles[kind]
        extra = 26 if icon else 0
        if w is None:
            w = self.tw(label, size, "bold") + 30 + extra
        self.rect(x, y, w, h, fill=fill, outline=ol, r=10)
        tw_ = self.tw(label, size, "bold") + extra
        tx = x + (w - tw_) / 2
        if icon == "muse":
            self.muse_avatar(tx + 10, y + h / 2, 10, ring="#FFFFFF" if kind != "muse" else None)
        self.text(tx + extra, y + h / 2, label, size, "bold", fg, anchor="lm")
        return w

    def muse_avatar(self, cx, cy, r=12, ring=None):
        # Official Muse avatar (assets/muse_avatar.png) with a Meta-blue ring.
        rw = max(1.6, r * 0.14)
        if ring:
            self.circle(cx, cy, r + rw + 1.5, ring)
        self.circle(cx, cy, r + rw, META_BLUE)
        size = max(2, int(2 * r * S))
        av = MUSE_AVATAR.resize((size, size), Image.LANCZOS)
        self.img.paste(av, (int((cx - r) * S), int((cy - r) * S)), av)
        self._refresh()

    def agent_chip(self, x, y, name, h=26, size=12, greyed=False):
        if name == "Muse":
            w = self.tw(name, size, "bold") + 40
            self.rect(x, y, w, h, fill=MUSE_SOFT, outline=MUSE_LINE, r=h / 2)
            self.muse_avatar(x + 14, y + h / 2, h * 0.34)
            self.text(x + 26, y + h / 2, name, size, "bold", MUSE_DARK, anchor="lm")
            return w
        if greyed:
            return self.chip(x, y, name, size, "#F5F4F1", GREYED, BORDER, h=h, pad=10)
        return self.chip(x, y, name, size, h=h, pad=10)

    def avatar(self, cx, cy, letter, bg="#DBEAFE", fg="#1E40AF", r=13, check=False):
        self.circle(cx, cy, r, bg, "#FFFFFF", 2)
        self.text(cx, cy, letter, r * 0.9, "bold", fg, anchor="mm")
        if check:
            self.circle(cx + r * 0.7, cy + r * 0.7, 6, ACCENT, "#FFFFFF", 1.5)

    def agent_dot(self, x, y, letter, color, size=20):
        if letter == "M":
            self.muse_avatar(x + size / 2, y + size / 2, size / 2)
            return size
        self.rect(x, y, size, size, fill=color, r=5)
        self.text(x + size / 2, y + size / 2, letter, size * 0.5, "bold", "#FFFFFF", anchor="mm")
        return size

    def icon_tile(self, x, y, glyph, bg=SOFT, size=44, fg=TEXT):
        self.rect(x, y, size, size, fill=bg, r=12)
        self.text(x + size / 2, y + size / 2, glyph, size * 0.42, "bold", fg, anchor="mm")

    def outcome_bar(self, x, y, w, h, worked, partly, didnt):
        tot = worked + partly + didnt
        ww, pw = w * worked / tot, w * partly / tot
        self.rect(x, y, w, h, fill=DIDNT, r=h / 2)
        self.rect(x, y, ww + pw, h, fill=PARTLY, r=h / 2)
        self.rect(x, y, ww, h, fill=WORKED, r=h / 2)
        self.rect(x + ww - 1, y, 3, h, fill=PARTLY)
        self.rect(x + ww + pw - 1, y, 3, h, fill=DIDNT)

    def magnifier(self, cx, cy, color=TEXT):
        self.circle(cx, cy, 7, None, color, 2)
        self.line(cx + 5, cy + 5, cx + 10, cy + 10, color, 2.2)

    def search_box(self, x, y, w, h, placeholder, size=16, button=None, typed=False):
        self.card(x, y, w, h, r=h * 0.28)
        self.magnifier(x + 24, y + h / 2 - 1)
        self.text(x + 44, y + h / 2, placeholder, size, "regular", TEXT if typed else "#8A877F", anchor="lm")
        if button:
            self.button(x + w - 112, y + (h - 40) / 2, 100, 40, button, "primary")

    def share_icons(self, x, y, size=44, labels=True, gap=18):
        items = [("X", "#000000", "X"), ("IG", "#E1306C", "Instagram"), ("@", "#111111", "Threads"),
                 ("f", MUSE, "Facebook"), ("WA", "#25D366", "WhatsApp"), ("TT", "#010101", "TikTok"),
                 ("⧉", "#E9E7E2", "Copy link")]
        xx = x
        for g, col, name in items:
            r = size / 2
            if name == "Instagram":
                self.circle(xx + r, y + r, r, "#E1306C")
                self.circle(xx + r * 0.7, y + r * 1.3, r * 0.6, "#F77737")
                self.circle(xx + r * 1.2, y + r * 0.7, r * 0.55, "#C13584")
            else:
                self.circle(xx + r, y + r, r, col)
            if name == "Copy link":
                self.rect(xx + r - 8, y + r - 6, 11, 13, outline=TEXT, r=2, width=1.6)
                self.rect(xx + r - 3, y + r - 9, 11, 13, fill="#E9E7E2", outline=TEXT, r=2, width=1.6)
            else:
                self.text(xx + r, y + r, g, size * (0.42 if len(g) == 1 else 0.3), "bold", "#FFFFFF", anchor="mm")
            if labels:
                self.text(xx + r, y + size + 14, name, 11, "regular", MUTED, anchor="mm")
            xx += size + gap
        return xx - x

    def toast(self, x, y, w, msg, sub=None, link=None):
        h = 48 if not sub else 62
        self.shadow(x, y, w, h, r=12, spread=8, alpha=22)
        self.rect(x, y, w, h, fill="#1F1E1C", r=12)
        self.circle(x + 24, y + 24, 10, WORKED)
        self.text(x + 24, y + 24, "✓", 12, "bold", "#FFFFFF", anchor="mm")
        self.text(x + 44, y + 24, msg, 14, "bold", "#FFFFFF", anchor="lm")
        if sub:
            self.text(x + 44, y + 45, sub, 12.5, "regular", "#CFCBC3", anchor="lm")
        if link:
            self.text(x + w - 16, y + 24, link, 13, "bold", "#FFB08F", anchor="rm")
        return h

    def frame_label(self, label, left=False):
        w = self.tw(label, 11.5) + 20
        x = 16 if left else self.w - w - 16
        self.rect(x, 68, w, 22, fill=CARD, outline=BORDER, r=6)
        self.text(x + 10, 79, label, 11.5, "regular", MUTED, anchor="lm")

    def logo(self, x, y, size=20):
        x += self.text(x, y, "Playbook", size, "bold", TEXT, anchor="lm")
        self.text(x, y, "Hunt", size, "bold", ACCENT, anchor="lm")

    def nav(self, active=None, signed_in=False):
        self.rect(0, 0, self.w, 64, fill=BG)
        self.line(0, 64, self.w, 64)
        self.logo(32, 32)
        x = 210
        for item in ["Playbooks", "Starter kits", "Categories"]:
            c = ACCENT if item == active else "#3D3B37"
            x += self.text(x, 32, item, 14, "medium", c, anchor="lm") + 24
        R = self.w - 32
        if signed_in:
            self.avatar(R - 18, 33, "J", r=17)
            R -= 36 + 14
        else:
            self.button(R - 94, 16, 94, 34, "Sign in", "dark", 13)
            R -= 94 + 12
        self.button(R - 138, 16, 138, 34, "Report a result", "secondary", 13)
        R -= 138 + 12
        self.button(R - 178, 16, 178, 34, "+ Create a playbook", "secondary", 13)
        R -= 178 + 12
        sx = R - 230
        self.rect(sx, 17, 230, 32, fill=CARD, outline=BORDER, r=9)
        self.text(sx + 12, 33, "Search playbooks", 13, "regular", MUTED, anchor="lm")
        self.rect(sx + 230 - 38, 24, 28, 18, fill=BG, outline=BORDER, r=4)
        self.text(sx + 230 - 24, 33, "⌘K", 10.5, "regular", MUTED, anchor="mm")

    def crop_to(self, h):
        self.h = int(h)
        self.img = self.img.crop((0, 0, self.w * S, self.h * S))
        self._refresh()

    def save(self, name):
        path = os.path.join(OUT, name)
        self.img.resize((int(self.w * 1.5), int(self.h * 1.5)), Image.LANCZOS).save(path, optimize=True)
        print("wrote", path)
        return path


# --------------------------------------------------------------------------
# Illustrations for starter kits (drawn in scene pixel space)
def _vgrad(im, top, bottom):
    W, H = im.size
    g = Image.linear_gradient("L").resize((W, H))
    im.paste(Image.composite(Image.new("RGB", (W, H), bottom), Image.new("RGB", (W, H), top), g), (0, 0))


def scene_fuji(im, d, W, H):
    _vgrad(im, "#FCDCC8", "#FBF1E6")
    d = ImageDraw.Draw(im)
    d.ellipse([W * 0.62, H * 0.12, W * 0.86, H * 0.12 + W * 0.24], fill="#F08A68")
    d.polygon([(-W * 0.1, H), (W * 0.40, H * 0.30), (W * 0.60, H * 0.30), (W * 1.1, H)], fill="#566094")
    d.polygon([(W * 0.40, H * 0.30), (W * 0.60, H * 0.30), (W * 0.70, H * 0.44), (W * 0.63, H * 0.41),
               (W * 0.57, H * 0.47), (W * 0.50, H * 0.40), (W * 0.43, H * 0.47), (W * 0.37, H * 0.41),
               (W * 0.30, H * 0.44)], fill="#FFFFFF")
    d.ellipse([-W * 0.3, H * 0.80, W * 0.8, H * 1.3], fill="#3E6356")
    d.ellipse([W * 0.4, H * 0.84, W * 1.4, H * 1.35], fill="#4F7566")
    # torii gate
    tx, ty = W * 0.14, H * 0.66
    tw_, th = W * 0.22, H * 0.20
    red = "#D9482B"
    d.rectangle([tx + tw_ * 0.15, ty, tx + tw_ * 0.25, ty + th], fill=red)
    d.rectangle([tx + tw_ * 0.75, ty, tx + tw_ * 0.85, ty + th], fill=red)
    d.rectangle([tx - tw_ * 0.05, ty - th * 0.12, tx + tw_ * 1.05, ty], fill=red)
    d.rectangle([tx + tw_ * 0.05, ty + th * 0.18, tx + tw_ * 0.95, ty + th * 0.26], fill=red)


def scene_bills(im, d, W, H):
    _vgrad(im, "#DDEFE3", "#F1F8F3")
    d = ImageDraw.Draw(im)
    for i, off in enumerate([(0.30, 0.34), (0.24, 0.26), (0.18, 0.18)]):
        x0, y0 = W * off[0] - W * 0.08, H * off[1]
        d.rounded_rectangle([x0, y0, x0 + W * 0.66, y0 + H * 0.56], radius=W * 0.04,
                            fill="#FFFFFF", outline="#D5E5DA", width=max(2, int(W * 0.008)))
    x0, y0 = W * 0.10, H * 0.18
    for k in range(3):
        d.rounded_rectangle([x0 + W * 0.06, y0 + H * (0.10 + k * 0.08), x0 + W * (0.40 - k * 0.08),
                             y0 + H * (0.13 + k * 0.08)], radius=4, fill="#E7EFE9")
    f1 = ImageFont.truetype(FONT, int(W * 0.075), index=0)
    f2 = ImageFont.truetype(FONT, int(W * 0.10), index=1)
    d.text((x0 + W * 0.06, y0 + H * 0.36), "$89.99", font=f1, fill="#A7B2AA")
    w1 = d.textlength("$89.99", font=f1)
    d.line([(x0 + W * 0.06, y0 + H * 0.36 + W * 0.045), (x0 + W * 0.06 + w1, y0 + H * 0.36 + W * 0.045)],
           fill="#A7B2AA", width=max(2, int(W * 0.008)))
    d.text((x0 + W * 0.06, y0 + H * 0.46), "$64.99", font=f2, fill="#16A34A")
    cx, cy, r = W * 0.78, H * 0.30, W * 0.15
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#FF5A1F")
    f3 = ImageFont.truetype(FONT, int(W * 0.075), index=1)
    d.text((cx, cy), "-$25", font=f3, fill="#FFFFFF", anchor="mm")


def scene_shop(im, d, W, H):
    _vgrad(im, "#E3E7F6", "#F2F4FB")
    d = ImageDraw.Draw(im)
    d.ellipse([W * 0.70, H * 0.10, W * 0.88, H * 0.10 + W * 0.18], fill="#FFD27A")
    bx0, by0, bx1, by1 = W * 0.14, H * 0.34, W * 0.86, H * 0.92
    d.rectangle([bx0, by0, bx1, by1], fill="#FFFFFF", outline="#C9CFE6", width=max(2, int(W * 0.01)))
    d.rectangle([bx0 - W * 0.03, by0 - H * 0.10, bx1 + W * 0.03, by0], fill="#4F5180")
    f = ImageFont.truetype(FONT, int(W * 0.07), index=1)
    d.text(((bx0 + bx1) / 2, by0 - H * 0.05), "SHOP", font=f, fill="#FFFFFF", anchor="mm")
    n = 6
    sw = (bx1 - bx0 + W * 0.06) / n
    for i in range(n):
        x = bx0 - W * 0.03 + i * sw
        d.rectangle([x, by0, x + sw, by0 + H * 0.10], fill="#FF5A1F" if i % 2 == 0 else "#FFFFFF")
        d.ellipse([x, by0 + H * 0.10 - sw / 2, x + sw, by0 + H * 0.10 + sw / 2],
                  fill="#FF5A1F" if i % 2 == 0 else "#FFFFFF")
    d.rectangle([W * 0.22, H * 0.56, W * 0.50, H * 0.78], fill="#CFE0FB")
    d.rectangle([W * 0.58, H * 0.54, W * 0.76, H * 0.92], fill="#2A2926")
    d.ellipse([W * 0.72, H * 0.72, W * 0.745, H * 0.72 + W * 0.025], fill="#FFD27A")


# --------------------------------------------------------------------------
# Shared content
PLAYBOOKS = [
    dict(title="Lower your internet bill", promise="Negotiate a lower rate with your provider using Muse.",
         cat="Personal finance", tried="1,247", pct=68, n=412, med="$18/mo", ver="3d", agents=["Muse", "+3"],
         prev="#EAF4EE", kind="bill", a="Xfinity · Monthly bill", b="$89.99/mo", c="$64.99/mo"),
    dict(title="Cheaper car insurance", promise="Compare quotes and ask your insurer for a better rate.",
         cat="Personal finance", tried="612", pct=54, n=203, med="$240/yr", ver="9d", agents=["Muse", "+2"],
         prev="#EEF0F8", kind="bill", a="Auto policy renewal", b="$1,480/yr", c="$1,215/yr"),
    dict(title="Plan 7 days in Japan", promise="A day-by-day itinerary tuned to your pace and budget.",
         cat="Trip planning", tried="903", pct=81, n=340, med="3 hrs saved", ver="5d", agents=["Muse", "+3"],
         prev="#FBF1E6", kind="itin", a="Japan · 7-day itinerary",
         lines=["Day 1  Tokyo · Asakusa, Ueno", "Day 3  Hakone · onsen ryokan", "Day 4  Kyoto · Fushimi Inari"]),
]
DOT_COLORS = {"M": MUSE, "C": "#D97757", "G": "#10A37F", "B": "#4285F4"}


def preview(c, x, y, w, h, p, badge=True):
    c.rect(x, y, w, h, fill=p["prev"], r=14)
    c.rect(x, y + h - 14, w, 14, fill=p["prev"])
    c.line(x, y + h, x + w, y + h)
    px, py, pw, ph = x + 34, y + 24, w - 68, h - 44
    c.shadow(px, py, pw, ph, r=8, spread=6, alpha=14)
    c.rect(px, py, pw, ph, fill=CARD, r=8)
    c.text(px + 12, py + 12, p["a"], 11, "bold", "#444")
    if p["kind"] == "bill":
        c.rect(px + 12, py + 32, pw - 24, 6, fill="#ECEAE4", r=3)
        c.text(px + 12, py + 50, p["b"], 12, "regular", "#AAAAAA")
        bw = c.tw(p["b"], 12)
        c.line(px + 12, py + 57, px + 12 + bw, py + 57, "#AAAAAA", 1)
        c.text(px + pw - 12, py + 48, p["c"], 14, "bold", WORKED, anchor="ra")
        c.rect(px + 12, py + 74, (pw - 24) * 0.6, 6, fill="#ECEAE4", r=3)
    else:
        for i, ln in enumerate(p["lines"]):
            c.text(px + 12, py + 32 + i * 17, ln, 10.5, "regular", "#555")
    c.tag(x + 12, y + 12, p["cat"])
    if badge:
        lbl = f"✓ Verified {p['ver']} ago"
        bw = c.tw(lbl, 11.5, "bold") + 18
        c.badge(x + w - bw - 12, y + 12, lbl, "verified")


def rich_card(c, x, y, w, p, primary=False, hover=False):
    h = 330
    c.card(x, y, w, h, shadow=hover)
    preview(c, x, y, w, 150, p)
    bx, by = x + 18, y + 166
    c.text(bx, by, p["title"], 17, "bold")
    c.wrap(bx, by + 26, p["promise"], w - 36, 13, "regular", MUTED, max_lines=1)
    ex = bx
    ex += c.text(ex, by + 56, p["tried"], 13.5, "bold")
    ex += c.text(ex, by + 56, " tried · ", 13.5, "regular", "#3D3B37")
    ex += c.text(ex, by + 56, f"{p['pct']}% worked", 13.5, "bold", WORKED)
    c.text(ex, by + 56, f"  (n={p['n']})", 13.5, "regular", MUTED)
    ex = bx
    ex += c.text(ex, by + 78, "Median ", 13.5, "regular", MUTED)
    ex += c.text(ex, by + 78, p["med"], 13.5, "bold")
    c.text(ex, by + 78, f" · verified {p['ver']} ago", 13.5, "regular", MUTED)
    cx = bx
    for a in p["agents"]:
        cx += c.agent_chip(cx, by + 116, a) + 6
    c.avatar(x + w - 110, by + 129, "J", check=True)
    c.button(x + w - 88, by + 113, 70, 32, "▶ Try", "primary" if (primary or hover) else "secondary", 13)
    return h


def compact_card(c, x, y, w, title, evidence, early=False, agents=("M",), avatar="J", h=128):
    c.card(x, y, w, h)
    c.wrap(x + 16, y + 16, title, w - 32, 15, "medium", TEXT, max_lines=2)
    if early:
        c.badge(x + 16, y + 62, evidence, "early")
    else:
        pct, rest = evidence
        xx = x + 16
        xx += c.text(xx, y + 66, pct, 13.5, "bold", WORKED)
        c.text(xx, y + 66, " worked · " + rest, 13.5, "regular", "#3D3B37")
    ax = x + 16
    for a in agents:
        ax += c.agent_dot(ax, y + h - 36, a, DOT_COLORS.get(a, "#555")) + 5
    c.avatar(x + w - 28, y + h - 26, avatar, check=True)


def list_row(c, x, y, w, rank, glyph, title, sub, pct=None, n=None, extra="", early=None, h=72):
    c.text(x + 20, y + h / 2, str(rank), 18, "bold", MUTED, anchor="lm")
    c.icon_tile(x + 52, y + (h - 44) / 2, glyph)
    c.text(x + 110, y + h / 2 - 10, title, 15, "bold", anchor="lm")
    c.text(x + 110, y + h / 2 + 11, sub, 12.5, "regular", MUTED, anchor="lm")
    bx = x + w - 172
    c.rect(bx, y + 12, 152, h - 24, fill=CARD, outline=BORDER, r=12)
    if early:
        bw = c.tw(early, 11.5, "bold") + 18
        c.badge(bx + (152 - bw) / 2, y + h / 2 - 11, early, "early")
    else:
        c.text(bx + 76, y + h / 2 - 8, f"{pct}% worked", 16, "bold", WORKED, anchor="mm")
        c.text(bx + 76, y + h / 2 + 11, f"n={n} · {extra}", 11.5, "regular", MUTED, anchor="mm")


def footer(c, L, R, y):
    c.line(L, y, R, y)
    c.logo(L, y + 36, 15)
    xx = L + 140
    for f in ["How we verify", "Request a playbook", "Create a playbook (beta)", "Privacy", "Terms"]:
        xx += c.text(xx, y + 37, f, 13, "regular", MUTED) + 26


# --------------------------------------------------------------------------
def frame_homepage():
    W, H = 1440, 3000
    c = Canvas(W, H)
    c.nav()
    L, R = 120, W - 120
    cw = R - L
    # hero
    t1, t2, t3 = "What do you want ", "Muse", " to do?"
    tot = c.tw(t1, 46, "bold") + c.tw(t2, 46, "bold") + c.tw(t3, 46, "bold")
    xx = W / 2 - tot / 2
    xx += c.text(xx, 128, t1, 46, "bold", anchor="lm")
    xx += c.text(xx, 128, t2, 46, "bold", MUSE, anchor="lm")
    c.text(xx, 128, t3, 46, "bold", anchor="lm")
    c.text(W / 2, 172, "Proven playbooks with real results", 17, "regular", MUTED, anchor="mm")
    c.shadow(W / 2 - 360, 206, 720, 64, r=18, spread=12, alpha=10)
    c.search_box(W / 2 - 360, 206, 720, 64, "Save $100 on internet bill", 17, button="Search")
    a, b = "48 playbooks · ", "3,210 real results"
    tw_ = c.tw(a, 14) + c.tw(b, 14, "bold") + c.tw(" reported", 14)
    xx = W / 2 - tw_ / 2
    xx += c.text(xx, 300, a, 14, "regular", MUTED, anchor="lm")
    xx += c.text(xx, 300, b, 14, "bold", ACCENT, anchor="lm")
    c.text(xx, 300, " reported", 14, "regular", MUTED, anchor="lm")
    c.text(W / 2, 326, "Best results 2026      Trending      Recently verified", 13, "medium", "#3D3B37", anchor="mm")
    chips = ["Save money", "Book travel", "Plan a trip", "Shopping", "Small business", "Productivity", "Health", "Creativity"]
    total = sum(c.tw(ch, 14) + 28 for ch in chips) + 10 * (len(chips) - 1)
    xx = W / 2 - total / 2
    for ch in chips:
        xx += c.chip(xx, 356, ch, 14, h=36, pad=14) + 10
    # popular use cases: 4 visible, gradient tiles, centered text, right arrow + fade
    y = 440
    c.text(L, y, "Popular Use Cases", 22, "bold")
    c.text(R, y + 5, "4 of 10", 13, "medium", MUTED, anchor="ra")
    tiles = [("Cut monthly bills", "#2F4F46", "#5E7F73"), ("Cheaper flights", "#8A5A1F", "#C0925A"),
             ("Plan a trip", "#3E3F63", "#7E7FA6"), ("Doctor visit prep", "#4A6670", "#8FA9B0"),
             ("Research competitors", "#6B3B4E", "#A5708A")]
    gap = 16
    tile_w = (cw - 3 * gap - 70) / 4
    th = 88
    for i, (name, c1, c2) in enumerate(tiles):
        tx = L + i * (tile_w + gap)
        if i < 4:
            c.gradient_rect(tx, y + 40, tile_w, th, c1, c2, r=12)
            c.text(tx + tile_w / 2, y + 40 + th / 2, name, 17, "bold", "#FFFFFF", anchor="mm")
        else:
            part = R - tx
            c.gradient_rect(tx, y + 40, tile_w, th, c1, c2, r=12)
            c.rect(R, y + 30, W - R, th + 20, fill=BG)   # hide anything right of the arrow
            c.fade_right(tx, y + 40, part, th)
    c.shadow(R - 22, y + 40 + th / 2 - 22, 44, 44, r=22, spread=6, alpha=16)
    c.circle(R - 0, y + 40 + th / 2, 22, CARD, BORDER, 1)
    c.text(R, y + 40 + th / 2, "›", 24, "bold", TEXT, anchor="mm")
    # dots
    for k in range(3):
        c.circle(W / 2 - 14 + k * 14, y + 146, 3.5, TEXT if k == 0 else "#CFCBC3")
    # proven to work
    y = 630
    c.text(L, y, "Proven to work", 22, "bold")
    c.badge(L + c.tw("Proven to work", 22, "bold") + 12, y + 3, "Backed by verified results", "verified")
    c.text(R, y + 5, "See all →", 13, "bold", MUTED, anchor="ra")
    colw = (cw - 36) / 3
    for i, p in enumerate(PLAYBOOKS):
        rich_card(c, L + i * (colw + 18), y + 44, colw, p, primary=(i == 0), hover=(i == 0))
    # top list + trending
    y = 1060
    lw = cw * 0.55
    c.text(L, y, "Top playbooks this week", 22, "bold")
    c.text(L + lw, y + 5, "Ranked by evidence →", 13, "bold", MUTED, anchor="ra")
    rows = [(1, "$", "Lower your internet bill", "Negotiate with your ISP · Personal finance", 68, 412, "$18/mo", None),
            (2, "JP", "Plan 7 days in Japan", "Day-by-day itinerary · Trip planning", 81, 340, "3 hrs", None),
            (3, "$", "Cut your phone bill", "Switch or renegotiate · Personal finance", 59, 188, "$15/mo", None),
            (4, "✈", "Claim flight delay compensation", "Claim letter · Travel booking", 62, 97, "$400", None),
            (5, "?", "Research my competitors", "Structured report · Small business", None, None, "", "Early · 14 reports")]
    c.card(L, y + 42, lw, 72 * 5)
    for i, r in enumerate(rows):
        list_row(c, L, y + 42 + i * 72, lw, *r)
        if i:
            c.line(L + 16, y + 42 + i * 72, L + lw - 16, y + 42 + i * 72)
    tx = L + lw + 32
    tw2 = R - tx
    xx = tx + c.text(tx, y, "Trending ", 22, "bold")
    # category switcher: $ icon + label + dropdown caret
    cw_chip = c.tw("Finance", 15, "bold") + 64
    c.rect(xx + 2, y - 4, cw_chip, 34, fill=CARD, outline=BORDER, r=17)
    c.circle(xx + 20, y + 13, 10, WORKED_SOFT)
    c.text(xx + 20, y + 13, "$", 12, "bold", "#166534", anchor="mm")
    c.text(xx + 36, y + 13, "Finance", 15, "bold", TEXT, anchor="lm")
    c.text(xx + cw_chip - 12, y + 13, "▾", 12, "regular", MUTED, anchor="rm")
    c.text(xx + cw_chip + 12, y, "playbooks", 22, "bold")
    ccw = (tw2 - 14) / 2
    items = [("Cancel unused subscriptions", ("72%", "$31/mo"), False, ("M", "C")),
             ("Get a bank fee refunded", ("64%", "$35"), False, ("M", "G")),
             ("Analyze my monthly spending", "Early · 9 reports", True, ("M",)),
             ("Appeal a medical bill", ("48%", "$210"), False, ("M", "B"))]
    for i, it in enumerate(items):
        compact_card(c, tx + (i % 2) * (ccw + 14), y + 42 + (i // 2) * 146, ccw, it[0], it[1], it[2], it[3], "JAHK"[i], h=132)
    # starter kits with illustrations (right third)
    y = 1520
    c.text(L, y, "Starter kits", 22, "bold")
    c.text(R, y + 5, "Browse all kits →", 13, "bold", MUTED, anchor="ra")
    kits = [("Cut your bills kit", "Internet, phone, insurance and subscriptions: the playbooks that saved people the most.", "6 playbooks", scene_bills),
            ("Japan trip kit", "Flights, rail pass math, itinerary, packing and phrases, from booking to boarding.", "5 playbooks", scene_fuji),
            ("Small-business launch kit", "Competitor research, pricing, Google profile and a first marketing plan.", "6 playbooks", scene_shop)]
    kh = 180
    for i, k in enumerate(kits):
        kx = L + i * (colw + 18)
        c.card(kx, y + 44, colw, kh)
        iw = colw / 3
        c.scene(kx + colw - iw, y + 44, iw, kh, k[3], r=14)
        c.line(kx + colw - iw, y + 44, kx + colw - iw, y + 44 + kh)
        c.rect(kx, y + 44, colw, kh, outline=BORDER, r=14)
        c.text(kx + 20, y + 66, k[0], 17, "bold")
        c.wrap(kx + 20, y + 96, k[1], colw - iw - 36, 13, "regular", MUTED, max_lines=3)
        c.text(kx + 20, y + 194, k[2], 12.5, "bold")
    # explorer
    y = 1790
    c.text(L, y, "Explore by category", 22, "bold")
    cats = [("Personal finance", "12"), ("Travel – booking", "6"), ("Travel – planning", "6"), ("Shopping", "6"),
            ("Small business", "6"), ("Productivity", "6"), ("Health", "6"), ("Creativity", "6")]
    for i, (n_, cnt) in enumerate(cats):
        cy_ = y + 44 + i * 42
        if i == 0:
            c.rect(L, cy_, 260, 36, fill=CARD, outline=ACCENT, r=10)
        c.text(L + 14, cy_ + 18, n_, 15, "medium" if i == 0 else "regular", ACCENT if i == 0 else TEXT, anchor="lm")
        c.text(L + 246, cy_ + 18, cnt, 13, "regular", ACCENT if i == 0 else MUTED, anchor="rm")
    gx = L + 290
    gw = (R - gx - 32) / 3
    tiles = [("Lower your internet bill", "68%", "(412) · $18/mo"), ("Cut your phone bill", "59%", "(188) · $15/mo"),
             ("Cheaper car insurance", "54%", "(203) · $240/yr"), ("Cancel unused subscriptions", "72%", "(64) · $31/mo"),
             ("Get a bank fee refunded", "64%", "(41) · $35"), ("Analyze my monthly spending", None, "Early · 9 reports")]
    for i, t in enumerate(tiles):
        tx_ = gx + (i % 3) * (gw + 16)
        ty_ = y + 44 + (i // 3) * 104
        c.card(tx_, ty_, gw, 88)
        c.text(tx_ + 16, ty_ + 18, t[0], 14.5, "medium")
        if t[1]:
            xx = tx_ + 16 + c.text(tx_ + 16, ty_ + 50, t[1], 13.5, "bold", WORKED)
            c.text(xx + 4, ty_ + 50, t[2], 13.5, "regular", MUTED)
        else:
            c.badge(tx_ + 16, ty_ + 48, t[2], "early")
    # report CTA with referral line
    y = 2200
    c.card(L, y, cw, 360, r=20)
    reports = [(0, 0, "Worked", "verified", "Saved $25/mo", "Lower your internet bill · Muse · 2 days ago"),
               (80, 86, "Partly", "partly", "Saved $8/mo", "Cut your phone bill · Muse · 1 week ago"),
               (24, 172, "Worked", "verified", "4 hrs saved", "Plan 7 days in Japan · Muse · 3 days ago")]
    for dx, dy, b, k, amt, sub in reports:
        rx, ry = L + 50 + dx, y + 56 + dy
        c.card(rx, ry, 330, 70, r=12, shadow=True)
        bw = c.badge(rx + 16, ry + 14, b, k)
        c.text(rx + 26 + bw, ry + 25, amt, 14.5, "bold", anchor="lm")
        c.text(rx + 16, ry + 50, sub, 12, "regular", MUTED, anchor="lm")
    ox = L + cw / 2 + 20
    c.text(ox, y + 70, "Tried an AI playbook?", 32, "bold", ACCENT)
    c.text(ox, y + 112, "Report your result.", 32, "bold")
    c.wrap(ox, y + 164, "Takes 30 seconds. Every report makes the rankings more honest for the next person.", 480, 15, "regular", MUTED)
    c.rect(ox, y + 216, 500, 62, fill=MUSE_SOFT, r=12)
    c.muse_avatar(ox + 26, y + 247, 13)
    c.wrap(ox + 50, y + 226, "Bonus: add your Muse referral code to a verified report. If people join Muse with it, you could earn up to 1B Muse tokens.*", 436, 13, "medium", MUSE_DARK, lh=19)
    c.button(ox, y + 294, None, 44, "Report a result", "primary", 15)
    c.text(ox + 170, y + 316, "*Per Muse's referral terms. Never affects rankings.", 11.5, "regular", MUTED, anchor="lm")
    footer(c, L, R, 2620)
    c.wrap(L, 2690, "Numbers shown are illustrative. Real stats appear only after enough verified reports. Muse avatar is a placeholder for the official asset.", 900, 12, "regular", MUTED)
    c.frame_label("Frame 1 · Homepage v2.3 · desktop 1440 · illustrative data")
    c.crop_to(2740)
    return c.save("01_homepage.png")


def frame_search():
    W = 1440
    c = Canvas(W, 1300)
    c.nav("Playbooks")
    L, R = 80, W - 80
    c.search_box(L, 96, 760, 54, "lower my bills", 16, typed=True)
    c.text(L + 780, 114, "18 playbooks", 14, "medium", MUTED, anchor="lm")
    c.text(L + 780, 134, "Matched: \"bills\" → Personal finance", 12.5, "regular", MUTED, anchor="lm")
    xx = L
    for i, p in enumerate(["All", "Save money", "Save time", "Plan", "Research", "Create"]):
        if i == 1:
            xx += c.chip(xx, 172, p, 13.5, TEXT, "#FFFFFF", TEXT, h=34, pad=14) + 8
        else:
            xx += c.chip(xx, 172, p, 13.5, h=34, pad=14) + 8
    c.text(R - 240, 189, "Sort:", 13, "regular", MUTED, anchor="lm")
    c.chip(R - 200, 174, "Best evidence ▾", 13, h=30, pad=12, weight="medium")
    c.rect(R - 70, 174, 70, 30, fill=CARD, outline=BORDER, r=8)
    c.rect(R - 68, 176, 33, 26, fill=SOFT, r=6)
    c.text(R - 51, 189, "▦", 13, "bold", TEXT, anchor="mm")
    c.text(R - 18, 189, "☰", 13, "regular", MUTED, anchor="mm")
    sy = 236
    c.card(L, sy, 260, 890)
    groups = [("Agent", [("Muse", True), ("ChatGPT · Dots", None), ("Grok-Bot", None), ("Manus", None), ("Instinct", None)]),
              ("Category", [("Personal finance", True), ("Shopping", False), ("Small business", False), ("Health", False)]),
              ("Evidence", [("Verified in last 30 days", True), ("20+ reports", False), ("100+ reports", False), ("Has evidence photos", False)]),
              ("Time to complete", [("Under 15 min", False), ("15–60 min", True), ("60+ min", False)])]
    gy = sy + 20
    for g, opts in groups:
        c.text(L + 20, gy, g, 13, "bold")
        gy += 28
        for o, on in opts:
            col = MUSE if o == "Muse" else ACCENT
            if on is None:  # disabled, not selectable yet
                c.rect(L + 20, gy - 2, 16, 16, fill="#EFEEEA", outline="#DAD7D0", r=4)
                c.text(L + 46, gy + 6, o, 13.5, "regular", GREYED, anchor="lm")
            else:
                c.rect(L + 20, gy - 2, 16, 16, fill=col if on else CARD, outline=col if on else "#C9C6BE", r=4)
                if on:
                    c.text(L + 28, gy + 6, "✓", 11, "bold", "#FFFFFF", anchor="mm")
                if o == "Muse":
                    c.muse_avatar(L + 56, gy + 6, 9)
                    c.text(L + 72, gy + 6, o, 13.5, "bold", MUSE_DARK, anchor="lm")
                else:
                    c.text(L + 46, gy + 6, o, 13.5, "regular", TEXT, anchor="lm")
            gy += 28
        gy += 14
        c.line(L + 20, gy - 8, L + 240, gy - 8)
    c.text(L + 20, gy + 6, "Clear all filters", 13, "bold", ACCENT)
    gx = L + 290
    xx = gx
    for f in ["Muse ×", "Personal finance ×", "Verified 30d ×", "15–60 min ×"]:
        xx += c.chip(xx, 236, f, 12.5, ACCENT_SOFT, "#C2410C", None, h=28, pad=11, weight="medium") + 8
    colw = (R - gx - 36) / 3
    data = [("Lower your internet bill", ("68%", "$18/mo"), False, ("M", "C", "G"), "1,247 tried · n=412"),
            ("Cut your phone bill", ("59%", "$15/mo"), False, ("M", "C"), "688 tried · n=188"),
            ("Cheaper car insurance", ("54%", "$240/yr"), False, ("M", "G"), "612 tried · n=203"),
            ("Cancel unused subscriptions", ("72%", "$31/mo"), False, ("M",), "204 tried · n=64"),
            ("Get a bank fee refunded", ("64%", "$35"), False, ("M", "G"), "150 tried · n=41"),
            ("Appeal a medical bill", ("48%", "$210"), False, ("M", "B"), "121 tried · n=33"),
            ("Analyze my monthly spending", "Early · 9 reports", True, ("M",), "37 tried"),
            ("Negotiate a gym cancellation", "Early · 4 reports", True, ("M",), "12 tried"),
            ("Lower your energy bill", "Early · 11 reports", True, ("M", "C"), "40 tried")]
    for i, d in enumerate(data):
        x = gx + (i % 3) * (colw + 18)
        y = 284 + (i // 3) * 200
        c.card(x, y, colw, 184)
        c.tag(x + 16, y + 16, "Personal finance")
        if i < 2:
            c.badge(x + colw - 110, y + 16, "✓ Verified", "verified")
        c.wrap(x + 16, y + 50, d[0], colw - 32, 16, "bold", TEXT, max_lines=2)
        if d[2]:
            c.badge(x + 16, y + 96, d[1], "early")
        else:
            xx = x + 16 + c.text(x + 16, y + 100, d[1][0] + " worked", 14, "bold", WORKED)
            c.text(xx, y + 100, "  ·  median " + d[1][1], 14, "regular", "#3D3B37")
        c.text(x + 16, y + 124, d[4], 12.5, "regular", MUTED)
        ax = x + 16
        for a in d[3]:
            ax += c.agent_dot(ax, y + 148, a, DOT_COLORS[a]) + 5
        c.button(x + colw - 76, y + 142, 60, 30, "Try", "secondary", 12.5)
    y = 900
    c.card(gx, y, R - gx, 150, r=16, fill="#FFFDFB")
    c.text(gx + 24, y + 30, "Can't find what you need?", 18, "bold")
    c.wrap(gx + 24, y + 60, "Tell us the task, or paste a post you saw. We'll test it and email you when it has results.", 520, 14, "regular", MUTED)
    c.search_box(gx + 580, y + 42, R - 170 - (gx + 580), 44, "e.g. lower my water bill", 14)
    c.button(R - 150, y + 44, 126, 40, "Request it", "primary")
    c.text(gx + 24, y + 116, "Empty results never dead-end: we fall back to the closest category, then popular playbooks, then this form.", 12.5, "regular", MUTED)
    c.text(gx + (R - gx) / 2, 1100, "‹  1  2  ›", 15, "medium", TEXT, anchor="mm")
    c.frame_label("Frame 2 · Search results · keyword + category matching · illustrative data")
    c.crop_to(1150)
    return c.save("02_search_results.png")


OTHER_AGENTS = ["ChatGPT · Dots", "Grok-Bot", "Manus", "Instinct"]


def works_with(c, sx, sy, sw):
    c.text(sx + 18, sy, "Works with", 13, "bold", MUTED)
    y = sy + 22
    c.rect(sx + 18, y, sw - 36, 54, fill=MUSE_SOFT, outline=MUSE_LINE, r=12)
    c.muse_avatar(sx + 42, y + 27, 15)
    c.text(sx + 66, y + 18, "Muse", 14.5, "bold", MUSE_DARK, anchor="lm")
    c.text(sx + 66, y + 38, "Calls and chats for you · 71% worked (n=301)", 12, "regular", MUSE_SUB, anchor="lm")
    y += 66
    xx = sx + 18
    for a in OTHER_AGENTS:
        xx += c.agent_chip(xx, y, a, greyed=True) + 6
    return y + 30


def detail_page(c, L=80, R=1360, with_popover=True, with_toast=True, saved=False, signed_in=False):
    c.nav("Playbooks", signed_in=signed_in)
    main_w = 820
    x = L
    y = 92
    c.text(x, y, "Home  /  Personal finance  /  Lower your internet bill", 13, "regular", MUTED)
    c.text(x, y + 26, "Lower your internet bill", 34, "bold")
    c.button(x + main_w - 96, y + 28, 96, 38, "↗ Share", "secondary", 13.5)
    if saved:
        c.button(x + main_w - 96 - 10 - 96, y + 28, 96, 38, "★ Saved", "muse", 13.5)
    else:
        c.button(x + main_w - 96 - 10 - 90, y + 28, 90, 38, "☆ Save", "secondary", 13.5)
    c.text(x, y + 76, "Negotiate a lower rate with your provider using Muse.", 16, "regular", MUTED)
    xx = x
    xx += c.chip(xx, y + 108, "Personal finance", 12.5, h=28, pad=11) + 8
    w = c.tw("Tested with Muse", 12.5, "bold") + 44
    c.rect(xx, y + 108, w, 28, fill=MUSE_SOFT, outline=MUSE_LINE, r=14)
    c.muse_avatar(xx + 15, y + 122, 9)
    c.text(xx + 30, y + 122, "Tested with Muse", 12.5, "bold", MUSE_DARK, anchor="lm")
    xx += w + 8
    c.chip(xx, y + 108, "10 to 20 min", 12.5, h=28, pad=11)
    ty = y + 156
    tw_ = (main_w - 24) / 3
    for i, (a, b, s) in enumerate([("Tried", "1,247", ""), ("Worked", "68%", "n = 412 reports"), ("Median saved", "$18/mo", "n = 236 with amounts")]):
        tx = x + i * (tw_ + 12)
        c.card(tx, ty, tw_, 96)
        c.text(tx + 18, ty + 18, a, 13, "regular", MUTED)
        c.text(tx + 18, ty + 40, b, 28, "bold", WORKED if a == "Worked" else TEXT)
        if s:
            c.text(tx + 18, ty + 76, s, 12, "regular", MUTED)
    py = ty + 116
    c.card(x, py, main_w, 180)
    preview(c, x, py, main_w, 150, PLAYBOOKS[0], badge=False)
    c.text(x + 18, py + 164, "Example result (redacted) · submitted by a verified reporter", 12, "regular", MUTED, anchor="lm")
    wy = py + 200
    hw = (main_w - 12) / 2
    c.card(x, wy, hw, 120)
    c.text(x + 18, wy + 18, "Who this is for", 16, "bold")
    c.wrap(x + 18, wy + 46, "US home internet customers paying over $60/month, 6+ months with the same provider.", hw - 36, 13.5, "regular", "#3D3B37")
    c.card(x + hw + 12, wy, hw, 120)
    c.text(x + hw + 30, wy + 18, "Not for", 16, "bold")
    c.wrap(x + hw + 30, wy + 46, "People still on promo pricing, or in areas with a single provider. Less likely to work.", hw - 36, 13.5, "regular", "#3D3B37")
    ny = wy + 140
    c.card(x, ny, main_w, 150)
    c.text(x + 18, ny + 18, "What you'll need", 16, "bold")
    c.text(x + main_w - 18, ny + 20, "Only your provider is required", 12.5, "regular", MUTED, anchor="ra")
    for i, (item, req) in enumerate([("Your provider (Xfinity, Spectrum, AT&T…)", "Required"), ("Your monthly price and ZIP code", "Optional · better offers"), ("Your latest bill", "Optional · most accurate")]):
        iy = ny + 52 + i * 32
        c.rect(x + 18, iy, 20, 20, fill=SOFT, r=5)
        c.text(x + 28, iy + 10, "•", 13, "bold", MUTED, anchor="mm")
        c.text(x + 48, iy + 10, item, 14, "regular", TEXT, anchor="lm")
        c.text(x + main_w - 18, iy + 10, req, 12.5, "medium", ACCENT if req == "Required" else MUTED, anchor="rm")
        if i:
            c.line(x + 18, iy - 6, x + main_w - 18, iy - 6)
    pby = ny + 170
    c.card(x, pby, main_w, 262)
    c.text(x + 18, pby + 20, "The playbook", 16, "bold")
    c.button(x + main_w - 130, pby + 12, 112, 36, "✓ Copied", "success", 13)
    c.rect(x + 18, pby + 60, main_w - 36, 88, fill="#F5F4F0", r=10)
    c.wrap(x + 32, pby + 74, "You are helping me lower my internet bill. My provider is {{provider}}, I pay {{price}} in ZIP {{zip}}. Find current offers from my provider and competitors, draft a call script with fallback asks, and...", main_w - 64, 12.5, "regular", "#2D2B28", lh=19, mono=True, max_lines=3)
    c.text(x + 18, pby + 172, "Steps: 1 Pick provider · 2 Review offers · 3 Muse calls or chats (or use the script) · 4 Log the result", 13, "regular", MUTED)
    if with_toast:
        tx_, ty_, tww = x + 18, pby + 190, main_w - 36
        c.shadow(tx_, ty_, tww, 62, r=12, spread=8, alpha=22)
        c.rect(tx_, ty_, tww, 62, fill="#1F1E1C", r=12)
        c.circle(tx_ + 24, ty_ + 24, 10, WORKED)
        c.text(tx_ + 24, ty_ + 24, "✓", 12, "bold", "#FFFFFF", anchor="mm")
        c.text(tx_ + 44, ty_ + 24, "Copied! Paste it into Muse.", 14, "bold", "#FFFFFF", anchor="lm")
        q = "Want it filled in with your details? "
        c.text(tx_ + 44, ty_ + 45, q, 12.5, "regular", "#CFCBC3", anchor="lm")
        c.text(tx_ + 44 + c.tw(q, 12.5), ty_ + 45, "Try this playbook →", 12.5, "bold", "#FFB08F", anchor="lm")
    hy = pby + 282
    c.card(x, hy, main_w, 300)
    c.text(x + 18, hy + 20, "What happened for others", 16, "bold")
    c.outcome_bar(x + 18, hy + 54, main_w - 36, 12, 68, 18, 14)
    c.text(x + 18, hy + 84, "Worked 68%  ·  Partly 18%  ·  Didn't 14%  ·  Last 30 days: 71%", 13, "regular", "#3D3B37")
    xx = x + main_w - 18
    for f in reversed(["Provider ▾", "Agent ▾", "Result ▾"]):
        w = c.tw(f, 12, "medium") + 22
        xx -= w
        c.chip(xx, hy + 14, f, 12, h=26, pad=11, weight="medium")
        xx -= 6
    c.text(xx - 4, hy + 27, "Filter:", 12, "regular", MUTED, anchor="rm")
    reps = [("Worked", "verified", "Saved $25/mo", "Evidence reviewed · 2 days ago · Muse · Xfinity · 20 min"),
            ("Partly", "partly", "Saved $8/mo", "1 week ago · Muse · Spectrum · 35 min"),
            ("Didn't", "didnt", "No change", "2 weeks ago · Muse · AT&T · \"They only offered a speed upgrade\"")]
    for i, (b, k, amt, sub) in enumerate(reps):
        ry = hy + 112 + i * 56
        c.line(x + 18, ry - 6, x + main_w - 18, ry - 6)
        c.rect(x + 18, ry + 2, 40, 40, fill=SOFT, outline=BORDER, r=8)
        bw = c.badge(x + 72, ry + 4, b, k)
        c.text(x + 82 + bw, ry + 15, amt, 14.5, "bold", anchor="lm")
        c.text(x + 72, ry + 36, sub, 12.5, "regular", MUTED, anchor="lm")
    c.text(x + 18, hy + 282, "Show all 412 reports", 13, "bold", ACCENT)
    dy = hy + 320
    c.card(x, dy, main_w, 110)
    c.text(x + main_w / 2, dy + 30, "Did it work for you?", 17, "bold", anchor="mm")
    c.button(x + main_w / 2 - 90, dy + 52, 180, 42, "Report your result", "dark")
    ry = dy + 134
    c.text(x, ry, "Related playbooks", 15, "bold", MUTED)
    rw = (main_w - 24) / 3
    for i, (t, e) in enumerate([("Cut your phone bill", "59% worked"), ("Cheaper car insurance", "54% worked"), ("Lower your energy bill", "Early · 11 reports")]):
        rx = x + i * (rw + 12)
        c.card(rx, ry + 28, rw, 80)
        c.text(rx + 16, ry + 46, t, 15, "bold")
        if "Early" in e:
            c.badge(rx + 16, ry + 72, e, "early")
        else:
            c.text(rx + 16, ry + 76, e, 13, "regular", WORKED)
    sy2 = ry + 134 - 136
    # sidebar
    sx = L + main_w + 32
    sw = R - sx
    sy = 92
    c.card(sx, sy, sw, 240)
    c.badge(sx + 18, sy + 18, "✓ Verified 3 days ago", "verified")
    c.button(sx + 18, sy + 52, sw - 36, 46, "▶  Try this playbook", "primary", 15)
    works_with(c, sx, sy + 122, sw)
    c.card(sx, sy + 256, sw, 110)
    c.text(sx + 18, sy + 276, "Playbook by", 15, "bold")
    c.avatar(sx + 38, sy + 324, "H", r=18)
    c.text(sx + 66, sy + 314, "Playbook Hunt team", 14.5, "bold", anchor="lm")
    c.text(sx + 66, sy + 334, "Tested 2x before publishing", 12.5, "regular", MUTED, anchor="lm")
    c.card(sx, sy + 382, sw, 210)
    c.text(sx + 18, sy + 402, "Inspired by", 15, "bold")
    c.text(sx + 18, sy + 428, "Original ideas from creators. Structured and tested here.", 12.5, "regular", MUTED)
    for i, (pf, h_) in enumerate([("X", "@handle_one · thread"), ("@", "@handle_two · Threads post"), ("R", "Rednote · handle_three")]):
        iy = sy + 462 + i * 34
        c.line(sx + 18, iy - 8, sx + sw - 18, iy - 8)
        c.agent_dot(sx + 18, iy - 1, pf, "#2A2926", 20)
        c.text(sx + 48, iy + 9, h_, 13.5, "regular", TEXT, anchor="lm")
        c.text(sx + sw - 18, iy + 9, "↗", 13, "regular", MUTED, anchor="rm")
    c.text(sx + 18, sy + 568, "Their idea helped 1,247 people try this.", 12.5, "regular", MUTED)
    c.card(sx, sy + 608, sw, 120)
    c.text(sx + 18, sy + 628, "Good to know", 15, "bold")
    c.wrap(sx + 18, sy + 656, "Results vary by provider and region. Last changed: call script updated Sept 2026 (v3).", sw - 36, 13, "regular", "#3D3B37")
    if with_popover:
        px_, py_ = x + main_w - 420, y + 74
        c.card(px_, py_, 420, 150, r=16, shadow=True)
        c.text(px_ + 20, py_ + 22, "Share this playbook", 15, "bold")
        c.share_icons(px_ + 20, py_ + 52, size=40, gap=14)
    return sy2 + 136


def frame_detail():
    c = Canvas(1440, 2600)
    end = detail_page(c)
    c.frame_label("Frame 3 · Playbook detail v2.3 · share open, copy confirmed · illustrative data")
    c.crop_to(end + 10)
    return c.save("03_playbook_detail.png")


def overlay(c, alpha=110):
    layer = Image.new("RGBA", c.img.size, (28, 27, 25, alpha))
    c.img.paste(layer, (0, 0), layer)
    c._refresh()


def frame_try():
    W, H = 1440, 1240
    c = Canvas(W, H)
    detail_page(c, with_popover=False, with_toast=False)
    overlay(c)
    sx, sw = W - 580, 580
    c.rect(sx, 0, sw, H, fill=CARD)
    x = sx + 32
    fw = sw - 64
    c.text(x, 36, "Try: Lower your internet bill", 20, "bold")
    c.text(sx + sw - 32, 38, "✕", 18, "regular", MUTED, anchor="ra")
    y = 84
    c.text(x, y, "1  Pick your agent", 15, "bold")
    c.rect(x, y + 28, fw, 64, fill=MUSE_SOFT, outline=MUSE, r=12, width=1.6)
    c.muse_avatar(x + 32, y + 60, 18)
    c.text(x + 62, y + 50, "Muse", 16, "bold", MUSE_DARK, anchor="lm")
    c.badge(x + 62 + c.tw("Muse", 16, "bold") + 10, y + 39, "Recommended", "muse")
    c.text(x + 62, y + 74, "Calls or chats with your provider for you · 71% worked (n=301)", 12.5, "regular", MUSE_SUB, anchor="lm")
    c.circle(x + fw - 24, y + 60, 10, MUSE)
    c.text(x + fw - 24, y + 60, "✓", 11, "bold", "#FFFFFF", anchor="mm")
    xx = x
    for a in OTHER_AGENTS:
        xx += c.agent_chip(xx, y + 104, a, h=30, size=12.5, greyed=True) + 6
    y = 238
    c.text(x, y, "2  Your details", 15, "bold")
    c.text(x + fw, y + 2, "Only provider is required · stays in your browser", 12, "regular", MUTED, anchor="ra")
    c.text(x, y + 30, "Provider *", 13, "bold")
    xx = x
    for i, p in enumerate(["Xfinity", "Spectrum", "AT&T", "Verizon", "T-Mobile", "Cox", "Other"]):
        if i == 0:
            xx += c.chip(xx, y + 50, p, 13, TEXT, "#FFFFFF", TEXT, h=32, pad=12) + 7
        else:
            xx += c.chip(xx, y + 50, p, 13, h=32, pad=12) + 7
    half = (fw - 12) / 2
    c.text(x, y + 104, "Monthly price", 13, "bold")
    c.text(x + c.tw("Monthly price", 13, "bold") + 8, y + 105, "optional", 12, "regular", MUTED)
    c.rect(x, y + 124, half, 40, fill=CARD, outline=BORDER, r=10)
    c.text(x + 12, y + 144, "$ 89.99", 13.5, "regular", TEXT, anchor="lm")
    c.text(x + half + 12, y + 104, "ZIP code", 13, "bold")
    c.text(x + half + 12 + c.tw("ZIP code", 13, "bold") + 8, y + 105, "optional · finds local offers", 12, "regular", MUTED)
    c.rect(x + half + 12, y + 124, half, 40, fill=CARD, outline=BORDER, r=10)
    c.text(x + half + 24, y + 144, "94110", 13.5, "regular", TEXT, anchor="lm")
    c.text(x, y + 184, "Your latest bill", 13, "bold")
    c.text(x + c.tw("Your latest bill", 13, "bold") + 8, y + 185, "optional · makes the prompt most accurate", 12, "regular", MUTED)
    c.rect(x, y + 204, fw, 48, fill=CARD, outline=BORDER, r=10)
    c.text(x + 12, y + 228, "Paste key lines, e.g. plan name, speed, promo end date…", 13.5, "regular", MUTED, anchor="lm")
    y = 510
    c.text(x, y, "3  Your prompt", 15, "bold")
    c.rect(x, y + 28, fw, 156, fill="#F5F4F0", r=10)
    lines = ["You are helping me lower my internet bill.", "My provider is Xfinity. I pay $89.99/month", "in ZIP 94110. My bill: [Your latest bill]",
             "Find current offers from Xfinity and local", "competitors, then negotiate a lower rate", "with fallback asks, and…"]
    for i, ln in enumerate(lines):
        c.text(x + 14, y + 44 + i * 21, ln, 12.5, "regular", "#2D2B28", mono=True)
    for word, row, col_fill, col_txt in [("Xfinity.", 1, WORKED_SOFT, "#166534"), ("[Your latest bill]", 2, "#FFE8DC", "#B4400F")]:
        pre = lines[row].split(word)[0]
        hx = x + 14 + c.tw(pre, 12.5, mono=True)
        c.rect(hx - 2, y + 41 + row * 21, c.tw(word, 12.5, mono=True) + 4, 19, fill=col_fill, r=4)
        c.text(hx, y + 44 + row * 21, word, 12.5, "regular", col_txt, mono=True)
    by = y + 200
    bw = (fw - 12) / 2
    c.button(x, by, bw, 46, "✓ Copied", "success", 15)
    c.button(x + bw + 12, by, bw, 46, "Open in Muse", "muse", 15, icon="muse")
    # soft sign-in prompt shown once after copy (dismissible)
    cy = by + 66
    c.card(x, cy, fw, 176, r=14, shadow=True)
    c.text(x + 18, cy + 22, "Save this prompt and get a reminder?", 15.5, "bold")
    c.wrap(x + 18, cy + 48, "Sign in to keep your filled-in prompt, get a 7-day \"did it work?\" reminder, and report in one tap.", fw - 36, 13, "regular", MUTED)
    c.button(x + 18, cy + 100, fw - 36, 42, "Sign in", "dark", 14)
    c.text(x + fw / 2, cy + 160, "Not now", 13, "bold", MUTED, anchor="mm")
    c.frame_label("Frame 4 · Try flow v2.3 · after Copy", left=True)
    c.crop_to(cy + 200)
    return c.save("04_try_flow.png")


def frame_report():
    W, H = 1440, 1320
    c = Canvas(W, H)
    detail_page(c, with_popover=False, with_toast=False)
    overlay(c, 120)
    mw, mh = 620, 914
    mx, my = 150, 70
    c.card(mx, my, mw, mh, r=18, shadow=True)
    x = mx + 32
    fw = mw - 64
    c.text(x, my + 32, "Report your result", 22, "bold")
    c.text(x, my + 64, "Lower your internet bill · about 30 seconds · only the first question is required", 13, "regular", MUTED)
    c.text(mx + mw - 32, my + 34, "✕", 18, "regular", MUTED, anchor="ra")
    y = my + 100
    c.text(x, y, "Did it work? *", 14, "bold")
    bw = (fw - 24) / 3
    for i, (lbl, col, soft) in enumerate([("Worked", WORKED, WORKED_SOFT), ("Partly", PARTLY, PARTLY_SOFT), ("Didn't", DIDNT, DIDNT_SOFT)]):
        bx = x + i * (bw + 12)
        on = i == 0
        c.rect(bx, y + 26, bw, 60, fill=soft if on else CARD, outline=col if on else BORDER, r=12, width=2 if on else 1)
        c.circle(bx + bw / 2, y + 46, 7, col)
        c.text(bx + bw / 2, y + 68, lbl, 15, "bold", TEXT, anchor="mm")
    y += 108
    half = (fw - 12) / 2
    c.text(x, y, "Agent used", 14, "bold")
    c.rect(x, y + 24, half, 42, fill=CARD, outline=BORDER, r=10)
    c.muse_avatar(x + 22, y + 45, 10)
    c.text(x + 40, y + 45, "Muse (last try)", 14, "regular", TEXT, anchor="lm")
    c.text(x + half - 12, y + 45, "▾", 12, "regular", MUTED, anchor="rm")
    c.text(x + half + 12, y, "Provider", 14, "bold")
    c.rect(x + half + 12, y + 24, half, 42, fill=CARD, outline=BORDER, r=10)
    c.text(x + half + 24, y + 45, "Xfinity", 14, "regular", TEXT, anchor="lm")
    c.text(x + fw - 12, y + 45, "▾", 12, "regular", MUTED, anchor="rm")
    y += 88
    c.text(x, y, "How much did you save?", 14, "bold")
    c.text(x + c.tw("How much did you save?", 14, "bold") + 8, y + 1, "optional", 12.5, "regular", MUTED)
    c.rect(x, y + 24, 180, 42, fill=CARD, outline=ACCENT, r=10, width=1.5)
    c.text(x + 14, y + 45, "$  25", 15, "medium", TEXT, anchor="lm")
    c.rect(x + 192, y + 24, 120, 42, fill=CARD, outline=BORDER, r=10)
    c.text(x + 206, y + 45, "per month ▾", 14, "regular", TEXT, anchor="lm")
    y += 88
    c.text(x, y, "How long did it take you?", 14, "bold")
    c.text(x + c.tw("How long did it take you?", 14, "bold") + 8, y + 1, "optional", 12.5, "regular", MUTED)
    xx = x
    for i, t in enumerate(["< 15 min", "15–30 min", "30–60 min", "1–2 hrs", "2 hrs+"]):
        if i == 1:
            xx += c.chip(xx, y + 24, t, 13, TEXT, "#FFFFFF", TEXT, h=32, pad=13) + 8
        else:
            xx += c.chip(xx, y + 24, t, 13, h=32, pad=13) + 8
    y += 78
    c.text(x, y, "Anything others should know?", 14, "bold")
    c.rect(x, y + 24, fw, 56, fill=CARD, outline=BORDER, r=10)
    c.text(x + 14, y + 44, "Mentioned a competitor's $50 offer; they matched on the second ask.", 13.5, "regular", "#3D3B37")
    y += 100
    c.text(x, y, "Evidence", 14, "bold")
    c.text(x + 72, y + 1, "optional · private, only reviewers see it", 12.5, "regular", MUTED)
    c.rect(x, y + 24, fw, 64, fill="#FCFBF8", outline="#C9C6BE", r=10)
    c.text(x + fw / 2, y + 47, "Drop a screenshot of your new bill", 13.5, "medium", TEXT, anchor="mm")
    c.text(x + fw / 2, y + 68, "PNG, JPG or PDF · up to 5MB · hide account numbers first", 12, "regular", MUTED, anchor="mm")
    y += 106
    c.rect(x, y, fw, 118, fill=MUSE_SOFT, outline=MUSE_LINE, r=12)
    c.muse_avatar(x + 26, y + 28, 13)
    c.text(x + 48, y + 28, "Your Muse referral code", 14, "bold", MUSE_DARK, anchor="lm")
    c.text(x + 48 + c.tw("Your Muse referral code", 14, "bold") + 8, y + 29, "optional", 12.5, "regular", MUSE_SUB, anchor="lm")
    c.rect(x + 16, y + 48, 170, 38, fill=CARD, outline=MUSE_LINE, r=9)
    c.text(x + 30, y + 67, "e.g. GT09WC", 14, "regular", "#B5B2AB", anchor="lm")
    c.text(x + 200, y + 67, "6 characters, letters and numbers", 12, "regular", MUSE_SUB, anchor="lm")
    c.text(x + 16, y + 102, "Shown on your report once it's verified. Earn up to 1B tokens per Muse's terms. Never affects rankings.", 11.5, "regular", MUSE_SUB, anchor="lm")
    y += 136
    c.button(x, y, fw, 48, "Submit result", "primary", 15)
    # success + share sheet
    sx, sy, sw = 830, 300, 470
    c.text(sx, sy - 26, "After submit →", 14, "bold", "#FFFFFF")
    c.card(sx, sy, sw, 400, r=18, shadow=True)
    c.circle(sx + sw / 2, sy + 58, 28, WORKED_SOFT)
    c.text(sx + sw / 2, sy + 58, "✓", 26, "bold", WORKED, anchor="mm")
    c.text(sx + sw / 2, sy + 112, "Thanks! Your result is in.", 19, "bold", anchor="mm")
    c.wrap(sx + 36, sy + 138, "It updates the stats for everyone. Share your win so friends can try it too.", sw - 72, 13.5, "regular", MUTED)
    c.text(sx + 36, sy + 196, "Share to", 13, "bold", MUTED)
    c.share_icons(sx + 36, sy + 218, size=40, gap=19)
    c.line(sx + 36, sy + 300, sx + sw - 36, sy + 300)
    c.text(sx + 36, sy + 326, "Your share link includes your referral code if you added one.", 12.5, "regular", MUTED)
    c.text(sx + 36, sy + 358, "Try next: Cut your phone bill · 59% worked →", 13, "bold", ACCENT)
    c.frame_label("Frame 5 · Report result v2.3 · form + success share sheet")
    c.crop_to(my + mh + 30)
    return c.save("05_report_result.png")


def frame_cards():
    W = 1440
    c = Canvas(W, 1260)
    L = 80
    c.text(L, 60, "Design system: PlaybookCard in three densities", 28, "bold")
    c.text(L, 100, "One component, three layouts. Below 20 reports every density shows the Early state instead of a percentage.", 15, "regular", MUTED)
    c.text(L, 150, "Rich · homepage features", 14, "bold", MUTED)
    rich_card(c, L, 176, 400, PLAYBOOKS[0], hover=True)
    c.text(L + 410, 360, "← hover shows Try in accent", 12.5, "regular", MUTED)
    cx = L + 620
    c.text(cx, 150, "Compact · trending rows, search grid", 14, "bold", MUTED)
    compact_card(c, cx, 176, 300, "Cancel unused subscriptions", ("72%", "$31/mo"), False, ("M", "C"), "J", h=132)
    compact_card(c, cx + 320, 176, 300, "Analyze my monthly spending", "Early · 9 reports", True, ("M",), "H", h=132)
    c.text(cx, 330, "Normal", 12.5, "regular", MUTED)
    c.text(cx + 320, 330, "Early state (< 20 reports)", 12.5, "regular", MUTED)
    c.text(cx, 372, "Row · ranked lists, list view", 14, "bold", MUTED)
    c.card(cx, 398, 620, 144)
    list_row(c, cx, 398, 620, 1, "$", "Lower your internet bill", "Negotiate with your ISP · Personal finance", 68, 412, "$18/mo")
    c.line(cx + 16, 470, cx + 604, 470)
    list_row(c, cx, 470, 620, 5, "?", "Research my competitors", "Structured report · Small business", early="Early · 14 reports")
    y = 590
    c.line(L, y, W - L, y)
    c.text(L, y + 30, "Tokens", 20, "bold")
    sw = [("Background", BG), ("Card", CARD), ("Border", BORDER), ("Text", TEXT), ("Muted", MUTED), ("Accent", ACCENT),
          ("Muse blue", MUSE), ("Worked", WORKED), ("Partly", PARTLY), ("Didn't", DIDNT)]
    for i, (n_, col) in enumerate(sw):
        x = L + i * 128
        c.rect(x, y + 70, 112, 70, fill=col, outline=BORDER, r=12)
        c.text(x, y + 156, n_, 13, "bold")
        c.text(x, y + 176, col, 12, "regular", MUTED)
    y += 220
    c.text(L, y, "Agents, badges & chips", 20, "bold")
    xx = L
    xx += c.agent_chip(xx, y + 40, "Muse", h=30, size=13) + 10
    for a in OTHER_AGENTS:
        xx += c.agent_chip(xx, y + 40, a, h=30, size=13, greyed=True) + 6
    xx += 18
    for lbl, k in [("✓ Verified 3d ago", "verified"), ("New", "new"), ("Early · 7 reports", "early"), ("Worked", "verified"), ("Partly", "partly"), ("Didn't", "didnt")]:
        xx += c.badge(xx, y + 44, lbl, k) + 10
    c.tag(xx + 10, y + 44, "Personal finance")
    y += 100
    c.text(L, y, "Buttons, toast & outcome bar", 20, "bold")
    c.button(L, y + 40, 200, 44, "▶  Try this playbook", "primary")
    c.button(L + 216, y + 40, 180, 44, "Report your result", "dark")
    c.button(L + 412, y + 40, 170, 44, "Open in Muse", "muse", icon="muse")
    c.button(L + 598, y + 40, 120, 44, "✓ Copied", "success")
    c.outcome_bar(L + 750, y + 56, 380, 12, 68, 18, 14)
    c.text(L + 750, y + 86, "Worked 68% · Partly 18% · Didn't 14%", 12.5, "regular", MUTED)
    c.toast(L, y + 110, 520, "Copied! Paste it into Muse.", None, "Try this playbook →")
    c.text(L + 560, y + 128, "Share sheet:", 13, "bold", MUTED)
    c.share_icons(L + 660, y + 108, size=36, gap=14)
    c.text(L, y + 214, "Type: Helvetica Neue / Inter · H1 46 bold · section 22 bold · body 14 · mono for prompts. Radius 12–16px. Light theme. Muse avatar is a placeholder.", 13, "regular", MUTED)
    c.frame_label("Frame 6 · Card system & tokens v2.3")
    c.crop_to(y + 250)
    return c.save("06_card_system.png")


def phone(c, ox, oy, title, draw_fn):
    pw, ph = 390, 844
    c.shadow(ox, oy, pw, ph, r=44, spread=14, alpha=16)
    c.rect(ox - 10, oy - 10, pw + 20, ph + 20, fill="#1C1B19", r=52)
    c.rect(ox, oy, pw, ph, fill=BG, r=42)
    draw_fn(ox, oy + 50, pw)
    c.rect(ox + pw / 2 - 60, oy + 10, 120, 30, fill="#1C1B19", r=15)
    c.text(ox + pw / 2, oy + ph + 40, title, 14, "bold", MUTED, anchor="mm")


def m_header(c, x, y, w, signed_in=False):
    L = x + 20
    c.logo(L, y + 16, 18)
    c.magnifier(x + w - 76, y + 15)
    if signed_in:
        c.avatar(x + w - 34, y + 16, "J", r=14)
    else:
        c.text(x + w - 22, y + 17, "☰", 19, "regular", TEXT, anchor="rm")


def m_sheet(c, x, y, w, top):
    # dimmed page + bottom sheet from `top` to the phone bottom
    c.rect(x, y - 50, w, 844, fill="#8E8B85", r=42)
    c.rect(x, top, w, (y - 50 + 844) - top, fill=CARD, r=40)
    c.rect(x + w / 2 - 20, top + 8, 40, 5, fill="#D6D3CC", r=3)


def m_home(c, x, y, w):
    L = x + 20
    m_header(c, x, y, w)
    c.text(L, y + 70, "What do you want", 27, "bold", anchor="lm")
    xx = L + c.text(L, y + 104, "Muse", 27, "bold", MUSE, anchor="lm")
    c.text(xx, y + 104, " to do?", 27, "bold", anchor="lm")
    c.search_box(L, y + 134, w - 40, 50, "Save $100 on internet bill", 14.5)
    c.text(L, y + 202, "48 playbooks · 3,210 real results", 12.5, "regular", MUTED)
    xx = L
    for ch in ["Save money", "Book travel", "Plan a trip", "Shopping"]:
        xx += c.chip(xx, y + 222, ch, 13, h=32, pad=12) + 8
    c.rect(x + w - 20, y + 218, 20, 40, fill=BG)
    c.fade_right(x + w - 70, y + 222, 50, 32)
    c.text(L, y + 290, "Popular Use Cases", 18, "bold")
    tw_ = (w - 40 - 12) / 2 - 16
    tiles = [("Cut monthly bills", "#2F4F46", "#5E7F73"), ("Cheaper flights", "#8A5A1F", "#C0925A"), ("Plan a trip", "#3E3F63", "#7E7FA6")]
    R = x + w - 20
    for i, (n_, c1, c2) in enumerate(tiles):
        tx = L + i * (tw_ + 12)
        c.gradient_rect(tx, y + 314, tw_ if i < 2 else max(8, R - tx), 70, c1, c2, r=12 if i < 2 else 4)
        if i < 2:
            c.text(tx + tw_ / 2, y + 349, n_, 14, "bold", "#FFFFFF", anchor="mm")
    c.rect(R, y + 310, x + w - R, 80, fill=BG)
    c.fade_right(R - 34, y + 314, 34, 70)
    c.circle(R - 4, y + 349, 17, CARD, BORDER, 1)
    c.text(R - 4, y + 349, "›", 20, "bold", TEXT, anchor="mm")
    for k in range(3):
        c.circle(x + w / 2 - 12 + k * 12, y + 398, 3, TEXT if k == 0 else "#CFCBC3")
    c.text(L, y + 426, "Proven to work", 18, "bold")
    p = PLAYBOOKS[0]
    c.card(L, y + 452, w - 40, 290)
    preview(c, L, y + 452, w - 40, 124, p)
    c.text(L + 16, y + 592, p["title"], 16, "bold")
    xx = L + 16 + c.text(L + 16, y + 620, "1,247 tried · ", 13, "regular", "#3D3B37")
    c.text(xx, y + 620, "68% worked (n=412)", 13, "bold", WORKED)
    c.text(L + 16, y + 642, "Median $18/mo · verified 3d ago", 13, "regular", MUTED)
    c.agent_chip(L + 16, y + 674, "Muse")
    c.button(x + w - 20 - 16 - 90, y + 670, 90, 36, "▶ Try", "primary", 14)


def m_detail(c, x, y, w):
    L = x + 20
    c.text(L, y + 16, "‹ Personal finance", 13, "medium", MUTED, anchor="lm")
    c.rect(x + w - 100, y, 36, 32, fill=CARD, outline=BORDER, r=9)
    c.text(x + w - 82, y + 16, "☆", 15, "bold", TEXT, anchor="mm")
    c.rect(x + w - 56, y, 36, 32, fill=CARD, outline=BORDER, r=9)
    c.text(x + w - 38, y + 16, "↗", 15, "bold", TEXT, anchor="mm")
    c.wrap(L, y + 46, "Lower your internet bill", w - 40, 25, "bold", TEXT, lh=30)
    c.wrap(L, y + 82, "Negotiate a lower rate with your provider using Muse.", w - 40, 13.5, "regular", MUTED)
    bw = c.badge(L, y + 128, "✓ Verified 3 days ago", "verified")
    c.agent_chip(L + bw + 8, y + 126, "Muse")
    tw_ = (w - 40 - 16) / 3
    for i, (a, b, n_) in enumerate([("Tried", "1,247", ""), ("Worked", "68%", "n=412"), ("Median", "$18/mo", "n=236")]):
        tx = L + i * (tw_ + 8)
        c.card(tx, y + 164, tw_, 74, r=12)
        c.text(tx + 12, y + 177, a, 11.5, "regular", MUTED)
        c.text(tx + 12, y + 195, b, 19, "bold", WORKED if a == "Worked" else TEXT)
        if n_:
            c.text(tx + 12, y + 222, n_, 10.5, "regular", MUTED)
    c.text(L, y + 256, "Works with", 12.5, "bold", MUTED)
    c.rect(L, y + 276, w - 40, 50, fill=MUSE_SOFT, outline=MUSE_LINE, r=12)
    c.muse_avatar(L + 24, y + 301, 13)
    c.text(L + 46, y + 293, "Muse", 14, "bold", MUSE_DARK, anchor="lm")
    c.text(L + 46, y + 311, "Calls and chats for you · 71% worked", 11.5, "regular", MUSE_SUB, anchor="lm")
    xx = L
    for a in OTHER_AGENTS:
        xx += c.agent_chip(xx, y + 334, a, h=24, size=11, greyed=True) + 4
    c.card(L, y + 374, w - 40, 170)
    c.text(L + 16, y + 390, "The playbook", 14.5, "bold")
    c.button(x + w - 20 - 16 - 92, y + 382, 92, 30, "✓ Copied", "success", 12.5)
    c.rect(L + 16, y + 422, w - 72, 62, fill="#F5F4F0", r=8)
    c.wrap(L + 26, y + 432, "You are helping me lower my internet bill. My provider is {{provider}}…", w - 92, 11.5, "regular", "#2D2B28", lh=17, mono=True, max_lines=2)
    c.text(L + 16, y + 504, "What you'll need: Provider (required),", 12, "regular", MUTED)
    c.text(L + 16, y + 522, "price, ZIP, bill (optional)", 12, "regular", MUTED)
    # toast above sticky bar
    ty = y + 572
    c.shadow(L, ty, w - 40, 78, r=12, spread=8, alpha=22)
    c.rect(L, ty, w - 40, 78, fill="#1F1E1C", r=12)
    c.circle(L + 22, ty + 22, 9, WORKED)
    c.text(L + 22, ty + 22, "✓", 11, "bold", "#FFFFFF", anchor="mm")
    c.text(L + 40, ty + 22, "Copied! Paste it into Muse.", 13.5, "bold", "#FFFFFF", anchor="lm")
    c.text(L + 40, ty + 44, "Want it filled in with your details?", 12, "regular", "#CFCBC3", anchor="lm")
    c.text(L + 40, ty + 63, "Try this playbook →", 12, "bold", "#FFB08F", anchor="lm")
    by = y + 672
    c.rect(x, by - 12, w, 90, fill=CARD)
    c.line(x, by - 12, x + w, by - 12)
    c.button(L, by, (w - 52) * 0.62, 46, "▶ Try this playbook", "primary", 14)
    c.button(L + (w - 52) * 0.62 + 12, by, (w - 52) * 0.38, 46, "Report", "secondary", 14)


def m_try(c, x, y, w):
    L = x + 20
    sy = y + 10
    m_sheet(c, x, y, w, sy)
    c.text(L, sy + 34, "Try: Lower your internet bill", 16, "bold")
    c.text(x + w - 20, sy + 34, "✕", 15, "regular", MUTED, anchor="ra")
    c.rect(L, sy + 56, w - 40, 56, fill=MUSE_SOFT, outline=MUSE, r=12, width=1.5)
    c.muse_avatar(L + 27, sy + 84, 15)
    c.text(L + 52, sy + 76, "Muse", 14.5, "bold", MUSE_DARK, anchor="lm")
    c.text(L + 52, sy + 95, "Calls or chats for you · 71% worked", 11.5, "regular", MUSE_SUB, anchor="lm")
    c.circle(x + w - 40, sy + 84, 9, MUSE)
    c.text(x + w - 40, sy + 84, "✓", 10, "bold", "#FFFFFF", anchor="mm")
    xx = L
    for a in OTHER_AGENTS:
        xx += c.agent_chip(xx, sy + 120, a, h=24, size=11, greyed=True) + 4
    c.text(L, sy + 166, "Provider *", 13, "bold")
    c.text(x + w - 20, sy + 166, "only required field", 11, "regular", MUTED, anchor="ra")
    xx, yy = L, sy + 182
    for i, p in enumerate(["Xfinity", "Spectrum", "AT&T", "Verizon", "T-Mobile", "Cox", "Other"]):
        wv = c.tw(p, 13) + 24
        if xx + wv > x + w - 20:
            xx, yy = L, yy + 38
        if i == 0:
            c.chip(xx, yy, p, 13, TEXT, "#FFFFFF", TEXT, h=32, pad=12)
        else:
            c.chip(xx, yy, p, 13, h=32, pad=12)
        xx += wv + 7
    yy += 50
    half = (w - 40 - 10) / 2
    c.text(L, yy, "Monthly price · optional", 12, "bold")
    c.text(L + half + 10, yy, "ZIP code · optional", 12, "bold")
    c.rect(L, yy + 16, half, 38, fill=CARD, outline=BORDER, r=10)
    c.text(L + 12, yy + 35, "$ 89.99", 13.5, "regular", TEXT, anchor="lm")
    c.rect(L + half + 10, yy + 16, half, 38, fill=CARD, outline=BORDER, r=10)
    c.text(L + half + 22, yy + 35, "94110", 13.5, "regular", TEXT, anchor="lm")
    yy += 68
    c.text(L, yy, "Your latest bill · optional", 12, "bold")
    c.rect(L, yy + 16, w - 40, 38, fill=CARD, outline=BORDER, r=10)
    c.text(L + 12, yy + 35, "Paste key lines…", 13, "regular", MUTED, anchor="lm")
    yy += 68
    hb = (w - 40 - 10) / 2
    c.button(L, yy, hb, 44, "✓ Copied", "success", 14)
    c.button(L + hb + 10, yy, hb, 44, "Open in Muse", "muse", 13.5, icon="muse")
    yy += 58
    c.card(L, yy, w - 40, 126, r=14, shadow=True)
    c.text(L + 14, yy + 18, "Save this prompt and get a reminder?", 13.5, "bold")
    c.wrap(L + 14, yy + 38, "Keep your filled-in prompt and get a 7-day \"did it work?\" reminder.", w - 68, 11.5, "regular", MUTED)
    c.button(L + 14, yy + 74, w - 68, 34, "Sign in", "dark", 13)
    c.text(x + w / 2, yy + 118, "Not now", 11.5, "bold", MUTED, anchor="mm")


def m_menu(c, x, y, w):
    m_home(c, x, y, w)
    layer = Image.new("RGBA", c.img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle([x * S, (y - 50) * S, (x + w) * S, (y + 794) * S], radius=42 * S, fill=(28, 27, 25, 120))
    c.img.paste(layer, (0, 0), layer)
    c._refresh()
    dx = x + 56
    c.rect(dx, y - 50, x + w - dx, 844, fill=CARD, r=42)
    c.rect(dx, y - 50, 44, 844, fill=CARD)
    L = dx + 24
    c.text(x + w - 24, y + 16, "✕", 17, "regular", TEXT, anchor="rm")
    c.button(L, y + 50, x + w - 24 - L, 44, "Sign in", "dark", 14)
    items = ["Playbooks", "Starter kits", "Categories"]
    for i, t in enumerate(items):
        c.text(L, y + 132 + i * 46, t, 17, "medium", TEXT, anchor="lm")
    c.line(L, y + 254, x + w - 24, y + 254)
    c.button(L, y + 274, x + w - 24 - L, 42, "+ Create a playbook", "secondary", 14)
    c.button(L, y + 326, x + w - 24 - L, 42, "Report a result", "secondary", 14)
    c.line(L, y + 392, x + w - 24, y + 392)
    for i, t in enumerate(["How we verify", "Request a playbook", "Privacy", "Terms"]):
        c.text(L, y + 420 + i * 34, t, 14, "regular", MUTED, anchor="lm")


def m_report(c, x, y, w):
    L = x + 20
    sy = y + 10
    m_sheet(c, x, y, w, sy)
    fw = w - 40
    c.text(L, sy + 34, "Report your result", 17, "bold")
    c.text(x + w - 20, sy + 34, "✕", 15, "regular", MUTED, anchor="ra")
    c.text(L, sy + 56, "Only the first question is required", 11.5, "regular", MUTED)
    c.text(L, sy + 84, "Did it work? *", 13, "bold")
    bw = (fw - 16) / 3
    for i, (lbl, col, soft) in enumerate([("Worked", WORKED, WORKED_SOFT), ("Partly", PARTLY, PARTLY_SOFT), ("Didn't", DIDNT, DIDNT_SOFT)]):
        bx = L + i * (bw + 8)
        on = i == 0
        c.rect(bx, sy + 100, bw, 52, fill=soft if on else CARD, outline=col if on else BORDER, r=12, width=2 if on else 1)
        c.circle(bx + bw / 2, sy + 116, 6, col)
        c.text(bx + bw / 2, sy + 137, lbl, 13, "bold", TEXT, anchor="mm")
    half = (fw - 10) / 2
    y2 = sy + 170
    c.text(L, y2, "Agent used", 12, "bold")
    c.text(L + half + 10, y2, "Provider", 12, "bold")
    c.rect(L, y2 + 16, half, 38, fill=CARD, outline=BORDER, r=10)
    c.muse_avatar(L + 18, y2 + 35, 9)
    c.text(L + 34, y2 + 35, "Muse", 13, "regular", TEXT, anchor="lm")
    c.rect(L + half + 10, y2 + 16, half, 38, fill=CARD, outline=BORDER, r=10)
    c.text(L + half + 22, y2 + 35, "Xfinity ▾", 13, "regular", TEXT, anchor="lm")
    y2 += 70
    c.text(L, y2, "How much did you save? · optional", 12, "bold")
    c.rect(L, y2 + 16, 130, 38, fill=CARD, outline=ACCENT, r=10, width=1.5)
    c.text(L + 12, y2 + 35, "$  25", 13.5, "medium", TEXT, anchor="lm")
    c.rect(L + 140, y2 + 16, 110, 38, fill=CARD, outline=BORDER, r=10)
    c.text(L + 152, y2 + 35, "per month ▾", 13, "regular", TEXT, anchor="lm")
    y2 += 70
    c.text(L, y2, "How long did it take? · optional", 12, "bold")
    xx, yy = L, y2 + 16
    for i, t in enumerate(["< 15 min", "15–30 min", "30–60 min", "1–2 hrs", "2 hrs+"]):
        wv = c.tw(t, 12) + 22
        if xx + wv > x + w - 20:
            xx, yy = L, yy + 36
        if i == 1:
            c.chip(xx, yy, t, 12, TEXT, "#FFFFFF", TEXT, h=30, pad=11)
        else:
            c.chip(xx, yy, t, 12, h=30, pad=11)
        xx += wv + 6
    y2 = yy + 48
    c.text(L, y2, "Evidence · optional, private", 12, "bold")
    c.rect(L, y2 + 16, fw, 44, fill="#FCFBF8", outline="#C9C6BE", r=10)
    c.text(L + fw / 2, y2 + 38, "Add a screenshot (hide account numbers)", 12.5, "medium", TEXT, anchor="mm")
    y2 += 76
    c.rect(L, y2, fw, 96, fill=MUSE_SOFT, outline=MUSE_LINE, r=12)
    c.muse_avatar(L + 22, y2 + 22, 11)
    c.text(L + 40, y2 + 22, "Muse referral code · optional", 12.5, "bold", MUSE_DARK, anchor="lm")
    c.rect(L + 12, y2 + 40, 140, 36, fill=CARD, outline=MUSE_LINE, r=9)
    c.text(L + 24, y2 + 58, "e.g. GT09WC", 13, "regular", "#B5B2AB", anchor="lm")
    c.text(L + 162, y2 + 58, "6 letters/numbers", 11, "regular", MUSE_SUB, anchor="lm")
    c.text(L + 12, y2 + 86, "Never affects rankings.", 10.5, "regular", MUSE_SUB, anchor="lm")
    c.button(L, y2 + 110, fw, 46, "Submit result", "primary", 15)


def m_signin(c, x, y, w):
    m_detail(c, x, y, w)
    sy = y + 190
    layer = Image.new("RGBA", c.img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle([x * S, (y - 50) * S, (x + w) * S, (y + 794) * S], radius=42 * S, fill=(28, 27, 25, 120))
    c.img.paste(layer, (0, 0), layer)
    c._refresh()
    c.rect(x, sy, w, (y + 794) - sy, fill=CARD, r=40)
    c.rect(x + w / 2 - 20, sy + 8, 40, 5, fill="#D6D3CC", r=3)
    L, fw = x + 24, w - 48
    c.circle(L + 20, sy + 50, 20, MUSE_SOFT)
    c.text(L + 20, sy + 50, "☆", 18, "bold", MUSE, anchor="mm")
    c.text(x + w - 24, sy + 36, "✕", 15, "regular", MUTED, anchor="ra")
    c.text(L, sy + 92, "Sign in to save this playbook", 19, "bold")
    c.wrap(L, sy + 118, "Save playbooks, get reminders, and report results in one tap. Free.", fw, 12.5, "regular", MUTED)
    yy = sy + 164
    google_button(c, L, yy, fw, 44, "Continue with Google")
    c.rect(L, yy + 54, fw, 44, fill=FB_BLUE, r=10)
    tw_ = c.tw("Continue with Facebook", 14.5, "bold") + 30
    fx = L + (fw - tw_) / 2
    c.circle(fx + 10, yy + 76, 10, "#FFFFFF")
    c.text(fx + 11, yy + 77, "f", 15, "bold", FB_BLUE, anchor="mm")
    c.text(fx + 30, yy + 76, "Continue with Facebook", 14.5, "bold", "#FFFFFF", anchor="lm")
    c.line(L, yy + 124, L + fw / 2 - 16, yy + 124)
    c.text(L + fw / 2, yy + 124, "or", 12, "regular", MUTED, anchor="mm")
    c.line(L + fw / 2 + 16, yy + 124, L + fw, yy + 124)
    c.rect(L, yy + 144, fw, 42, fill=CARD, outline=BORDER, r=10)
    c.text(L + 12, yy + 165, "you@example.com", 13.5, "regular", MUTED, anchor="lm")
    c.button(L, yy + 196, fw, 44, "Email me a sign-in link", "primary", 14)
    c.wrap(L, yy + 254, "New here? This creates your free account. No password needed.", fw, 11.5, "regular", MUTED)


def m_saved(c, x, y, w):
    L = x + 20
    m_header(c, x, y, w, signed_in=True)
    c.text(L, y + 66, "My playbooks", 24, "bold", anchor="lm")
    xx = L
    for t, n, on in [("Saved", "6", True), ("Tried", "4", False), ("Reported", "2", False)]:
        c.text(xx, y + 108, t, 14, "bold", TEXT if on else MUTED, anchor="lm")
        tx = xx + c.tw(t, 14, "bold") + 6
        c.rect(tx, y + 99, c.tw(n, 11, "bold") + 12, 18, fill=ACCENT_SOFT if on else SOFT, r=9)
        c.text(tx + 6, y + 108, n, 11, "bold", "#C2410C" if on else MUTED, anchor="lm")
        if on:
            c.rect(xx, y + 126, tx - xx + 24, 3, fill=ACCENT, r=1.5)
        xx = tx + 44
    c.line(L, y + 129, x + w - 20, y + 129)
    xx = L
    for i, ch in enumerate(["All", "Personal finance", "Travel", "Small business"]):
        if i == 0:
            xx += c.chip(xx, y + 144, ch, 12.5, TEXT, "#FFFFFF", TEXT, h=30, pad=12) + 6
        else:
            xx += c.chip(xx, y + 144, ch, 12.5, h=30, pad=12) + 6
    c.rect(x + w - 20, y + 140, 20, 38, fill=BG)
    c.fade_right(x + w - 60, y + 144, 40, 30)
    cards = [("Lower your internet bill", "68%", "$18/mo", "Saved 2 days ago · tried", True, False),
             ("Plan 7 days in Japan", "81%", "3 hrs", "Saved 1 week ago", False, True),
             ("Cheaper car insurance", "54%", "$240/yr", "Saved 1 week ago", False, False)]
    cy = y + 192
    for t, pct, med, when, tried, upd in cards:
        h = 176 if tried or upd else 150
        c.card(L, cy, w - 40, h)
        c.text(L + 16, cy + 22, t, 15.5, "bold", anchor="lm")
        c.rect(x + w - 20 - 46, cy + 8, 32, 28, fill=MUSE_SOFT, outline=MUSE_LINE, r=8)
        c.text(x + w - 20 - 30, cy + 22, "★", 14, "bold", MUSE, anchor="mm")
        xx = L + 16 + c.text(L + 16, cy + 52, pct + " worked", 13, "bold", WORKED, anchor="lm")
        c.text(xx, cy + 52, "  ·  median " + med, 13, "regular", "#3D3B37", anchor="lm")
        c.text(L + 16, cy + 76, when, 12, "regular", MUTED, anchor="lm")
        yb = cy + 96
        if upd:
            c.badge(L + 16, yb, "Updated since you saved", "new")
            yb += 30
        if tried:
            c.badge(L + 16, yb, "Did it work? Report →", "dark")
            yb += 30
        c.button(L + 16, yb, 76, 32, "▶ Try", "primary", 12.5)
        cy += h + 12


def frame_mobile_a():
    W, H = 1560, 1070
    c = Canvas(W, H)
    c.text(80, 50, "Mobile · 390pt (1 of 2)", 24, "bold")
    c.text(80, 84, "Same content and rules as desktop, single column. Try opens as a bottom sheet; Try and Report stay in a sticky bar on detail.", 14, "regular", MUTED)
    phone(c, 110, 130, "Homepage", lambda x, y, w: m_home(c, x, y, w))
    phone(c, 585, 130, "Playbook detail (after Copy)", lambda x, y, w: m_detail(c, x, y, w))
    phone(c, 1060, 130, "Try (bottom sheet)", lambda x, y, w: m_try(c, x, y, w))
    c.frame_label("Frame 7a · Mobile v2.3")
    return c.save("07a_mobile.png")


def frame_mobile_b():
    W, H = 2040, 1070
    c = Canvas(W, H)
    c.text(80, 50, "Mobile · 390pt (2 of 2)", 24, "bold")
    c.text(80, 84, "Menu holds the desktop header links; Report and Sign-in are bottom sheets; My playbooks mirrors the desktop page.", 14, "regular", MUTED)
    phone(c, 110, 130, "Menu (☰)", lambda x, y, w: m_menu(c, x, y, w))
    phone(c, 585, 130, "Report result (sheet)", lambda x, y, w: m_report(c, x, y, w))
    phone(c, 1060, 130, "Sign in (sheet, from Save)", lambda x, y, w: m_signin(c, x, y, w))
    phone(c, 1535, 130, "My playbooks", lambda x, y, w: m_saved(c, x, y, w))
    c.frame_label("Frame 7b · Mobile v2.3")
    return c.save("07b_mobile.png")


def google_button(c, x, y, w, h, label):
    c.rect(x, y, w, h, fill=CARD, outline=BORDER, r=10)
    tw_ = c.tw(label, 14.5, "bold") + 28
    gx = x + (w - tw_) / 2
    c.text(gx + 8, y + h / 2, "G", 17, "bold", "#4285F4", anchor="mm")
    c.text(gx + 28, y + h / 2, label, 14.5, "bold", TEXT, anchor="lm")


def signin_modal(c, mx, my, mw, title, sub, icon="☆"):
    mh = 520
    c.card(mx, my, mw, mh, r=18, shadow=True)
    x, fw = mx + 32, mw - 64
    c.text(mx + mw - 30, my + 30, "✕", 17, "regular", MUTED, anchor="ra")
    c.circle(x + 22, my + 50, 22, MUSE_SOFT)
    c.text(x + 22, my + 50, icon, 20, "bold", MUSE, anchor="mm")
    c.text(x, my + 96, title, 22, "bold")
    c.wrap(x, my + 128, sub, fw, 14, "regular", MUTED)
    y = my + 184
    google_button(c, x, y, fw, 46, "Continue with Google")
    c.rect(x, y + 56, fw, 46, fill=FB_BLUE, r=10)
    tw_ = c.tw("Continue with Facebook", 14.5, "bold") + 30
    fx = x + (fw - tw_) / 2
    c.circle(fx + 10, y + 79, 10, "#FFFFFF")
    c.text(fx + 11, y + 80, "f", 15, "bold", FB_BLUE, anchor="mm")
    c.text(fx + 30, y + 79, "Continue with Facebook", 14.5, "bold", "#FFFFFF", anchor="lm")
    c.line(x, y + 132, x + fw / 2 - 18, y + 132)
    c.text(x + fw / 2, y + 132, "or", 12.5, "regular", MUTED, anchor="mm")
    c.line(x + fw / 2 + 18, y + 132, x + fw, y + 132)
    c.rect(x, y + 152, fw, 44, fill=CARD, outline=BORDER, r=10)
    c.text(x + 14, y + 174, "you@example.com", 14, "regular", MUTED, anchor="lm")
    c.button(x, y + 206, fw, 46, "Email me a sign-in link", "primary", 14.5)
    c.wrap(x, y + 268, "New here? This creates your free account, no password needed. By continuing you agree to the Terms and Privacy Policy.", fw, 12, "regular", MUTED)
    return mh


def frame_signin():
    W, H = 1440, 1120
    c = Canvas(W, H)
    detail_page(c, with_popover=False, with_toast=False)
    overlay(c, 130)
    signin_modal(c, 140, 120, 470, "Sign in to save this playbook",
                 "Save playbooks, get a \"did it work?\" reminder, and report results in one tap. Free.")
    # right column: how it works
    rx, rw = 680, 680
    c.text(rx, 110, "How sign-in works (for review)", 16, "bold", "#FFFFFF")
    y = 130
    c.card(rx, y, rw, 350, r=16)
    c.text(rx + 20, y + 22, "When we ask", 15, "bold")
    rows = [("Browse, search, open playbooks", "Never", "early"),
            ("Try + Copy prompt, Open in Muse", "Never (one soft reminder card after first copy)", "early"),
            ("Save a playbook", "Required · \"Sign in to save this playbook\"", "muse"),
            ("Report a result", "Required · \"Sign in to report your result\"", "muse"),
            ("Create a playbook", "Required · \"Sign in to create a playbook\"", "muse"),
            ("Get a \"did it work?\" reminder", "Required · opt-in from Try or Report", "muse")]
    for i, (a, b, k) in enumerate(rows):
        ry = y + 56 + i * 46
        if i:
            c.line(rx + 20, ry - 10, rx + rw - 20, ry - 10)
        c.text(rx + 20, ry + 8, a, 13.5, "medium", TEXT, anchor="lm")
        c.badge(rx + 290, ry - 3, b, k)
    y += 370
    hw = (rw - 16) / 2
    c.card(rx, y, hw, 220, r=16)
    c.circle(rx + 42, y + 44, 22, SOFT)
    c.rect(rx + 30, y + 36, 24, 17, outline=TEXT, r=3, width=1.6)
    c.line(rx + 30, y + 37, rx + 42, y + 46, TEXT, 1.6)
    c.line(rx + 54, y + 37, rx + 42, y + 46, TEXT, 1.6)
    c.text(rx + 20, y + 84, "Check your email", 16, "bold")
    c.wrap(rx + 20, y + 110, "We sent a sign-in link to jane@example.com. It expires in 15 minutes.", hw - 40, 13, "regular", MUTED)
    c.text(rx + 20, y + 176, "Resend link", 13, "bold", ACCENT)
    c.text(rx + 20 + c.tw("Resend link", 13, "bold") + 18, y + 176, "Use a different email", 13, "bold", MUTED)
    bx = rx + hw + 16
    c.card(bx, y, hw, 220, r=16)
    c.text(bx + 20, y + 26, "After sign-in, we finish the action", 15, "bold")
    c.wrap(bx + 20, y + 52, "You land back on the same page and scroll position; the save, report or create you started completes automatically.", hw - 40, 13, "regular", MUTED)
    c.rect(bx + 20, y + 136, hw - 40, 52, fill="#1F1E1C", r=12)
    c.circle(bx + 42, y + 162, 10, WORKED)
    c.text(bx + 42, y + 162, "✓", 12, "bold", "#FFFFFF", anchor="mm")
    c.text(bx + 60, y + 162, "Saved", 13.5, "bold", "#FFFFFF", anchor="lm")
    c.text(bx + hw - 34, y + 162, "View saved →", 13, "bold", "#FFB08F", anchor="rm")
    y += 240
    c.card(rx, y, rw, 150, r=16)
    c.text(rx + 20, y + 22, "Rules", 15, "bold")
    for i, t in enumerate(["Sign-in never blocks reading, trying or copying a prompt.",
                           "One modal, three ways in: Google, Facebook (Meta), or an email magic link. Sign-up = sign-in.",
                           "Closing the modal cancels only the pending action; the page stays as it was.",
                           "Saved items made while signed out are not kept locally (keeps it simple and private)."]):
        c.text(rx + 20, y + 52 + i * 23, "•  " + t, 12.5, "regular", "#3D3B37")
    c.frame_label("Frame 8 · Sign-in / sign-up · triggered by Save", left=True)
    c.crop_to(y + 170)
    return c.save("08_sign_in.png")


def saved_card(c, x, y, w, title, cat, evidence, early=False, note=None, tried=False, updated=False, when="Saved 2 days ago"):
    h = 196
    c.card(x, y, w, h)
    c.tag(x + 16, y + 16, cat)
    c.rect(x + w - 50, y + 12, 34, 30, fill=MUSE_SOFT, outline=MUSE_LINE, r=8)
    c.text(x + w - 33, y + 27, "★", 15, "bold", MUSE, anchor="mm")
    c.wrap(x + 16, y + 52, title, w - 80, 16, "bold", TEXT, max_lines=2)
    if early:
        c.badge(x + 16, y + 96, evidence, "early")
    else:
        pct, rest = evidence
        xx = x + 16 + c.text(x + 16, y + 100, pct + " worked", 14, "bold", WORKED)
        c.text(xx, y + 100, "  ·  median " + rest, 14, "regular", "#3D3B37")
    c.text(x + 16, y + 126, when, 12.5, "regular", MUTED)
    if updated:
        c.badge(x + 16 + c.tw(when, 12.5) + 10, y + 123, "Updated since you saved", "new")
    if tried:
        c.button(x + 16, y + 148, 110, 32, "▶ Try again", "secondary", 12.5)
        c.button(x + 134, y + 148, 150, 32, "Did it work? Report", "dark", 12.5)
    else:
        c.button(x + 16, y + 148, 80, 32, "▶ Try", "primary", 12.5)


def frame_saved():
    W = 1440
    c = Canvas(W, 1300)
    c.nav(signed_in=True)
    L, R = 80, W - 80
    c.text(L, 104, "My playbooks", 30, "bold")
    c.text(L, 146, "Everything you've saved, tried and reported. Only you can see this page.", 14.5, "regular", MUTED)
    tabs = [("Saved", "6", True), ("Tried", "4", False), ("Reported", "2", False)]
    xx = L
    for t, n, on in tabs:
        w = c.tw(t, 15, "bold") + c.tw(n, 12, "bold") + 30
        c.text(xx, 196, t, 15, "bold", TEXT if on else MUTED, anchor="lm")
        tx = xx + c.tw(t, 15, "bold") + 8
        c.rect(tx, 186, c.tw(n, 12, "bold") + 14, 20, fill=ACCENT_SOFT if on else SOFT, r=10)
        c.text(tx + 7, 196, n, 12, "bold", "#C2410C" if on else MUTED, anchor="lm")
        if on:
            c.rect(xx, 218, w - 6, 3, fill=ACCENT, r=1.5)
        xx += w + 26
    c.line(L, 221, R, 221)
    xx = L
    for i, ch in enumerate(["All", "Personal finance", "Travel", "Small business"]):
        if i == 0:
            xx += c.chip(xx, 244, ch, 13, TEXT, "#FFFFFF", TEXT, h=32, pad=13) + 8
        else:
            xx += c.chip(xx, 244, ch, 13, h=32, pad=13) + 8
    c.chip(xx + 16, 244, "Sort: Recently saved ▾", 13, h=32, pad=13, weight="medium")
    colw = (R - L - 36) / 3
    cards = [("Lower your internet bill", "Personal finance", ("68%", "$18/mo"), False, True, False, "Saved 2 days ago · tried yesterday"),
             ("Plan 7 days in Japan", "Trip planning", ("81%", "3 hrs"), False, False, True, "Saved 1 week ago"),
             ("Cheaper car insurance", "Personal finance", ("54%", "$240/yr"), False, False, False, "Saved 1 week ago"),
             ("Claim flight delay compensation", "Travel booking", ("62%", "$400"), False, False, False, "Saved 2 weeks ago"),
             ("Research my competitors", "Small business", "Early · 14 reports", True, False, False, "Saved 3 weeks ago"),
             ("Cancel unused subscriptions", "Personal finance", ("72%", "$31/mo"), False, True, False, "Saved 1 month ago · tried")]
    for i, (t, cat, ev, early, tried, upd, when) in enumerate(cards):
        saved_card(c, L + (i % 3) * (colw + 18), 300 + (i // 3) * 214, colw, t, cat, ev, early, tried=tried, updated=upd, when=when)
    y = 750
    c.card(L, y, R - L, 120, r=16, fill="#FFFDFB")
    c.text(L + 24, y + 30, "Empty state", 12.5, "bold", MUTED)
    c.text(L + 24, y + 58, "No saved playbooks yet. Tap ☆ Save on any playbook to keep it here.", 16, "bold")
    c.button(R - 220, y + 38, 196, 42, "Browse Proven to work", "primary", 14)
    # avatar menu open
    mx, mw = W - 32 - 250, 250
    c.card(mx, 60, mw, 256, r=14, shadow=True)
    c.avatar(mx + 32, 96, "J", r=16)
    c.text(mx + 56, 88, "Jane Doe", 14, "bold", anchor="lm")
    c.text(mx + 56, 106, "jane@example.com", 12, "regular", MUTED, anchor="lm")
    c.line(mx + 14, 128, mx + mw - 14, 128)
    for i, (t, on) in enumerate([("My playbooks", True), ("Create a playbook", False), ("Settings & reminders", False), ("Sign out", False)]):
        iy = 150 + i * 40
        if on:
            c.rect(mx + 8, iy - 16, mw - 16, 34, fill=SOFT, r=8)
        c.text(mx + 20, iy + 1, t, 14, "medium" if on else "regular", TEXT, anchor="lm")
    c.frame_label("Frame 9 · My playbooks (saved) · signed in · avatar menu open", left=True)
    c.crop_to(y + 150)
    return c.save("09_saved_playbooks.png")


if __name__ == "__main__":
    for fn in [frame_homepage, frame_search, frame_detail, frame_try, frame_report, frame_cards, frame_signin, frame_saved, frame_mobile_a, frame_mobile_b]:
        fn()
