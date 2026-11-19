# GitHub README

提交到 GitHub 的仓库，README.md 是访客最先看到的页面。它不在本系统的暗夜页面里显示，而是由 GitHub 渲染：底色跟随访客的浅色或深色主题，HTML 会被过滤，宽度在桌面约 880px、手机约 360px。所以 README 不复刻页面的视觉，只做到三件事：原生可读、双语对照、数据与页面一致。

## 为什么不放图片
两个已交付仓库都试过首屏大图（截图、AI 生成的横幅），最后全部撤掉，换成原生表格：
- 深色大图放在浅色主题的白底页面上很突兀；反过来也一样。
- 图里的文字不能选中、搜索和翻译，缩小显示后发虚，最小字号无法保证。
- 生成图会画错事实（把训练器写成推理工具、漏掉一门课、把课程放错轨道），每次都要逐字校对。
- 图片要随内容更新，否则很快和页面对不上；原生文字改一处就够了。

## 适用范围
- 仓库根目录的 `README.md`。GitHub 依次在 `.github/`、根目录、`docs/` 里找 README，所以其他两处不要再放 README，免得把根目录那份顶掉。
- `docs/` 下的 Markdown 手册不受本节的图片和 Mermaid 限制，仍按“图表实现”一节处理。

## 可以用的写法
- GitHub Flavored Markdown：标题、段落、列表、表格（含对齐）、标明语言的代码块、行内代码、链接、引用、任务列表、脚注。
- 提示块 `> [!NOTE]`、`[!TIP]`、`[!IMPORTANT]`、`[!WARNING]`、`[!CAUTION]`：全文最多两个，不连续使用，只写真正会影响操作的信息。
- 白名单 HTML，只用于 Markdown 做不到的结构：
  - `<div align="center">`：只用于标题区。
  - `<table>`、`<thead>`、`<tbody>`、`<tr>`、`<th>`、`<td>`：需要分组时用 `rowspan` / `colspan`，对齐用 `align`。
  - `<details>` + `<summary>`：折叠很长但只有少数人需要的内容。
  - `<sub>`、`<br>`、`<b>`、`<code>`、`<a href>`、`<kbd>`。
- HTML 块前后各空一行。HTML 块里面的 Markdown 不会被解析，链接和代码要写成 `<a href>`、`<code>`。

## 不能用的写法
- 内容图片：截图、横幅、插画、GIF、视频，以及按明暗主题切换的 `<picture>`。唯一的例外是下面的功能徽章。
- 会被 GitHub 过滤掉的写法：`<style>`、`style=""`、`class`、`id`、`<script>`、`<iframe>`、内联 `<svg>`、`<span>`、`<font>`、表单。
- 只有 GitHub 才会渲染的图形：Mermaid、`$…$` 数学公式。npm、PyPI、编辑器预览里会显示成源码。关系和流程改用表格或列表写。
- emoji 和字符图标（☰ ↗ ▶ ◆）。表示流程的“→”可以用。
- 手写的完整目录：GitHub 会根据标题自动生成目录（文件右上角的 Outline）。标题区只放不超过 5 个最常用的章节链接。
- 用 `&nbsp;`、多个 `<br>` 或空标题凑间距。

## 徽章：唯一允许的图片
- **功能徽章**：在线访问、部署状态（GitHub Actions 的 `badge.svg`），有许可证或版本号时再加对应徽章。放在标题区同一行，最多 3 个。
- **颜色标签**：表格里用来标层级或轨道颜色，写法固定为
  `https://img.shields.io/badge/<代号>-%20-<色值>?style=flat-square&labelColor=111723`。左侧深色底写代号，右侧色块取 `l1`–`l7` 的色值。不要用“彩色底 + 白字”，白字在亮绿、粉色、黄色上对比度不够。
- 所有 shields 徽章统一 `style=flat-square&labelColor=111723`；在线访问徽章的右侧用 `amber`（`ffb347`）。
- 每个徽章都写 alt 文本，并且旁边有文字说明它的含义，颜色不单独承担信息。

## 结构
按下面的顺序写，没有内容的节可以省略，不要调换顺序：

1. **标题区**（`<div align="center">`）
   - eyebrow：`<sub><b>英文大写短语</b></sub>`，与页面上的 eyebrow 一致。
   - `# 中文名`：全文唯一的一级标题。下一行 `**English name**`。
   - 标语：中文一行，`<br>`，英文斜体一行。中文较长时用 `<br>` 拆成均衡的两行，不留单字孤行。
   - 徽章行，然后是章节导航：不超过 5 个短链接，用 `·` 分隔，写成“短中文 English”。
2. **亮点区**：用一张表呈现项目的标志性结构（例如“七级抽象阶梯”“七条知识轨道”），代替首屏大图。表下用 `<sub>` 写一两句读表说明，中英各一行。
3. **概览 · Overview**：中文一到两段，英文对应一到两段，然后是 3–5 个数字的统计表（数字加粗作表头，下面写口径）。
4. **页面内容 / 功能 · Contents**：章节或功能对照表。
5. **本地运行 · Run locally**：可以直接复制执行的命令，代码块标明语言。
6. **项目结构 · Structure**：代码块里的目录树，每行“路径 + 中文说明 · English”。
7. **数据说明 · Data notes**：数据来源、核对日期（`YYYY-MM-DD`）、估算口径。
8. **同系列 · Companion project**、**许可证 · License**：有才写。

README 写给使用者，不写维护者的事：部署流程、检查脚本的细节、页面截图预览、设计语言复述、技术实现细节都不放，需要时放到 `docs/`。全文一般不超过 150 行，标题区加亮点区在桌面上约一屏。

## 双语
- 二级标题写成 `## 中文 · English`，英文用句首大写（Run locally、Data notes）。
- 段落：先写中文段落，再写对应的英文段落，内容一一对应，不另加信息。
- 表格：表头写“中文 English”，单元格写 `中文<br><sub>English</sub>`。列表项同样处理。
- 仓库名、课程代号、命令、路径不翻译，用行内代码。
- 中文部分遵守原则 8 的排版规则：中英文之间加空格，全角标点，引号用“”，范围用 en dash。

## 表格
- 文字列不超过 4 列，纯数字的统计表可以到 5 列。项目再多就转置成“每行一项”，或者用 HTML 表加 `rowspan` 分组。7 列的课程表在 README 宽度下会把课名挤断成“深度学 / 习”，已经改成按轨道分行。
- 需要分组时用 `rowspan`，不要在每一行重复分组名。
- 层级或轨道的颜色用上面的颜色标签，放在第一列；同一个对象的颜色与页面一致。

## 链接
- 仓库内文件用相对路径（GitHub 推荐，克隆到本地也能用），外部页面写完整的 `https://` 地址，不放裸 URL。
- 链接文字说明去向（“在线访问”“课程档案”），不写“点这里”。表格里的代号可以链接到在线页面的对应锚点，仓库名链接到原仓库。
- 页内锚点按 GitHub 的规则生成：转小写，去掉字母、数字、`_`、`-`、空格以外的字符，每个空格换成 `-`（不合并）。所以 `概览 · Overview` 的锚点是 `#概览--overview`。

## 数据与生成
- README 里的数字、名称和链接都取自页面或项目的数据源，修改页面后同步 README；推荐用脚本生成，不手抄。
- 统计表的数字与页面首屏一致，合计等于明细之和，例如课程表的讲数和视频数加起来等于首屏的 219。

## 仓库信息（About）
- Description：一句话说明是什么，中文在前，英文在后。
- Website：填在线地址（GitHub Pages）。
- Topics：小写英文，单词之间用连字符，覆盖领域、技术和内容类型。

## 验收
提交前跑一遍下面的检查脚本（`python3 readme_check.py README.md`，有错误时退出码为 1），然后人工预览：用 github-markdown-css 的浅色和深色样式，在 880px 和 390px 两个宽度下各看一遍，重点看表格里的中文有没有被挤断、标题区有没有单字孤行。

```python
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
```

脚本只覆盖能机械判断的部分。下面几项要人工确认：
- 标语和导航没有单字孤行，表格里的中文没有被挤断。
- 英文是中文的对应翻译，没有多出或漏掉信息。
- 数字、名称、链接与在线页面一致，核对日期是最新的。
- 浅色和深色主题下徽章都清楚可读。
