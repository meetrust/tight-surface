---
name: "tight-surface-ui"
description: "Build or review any UI, web page, dashboard or data visualization, or write the README.md of a repo pushed to GitHub, in 韩同学's Tight Surface design language: dark Night theme by default plus an opt-in light Day theme, single amber accent, info-first, native GitHub-renderable READMEs, with tokens, components and a QA checklist."
---

# Tight Surface UI

Use this skill for any interface, web page, artifact, dashboard, chart or front-end component, when reviewing one, and whenever you write or update the README.md of a repository that goes to GitHub (see GitHub README). The full reference (brand book, token table, 21 component previews, native chart rules, data-viz rules, interaction-state rules, GitHub README rules, Kumo adapter, QA checklist) is the Design System artifact "Tight Surface": https://claude.ai/artifact/8kSJvpj18PrfmX1ToQ3Wqk. When an artifacts tool can read it, read `project/README.md` first; otherwise this file is self-contained.

Write user-facing copy in Simplified Chinese unless asked otherwise.

## Principles (v2)
1. 信息优先: every visual encodes data (colour = layer/track, position = order, line style = required/optional). Every number traceable; totals must equal their parts; footer states the data-check date (YYYY-MM-DD).
2. 紧凑: 4px spacing scale only; same element type = same size (pill 26, micro tag 20, resource button 48, action button and filter 36, copy 28, nav link 40, back-to-top 44); app controls (inputs, selects, action buttons, tabs) are 36 by default and 26 when compact inside tables, toolbars or task rows; 40 is for navigation only and 48 for the `.btn` resource link only; labels nowrap + ellipsis; tabular-nums.
3. 平静: UI accent is only `amber` (current/focus/selected/table head/numbers) and `ice` (links). Data colours `l0`-`l7` never mean UI state. Borders over shadows; glow only on hover/current/milestone. One easing, one duration.
4. 具触感: hover lift 2px (`translateY(-2px)`) or slide 3-6px, border tints to the item colour; hover rules only inside `@media (hover: hover) and (pointer: fine)`, and in JS hover handlers only for `pointerType === "mouse"` (see Interaction states).
5. 可访问性: text >=4.5:1; focus ring 2px amber, offset 3px; `prefers-reduced-motion` disables all animation and smooth scroll; decorative icons `aria-hidden`, icon-only buttons get `aria-label`; never colour alone. Containers that scroll sideways (tables, code, wide figures) get `tabindex="0"`, `role="region"` and a page-unique `aria-label` while they overflow; value-only graphics (meters, ratings, meaningful swatches) get `role="img"` + `aria-label`, never `title` alone; an `aria-label` contains the visible text verbatim (put a space between adjacent code + name elements). In `forced-colors: active` (Windows contrast themes) anything painted with `background` vanishes: data marks get `forced-color-adjust: none`, mask icons `background: CanvasText` (`LinkText` inside links).
6. 同一系列，不同版式: tokens, fonts, accent, chips, buttons, icons, focus, motion and FIG numbering stay identical; page skeleton, hero, background texture, section-head style and signature figure may differ. Sibling pages credit each other in the footer.
7. 可验证: ship only after the QA checklist below passes, interaction states included (not only static screenshots).
8. 中文排版优先: space between CJK and Latin/digits; no space at all between two CJK characters or next to full-width punctuation, ideographic space (U+3000) included (需云 GPU, not 需 云 GPU; separate list items with " · " or punctuation, never with spaces); full-width punctuation in Chinese; quotes “”; ranges with en dash (8–12 h); `text-wrap: balance` on headings; no single-character orphan lines, no line starting with "/".
9. 原生实现优先: charts in web pages are native HTML/CSS with inline SVG for lines and shapes only; no Mermaid, Chart.js or ECharts by default, and no components built on them, such as Kumo's 6 chart components (see Charts: native first).
10. README 原生可读: a README.md pushed to GitHub uses only GitHub-renderable Markdown plus whitelisted HTML; no screenshots, banners or other content images (only functional badges and colour chips), no Mermaid or math; the project's signature structure is a native table instead of a hero image; bilingual (Chinese first); numbers and names match the page; run the checker before pushing (see GitHub README).

## Tokens (Night, the default — paste as :root)
```css
:root {
  color-scheme: dark;
  --void: #0a0d14; --panel: #111723; --panel-2: #172031;
  --ink: #e8edf5; --ink-2: #c3ccdb; --dim: #a3aec0; --faint: #7d8aa3; --muted: #56637b;
  --rule: #243049; --rule-2: #33425f;
  --amber: #ffb347; --on-amber: var(--void); --amber-ink: #ffd59a; --ice: #7cc8ff;
  --l0: #8b97ab; --l1: #7cc8ff; --l2: #a99bff; --l3: #ffd166; --l4: #ff9f5a; --l5: #ff6b6b; --l6: #4fd6a0; --l7: #ff7ad9;
  --good: var(--l6); --bad: var(--l5); --warn: var(--l4); --pop: var(--panel-2);
  --heat-1: #12304a; --heat-1-ink: #9fd4ff; --heat-2: #123a30; --heat-2-ink: #86ebc0; --heat-3: #3d3414; --heat-3-ink: #ffe08a;
  --heat-4: #4a2c16; --heat-4-ink: #ffbe8a; --heat-5: #4f1c24; --heat-5-ink: #ffa3aa;
  --code-bg: #070a10; --code-bar: #0d121c; --code-ink: #cdd7e6; --code-comment: #7a88a3; --inline-code-ink: #cfe9ff;
  --chart-label-bg: #0b1019; --chart-text: #c9d3e3; --nav-glass: rgba(10, 13, 20, .86); --selection: rgba(255, 179, 71, .35);
  --shadow-drawer: 30px 0 60px rgba(0, 0, 0, .5); --shadow-glow: 0 0 12px rgba(255, 179, 71, .45);
  --font-display: "Chakra Petch", "Noto Sans SC", "PingFang SC", sans-serif;
  --font-body: "Noto Sans SC", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", "Sarasa Mono SC", ui-monospace, Menlo, Consolas, monospace;
  --fs-2xs: 12px; --fs-xs: 13px; --fs-sm: 14px; --fs-base: 15px; --fs-body: 16px; --fs-lg: 18px; --fs-xl: 22px;
  --fs-2xl: clamp(26px, 3.4vw, 36px); --fs-hero: clamp(42px, 6.4vw, 72px);
  --sp-1: 4px; --sp-2: 8px; --sp-3: 12px; --sp-4: 16px; --sp-5: 24px; --sp-6: 32px; --sp-7: 48px; --sp-8: 64px; --sp-9: 96px;
  --r-sm: 8px; --r-md: 12px; --r-lg: 16px; --r-pill: 999px;
  --ease: cubic-bezier(.2, .7, .2, 1); --dur: .28s; --lift: translateY(-2px);
}
*, *::before, *::after { box-sizing: border-box; }   /* every size in this skill is the outer border-box size */
```
Google Fonts: `family=Chakra+Petch:wght@500;600;700&family=JetBrains+Mono:wght@400;600;700&family=Noto+Sans+SC:wght@400;500;700;900&display=swap`.
Night contrast: `ink` / `dim` / `faint` >=13.8 / 7.2 / 4.6 : 1 on all three surfaces, focus ring >=9.1:1, heat pairs >=7.2:1, code text 13.6:1 and comments 5.6:1. `muted` (3.0:1) is no longer used by any component; the “暂无” chip uses `faint`. Contrast is measured against each text's actual background: on the amber tint of `.btn.video` and on tinted graph nodes small text uses `dim`, not `faint` (faint drops to 4.2–4.4:1 there).
Status and layers: `warn` is an alias of `l4` and follows the `good` / `bad` rules (always with an icon or text, 12% tint for chips and banners on `void` or `panel`; Day `warn` on a 12% tint over `panel-2` is only 4.49:1, so keep status chips and banners off `panel-2`). Info states use neutral `ink-2` text on an `ink` 6% tint, never `ice`, which only means clickable. Floating layers (dropdowns, popovers, toasts, inputs) use `pop` with a `rule-2` border and no shadow; the dialog scrim is `void` at 80%.

## Day theme (light, opt-in)
Night stays the default on `:root`; existing pages need no change. Switch a page with `<html data-theme="day">`: components, sizes, fonts, spacing and motion are identical, only colours change. Use Day for dev tools, dense forms and tables, long-read docs and print; keep Night for immersive data stories and the pages already delivered. One theme per page; if a page offers both, pick the initial one from `prefers-color-scheme` and add a toggle with `aria-pressed` that only changes `data-theme`.
```css
[data-theme="day"] {
  --void: #f4f6f9; --panel: #ffffff; --panel-2: #eef1f6;
  --ink: #121826; --ink-2: #2f3a4d; --dim: #4a5568; --faint: #5b6679; --muted: #637086;
  --rule: #dfe4ec; --rule-2: #c3cbd8;
  --amber: #995300; --on-amber: var(--panel); --amber-ink: #7a4100; --ice: #0a5fae;
  --l0: #56637a; --l1: #0a5fae; --l2: #6248cc; --l3: #7a5a00; --l4: #a8430c; --l5: #b62a36; --l6: #096b4a; --l7: #a82d83;
  --good: var(--l6); --bad: var(--l5); --warn: var(--l4); --pop: var(--panel);
  --heat-1: #e2eefa; --heat-1-ink: #0b4475; --heat-2: #dff3e9; --heat-2-ink: #0a5639; --heat-3: #fbf0cc; --heat-3-ink: #5e4600;
  --heat-4: #fde5d2; --heat-4-ink: #7f3608; --heat-5: #fbdfe1; --heat-5-ink: #8e1b2a;
  --code-bg: #f2f5f9; --code-bar: #e8ecf2; --code-ink: #1d2738; --code-comment: #596579; --inline-code-ink: #0b4f8c;
  --chart-label-bg: #ffffff; --chart-text: #2a3446; --nav-glass: rgba(244, 246, 249, .86); --selection: rgba(255, 179, 71, .35);
  --shadow-drawer: 30px 0 60px rgba(18, 24, 38, .16); --shadow-glow: 0 0 12px rgba(153, 83, 0, .35);
}
html[data-theme="day"] { color-scheme: light; }
```
- Same layer meaning: `void` page, `panel` cards / charts / tables, `panel-2` heads and captions. Cards are white on #f4f6f9 and separated by 1px `rule`; still no shadows.
- `ink` / `ink-2` / `dim` / `faint` are >=4.5:1 on all three surfaces (faint 5.1 on panel-2). `amber` and `ice` are dark versions usable as text (>=5.1:1); solid amber takes white text via `on-amber`.
- `l0`-`l7` keep hue and order and are dark enough for 12px text, including chips on a 12% tint over `void` or `panel` (>=4.6:1; Day `l4` on a 12% tint over `panel-2` drops to 4.49:1); the same object keeps the same index in both themes. Heat cells are light fill + dark ink (>=7.1:1). Code blocks are light.
- Never hard-code `#fff` or dark `rgba()` in a component: use tokens, and for alpha `color-mix(in srgb, var(--token) N%, transparent)`. Stat numbers and element-tile codes are `ink` in Day. When a component must differ, scope it `:where([data-theme="day"]) .x { … }` so state rules (hover, `.ok`, `.video`) keep winning.
- Exceptions: no amber → #ffd9a0 gradient title in Day (solid `amber`); background textures use Day `ice` and stay <=0.11 opacity; glows are weaker.
- QA: run checklist groups 1-6 in Day with Day values; on a page offering both themes, switching `data-theme` must not change any size, layout or truncation.

## Typography
- display (Chakra Petch): numbers, eyebrows (12px, 600, uppercase, letter-spacing .18em, amber), figure labels "FIG.0n · 标题" (13px, .1em), table heads (12px, amber), stats (26-30px, 700, white in Night, `ink` in Day).
- body (Noto Sans SC): all Chinese text; h1/h2 weight 900; body 16px / line-height 1.8.
- Chinese uses only the loaded weights 400 / 500 / 700 / 900 (a 600 renders as 700): body, option text, tabs and chips 400; field labels, action and filter buttons 500; selected items 700; headings 900. Never set Chinese text in the display font with letter-spacing: eyebrows in Chakra Petch are English uppercase.
- mono (JetBrains Mono): repo/course codes, code, relation chips, TOC sub-items.
- Visible text never below 12px (11px only for nav numbers and brand mark); inline `code` is .86em but never below 12px (`max(.86em, 12px)`).

## Layout
- Two skeletons: handbook (272px sticky left TOC, drawer at <=1024px) or atlas (60px sticky glass top nav, max width 1160px). Pick one per page.
- Background: one texture per page — 40px grid lines (ice 4%; Day 6%) or 24px dot grid (ice 11%) — plus two soft radial glows.
- Global `*, *::before, *::after { box-sizing: border-box; }`: pill 26, button 48, TOC 272 and every other size here are outer sizes including padding and border.
- Grid columns `minmax(0, 1fr)` and `min-width: 0`, also in the mobile single-column override (a bare `1fr` lets a wide table's min-content stretch the column; it shows only at 320px); the page never scrolls horizontally down to 320px (WCAG 1.4.10); tables and code scroll inside their own container; sticky first table column.
- Copy buttons try `navigator.clipboard.writeText` and fall back to a hidden textarea + `document.execCommand("copy")` (embeds often block the async API); only when both fail show “复制失败”.
- Breakpoint 760px is shared; cards stack to one column there.

## Components (class names)
- Section head: `.sec-head` (88px outlined amber numeral + eyebrow + h2 + `.sub`) or `.sh` (index bar). Numbers continuous, sources section numbered too.
- Figure: `.fig` > `figcaption` (`<b>FIG.0n · 标题</b>` + reading hint) + `.fig-body` (padding 24px) + optional `.fig-foot` (line-style legend).
- Legend: HTML `.fig-key` (12px swatch + name + value); hide chart-library legends.
- Buttons: `.btn` 48px resource link only (icon 15px + two-line label, both lines nowrap + ellipsis, + 13px external arrow), `.btn.video` (amber tint, max one per card), `.btn.off` (dashed, faint, `aria-disabled`, keeps its place: "暂无公开链接"); `.act` 36px action button for in-page actions (`.act.primary` amber tint like `.btn.video`, max one per group (on hover the border turns solid `amber` / `bad` and the 11% tint stays, as in Kumo's TsButton, which keeps Day text above 4.5:1); `.act.danger` `bad` tint; `.act.ghost` no border for skip / cancel; `.act.sm` 26px in table and task rows; `disabled` or `aria-disabled` = dashed `rule` + `faint`; an icon before the label is 15px, 12px in `.act.sm`); `.fbtn` 36px pill with `aria-pressed`, `.copy` 28px. Button heights are only 48 / 36 / 28 / 26. Never a solid-amber primary button: solid amber + `on-amber` means selected (filters, checkbox, radio, switch, date).
- Chips 26px: `.lvl` (layer, 12% tint), `.rel` (mono relation "A → B"), `.tk` (dot + track), `.st` (video / code / none; `.st.ok` / `.st.bad` for task status with i-check / i-x), `.k-chip` (MECHANISM / HIGHLIGHTS / OUTPUT), `.specs` key-value strip; 20px micro tags inside graph nodes.
- Stats: `.stat` cards or `.datastrip`; 3-5 numbers, each with unit and scope.
- Table: `.tbl` with amber heads, mono row heads in the row colour, optional heat cells, ★ ratings only with `aria-label`.
- Cards: `.mod` module card (3px glowing top bar in `--c`, 46px index, mono title, specs), `.el` periodic tile (124px rows), `.calib-card` fact check (struck-through myth + fact).
- Empty state: dashed box, two sentences (what happened + how to recover), `role="status"`.
- Agent UI (group "Agent" in the Design System):
  - ThinkingTrace `<details class="trace">`: 36px summary (`.trace-dot` + `.trace-title` 思考中 / 已思考 + `.trace-time` "12.4 s" + `.trace-meta` + `.trace-caret`, i-chevron-right rotated 90° when open), steps `<ol class="trace-steps">` with a `.tk` type chip in a 64px column (two-character names: step `l0`, search `l1`, reasoning `l2`, code `l6`), one sentence and a time; step times sum to the total. Running: `data-state="running"` + `open`, pulsing amber dot; done: collapsed, `faint` dot. Announce completion once in an existing `role="status"`, never `aria-live` on the summary.
  - ToolCall: `.tools-sum` ("4 次工具调用 · 2 条消息") + `<ul class="tools">` of 26px mono `<button class="tool">` pills: status icon (i-check `good`, i-x `bad`, running = `data-state="running"`, dashed + amber dot) + `.sr-only` status text + `.nm` in `--c` by tool kind + `.arg` ("→ file", ellipsis) + `.ms` time; `aria-expanded` + `aria-controls` open a `.tool-detail` CodeBlock.
  - TaskRow `<ol class="tasks">` > `<li class="task" data-state="done|running|failed|queued">`: `.task-no` (amber when running) + `.task-main` (`.task-title`, `.task-note`, optional 8px amber `.task-bar` with `--v` and `role="progressbar"`) + `.task-side` status chip (`.st.ok`, `.st.v` "进行中 68%", `.st.bad`, `.st.no`) and a `.act.sm` retry on failure; at <=760px `.task-side` moves under the note so the title keeps the full row.
  - ApprovalCard `<form class="approve">`: eyebrow NEEDS APPROVAL + `.approve-step` "1 / 3", `.approve-q` (18px 700), `<fieldset class="approve-opts">` of `<label class="opt">` native radios (name, effect, `.opt-conf` confidence; checked = amber radio + 9% amber card), footer `.act.ghost` skip + `.act` + `.act.primary` confirm (`.act.danger` when the decision deletes data or spends money); 2–4 options, the recommended one first and preselected.
- Back to top: 44px square, 18px i-arrow-up, appears after ~900px.
- Set the item colour with `style="--c: var(--lN)"`; components derive border (45%), tint (12%), gradient and glow from it.

## Kumo (app controls)
For app controls in React (forms, menus, dialogs, toasts, date pickers, sidebars, tabs, data tables) use Cloudflare Kumo (`@cloudflare/kumo`, pinned to 2.18.1) plus the adapter from the Design System: `project/kumo/` and its section “Kumo 适配”, which also lists every token mapping and the upgrade steps. Content components (SectionHead, Figure, DataTable, ModuleCard, Agent UI) stay native.
- Entry CSS: load the Google Fonts URL on line 1, then `@layer ts-important, theme, base, ts-base, components, utilities, ts-kumo;`, `@import "tailwindcss"`, `@import "@cloudflare/kumo/styles/tailwind"`, `@source` on Kumo's dist, `tokens.css` unlayered, `bundle.css` in `layer(ts-base)` with its own font `@import` removed, then `kumo-tight-surface.css`. Theme attributes: Night `data-mode="dark"`, Day `data-theme="day" data-mode="light"`, switched by `applyTheme()` from `kumo/theme.ts`; the app root gets `className="isolate"`.
- Sizes: Kumo xs 20 / sm 26 / base 36 / lg 40 = `h-tag` / `h-pill` / `h-filter` / `h-nav-link`; base by default, sm in tables and toolbars, lg for navigation only.
- Write buttons with the adapters: `TsButton tone="default|primary|danger|ghost"` (never Kumo `variant="primary"`, `destructive` or `secondary-destructive`), `FilterButton` (`aria-pressed`), `ResourceButton` (48px two-line link), `Chip c="l0"`–`"l7"`; Badge always with an explicit variant (the default is a solid inverted primary), and only success, warning, error, info, secondary. Icons come from `lucide-react` (`icon={<Download />}` under the root `<LucideProvider className="i">`); the adapter sizes them 15px in buttons and 12px in `TsButton size="sm"`, and the ESLint config rejects `@phosphor-icons/react` and other icon packages in app code. Put Kumo Table inside `<div class="tbl">`. Pass Chinese UI text everywhere (DatePicker `locale={zhCN}`, Pagination `text`). Do not pass className that changes colour, weight or focus; add a `data-ts-variant` to the adapter instead.
- Never import Chart, TimeseriesChart, SankeyChart, BubbleMap, ChoroplethMap, GlobeMap (ECharts), CloudflareLogo, or Empty / TableOfContents / Code (use EmptyState, SideToc, CodeBlock), nor `styles/standalone`; the `kumoTightSurface` ESLint config in `kumo/eslint-rules.js` enforces this. Do not install the kumo-design skill; look up component APIs with `npx @cloudflare/kumo doc <Component>`.
- After a Kumo upgrade or a first use of a new Kumo component, add it to the `kumo/demo/` page and rerun `kumo/qa/probe.py` (stored as `probe.py.txt`): Night and Day at 1440 and 390 must stay at zero computed-style differences, off-palette colours, contrast failures, axe violations, off-scale font sizes and overflow.
- Patterns from other libraries (Watermelon UI, Beautiful UI) are rewritten in Tight Surface tokens and classes, never copied in with their icon sets, motion libraries or raw colours.

## Icons
Lucide is the default icon library, pinned to 1.71.0 (ISC; some icons derive from Feather, MIT): 24×24 grid, stroke 2, round caps and joins, `currentColor`. Never mix in another icon set (Phosphor, Heroicons, Tabler, react-icons…); the only exception is the Phosphor glyphs Kumo draws inside its own components.
- Static pages and artifacts: an inline sprite, no CDN. Copy the symbols the page needs from the Design System's `icons/sprite.svg` (below) into one hidden `<svg>` at the top of `<body>`, keep the `<!-- @license lucide-static v1.71.0 - ISC -->` line above it, and draw `<svg class="i" aria-hidden="true"><use href="#i-play"/></svg>`. Symbols carry geometry only; `.i` supplies the stroke:
  `.i { display: inline-block; width: 1em; height: 1em; flex: none; vertical-align: -0.14em; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }`
- React: `lucide-react@1.71.0` (exact version). Wrap the app root in `<LucideProvider className="i">` so every icon gets `.i` and the size rules below; CSS sets the size, so `size` props have no effect; never change `strokeWidth` or use `absoluteStrokeWidth`. Icons without `aria-label` get `aria-hidden="true"` from lucide-react.
- Naming: sprite ids are `i-` + the Lucide name, one-to-one with lucide-react (`i-arrow-up-right` = `<ArrowUpRight />`). For a new icon, look the name up on lucide.dev, copy that symbol from lucide-static 1.71.0's `sprite.svg`, rename its id to `i-<name>` and add it to `icons/sprite.svg`. `i-move-right` (edge legend, viewBox cropped to 24×16) and its dashed-shaft variant `i-move-right-dashed` (optional edges) are the edge-legend marks.
```html
<!-- @license lucide-static v1.71.0 - ISC -->
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <symbol id="i-play" viewBox="0 0 24 24"><path d="M5 5a2 2 0 0 1 3.008-1.728l11.997 6.998a2 2 0 0 1 .003 3.458l-12 7A2 2 0 0 1 5 19z"/></symbol>
  <symbol id="i-code" viewBox="0 0 24 24"><path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/></symbol>
  <symbol id="i-arrow-up-right" viewBox="0 0 24 24"><path d="M7 7h10v10"/><path d="M7 17 17 7"/></symbol>
  <symbol id="i-arrow-up" viewBox="0 0 24 24"><path d="m5 12 7-7 7 7"/><path d="M12 19V5"/></symbol>
  <symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 5h16"/><path d="M4 12h16"/><path d="M4 19h16"/></symbol>
  <symbol id="i-chevron-right" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24"><path d="M20 6 9 17l-5-5"/></symbol>
  <symbol id="i-x" viewBox="0 0 24 24"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></symbol>
  <symbol id="i-download" viewBox="0 0 24 24"><path d="M12 15V3"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/></symbol>
  <symbol id="i-move-right" viewBox="0 4 24 16"><path d="M18 8L22 12L18 16"/><path d="M2 12H22"/></symbol>
  <symbol id="i-move-right-dashed" viewBox="0 4 24 16"><path d="M18 8L22 12L18 16"/><path d="M2 12H17" stroke-dasharray="3 3"/></symbol>
</svg>
```
- Uses: play = video, code = repository, arrow-up-right = external link, arrow-up = back to top, menu = TOC button, chevron-right = disclosure (rotate 90° when open), check / x = advice / myth and success / failure, download = export.
- Sizes: in chips and `.act.sm` 12, arrows / legends / list marks 13, resource and action buttons 15, menu 16, back-to-top 18, edge legend 22×14.
- Never glyph icons (☰ ↑ ↗ ▶ ◆ ▍ ✓ ✕) or emoji. For pseudo-elements use the same Lucide shape as a CSS mask (`background: currentColor`; data URI with `fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'`). Verdict lists (误区 / 建议) mark items with i-x / i-check as a mask in `bad` / `good` and start each item with a `.sr-only` “误区：” / “建议：” so the meaning never rests on the icon or colour alone; in Markdown write the labels “误区” / “建议” as text.
- Pages built before v2.4.0 keep their own 16×16 sprite; when one is upgraded, swap the sprite and rename `i-ext` → `i-arrow-up-right`, `i-up` → `i-arrow-up`, `i-cross` → `i-x`, `i-to` → `i-move-right`, `i-to-opt` → `i-move-right-dashed` (`i-play`, `i-code`, `i-menu`, `i-check` keep their ids).

## Charts: native first
- In web pages, artifacts and dashboards, build every chart natively. Do not add Mermaid, Chart.js, ECharts or similar libraries. Why: Mermaid renders one SVG scaled by its viewBox, with its own ID-scoped CSS, `!important` inline styles and HTML inside `foreignObject`; in the delivered pages this caused 5.6-7.8px text on phones, uncontrollable legends and overlapping labels, semi-transparent edge labels, highlighted labels turning grey, WebKit flashing overlapped text, a light default theme in a dark page, and version-specific config traps. Every native figure stayed clean.
- Exceptions: Markdown handbooks under `docs/` may use Mermaid because GitHub renders it; README.md never does (see GitHub README). In a web page, only a large auto-layout graph (about 15+ nodes) may: prefer a layout library (dagre, ELK) for coordinates only and still render nodes and labels in HTML; if Mermaid is truly needed, state why in a comment or README and follow the Mermaid rules below.
- Structure: all readable text (titles, ticks, labels, legends, values) lives in HTML with the page fonts and tokens, never SVG `<text>` and never a whole figure scaled through its viewBox. SVG draws only lines, areas and shapes, with `vector-effect: non-scaling-stroke`. Position with percentages or measured container sizes (`style="--x: .46; --y: .78"`, `left: calc(var(--x) * 100%)`). Keep the data in markup (one element per item or a `<script type="application/json">`) so it reads as a list or table without JS. Recompute lines and label positions with `ResizeObserver`; on narrow screens change the layout (stack chart and legend) instead of shrinking it.
- Recipes: bars = CSS grid name / track / value with width `--v`% (BarList); pie or donut = `conic-gradient` or an SVG ring with `stroke-dasharray`, names and values in an HTML legend; line or area = SVG `path` with `preserveAspectRatio="none"` and non-scaling stroke, axes and labels in HTML; scatter or quadrant = absolutely positioned dots via `--x` / `--y`, labels try above, right, left, below; radar = JS computes polygon vertices for an SVG `polygon`, axis names absolutely positioned in HTML; gantt or timeline = CSS grid with one column per time unit and `grid-column: start / span n`; DAG = nodes in CSS grid (`grid-template-areas`), JS measures them and draws SVG edges, edge labels are HTML chips; heatmap = table with heat cells; card matrix = CSS grid with fixed row height.
- Each object keeps one colour in every chart (`l0`-`l7`); solid = required, dashed = optional; heat scale for difficulty or intensity.
- Rendered chart text >= 12px at every width; zero label overlaps; nudge fixed titles off data points.
- Edge labels are opaque chips (`chart-label-bg`, 12.5px, border in the edge colour).
- Charts must not depend on a third-party CDN to render; every chart has a text equivalent (legend, list or table) and `role` + `aria-label`.
- Cross-check: pie total = stated total, gantt weeks = stage table, bar sum = hero stat, budget parts = total; same name for the same thing everywhere.
- Mermaid rules (exceptions only): pin an exact version, `theme: "base"` with themeVariables from tokens; measure the container with the raw diagram source hidden, size the geometry to it and crop the viewBox to content; replace library legends with HTML `.fig-key`; follow Interaction states for anything inside `foreignObject`.

## GitHub README
GitHub renders the README, not this design system: the background follows the visitor's light or dark theme, HTML is sanitized, and the body is about 880px wide on desktop and 360px on phones. So the README does not imitate the page; it is native, bilingual and consistent with the page's data. Banners and screenshots were tried on two repos and removed: a dark image looks jarring on light GitHub, its text cannot be selected, searched or translated, and generated images get facts wrong.

- Scope: the repo-root `README.md` only. GitHub looks in `.github/`, then the root, then `docs/`, so put no README in the other two. Markdown handbooks under `docs/` follow Charts: native first instead.
- Allowed: GFM (headings, paragraphs, lists, aligned tables, fenced code with a language, inline code, links, quotes, task lists, footnotes); at most two alerts (`> [!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]`, `[!CAUTION]`), never consecutive; whitelisted HTML only where Markdown cannot do it: `<div align="center">` (title block only), `<table>/<thead>/<tbody>/<tr>/<th>/<td>` with `rowspan`, `colspan`, `align`, `<details>/<summary>`, `<sub>`, `<br>`, `<b>`, `<code>`, `<a href>`, `<kbd>`. Leave a blank line before and after an HTML block; Markdown inside it is not parsed, so write `<a href>` and `<code>` there.
- Not allowed: content images (screenshots, banners, illustrations, GIFs, video, theme-switching `<picture>`); anything GitHub strips (`<style>`, `style=""`, `class`, `id`, `<script>`, `<iframe>`, inline `<svg>`, `<span>`, `<font>`, forms); GitHub-only graphics (Mermaid, `$…$` math), which show as source on npm, PyPI and editor previews: write relations as tables or lists; emoji and glyph icons ("→" for flow is fine); a hand-written full table of contents (GitHub builds one from the headings); spacing hacks (` `, ideographic spaces, stacked `<br>`, empty headings).
- Badges, the only images: functional badges (live site, GitHub Actions deploy `badge.svg`, license or version when they exist), at most 3, on one line in the title block. Colour chips in tables mark a level or track: `https://img.shields.io/badge/<code>-%20-<hex>?style=flat-square&labelColor=111723` (dark label with the code, colour segment from `l1`-`l7`); never white text on a coloured background (fails contrast on green, pink, yellow). Every shields badge uses `style=flat-square&labelColor=111723`; the live-site badge message colour is `ffb347`. Every badge has alt text and a text label beside it; colour never carries meaning alone.
- Structure, in this order (omit empty ones, never reorder): 1) title block in `<div align="center">`: eyebrow `<sub><b>UPPERCASE PHRASE</b></sub>` matching the page, `# 中文名` (the only H1), `**English name**`, slogan (Chinese line, `<br>`, English line in italics; split a long Chinese line into two balanced lines with `<br>`, no single-character orphan), badges, then a nav of at most 5 short links separated by `·` ("短中文 English"); 2) highlight: one table showing the project's signature structure (e.g. a seven-level ladder, seven knowledge tracks) instead of a hero image, with a `<sub>` reading note under it in Chinese and English; 3) 概览 · Overview: one or two Chinese paragraphs, the matching English paragraphs, then a stats table of 3-5 numbers (bold numbers as the header row, scope below); 4) 页面内容 · Contents (or features); 5) 本地运行 · Run locally: copy-pasteable commands; 6) 项目结构 · Structure: a tree in a code block, each line "path  中文说明 · English"; 7) 数据说明 · Data notes: sources, check date `YYYY-MM-DD`, estimate scope; 8) 同系列 · Companion project and 许可证 · License when they exist. Write for users, not maintainers: no deployment steps, audit-script details, page screenshots, design-language recap or implementation details (put those in `docs/`). Usually under 150 lines; title block plus highlight fit about one desktop screen.
- Bilingual: H2 is `## 中文 · English` (English in sentence case); a Chinese paragraph then its English counterpart with the same content; table headers "中文 English", cells `中文<br><sub>English</sub>`, list items the same; repo names, course codes, commands and paths stay untranslated in inline code; Chinese follows principle 8.
- Tables: at most 4 text columns (pure-number stats tables may have 5); with more items, transpose to one item per row or use an HTML table with `rowspan` groups (a 7-column course table broke CJK names like "深度学 / 习" at README width). Put the colour chip in the first column; colours match the page.
- Links: relative paths for files in the repo, full `https://` URLs for external pages, no bare URLs; link text names the destination ("在线访问", "课程档案"), never "click here"; codes in tables may link to the live page's anchors and repo names to the source repo. GitHub anchors: lowercase, drop every character except letters, digits, `_`, `-` and spaces, then turn each space into `-` without collapsing, so `概览 · Overview` is `#概览--overview`.
- Data: numbers, names and links come from the page or the project's data source, preferably generated by a script, never retyped; totals equal their parts (e.g. lectures plus videos in the course table = the 219 on the page); update the README whenever the page changes.
- Repo About: Description is one sentence, Chinese then English; Website is the live URL (GitHub Pages); Topics are lowercase English with hyphens covering domain, technology and content type.
- Verify before pushing: run the checker below (exit code 1 on any error), then preview with github-markdown-css in light and dark at 880px and 390px: no CJK names broken inside table cells, no orphan characters in the title block, badges legible in both themes. Manually confirm the English matches the Chinese and the data matches the live page.

```python
"""Tight Surface README check: python3 readme_check.py README.md  (exit 1 on any error)."""
import re, sys
from urllib.parse import unquote

src = open(sys.argv[1], encoding='utf-8').read()
err, warn = [], []
CJK = '一-鿿㐀-䶿'
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
FW = '，。、；：！？）」”》'          # ，。、；：！？）」”》
FO = '（「“《'                                       # （「“《
for pat, why in [(rf'[{CJK}]\x02?[A-Za-z0-9]|[A-Za-z0-9]\x02?[{CJK}]', 'missing CJK-Latin space'),
                 (rf'[{CJK}][  　]+[{CJK}]', 'space between CJK characters'),
                 (rf'[^\s{FW}][  ]+[{FW}]|[{FW}][  ]+[^\s{FW}{FO}]|[{FO}][  ]+\S|[^\s{FO}{FW}\x02][  ]+[{FO}]', 'space next to full-width punctuation'),
                 (r'　', 'ideographic space'),
                 (rf'[{CJK}][,;:!?()]|[,;:!?()][{CJK}]', 'half-width punctuation in Chinese'),
                 (rf'[{CJK}]"|"[{CJK}]', 'ASCII quote in Chinese'),
                 (r'[\U0001F000-\U0001FAFF☀-➿⬀-⯿\N{VARIATION SELECTOR-16}]', 'emoji or glyph icon')]:
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

## Interaction states (focus + context)
- When a node is hovered or focused, related lines, nodes and labels stay at effective opacity 1; unrelated lines fade to 12%, node shapes to 30%, node text to `ink` 30%.
- Fade edge labels by colour only (label text colour at 24% — Night #eef2f8, Day `ink`; border at 30% of the edge colour); the label chip background stays opaque.
- Scope state selectors to the chart's own SVG groups (`g.edgeLabel`, `.node .label-container`), never a bare class: Mermaid puts the same class on the outer `<g>` and the inner HTML `<span>`, so a bare class stacks the fade (0.15 x 0.15) and also dims the highlighted labels.
- Never put `opacity`, `transform`, `filter`, `transition` or `will-change` on HTML inside an SVG `<foreignObject>` (Mermaid htmlLabels). Change `color` / `border-color`, or style the pure SVG shape instead. WebKit (Safari, iOS, in-app WebViews) composites such HTML and paints it at the wrong position, which shows up as overlapping text flashing in the chart's top-left corner; Chromium does not show it.
- JS: `pointerenter` / `pointerleave` handlers run only when `e.pointerType === "mouse"`; `focus` highlights only when the element `:focus-visible`; clear the highlight before a click or tap navigates. A touch tap fires pointerenter, pointerleave, focus and click, toggling the state on, off and on within ~10ms and leaving it stuck.
- On touch, tapping a node opens its details; the dependency chain is carried by the text list beside the graph.
- A click or tap that pins an item (legend entry, edge list) must be a toggle button: `aria-pressed` mirrors the state and a second press releases it; hover and keyboard focus only preview and fall back to the pinned item or to nothing. Never rely on `blur` to clear a highlight: iOS Safari does not focus a tapped button, so the dimmed state would stay.

## QA checklist (run before delivery, Playwright at 1440 and 390; overflow also at 1180/1024/760/360/320)
1. Text: no missing CJK–Latin spaces, no spaces between CJK characters or next to full-width punctuation (U+3000 included), no half-width punctuation in Chinese, no ASCII quotes, no double spaces, no glyph icons, no orphan single characters. Check rendered text at both widths (variants hidden by media queries differ), Markdown docs and attributes such as `aria-label` and `title`; the extra-space rule is `/[一-鿿][  　]+[一-鿿]/`. Glyph icons also hide in CSS, where a text scan never sees them: walk every rule in `document.styleSheets` (nested @media rules, hover-only rules and escapes such as `"\25B6"` included) and inline `style` attributes for `content` / `list-style-type` / `list-style`, and read the computed `::before` / `::after` / `::marker` content of every element; flag arrows, box-drawing, block, geometric, misc-symbol, dingbat and emoji characters (`tools/audit.js` in llm-visual-guide implements this). Contrast: measure every text against its actual background (amber-tint buttons, tinted nodes, heat cells): >=4.5:1, >=3:1 at 24px+; `aria-hidden` outlined numerals and gradient headline text excepted.
2. Sizes: group elements by role and measure outer (border-box) heights; each group has exactly one value: pill 26, micro tag 20, resource button 48, action button and filter 36, compact action 26, copy 28, nav link 40, TOC link 36 / sub-item 32, back-to-top 44; Kumo controls 36 (compact 26, Badge 20); icons 12 / 13 / 15 / 16 / 18 / 22×14, all Lucide with stroke 2, sprite symbols identical to `icons/sprite.svg`.
3. Layout: `scrollWidth` equals viewport; zero unintended ellipsis truncation; chart text >= 12px; zero label overlaps.
4. Links and data: anchors resolve; external links `target="_blank" rel="noopener"`; FIG and TOC numbering continuous; cross-checks pass; no console errors; axe-core (tags wcag2a, wcag2aa, wcag21aa, wcag22aa, best-practice) reports zero violations at 1440 and 390; searching the page source for `mermaid`, `chart.js` and `echarts` finds nothing unless an exception is documented.
5. Interaction: exercise each chart with mouse hover, keyboard Tab and touch tap (Playwright `hasTouch` + `touchscreen.tap`); record state-class changes with a MutationObserver (a tap may change state at most once and nothing stays dimmed afterwards, except a pin toggle, whose `aria-pressed` turns true and returns to false on a second tap); in the focused state related labels have effective opacity 1 and zero elements inside `foreignObject` carry opacity, transform, filter or transition.
6. Manual: full-page screenshots at both widths, hover only on desktop, reduced motion, one screenshot with `forced-colors: active` (mask icons, bars, swatches and meters still visible), keyboard focus order and arrow-key scrolling of every sideways scroller, footer has data date + estimate note + series credit; when possible tap a chart once in Safari or on an iPhone.
7. GitHub README (repos only, before pushing): the checker passes with zero errors; light and dark previews at 880px and 390px look right; numbers, names and links match the live page; repo About has Description, Website and Topics.

Report findings as a short list grouped by these seven areas, then fix with minimal edits; do not redesign pages the user has already approved.