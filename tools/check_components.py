"""Tight Surface component check.

Renders every design-system/components/*/preview.html in the Night and Day themes at
1000 / 390 / 320 px and checks what the QA list asks of the system itself:

  - text contrast against the real background (>= 4.5:1, >= 3:1 at 24px+)
  - no horizontal overflow (the fixed-size Cover card is exempt)
  - no visible text under 12px (brand mark and nav numbers at 11px are documented exceptions)
  - axe-core: zero violations (wcag2a/aa, wcag21aa, wcag22aa, best-practice), when installed
  - icons: every <symbol> in a preview is copied verbatim from design-system/icons/sprite.svg
    (Lucide), the Lucide license line sits above it, and every <use href="#i-..."> points at
    a symbol defined in the same preview
  - the page checks that apply to one component (tools/page_check.py): placeholder text,
    generic button copy, visible field labels and placeholder contrast, one primary action
    per group, and boxes in one row aligned at the top. Links to "#" are fine in previews.

Usage:  pip install playwright && python3 -m playwright install chromium
        npm install            # optional, adds axe-core
        python3 tools/check_components.py [--shots]   # exit 1 on any failure
"""
import os, re, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import page_check

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DS = os.path.join(ROOT, "design-system")
AXE_PATH = os.path.join(ROOT, "node_modules", "axe-core", "axe.min.js")
SHOTS = os.path.join(ROOT, "tools", "out")

PAGE_CHECKS = ["placeholder", "button-copy", "field-label", "primary", "row-align"]
THEMES = [None, "day"]                      # None = Night (the default on :root)
WIDTHS = [1000, 390, 320]
OVERFLOW_EXEMPT = {"Cover"}                 # 960 x 288 gallery cover, fixed by design
SMALL_OK = re.compile(r"\b(brand-mark|n)\b")  # 11px brand mark and nav numbers

# per-text contrast against the composited background (opacity and translucent layers included)
CONTRAST_JS = r'''
() => {
  const parse = s => { const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return [p[0],p[1],p[2],p.length>3?p[3]:1]; };
  const srgb = s => { if (s.startsWith('color(srgb')) { const p=s.match(/color\(srgb ([^)]+)\)/)[1].split(/[ \/]+/).map(Number); return [p[0]*255,p[1]*255,p[2]*255,p.length>3?p[3]:1]; } return parse(s); };
  const lin = c => { c/=255; return c<=0.04045? c/12.92 : Math.pow((c+0.055)/1.055,2.4); };
  const L = c => 0.2126*lin(c[0])+0.7152*lin(c[1])+0.0722*lin(c[2]);
  const over = (top, under) => { const a=top[3]; return [top[0]*a+under[0]*(1-a), top[1]*a+under[1]*(1-a), top[2]*a+under[2]*(1-a), 1]; };
  const bgOf = el => { const layers=[]; let e=el; while (e) { const c=srgb(getComputedStyle(e).backgroundColor); if (c && c[3]>0) { layers.push(c); if (c[3]>=1) break; } e=e.parentElement; }
    let base=[255,255,255,1]; if (!layers.length || layers[layers.length-1][3]<1) base = srgb(getComputedStyle(document.body).backgroundColor) || base;
    for (let i=layers.length-1;i>=0;i--) base=over(layers[i],base); return base; };
  const out=[];
  for (const el of document.querySelectorAll('body *')) {
    const own=[...el.childNodes].some(n=>n.nodeType===3 && n.textContent.trim());
    if (!own) continue; const cs=getComputedStyle(el); if (cs.visibility==='hidden'||el.closest('.sr-only')) continue;
    const r=el.getBoundingClientRect(); if (!r.width||!r.height) continue;
    let fg=srgb(cs.color); if (!fg) continue; const op=parseFloat(cs.opacity); const bg=bgOf(el); fg=over([fg[0],fg[1],fg[2],fg[3]*op],bg);
    const a=L(fg), b=L(bg); const ratio=(Math.max(a,b)+0.05)/(Math.min(a,b)+0.05);
    const size=parseFloat(cs.fontSize), bold=parseInt(cs.fontWeight)>=700;
    const need = (size>=24 || (bold && size>=18.66)) ? 3 : 4.5;
    out.push({text:el.textContent.trim().slice(0,24), cls:el.className && el.className.baseVal===undefined ? el.className : '', size, ratio:+ratio.toFixed(2), need, transparent: cs.color.includes('rgba(0, 0, 0, 0)')});
  }
  return out;
}'''

OVERFLOW_JS = r"""() => {
  const W = document.documentElement.clientWidth, out = [];
  for (const e of document.querySelectorAll('#wrap *')) {
    const cs = getComputedStyle(e); if (cs.position === 'fixed' || cs.visibility === 'hidden') continue;
    const r = e.getBoundingClientRect(); if (!r.width) continue;
    let q = e.parentElement, scrolls = false;
    while (q && q.id !== 'wrap') { if (getComputedStyle(q).overflowX !== 'visible') { scrolls = true; break; } q = q.parentElement; }
    if (!scrolls && r.right > W + 1) out.push(e.tagName.toLowerCase() + '.' + (typeof e.className === 'string' ? e.className : ''));
  }
  return { sw: document.documentElement.scrollWidth, W, out: out.slice(0, 4) };
}"""

SMALL_JS = r"""() => {
  const out = [], w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let t;
  while ((t = w.nextNode())) {
    const p = t.parentElement; if (!p || !t.nodeValue.trim() || p.closest('script,style,.sr-only')) continue;
    const s = getComputedStyle(p); if (s.display === 'none' || s.visibility === 'hidden' || !p.getBoundingClientRect().width) continue;
    const fs = parseFloat(s.fontSize); if (fs < 11.95) out.push([fs, String(p.className || p.tagName), t.nodeValue.trim().slice(0, 16)]);
  }
  return out;
}"""

SYMBOL_RE = re.compile(r'<symbol id="([^"]+)"[\s\S]*?</symbol>')


def icon_problems(comps):
    """Static check: preview sprites must be exact copies of the canonical Lucide sprite."""
    sprite = open(os.path.join(DS, "icons", "sprite.svg"), encoding="utf-8").read()
    canon = {m.group(1): m.group(0) for m in SYMBOL_RE.finditer(sprite)}
    out = []
    for c in comps:
        html = open(os.path.join(DS, "components", c, "preview.html"), encoding="utf-8").read()
        defined = {}
        for m in SYMBOL_RE.finditer(html):
            sid = m.group(1); defined[sid] = m.group(0)
            if sid not in canon:
                out.append(f"icon · {c} · symbol {sid} is not in icons/sprite.svg")
            elif m.group(0) != canon[sid]:
                out.append(f"icon · {c} · symbol {sid} differs from icons/sprite.svg")
        if defined and "@license lucide-static v1.71.0 - ISC" not in html:
            out.append(f"icon · {c} · the Lucide license line is missing above the sprite")
        for ref in sorted(set(re.findall(r'href="#(i-[a-z0-9-]+)"', html))):
            if ref not in defined:
                out.append(f"icon · {c} · #{ref} is used but not defined in the preview")
    return out


AXE_JS = r"""async () => {
  const r = await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a','wcag2aa','wcag21aa','wcag22aa','best-practice'] },
    rules: { 'page-has-heading-one': { enabled: false }, 'landmark-one-main': { enabled: false }, 'region': { enabled: false } } });
  return r.violations.map(v => v.id + ' (' + v.nodes.length + ') ' + v.nodes.slice(0, 2).map(n => n.target.join(' ')).join(', '));
}"""


def page(theme, ground, width, preview):
    tokens = open(os.path.join(DS, "tokens.css"), encoding="utf-8").read()
    bundle = open(os.path.join(DS, "components", "bundle.css"), encoding="utf-8").read()
    bundle = re.sub(r"^@import url\([^)]*\);\s*", "", bundle)   # no network fonts; fallbacks are fine for checks
    attr = f' data-theme="{theme}"' if theme else ""
    bg = "var(--panel)" if ground == "panel" else "var(--void)"
    return (f'<!doctype html><html lang="zh-CN"{attr}><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1"><title>preview</title>'
            f"<style>{tokens}</style><style>{bundle}</style></head>"
            f'<body style="margin:0;background:{bg}"><main id="wrap" style="max-width:{width}px">{preview}</main></body></html>')


def main():
    shots = "--shots" in sys.argv
    axe = open(AXE_PATH, encoding="utf-8").read() if os.path.exists(AXE_PATH) else None
    comps = sorted(d for d in os.listdir(os.path.join(DS, "components"))
                   if os.path.isfile(os.path.join(DS, "components", d, "preview.html")))
    problems = icon_problems(comps)
    if shots: os.makedirs(SHOTS, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for theme in THEMES:
            tname = theme or "night"
            for ground in ["void", "panel"]:
                for w in WIDTHS:
                    if ground == "panel" and w != 1000: continue
                    pg = b.new_page(viewport={"width": w, "height": 700})
                    pg.emulate_media(reduced_motion="reduce")
                    for c in comps:
                        html = open(os.path.join(DS, "components", c, "preview.html"), encoding="utf-8").read()
                        pg.set_content(page(theme, ground, w, html), wait_until="load")
                        where = f"{c} · {tname} · {ground} · {w}px"
                        for x in pg.evaluate(CONTRAST_JS):
                            if x["ratio"] < x["need"] and not x["transparent"]:
                                problems.append(f"contrast {x['ratio']}:1 < {x['need']} · {where} · {x['cls'] or '-'} “{x['text']}”")
                        if ground == "void":
                            for f in page_check.run(pg, PAGE_CHECKS, root="#wrap", links=False):
                                problems.append(f"{f['check']} · {where} · {f['sel']} “{f['text']}” · {f['msg']}")
                            o = pg.evaluate(OVERFLOW_JS)
                            if c not in OVERFLOW_EXEMPT and (o["sw"] > o["W"] or o["out"]):
                                problems.append(f"overflow · {where} · scrollWidth {o['sw']} · {o['out']}")
                            for fs, cls, text in pg.evaluate(SMALL_JS):
                                if not SMALL_OK.search(cls):
                                    problems.append(f"text {fs}px < 12px · {where} · {cls} “{text}”")
                            if axe and w in (1000, 390):
                                pg.add_script_tag(content=axe)
                                for v in pg.evaluate(AXE_JS):
                                    problems.append(f"axe · {where} · {v}")
                            if shots and w in (1000, 390):
                                pg.screenshot(path=os.path.join(SHOTS, f"{tname}-{w}-{c}.png"), full_page=True)
                    pg.close()
        b.close()
    seen = []
    for x in problems:
        if x not in seen: seen.append(x)
    for x in seen: print("FAIL", x)
    print(f"{len(comps)} previews · 2 themes · {len(WIDTHS)} widths · axe {'on' if axe else 'off (npm install to enable)'} · {len(seen)} problems")
    sys.exit(1 if seen else 0)


if __name__ == "__main__":
    main()
