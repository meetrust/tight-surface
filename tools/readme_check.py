"""Tight Surface README check: python3 readme_check.py README.md  (exit 1 on any error)."""
import re, sys
from urllib.parse import unquote

src = open(sys.argv[1], encoding='utf-8').read()
err, warn = [], []
CJK = '\u4e00-\u9fff\u3400-\u4dbf'
body = re.sub(r'^(```|~~~).*?^\1\s*$', '', src, flags=re.S | re.M)          # drop fenced code
heads = re.findall(r'^(#{1,6}) (.+?)\s*$', body, flags=re.M)

# 1 images: only functional badges
imgs = re.findall(r'!\[[^\]]*\]\(([^)\s]+)', body) + re.findall(r'<img[^>]*\bsrc="([^"]+)"', body)
for u in imgs:
    if not re.match(r'https://img\.shields\.io/|https://github\.com/[^/]+/[^/]+/actions/workflows/[^/]+/badge\.svg', u):
        err.append(f'image is not a badge: {u}')
for u in imgs:
    if 'img.shields.io' in u and not ('style=flat-square' in u and 'labelColor=111723' in u):
        err.append(f'badge must use style=flat-square&labelColor=111723: {u}')

# 2 markup GitHub strips or renders only on GitHub (code blocks and inline code are examples, not markup)
prose = re.sub(r'`[^`]*`', '', body)                                     # $`x`$ inline math becomes $$ here
for pat, why, where in [(r'<style|\sstyle=["\']', 'inline style', prose), (r'\sclass=["\']', 'class', prose),
                        (r'\sid=["\']', 'id', prose), (r'<(script|iframe|svg|span|font|picture|video|form|input)\b', 'disallowed tag', prose),
                        (r'^(```|~~~)\s*mermaid', 'Mermaid', src), (r'\$\$', 'math', prose)]:
    for m in re.finditer(pat, where, flags=re.M | re.I):
        err.append(f'{why}: {m.group(0).strip()}')

# 3 headings: one H1, every H2 is "中文 · English"
if sum(1 for h, _ in heads if h == '#') != 1:
    err.append('need exactly one H1')
for h, t in heads:
    if h == '##' and not re.fullmatch(rf'[^·]*[{CJK}][^·]* · [^·{CJK}]*[A-Za-z][^·{CJK}]*', t):
        err.append(f'H2 not "中文 · English": {t}')

# 4 in-page anchors resolve (GitHub slug: lowercase, keep word chars, - and spaces, spaces -> -)
slugs = {re.sub(r' ', '-', re.sub(r'[^\w\- ]', '', t.lower())) for _, t in heads}
for a in re.findall(r'\]\(#([^)]+)\)|href="#([^"]+)"', body):
    a = unquote(a[0] or a[1])
    if a not in slugs:
        err.append(f'broken anchor: #{a}')

# 5 text rules on visible prose
txt = re.sub(r'`[^`]*`', '\x02C\x02', body)                             # inline code -> marked placeholder
txt = re.sub(r'!\[[^\]]*\]\([^)]*\)', ' ', txt)                          # images
txt = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', txt)                      # links -> text
txt = re.sub(r'<(br|/?(div|p|li|td|th|tr|table|thead|tbody|details|summary))\b[^>]*>', '\n', txt)  # breaks
txt = re.sub(r'<[^>]+>', '', txt)                                        # inline tags vanish
txt = re.sub(r'https?://\S+', ' ', txt)
txt = re.sub(r'[ \t]*\|[ \t]*', '\n', txt)                                # table cell borders
txt = re.sub(r'[ \t]*·[ \t]*', '·', txt)                                  # " · " separators are fine
txt = re.sub(r'^(?:[ \t]*>)*[ \t]*(?:[-*+]|\d+\.)?[ \t]+', '', txt, flags=re.M)   # quote and list markers
FW = '\uff0c\u3002\u3001\uff1b\uff1a\uff01\uff1f\uff09\u300d\u201d\u300b'          # ，。、；：！？）」”》
FO = '\uff08\u300c\u201c\u300a'                                       # （「“《
for pat, why in [(rf'[{CJK}]\x02?[A-Za-z0-9]|[A-Za-z0-9]\x02?[{CJK}]', 'missing CJK-Latin space'),
                 (rf'[{CJK}][ \u00a0\u3000]+[{CJK}]', 'space between CJK characters'),
                 (rf'[^\s{FW}][ \u00a0]+[{FW}]|[{FW}][ \u00a0]+[^\s{FW}{FO}]|[{FO}][ \u00a0]+\S|[^\s{FO}{FW}\x02][ \u00a0]+[{FO}]', 'space next to full-width punctuation'),
                 (r'\u3000', 'ideographic space'),
                 (rf'[{CJK}][,;:!?()]|[,;:!?()][{CJK}]', 'half-width punctuation in Chinese'),
                 (rf'[{CJK}]"|"[{CJK}]', 'ASCII quote in Chinese'),
                 (r'[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F]', 'emoji or glyph icon')]:
    for m in re.finditer(pat, txt):
        err.append(f'{why}: …' + txt[max(0, m.start() - 8):m.end() + 8].replace(chr(10), ' ').replace(chr(2), '').strip() + '…')

# 6 every H2 section is bilingual; size
for sec in re.split(r'^## ', src, flags=re.M)[1:]:                       # code blocks count here
    name, rest = sec.split('\n', 1)
    if not re.search(rf'[{CJK}]', rest) or not re.search(r'\b[A-Za-z]{3,}\b.*\b[A-Za-z]{3,}\b', rest):
        err.append(f'section not bilingual: {name}')
if src.count('\n') > 150:
    warn.append(f'{src.count(chr(10))} lines; keep the README under about 150')

for e in err: print('ERROR', e)
for w in warn: print('WARN ', w)
print(f'{sys.argv[1]}: {len(err)} errors, {len(warn)} warnings')
sys.exit(1 if err else 0)
