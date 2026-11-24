"""Tight Surface page check.

Opens a finished page (a local HTML file or a served URL) in Chromium at 1440 / 390 / 320 px
and checks the QA items that need the whole page, not one component. The rules are Tight
Surface's own; the checks were suggested by Taste Skill's page checker (MIT) and Impeccable's
design rules (Apache-2.0). No code is taken from either.

  placeholder   leftovers that must not ship: lorem ipsum, TODO / TBD / FIXME, XXX, {{...}},
                待补充 / 待定 / 此处填写 ..., a bracketed stand-in noun ([公司名称], [Your name]),
                stand-in contacts (example.com, 555-01xx, a phone number of one repeated digit,
                1234567) and links to "#", "" or javascript:
  button-copy   a button whose whole label is generic: 了解更多 / 查看更多 / 更多 / 详情 /
                点击这里 / 提交 / 确定 / 确认 / 是 / 否 / OK / Submit / Learn more ...
  field-label   a form field named only by a placeholder, aria-label, title or a hidden
                <label>; placeholder text under 4.5:1 (Kumo Pagination's page-number box, named
                by labels.pageNumber, is the one exception)
  primary       more than one primary action (.act.primary, TsButton tone="primary") in one
                group: a form, dialog, fieldset or toolbar, else the nearest bordered or filled box
  row-align     boxes 40px or taller side by side in one row of a grid or flex container
                whose tops differ by more than 1px
  line-length   a line of running text wider than 75ch (about 42 CJK characters in Noto Sans SC);
                headings, captions, labels, table cells and code are not running text
  edge-gap      at 760px and narrower, text closer than 16px (sp-4) to the left or right edge
                of the screen (text in a sideways-scrolling table or code block is exempt)
  blank         a band across the page taller than 240px with no text, picture, control or
                drawn mark in it
  section-gap   (WARN) the space above a section heading differs from the page's median by
                more than 25%

Usage:  pip install playwright && python3 -m playwright install chromium
        python3 tools/page_check.py <page.html | URL> [--widths 1440,390,320] [--theme day] [--json]
Exit 1 when any check FAILs, 0 otherwise.
"""
import json, os, sys
from playwright.sync_api import sync_playwright

WIDTHS = [1440, 390, 320]
CHECKS = ["placeholder", "button-copy", "field-label", "primary", "row-align",
          "line-length", "edge-gap", "blank", "section-gap"]

# One function, run in the page. opts: {checks: [...], root: CSS selector, links: bool}
PAGE_JS = r"""
(opts) => {
  const want = new Set(opts.checks), out = [];
  const root = document.querySelector(opts.root || 'body') || document.body;
  const VW = document.documentElement.clientWidth, SY = window.scrollY;
  const CS = (e) => getComputedStyle(e);
  const add = (check, sev, el, msg) => out.push({ check, sev, sel: selOf(el), text: textOf(el), msg });
  const selOf = (el) => {
    if (!el || el.nodeType !== 1) return '';
    const parts = [];
    for (let e = el; e && e !== document.body && parts.length < 4; e = e.parentElement) {
      let s = e.tagName.toLowerCase();
      if (e.id) { parts.unshift(s + '#' + e.id); break; }
      const c = (typeof e.className === 'string' ? e.className : '').trim().split(/\s+/).filter(Boolean).slice(0, 2);
      if (c.length) s += '.' + c.join('.');
      parts.unshift(s);
    }
    return parts.join(' > ');
  };
  const textOf = (el) => (el && el.innerText ? el.innerText : el && el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 40);
  const SKIP = 'script, style, noscript, template, title, head';
  const CODE = 'code, pre, kbd, samp, textarea';
  const srOnly = (el) => {
    for (let e = el; e && e !== document.body; e = e.parentElement) {
      const c = CS(e);
      if (c.display === 'none' || c.visibility === 'hidden') return true;
      if (c.position === 'absolute' && (parseFloat(c.width) <= 1 || parseFloat(c.height) <= 1) && c.overflow !== 'visible') return true;
      if (c.clip && c.clip !== 'auto' && /rect\(0(px)?,? 0(px)?,? 0(px)?,? 0(px)?\)/.test(c.clip)) return true;
      if (c.clipPath && /inset\(50%/.test(c.clipPath)) return true;
    }
    return false;
  };
  const shown = (el) => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && !srOnly(el); };
  // colour
  const srgb = (s) => {
    if (!s) return null;
    let m = s.match(/color\(srgb ([^)]+)\)/); if (m) { const p = m[1].split(/[ \/]+/).map(Number); return [p[0] * 255, p[1] * 255, p[2] * 255, p.length > 3 ? p[3] : 1]; }
    m = s.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1];
  };
  const lin = (c) => { c /= 255; return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
  const lum = (c) => 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2]);
  const over = (t, u) => { const a = t[3]; return [t[0] * a + u[0] * (1 - a), t[1] * a + u[1] * (1 - a), t[2] * a + u[2] * (1 - a), 1]; };
  const bgOf = (el) => {
    const layers = []; for (let e = el; e; e = e.parentElement) { const c = srgb(CS(e).backgroundColor); if (c && c[3] > 0) { layers.push(c); if (c[3] >= 1) break; } }
    let base = [255, 255, 255, 1]; if (!layers.length || layers[layers.length - 1][3] < 1) base = srgb(CS(document.body).backgroundColor) || base;
    for (let i = layers.length - 1; i >= 0; i--) base = over(layers[i], base); return base;
  };
  const ratio = (fg, bg) => { const a = lum(fg), b = lum(bg); return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05); };
  const boxed = (el) => {
    const c = CS(el); const bc = srgb(c.borderTopColor), bg = srgb(c.backgroundColor);
    return (parseFloat(c.borderTopWidth) >= 1 && c.borderTopStyle !== 'none' && bc && bc[3] > 0) || (bg && bg[3] > 0) || c.backgroundImage !== 'none';
  };
  // text lines: [{el, r}] for every visible text fragment line
  const lines = [];
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    if (!n.textContent.trim()) continue;
    const el = n.parentElement; if (!el || el.closest(SKIP) || srOnly(el)) continue;
    const rg = document.createRange(); rg.selectNodeContents(n);
    for (const r of rg.getClientRects()) if (r.width > 0 && r.height > 0) lines.push({ el, r });
  }

  // ---- placeholder
  if (want.has('placeholder')) {
    const PH = /\bTODO\b|\bTBD\b|\bTBC\b|\bFIXME\b|\bX{3,}\b|\{\{[^}\n]{1,40}\}\}|待补充|待完善|待填写|待定(?!系数)|此处填写|这里填写|在此填写|在此输入|占位文字|占位文本|示例文字|示例文本/;
    const PH_WORD = /名称|姓名|名字|公司|品牌|客户|日期|时间|价格|金额|地址|电话|手机|邮箱|链接|网址|标题|图片|照片|作者|职位|\b(name|company|client|brand|date|price|city|address|e-?mail|phone|logo|photo|image|picture|title|link|url|number|author|role|product|headline|tagline|insert|placeholder)\b/i;
    const ADDR = /\bexample\.(?:com|org|net)\b|@example\.|\.example\b/i;
    const PHONE = /(?<!\d)555[-. ]?01\d\d(?!\d)|(?<!\d)1234567(?!\d)|(?<![\d.,])(\d)\1{6,}(?![\d.,])/;
    const STAND = new RegExp(ADDR.source + '|' + PHONE.source, 'i');
    const seen = new Set();
    for (const { el } of lines) {
      if (seen.has(el) || el.closest(CODE)) continue; seen.add(el);
      const t = [...el.childNodes].filter((x) => x.nodeType === 3).map((x) => x.textContent).join(' ');
      let m = t.match(PH) || t.match(/\blorem ipsum\b/i);
      if (!m) for (const b of t.matchAll(/[\[【［]([^\]】］\n]{1,24})[\]】］]/g)) if (PH_WORD.test(b[1])) { m = b; break; }
      if (m) { add('placeholder', 'FAIL', el, `占位文字“${m[0]}”留在页面上`); continue; }
      const s = t.match(STAND); if (s) add('placeholder', 'FAIL', el, `示例联系方式“${s[0]}”留在页面上`);
    }
    if (opts.links !== false) for (const a of root.querySelectorAll('a')) {
      const h = a.getAttribute('href');
      if (h === null) continue;
      if (h.trim() === '#' || h.trim() === '' || /^javascript:/i.test(h.trim())) add('placeholder', 'FAIL', a, `占位链接 href="${h}"：链接要指向真实地址或页内锚点，页内操作用 <button>`);
      else if (/^tel:/i.test(h.trim()) ? PHONE.test(h.replace(/[^\d]/g, '')) : ADDR.test(h)) add('placeholder', 'FAIL', a, `链接指向示例地址 ${h}`);
    }
  }

  // ---- button-copy
  if (want.has('button-copy')) {
    const BANNED = new Set(['了解更多', '查看更多', '阅读更多', '显示更多', '更多', '更多信息', '详情', '查看详情', '点击这里', '点击此处', '点此', '这里', '提交', '确定', '确认', '好', '好的', '是', '否',
      'learn more', 'read more', 'view more', 'show more', 'see more', 'more', 'more info', 'details', 'click here', 'here', 'find out more', 'discover', 'explore', 'go', 'submit', 'ok', 'okay', 'yes', 'no']);
    const norm = (s) => s.replace(/\s+/g, ' ').trim().replace(/[\s.…→›»>:：。!！]+$/u, '').trim().toLowerCase();
    for (const b of root.querySelectorAll('button, [role="button"], input[type="submit"], input[type="button"], input[type="reset"], .act, .btn, .fbtn')) {
      if (!shown(b)) continue;
      const label = b.matches('input') ? (b.value || '') : (b.innerText || '');
      const k = norm(label); if (!k) continue;
      if (BANNED.has(k)) add('button-copy', 'FAIL', b, `按钮文案“${label.trim()}”没有说明会发生什么：写成动词加对象，如“导出 CSV”“采用所选方案”`);
    }
  }

  // ---- field-label (+ placeholder contrast)
  if (want.has('field-label')) {
    const visText = (e) => e && shown(e) && (e.innerText || '').trim();
    for (const f of root.querySelectorAll('input, select, textarea, [role="textbox"], [role="combobox"], [role="searchbox"], [role="spinbutton"]')) {
      if (f.matches('input[type="hidden"], input[type="submit"], input[type="button"], input[type="reset"], input[type="image"]')) continue;
      if (f.closest('[aria-hidden="true"], [inert]')) continue;
      // Kumo Pagination's page-number box is part of the pager, named by labels.pageNumber (see kumo.md)
      if (f.closest('[data-slot="pagination-controls"]') && f.getAttribute('aria-label')) continue;
      const own = f.getBoundingClientRect();
      const isToggle = f.matches('input[type="checkbox"], input[type="radio"]');
      if (!isToggle && (own.width === 0 || own.height === 0 || srOnly(f))) continue;
      let named = false;
      for (const l of f.labels || []) {
        const clone = l.cloneNode(true); clone.querySelectorAll('input, select, textarea').forEach((x) => x.remove());
        if (shown(l) && clone.textContent.trim()) { named = true; break; }
      }
      if (!named) for (const id of (f.getAttribute('aria-labelledby') || '').split(/\s+/).filter(Boolean)) if (visText(document.getElementById(id))) { named = true; break; }
      if (!named) {
        const by = f.getAttribute('placeholder') ? `只有占位符“${f.getAttribute('placeholder')}”` : f.getAttribute('aria-label') ? `只有 aria-label“${f.getAttribute('aria-label')}”` : f.getAttribute('title') ? '只有 title' : (f.labels && f.labels.length) ? '<label> 被隐藏' : '没有任何名称';
        add('field-label', 'FAIL', f, `表单字段没有可见标签（${by}）：加一个看得见的 <label>，占位符只写示例`);
      }
      const ph = f.getAttribute('placeholder');
      if (ph && !isToggle) {
        const fg = srgb(getComputedStyle(f, '::placeholder').color), bg = bgOf(f);
        if (fg) { const r = ratio(over(fg, bg), bg); if (r < 4.5) add('field-label', 'FAIL', f, `占位文字对比度 ${r.toFixed(2)}:1，低于 4.5:1`); }
      }
    }
  }

  // ---- primary: one per group
  if (want.has('primary')) {
    const GROUP = 'form, dialog, [role="dialog"], [role="alertdialog"], fieldset, [role="toolbar"], [role="group"]';
    const groups = new Map();
    for (const p of root.querySelectorAll('.act.primary, [data-ts-variant="primary"]')) {
      if (!shown(p)) continue;
      let g = null;
      for (let e = p.parentElement; e && e !== document.body && e !== document.documentElement; e = e.parentElement) {
        if (e.matches(GROUP) || (boxed(e) && e.getBoundingClientRect().width < VW * 0.98)) { g = e; break; }
      }
      g = g || p.parentElement;
      if (!groups.has(g)) groups.set(g, []); groups.get(g).push(p);
    }
    for (const [g, ps] of groups) if (ps.length > 1) add('primary', 'FAIL', g, `同一组里有 ${ps.length} 个主操作（${ps.map(textOf).join('、')}）：每组只留一个，其余用默认样式`);
  }

  // ---- row-align
  if (want.has('row-align')) {
    for (const c of root.querySelectorAll('*')) {
      const cs = CS(c); const d = cs.display;
      const grid = /grid/.test(d), flexRow = /flex/.test(d) && /^row/.test(cs.flexDirection);
      if (!grid && !flexRow) continue;
      if (c.closest('svg, foreignObject')) continue;
      const kids = [...c.children].filter((k) => { const kc = CS(k); return kc.position !== 'absolute' && kc.position !== 'fixed' && shown(k) && k.getBoundingClientRect().height >= 40 && boxed(k); }).map((k) => ({ k, r: k.getBoundingClientRect() }));
      if (kids.length < 2) continue;
      const rows = [];
      for (const it of kids) {
        const row = rows.find((rw) => rw.some((o) => Math.min(o.r.bottom, it.r.bottom) - Math.max(o.r.top, it.r.top) > 8 && (it.r.left >= o.r.right - 1 || it.r.right <= o.r.left + 1)));
        if (row) row.push(it); else rows.push([it]);
      }
      for (const rw of rows) {
        if (rw.length < 2) continue;
        const tops = rw.map((o) => o.r.top), spread = Math.max(...tops) - Math.min(...tops);
        if (spread > 1) add('row-align', 'FAIL', c, `并排的 ${rw.length} 个盒子顶边相差 ${spread.toFixed(1)}px：同一行的卡片顶边对齐`);
      }
    }
  }

  // ---- line-length: a line is measured inside the block its text flows in (a flex or grid cell is
  // its own block, so a caption bar with a label at each end is two short lines, not one long one)
  if (want.has('line-length')) {
    const blockOf = (el) => { let e = el; while (e && e !== root && /^(inline|contents)$/.test(CS(e).display)) e = e.parentElement; return e; };
    const ctx = document.createElement('canvas').getContext('2d');
    const byBlock = new Map();
    for (const { el, r } of lines) { if (el.closest('svg')) continue; const b = blockOf(el); if (!byBlock.has(b)) byBlock.set(b, []); byBlock.get(b).push(r); }
    for (const [b, rs] of byBlock) {
      if (!b || b === root || b.matches('h1, h2, h3, h4, h5, h6, figcaption, label, legend, th, td, button, summary') || b.closest('table, nav, button, a.btn, figcaption, ' + CODE + ', [role="dialog"]')) continue;
      const c = CS(b), fs = parseFloat(c.fontSize) || 16;
      ctx.font = `${c.fontStyle} ${c.fontWeight} ${c.fontSize} ${c.fontFamily}`;
      const ch = ctx.measureText('0').width || fs * 0.55;
      const rows = [];
      for (const r of rs) {
        const row = rows.find((x) => Math.abs(x.top - r.top) < fs * 0.6);
        if (row) { row.left = Math.min(row.left, r.left); row.right = Math.max(row.right, r.right); } else rows.push({ top: r.top, left: r.left, right: r.right });
      }
      const w = Math.max(0, ...rows.map((x) => x.right - x.left));
      if (w / ch > 75.5) add('line-length', 'FAIL', b, `一行 ${Math.round(w / ch)}ch（约 ${Math.round(w / fs)} 个汉字）：正文每行不超过 75ch，给段落设 max-width: 75ch`);
    }
  }

  // ---- edge-gap (narrow screens only)
  if (want.has('edge-gap') && VW <= 760) {
    const scrolls = (el) => { for (let e = el; e && e !== document.body; e = e.parentElement) { const c = CS(e); if (c.overflowX !== 'visible' && e.scrollWidth > e.clientWidth + 1) return true; } return false; };
    const seen = new Set();
    for (const { el, r } of lines) {
      if (seen.has(el) || el.closest('[aria-hidden="true"]') || scrolls(el)) continue;
      const gap = Math.min(r.left, VW - r.right);
      if (gap < 15.5) { seen.add(el); add('edge-gap', 'FAIL', el, `文字距屏幕边缘只有 ${Math.max(0, gap).toFixed(0)}px：手机宽度下至少留 16px（sp-4）`); }
    }
  }

  // ---- content intervals (blank, section-gap)
  let items = null;
  const contentItems = () => {
    if (items) return items;
    items = lines.filter(({ el }) => CS(el).position !== 'fixed').map(({ r }) => ({ top: r.top + SY, bottom: r.bottom + SY }));
    for (const el of root.querySelectorAll('img, svg, canvas, video, iframe, picture, input, select, textarea, button, hr, *')) {
      const c = CS(el); if (c.position === 'fixed' || el.closest(SKIP)) continue;
      const r = el.getBoundingClientRect(); if (r.width < 2 || r.height < 1) continue;
      const media = el.matches('img, svg, canvas, video, iframe, picture, input, select, textarea, button, hr');
      if (!media && !(boxed(el) && r.width < VW * 0.95)) continue;
      if (srOnly(el)) continue;
      items.push({ top: r.top + SY, bottom: r.bottom + SY });
    }
    items.sort((a, b) => a.top - b.top);
    return items;
  };
  if (want.has('blank')) {
    const it = contentItems(); let cur = null, worst = null;
    for (const x of it) {
      if (cur && x.top - cur.bottom > (worst ? worst.h : 0)) worst = { h: x.top - cur.bottom, from: cur.bottom, to: x.top };
      if (!cur || x.top > cur.bottom) cur = { top: x.top, bottom: x.bottom }; else cur.bottom = Math.max(cur.bottom, x.bottom);
    }
    if (worst && worst.h > 240) {
      const y0 = window.scrollY; window.scrollTo(0, Math.max(0, worst.from + worst.h / 2 - innerHeight / 2));
      const el = document.elementFromPoint(VW / 2, worst.from + worst.h / 2 - window.scrollY) || document.body;
      window.scrollTo(0, y0);
      add('blank', 'FAIL', el, `页面 ${Math.round(worst.from)}–${Math.round(worst.to)}px 之间有 ${Math.round(worst.h)}px 高的空白，没有文字、图片、控件或数据标记`);
    }
  }
  if (want.has('section-gap')) {
    const heads = [...root.querySelectorAll('h2')].filter((h) => shown(h) && !h.closest('nav, aside, footer, dialog, [role="dialog"], header.nav'));
    const it = contentItems(), gaps = [];
    for (const h of heads.slice(1)) {
      const blk = h.closest('.sec-head, .sh') || h;
      const top = blk.getBoundingClientRect().top + SY;
      let prev = -Infinity; for (const x of it) if (x.bottom <= top + 1 && x.bottom > prev) prev = x.bottom;
      if (prev > -Infinity) gaps.push({ h, gap: top - prev });
    }
    if (gaps.length >= 3) {
      const s = gaps.map((g) => g.gap).sort((a, b) => a - b), med = s[Math.floor(s.length / 2)];
      for (const g of gaps) if (med > 0 && Math.abs(g.gap - med) > med * 0.25) add('section-gap', 'WARN', g.h, `章节上方间距 ${Math.round(g.gap)}px，与全页中位数 ${Math.round(med)}px 相差超过 25%`);
    }
  }
  return out;
}
"""


def run(page, checks, root="body", links=True):
    """Run the checks in an already loaded Playwright page; returns a list of findings."""
    return page.evaluate(PAGE_JS, {"checks": checks, "root": root, "links": links})


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__); sys.exit(0)
    target, widths, theme, as_json = None, WIDTHS, None, False
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--widths": widths = [int(x) for x in args[i + 1].split(",")]; i += 2; continue
        if a == "--theme": theme = args[i + 1]; i += 2; continue
        if a == "--json": as_json = True; i += 1; continue
        target = a; i += 1
    if not target:
        sys.exit("page_check: give a page file or URL")
    url = target if "://" in target else "file://" + os.path.abspath(target)
    if "://" not in target and not os.path.exists(target):
        sys.exit(f"page_check: {target} not found")
    report = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for w in widths:
            pg = b.new_page(viewport={"width": w, "height": 900 if w > 760 else 844})
            pg.emulate_media(reduced_motion="reduce")
            pg.goto(url, wait_until="load")
            if theme:
                pg.evaluate("t => document.documentElement.setAttribute('data-theme', t)", theme)
            pg.evaluate("() => document.fonts && document.fonts.ready")
            pg.wait_for_timeout(400)
            for f in run(pg, CHECKS):
                f["width"] = w; report.append(f)
            pg.close()
        b.close()
    seen, unique = set(), []
    for f in report:
        k = (f["check"], f["sel"], f["msg"])
        if k not in seen: seen.add(k); unique.append(f)
    if as_json:
        print(json.dumps(unique, ensure_ascii=False, indent=1))
    else:
        for f in unique:
            print(f"{f['sev']} {f['check']} · {f['width']}px · {f['sel']} “{f['text']}” · {f['msg']}")
        fails = sum(f["sev"] == "FAIL" for f in unique); warns = len(unique) - fails
        def mark(c):
            n = sum(f["check"] == c and f["sev"] == "FAIL" for f in unique)
            w = sum(f["check"] == c and f["sev"] == "WARN" for f in unique)
            return f"{c} " + (f"{n} FAIL" if n else f"{w} WARN" if w else "PASS")
        print(" · ".join(mark(c) for c in CHECKS))
        print(f"{target} · {'/'.join(map(str, widths))}px · {fails} FAIL · {warns} WARN")
    sys.exit(1 if any(f["sev"] == "FAIL" for f in unique) else 0)


if __name__ == "__main__":
    main()
