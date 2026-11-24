# 交付验收清单

每个页面交付前都要过一遍。前五组可以用 Playwright 脚本自动检查（在 1440 和 390 两个宽度下各跑一次）；第六组需要人工看截图，有条件时在 Safari 或 iOS 真机上点一次图形。第七组只针对提交到 GitHub 的仓库，在推送 README 前检查。

标“page_check”的各项由仓库里的 `tools/page_check.py` 检查：`python3 tools/page_check.py <页面文件或网址>`，在 1440 / 390 / 320px 下各跑一次，FAIL 为 0 才能交付，WARN 要人工确认。

## 1. 文字
- 中文与英文 / 数字之间缺空格：0 处。
- 汉字之间、全角标点前后的多余空格（含全角空格 U+3000）：0 处。例如“需 云 GPU”应为“需云 GPU”。
- 中文语境里的半角标点（, : ; ! ? ( )）：0 处。
- 可见文本里的 ASCII 直引号 "：0 处，统一用“”。
- 连续两个空格：0 处。
- 文字对比度：按每段文字实际所在的底色测量（琥珀淡底按钮、着色节点、热力格都要算），正文 ≥4.5:1、24px 以上 ≥3:1；`aria-hidden` 的空心编号和渐变字除外。只按 void / panel / panel-2 算会漏掉淡底上的小字。
- 字符图标 ☰ ↑ ↗ ▶ ◆ ▍ ⇢ ✓ ✕：0 处（★ 星级和流程“→”除外）。
- 样式表里的字符图标：`::before`、`::after`、`::marker` 的 `content` 和 `list-style-type` 里同样是 0 处。只检查可见文字查不到这些字符，要用脚本遍历 `document.styleSheets`（转义写法和只在悬停时生效的规则也要覆盖）并读取每个元素伪元素的计算样式；《大模型可视化学习指南》仓库的 `tools/audit.js` 有现成实现。
- 单字孤行、行首“/”：0 处（重点看手机宽度下的 h2 和首屏）。
- 占位内容（page_check）：0 处。lorem ipsum、TODO / TBD / FIXME、XXX、`{{…}}`、“待补充”“待定”“此处填写”、方括号里的占位名词（“[公司名称]”），以及 example.com 地址、555-01xx 或同一数字重复的电话；代码块里的示例代码不算。
- 按钮文案（page_check）：整条文案只是“了解更多”“查看更多”“更多”“详情”“点击这里”“确定”“确认”“提交”“是”“否”“OK”“Submit”“Learn more”这类通用词的按钮，0 个（完整词表见脚本）。
- 正文行长（page_check）：段落和列表项每行不超过 75ch（约 42 个汉字）；标题、图注、标签、表格和代码不算。

## 2. 尺寸一致
按选择器分组测量高度，同一组只能有一个值：
- 内容胶囊 26，微型标签 20，资源链接按钮 48，操作按钮和筛选按钮 36，紧凑操作按钮 26，复制按钮 28，导航链接 40，回到顶部 44。
- 用 Kumo 的页面：操作按钮、输入框、下拉、Tabs 36，表格和工具栏内的紧凑控件 26，Badge 20。
- 图标按场景：12 / 13 / 15 / 16 / 18 / 22×14。
- 图标只来自 Lucide 1.71.0：页面 sprite 里的 symbol 与 `icons/sprite.svg` 逐字一致，上方有 `@license lucide-static v1.71.0 - ISC` 注释（组件预览由 `tools/check_components.py` 检查）；React 项目只从 `lucide-react` 引入图标（`kumo/eslint-rules.js` 检查）。描边一律 2。
- 统计卡、图表卡的高度允许随内容变化，但同一行要对齐（page_check）：40px 以上、带描边或底色的盒子并排时，顶边相差不超过 1px。
- 主操作（page_check）：每组（按钮行、卡片、表单、对话框）里 `.act.primary` 或 `TsButton tone="primary"` 最多 1 个。

## 3. 布局
- `document.documentElement.scrollWidth` 等于视口宽度（1440 / 1180 / 1024 / 760 / 390 / 360 / 320 都要满足）。320 对应 WCAG 1.4.10 重排：手机单列网格写成 `1fr` 时，宽表的最小内容宽度会把列撑宽，只在这个宽度下暴露，所以一律写 `minmax(0, 1fr)`。
- 设了 nowrap 和省略号的标签：`scrollWidth > clientWidth` 的数量为 0。如果是本应完整显示的名称被截断，就加宽对应的列。
- 图表文字渲染后不小于 12px；标签之间、标签与数据点之间零重叠。
- 贴边（page_check）：390 / 320px 下，文字距屏幕左右边缘 ≥16px；在自身容器里横向滚动的表格和代码不算。
- 空白（page_check）：从左到右没有任何文字、图片、控件或数据标记的空白带，高度 ≤240px。
- 章节间距（page_check，WARN）：各章节标题上方的间距与全页中位数相差不超过 25%。

## 4. 链接与数据
- 页内锚点全部能找到目标；外链全部带 `target="_blank" rel="noopener"`。
- FIG 编号连续；目录编号与章节编号一一对应。
- 交叉核对：合计、总量、周数、预算、同一事物在各处的名称。
- 控制台无报错。
- 用 Kumo 的页面：升级或新增 Kumo 组件后跑 `kumo/qa/probe.py`（见“Kumo 适配”），色板、尺寸对照、对比度、axe 全部零差异。
- axe-core（标签 `wcag2a`、`wcag2aa`、`wcag21aa`、`wcag22aa`、`best-practice`）在 1440 和 390 下零违规。
- 占位链接（page_check）：指向“#”、空地址或 `javascript:` 的链接 0 个，页内操作用 `<button>`。
- 表单标签（page_check）：每个字段都有看得见的标签（`<label>` 或 Kumo 组件的 `label`），只靠占位符、`aria-label` 或 `title` 命名的字段 0 个；占位文字对比度 ≥4.5:1。axe 把占位符算作名称，查不出这一条。
- 只靠图形表达数值的元素（评分条、星级、含义色块）有文字替代：`role="img"` + `aria-label`，只写 `title` 读屏读不到。
- 带 `aria-label` 的链接和按钮，名称里原样包含可见文字（WCAG 2.5.3）；可见文字由两个相邻元素拼成时（代号 + 名称），中间留一个空格。
- 图表库：页面源码里搜 `mermaid`、`chart.js`、`echarts`，结果为 0；如果有例外，页面注释或 README 里必须写明原因，且该图的渲染数量等于源码块数量。

## 5. 交互状态
- 图形用桌面悬停、键盘 Tab、触屏轻点（Playwright `hasTouch` + `touchscreen.tap`）三种方式各走一遍。
- 状态类名的变化：一次轻点最多变化一次，操作结束后不残留淡出状态。可切换的固定按钮（图例、连线列表）例外：第一次轻点 `aria-pressed="true"`，再轻点一次变回 `false` 且不再淡出。
- 会横向滚动的表格、代码块和图表容器能用 Tab 聚焦、用方向键滚动（`tabindex="0"`、`role="region"`、全页唯一的 `aria-label`）。
- 复制按钮在异步剪贴板被拦截时仍显示“已复制”（退回 `execCommand("copy")`）。
- 聚焦状态下，相关标签的有效不透明度 = 1；`foreignObject` 内带 opacity、transform、filter、transition 的元素数量 = 0。

## 6. 人工检查
- 1440 和 390 各截一张全页图，按“名称 → 颜色 → 结构”的顺序扫一遍。
- 悬停态：只在桌面端出现，位移不超过 6px。
- 打开 prefers-reduced-motion 后，没有任何动画和平滑滚动。
- 打开 `forced-colors: active`（Playwright `emulateMedia({ forcedColors: "active" })`，对应 Windows 对比度主题）截一次图：遮罩图标、条形、图例色块、评分条都还看得见。
- 键盘 Tab 走一遍：焦点环始终可见，顺序与阅读顺序一致。
- 页脚：数据核对日期、估算口径、同系列声明，三项齐全。
- 用 Day 主题的页面：在 Day 下重跑第 1–6 组，对比度按 Day 的色值计算；同时提供两套主题时，切换 `data-theme` 前后元素尺寸、布局和截断结果完全一致，只有颜色变化。

## 7. GitHub README（提交到 GitHub 前）
- `python3 readme_check.py README.md` 零错误（脚本见“GitHub README”）：图片只有功能徽章和颜色标签，没有会被过滤的 HTML、Mermaid 和数学公式，只有一个一级标题，二级标题都是“中文 · English”，页内锚点全部有效，中文排版规则通过，每节都有中英文。
- 用 github-markdown-css 的浅色和深色样式，在 880px 和 390px 宽度下各预览一次：表格中文不被挤断，标题区没有单字孤行，徽章在两种主题下都清楚。
- 数字、名称、链接与在线页面一致；数据核对日期是最新的。
- 仓库 About 填好 Description、Website 和 Topics。
