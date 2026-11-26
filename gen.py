"""Generates the profile README header into ./assets (light + dark).

Run:  python gen.py
"""
from pathlib import Path
from textwrap import wrap
from html import escape

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
SERIF = "'Iowan Old Style', 'Palatino Linotype', Palatino, Georgia, serif"

THEMES = {
    "light": dict(
        bg="#fbfaf6", card="#ffffff", line="#e4e0d6", ink="#1f2328", soft="#59636e",
        faint="#8c959f", paren="#b7791f", key="#2f7f6f", str="#b4536a", sym="#4b5bb5",
        ok="#2f9e6b", warn="#e0702e", panel="#d9d6cf", panel2="#b9b5ac", node="#f3efe6",
    ),
    "dark": dict(
        bg="#0f1216", card="#151a21", line="#2a313b", ink="#e6edf3", soft="#9aa5b1",
        faint="#6e7781", paren="#e0a458", key="#6cc4b0", str="#e48aa0", sym="#9aa8ff",
        ok="#4cc38a", warn="#f08a4b", panel="#3a3f47", panel2="#59606a", node="#1d232c",
    ),
}


def svg(w, h, body, t, extra_style="", card=True):
    frame = (f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="14" '
             f'fill="{t["card"]}" stroke="{t["line"]}"/>') if card else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>
  .mono {{ font-family: {MONO}; }}
  .sans {{ font-family: {SANS}; }}
  .serif {{ font-family: {SERIF}; }}
  {extra_style}
</style>
{frame}
{body}
</svg>
"""


def text_lines(x, y, lines, size, lh, fill, cls="sans", weight=400):
    out = []
    for i, ln in enumerate(lines):
        out.append(
            f'<text x="{x}" y="{y + i*lh}" class="{cls}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}">{escape(ln)}</text>'
        )
    return "\n".join(out)


# ---------------------------------------------------------------- header
def header(t):
    W, H = 880, 260
    c = {"p": t["paren"], "k": t["key"], "s": t["str"], "y": t["sym"], "i": t["ink"]}
    code = [
        [("p", "("), ("y", "defvar "), ("i", "*mashrufa*")],
        [("i", "  "), ("p", "'("), ("k", ":based-in  "), ("s", '"Toronto"')],
        [("i", "    "), ("k", ":studying  "), ("s", '"computer science"')],
        [("i", "    "), ("k", ":into      "), ("p", "("), ("i", "robotics  vla-models")],
        [("i", "                "), ("i", "computer-vision"), ("p", ")))")],
    ]
    x0, y0, lh = 372, 82, 27
    rows = []
    for i, toks in enumerate(code):
        spans = "".join('<tspan fill="%s">%s</tspan>' % (c[k], escape(s)) for k, s in toks)
        rows.append(f'<text x="{x0}" y="{y0 + i*lh}" class="mono" font-size="16" xml:space="preserve">{spans}</text>')
    body = f"""
<rect x="340" y="32" width="1" height="{H-64}" fill="{t['line']}"/>
<text x="40" y="72" class="mono" font-size="13" letter-spacing="2" fill="{t['faint']}">HELLO, I'M</text>
<text x="38" y="124" class="serif" font-size="46" fill="{t['ink']}">Mashrufa</text>
<text x="38" y="172" class="serif" font-size="46" fill="{t['ink']}">Orchi</text>
<text x="40" y="208" class="sans" font-size="15" fill="{t['soft']}">Teaching machines to see, understand</text>
<text x="40" y="230" class="sans" font-size="15" fill="{t['soft']}">and act in the real world.</text>
{''.join(rows)}
"""
    return svg(W, H, body, t)


for name, t in THEMES.items():
    (OUT / f"header-{name}.svg").write_text(header(t), encoding="utf-8")


# ---------------------------------------------------------------- toolbox
def toolbox(t):
    W, H = 880, 270
    cx = 440
    groups = {"lang": t["sym"], "vision": t["key"], "data": t["str"], "web": t["paren"]}
    # rows from the top (furthest out of the box) down to just above the lid
    rows = [
        (78,  [("python", "lang"), ("typescript", "lang"), ("javascript", "lang"), ("java", "lang"),
               ("c", "lang"), ("c++", "lang"), ("common lisp", "lang")]),
        (128, [("react", "web"), ("next.js", "web"), ("tailwind", "web"), ("mongodb", "web"),
               ("prolog", "lang"), ("sql", "lang")]),
        (176, [("opencv", "vision"), ("mediapipe", "vision"), ("medsam", "vision"),
               ("numpy", "data"), ("pandas", "data")]),
    ]
    cw, pad, gap = 7.4, 22, 12

    def chip(x, y, label, color):
        w = len(label) * cw + pad
        ang = (x - cx) / 32          # tilt outward, like they're spilling out
        y = y + ((x - cx) / 250) ** 2 * 26  # outer chips sit lower: a fan
        return (f'<g transform="rotate({ang:.1f} {x:.0f} {y:.0f})">'
                f'<rect x="{x - w/2:.0f}" y="{y - 14:.0f}" width="{w:.0f}" height="28" rx="14" '
                f'fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-opacity="0.7"/>'
                f'<text x="{x:.0f}" y="{y + 4.5:.0f}" class="mono" font-size="12.5" fill="{color}" '
                f'text-anchor="middle">{escape(label)}</text></g>')

    chips = []
    for y, items in rows:
        widths = [len(l) * cw + pad for l, _ in items]
        total = sum(widths) + gap * (len(items) - 1)
        x = cx - total / 2
        for (label, g), w in zip(items, widths):
            chips.append(chip(x + w / 2, y, label, groups[g]))
            x += w + gap

    box = t["paren"]
    body = f"""
<path d="M352 238 L528 238 L548 206 L332 206 Z" fill="{box}" opacity="0.55"/>
<path d="M410 206 v-8 a6 6 0 0 1 6 -6 h48 a6 6 0 0 1 6 6 v8" fill="none" stroke="{box}" stroke-width="5" opacity="0.55"/>
{''.join(chips)}
<rect x="340" y="236" width="200" height="62" rx="8" fill="{box}"/>
<rect x="340" y="236" width="200" height="12" rx="4" fill="{t['card']}" opacity="0.18"/>
<rect x="428" y="256" width="24" height="12" rx="3" fill="{t['card']}" opacity="0.45"/>
<g class="mono" font-size="12">
  <circle cx="610" cy="258" r="4" fill="{groups['lang']}"/><text x="620" y="262" fill="{t['soft']}">languages</text>
  <circle cx="710" cy="258" r="4" fill="{groups['vision']}"/><text x="720" y="262" fill="{t['soft']}">vision</text>
  <circle cx="610" cy="282" r="4" fill="{groups['data']}"/><text x="620" y="286" fill="{t['soft']}">data</text>
  <circle cx="710" cy="282" r="4" fill="{groups['web']}"/><text x="720" y="286" fill="{t['soft']}">web</text>
</g>
"""
    return svg(W, H, f'<g transform="translate(0,-40)">{body}</g>', t, card=False)


for name, t in THEMES.items():
    (OUT / f"toolbox-{name}.svg").write_text(toolbox(t), encoding="utf-8")

print("wrote", sorted(p.name for p in OUT.iterdir()))
