# Kumo 适配

应用控件（表单、浮层、导航、反馈）用 Cloudflare 的 Kumo（`@cloudflare/kumo` 2.18.1），再加载本节的适配层：Kumo 组件在 Night 和 Day 下与 Tight Surface 视觉一致。适配层不改 Kumo 源码，文件都在 `kumo/` 目录。Tight Surface 已有的内容组件（SectionHead、Figure、DataTable、ModuleCard 等）继续用原生写法。

## 文件

| 文件 | 作用 |
|---|---|
| `kumo/kumo-tight-surface.css` | 适配层：语义 token 映射、焦点 / 悬停 / 选中 / 禁用补丁、构建期主题 |
| `kumo/adapters.tsx` | `TsButton`、`FilterButton`、`ResourceButton`、`Chip` 四个薄适配组件 |
| `kumo/theme.ts` | `applyTheme()`：同时维护 `data-theme` 与 `data-mode` |
| `kumo/app.css` | 入口样式表示例（层顺序） |
| `kumo/eslint-rules.js` | ESLint 规则：禁用图表等组件、强制走适配组件 |
| `kumo/qa/probe.py.txt`、`kumo/demo/` | 对照页与检查脚本，升级 Kumo 时重跑（脚本存成 .txt，取用时去掉后缀） |

对照页：新建一个 Vite 项目，放入 `kumo/demo/` 的文件；把 `kumo/` 下的适配文件放到 `src/kumo-ts/`，把本系统的 `tokens.css` 和 `components/bundle.css` 放到 `src/tight-surface/`（同样删掉字体 `@import`）；另装 `vite`、`@vitejs/plugin-react`、`lucide-react`、`axe-core` 和三个 `@fontsource` 字体包。`vite build` 后用 `vite preview --port 4173` 起服务，再跑 `python3 kumo/qa/probe.py`（需要 Python 的 playwright）。

依赖版本锁定为：`@cloudflare/kumo` 2.18.1、`@phosphor-icons/react` 2.1.10（Kumo 自身的依赖，应用代码不直接用）、`lucide-react` 1.71.0、`tailwindcss` 与 `@tailwindcss/vite` 4.3.5、React 18 或 19；用 DatePicker 的中文界面时另装 `react-day-picker` 9.x（Kumo 依赖它）。

## 接入

只走 Kumo 的 Tailwind 路径，不用 `@cloudflare/kumo/styles/standalone`：圆角、投影、字体、动效是在构建期改的，预编译的 CSS 不会生效。入口样式表的顺序是适配成立的前提：

```css
@import url("https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=JetBrains+Mono:wght@400;600;700&family=Noto+Sans+SC:wght@400;500;700;900&display=swap");

/* 层顺序：ts-important 最早（!important 在较早的层反而取胜），ts-kumo 最晚（压过 Kumo 工具类） */
@layer ts-important, theme, base, ts-base, components, utilities, ts-kumo;

@import "tailwindcss";
@import "@cloudflare/kumo/styles/tailwind";
@source "../node_modules/@cloudflare/kumo/dist/**/*.{js,jsx,ts,tsx}";

@import "./tight-surface/tokens.css";                 /* 不加 layer */
@import "./tight-surface/bundle.css" layer(ts-base);  /* components/bundle.css，删掉它第一行的字体 @import */
@import "./kumo-ts/kumo-tight-surface.css";
```

- 字体放在入口文件第一行加载：`bundle.css` 自带的 Google Fonts `@import` 被包进 `ts-base` 层后不合法，Tailwind 构建会报警告，开发模式下可能不加载，引入前删掉那一行。

- `tokens.css` 不加 layer：它的 `--font-mono` 与 Tailwind 默认主题同名，不分层的声明压过分层声明，Kumo 的 `font-mono` 直接得到 JetBrains Mono。
- `bundle.css` 放进 `ts-base` 层：否则 `a`、`code` 这类元素样式会压过 Kumo 工具类，把 LinkButton 染成链接色。
- `ts-kumo` 层排在 utilities 之后：状态补丁靠层序取胜，不靠提高选择器优先级。
- `ts-important` 层排在最前：Kumo 的强调按钮写了 `!text-white`，Dialog 用内联 style 写了投影；`!important` 声明是越早的层越优先。
- 主题属性：Night 写 `<html data-mode="dark">`，Day 写 `<html data-theme="day" data-mode="light">`，用 `kumo/theme.ts` 的 `applyTheme()` 切换。`data-theme` 给 Tight Surface 用，`data-mode` 给 Kumo 和 `dark:` 变体用。
- 应用根节点加 `className="isolate"`（Kumo 浮层的层叠要求）。
- 查组件 API 用 `npx @cloudflare/kumo doc <组件名>`；不装 kumo-design 技能，那是 Cloudflare 自己的设计规范。

## Token 映射

Kumo 的 54 个语义颜色 token 全部指向 Tight Surface token，没有新增色值；Day 主题只换 Tight Surface token，映射不用重写。

| Kumo token | Tight Surface | 说明 |
|---|---|---|
| `canvas` / `base` / `elevated` | `void` / `panel` / `panel-2` | 页面、卡片、表头三层底色 |
| `recessed` | `void` | 分段控件轨道、对话框遮罩（遮罩不透明度 80%） |
| `control` / `overlay` | `pop` | 输入框与浮层 |
| `tint` | `ink` 6% | 中性悬停底 |
| `contrast` | `ink` | 滚动条等小部件；勾选态另由补丁改成琥珀 |
| `line` / `hairline` / `fill` | `rule-2` / `rule` / `rule` | 控件描边用 `rule-2`，分隔线用 `rule` |
| `focus` | `rule-2` | Kumo 的焦点 ring 降为描边，焦点由 2px `amber` outline 表达 |
| `brand` / `brand-hover` | `amber` / `amber-ink` | 唯一界面强调色 |
| `shadow-edge` / `shadow-drop` / `arrow-edge` | 透明 | 不用投影 |
| `info` / `info-tint` | `ink-2` / `ink` 6% | 提示用中性色，`ice` 只表示“可以点” |
| `success` / `danger` / `warning` | `good` / `bad` / `warn`，淡底 12% | 状态色 |
| `badge-*` 具名色 | `l0`–`l6` | 只作分类；teal 与 green 同落在 `l6` |
| `text-default` / `strong` | `ink` | 正文 |
| `text-subtle` / `inactive` / `placeholder` | `dim` / `faint` / `faint` | Kumo 暗色的 inactive 只有 2.3–2.6:1，改用 `faint` |
| `text-link` / `text-inverse` | `ice` / `on-amber` | 链接、琥珀实底上的字 |

构建期主题：`--font-sans` 指向 `--font-body`；`--radius-xl` 为 16px（`r-lg`）；`--shadow-*` 全部归零；Tailwind 的 `text-xl` / `text-2xl` / `text-3xl` 对齐到 `fs-lg` 18、`fs-xl` 22、`fs-2xl`；默认过渡时长与缓动为 `dur` 和 `ease`，`duration-100`–`300` 与 `ease-out` 也统一成这一组。

## 尺寸、字重与组件取舍

Kumo 的四档控件高度正好落在已有的尺寸 token 上，按下表使用；除了资源链接按钮 `ResourceButton` 的 48px，不出现其他高度。

| Kumo 尺寸 | 高度 | Tight Surface | 用途 |
|---|---|---|---|
| `xs` | 20px | `h-tag` | 微型标签、Badge |
| `sm` | 26px | `h-pill` | 表格和工具栏里的紧凑控件 |
| `base` | 36px | `h-filter` | 默认：操作按钮、输入框、下拉、Tabs、筛选 |
| `lg` | 40px | `h-nav-link` | 只用于导航 |
| `ResourceButton` | 48px | `h-btn` | 两行标签的资源链接按钮 |

中文字重只用已加载的 400 / 500 / 700 / 900：选项文字、Tabs、Badge 为 400，字段标签、Banner 标题、操作按钮保持 Kumo 的 500，资源按钮与 `.btn` 一致写 600，选中的筛选按钮 700。适配层已把 Kumo 里 Tabs、Badge、开关文字的 500 降到 400，与勾选框文字一致。

| 处理 | Kumo 组件 | 写法 |
|---|---|---|
| 采用 | Input、InputArea、Select、Combobox、Autocomplete、Checkbox、Radio、Switch、Slider、DatePicker、TagInput、SensitiveInput、Field、Label | 默认 36px；示例里常见的 `w-72`（288px）在窄屏改成 `w-full max-w-72` |
| 采用 | Dialog、Popover、Tooltip、DropdownMenu、CommandPalette、Toasty | 浮层：`pop` 底色加 `rule-2` 描边，无投影；Toast 标题与说明为 14 / 13px |
| 采用 | Button、LinkButton、ButtonGroup、Tabs、Breadcrumbs、Pagination、Sidebar、MenuBar、Toolbar、Collapsible | 按钮走适配组件；导航用下划线 Tabs，当前项是 2px 琥珀底线；Sidebar 当前项是琥珀淡底加 3px 琥珀竖条 |
| 采用 | Banner、Badge（状态变体）、Meter、Loader、ClipboardText、InlineCopyText | Meter 表示数据系列时用 `indicatorClassName` 换成 `--c` |
| 采用，放进 `.tbl` | Table | 表头和单元格与 DataTable 一致，保留行选择和吸顶列 |
| 用 TS 的 | Empty、TableOfContents、Code、Text（标题）、LayerCard | 分别改用 EmptyState、SideToc、CodeBlock、SectionHead、Figure / ModuleCard |
| 不用 | Chart、TimeseriesChart、SankeyChart、BubbleMap、ChoroplethMap、GlobeMap | 依赖 ECharts，违反原则 9 |
| 不用 | CloudflareLogo | 品牌组件 |

## 写法规则

- 操作按钮写 `TsButton`：`tone="primary"` 是琥珀淡底，`tone="danger"` 是 `bad` 淡底，默认是描边按钮，`ghost` 无边框。不要直接写 `Button variant="primary"`、`"destructive"` 或 `"secondary-destructive"`，ESLint 会报错。
- 筛选写 `FilterButton`（`aria-pressed`），资源链接写 `ResourceButton`，分类胶囊写 `Chip c="l0"`–`"l7"`；Badge 必须写 `variant`，只用 success、warning、error、info、secondary（不写时默认 primary，是实底反色胶囊）。
- Kumo Table 放进 `<div class="tbl">`，表头自动变成 Display 字体、琥珀色、`panel-2` 底。
- Day 下 warning 的 12% 淡底放在 `panel-2` 上只有 4.49:1：状态 Badge 和 Banner 放在页面底或卡片上，不放进表头这类 `panel-2` 区域。
- Kumo 的默认文案和无障碍名称都是英文，一律传中文：DatePicker 传 `locale={zhCN}`（`react-day-picker/locale`），Pagination 用 `text` 写“第 11–20 条，共 86 条”这类文案；Tabs、Pagination 传 `labels`（如 `pageNumber: "页码"`），Combobox 的 `TriggerInput` 传 `clearLabel` 和 `showOptionsLabel`。Breadcrumbs 的导航名称（breadcrumb）和 Toast 区域的名称（Notifications）写死在组件里，改不了，保持原样。
- 表单字段用组件自带的 `label`（Input、Select、Combobox、TagInput、Slider 都有），占位符只写示例（“如 claude-sonnet-5-5”），不能只给 `aria-label` 或 `placeholder`。Pagination 的页码框是翻页控件的一部分，靠 `labels.pageNumber` 命名，`tools/page_check.py` 对它豁免。
- Combobox、Select 这类外壳被 grid 或 flex 拉伸时，清除和箭头按钮会下移：放进 grid 时给容器 `align-content: start`。
- Toast 的弹跳入场动画是 Kumo 自己的缓动曲线，不在“一条缓动、一个时长”的统一范围内；`prefers-reduced-motion` 下会关闭。
- 图标用 `lucide-react`：根节点包 `<LucideProvider className="i">`，传给 Kumo 时写 `icon={<Download />}`。按钮里的图标由适配层统一成 15px，`TsButton size="sm"` 里是 12px（靠 `data-ts-size`），描边 2。应用代码不直接引入 `@phosphor-icons/react` 或其他图标库，ESLint 会报错。
- Kumo 组件内部的下拉箭头、勾选、关闭图标是 Phosphor 的内联 SVG，线宽和造型与 Lucide 略有差别，不改源码换不掉，保持原样。
- 不要给 Kumo 组件传改颜色、字重、焦点的 className：适配层排在 utilities 之后，这些 className 不会生效。确实需要新样式时加一个 `data-ts-variant` 值，写进适配层。
- 新组件第一次用到时，先加进 `kumo/demo/` 对照页，跑一遍 `kumo/qa/probe.py` 和 `tools/page_check.py` 再上线。

## 验证

`kumo/qa/probe.py` 在 Night、Day 两套主题和 1440 / 390px 两个宽度下检查，基线结果（2026-11-16，Kumo 2.18.1）如下；升级 Kumo 后重跑，结果要回到这条基线。

| 检查项 | 方法 | 基线 |
|---|---|---|
| 样式对照 | `.btn` ↔ `ResourceButton`、`.fbtn` 选中与未选中 ↔ `FilterButton`、DataTable 表头与单元格 ↔ Kumo Table；比高度、圆角、文字色、底色、字体、字号、字重、字距 | 5 组全部一致 |
| 色板 | Kumo 元素的文字、底色、描边、outline、box-shadow 颜色逐一对 token；含打开的对话框、菜单、组合框、自动补全、命令面板、Toast | 0 个非 token 颜色 |
| 字号 | Kumo 文字的字号只能是 11–16、18、22px | 0 处越界 |
| 对比度 | 每段文字对实际叠加后的底色 | 0 处低于 4.5:1 |
| axe-core | wcag2a、wcag2aa、wcag21aa、wcag22aa、best-practice | 0 违规 |
| 横向溢出 | 320 / 360 / 760 / 1024 / 1440px | 0 处 |
| 页面检查 | `tools/page_check.py`（2026-11-24 加入）：占位内容、按钮文案、可见标签、主操作、并排对齐、行长、贴边、空白、章节间距 | 0 FAIL、0 WARN |
| 交互 | 键盘焦点、鼠标悬停、触屏轻点、选中态 | 2px `amber` outline 外偏移 3px；按钮上浮 2px、描边 `ice`；轻点不残留上浮；勾选、单选、开关、日期为琥珀实底 |

覆盖的组件：Button、LinkButton、Input、Select、Combobox、Autocomplete、Checkbox、Radio、Switch、Slider、DatePicker、TagInput、Tabs、Breadcrumbs、Pagination、Sidebar、Banner、Badge、Meter、Table、Dialog、DropdownMenu、CommandPalette、Toasty。

## 升级与维护

适配层有 7 处依赖 Kumo 的内部写法，升级时最可能失效，先看这里：

| 依赖点 | 用在哪里 | 失效后的表现 |
|---|---|---|
| `data-kumo-component` / `data-kumo-part` 属性 | 焦点、选中、禁用、悬停、字重补丁 | Kumo 称之为库自己维护的作用域原语，风险最低 |
| `--kumo-button-emphasis-*` 变量名 | 强调与危险按钮的淡底 | 强调按钮变回渐变实底 |
| `[style*="kumo-brand"]` 选择器 | 未经 `TsButton` 的 `variant="primary"` 兜底 | 白字配浅琥珀，Day 下对比度 1:1 |
| Dialog 内联写入的 `--tw-shadow` | 对话框投影归零 | 重新出现淡黑投影 |
| Toast 的 `[role=region][aria-live] [role=dialog] h2 / p` 结构 | Toast 字号 | 回到 15.6 / 14.8px |
| react-day-picker 的 `rdp-*` 类名与 `data-selected` | DatePicker 选中日 | 选中日变回 `ink` 底 |
| Sidebar 的 `data-active` 属性 | Sidebar 当前项 | 当前项只剩中性淡底 |

升级流程：

1. 在 `package.json` 里把 `@cloudflare/kumo` 锁在精确版本。
2. 升级分支里重新构建 `kumo/demo/`，跑 `python3 kumo/qa/probe.py` 和 `python3 tools/page_check.py http://localhost:4173/`。
3. 结果全部回到基线再合并；有差异先查上表 7 处。
4. 看 Kumo 的 CHANGELOG 有没有新增语义 token，新 token 补进映射表。

## Watermelon 与 Beautiful UI

两个库都是 MIT 许可，但都不直接引入代码，只借交互模式，用 Tight Surface token 和 Kumo 的无障碍基础组件重写。

- Watermelon UI：1,077 个 registry 条目，643 个依赖 lucide-react、463 个依赖 react-icons、415 个依赖 motion，大量条目还要求先装 shadcn 的 Radix 基础组件；代码里写死 Tailwind 原始色和 `dark:`。装进来会多一套图标、一套动效和第二套基础组件。
- Beautiful UI：21 个面向 AI 界面的组件，只能从网页复制，没有公开仓库、npm 包和版本号，无法审查和更新。
- 已按这种方式做成组件：ThinkingTrace、ToolCall、TaskRow、ApprovalCard（参考 Beautiful UI 的 Thinking、Tool Chips、Task Rows、Approval Card）。
- Watermelon 里的营销类动效（marquee、shimmer-button、text-gradient）和 web3 模板不借用。
- 候选组件，尚未制作；每个都只用已有 token 和组件拼出，不加新颜色、新尺寸或新依赖：

| 优先级 | 组件 | 设计参考 | 构成 |
|---|---|---|---|
| P2 | SourceCard 检索片段卡 | Beautiful UI · Context Cards、Streaming Text | 结构同 Callout：标题、字符数（Display）、摘录、来源文件链接（`ice`）；回答下方的来源列表和追问建议复用它 |
| P2 | Composer 输入栏 | Beautiful UI · Prompt Bar、Chat | Kumo InputArea；`@` 引用来源、`/` 命令用 Combobox；模型选择用 Select；发送用 36px `TsButton tone="primary"` |
| P2 | ToolOutput 终端输出 | Watermelon · terminal | CodeBlock（`.term`）加退出码 `.st` 胶囊；stdout / stderr 用 Collapsible 分段，stderr 行用 `bad` |
| P2 | UsageMeter 用量卡 | Watermelon · credit-usage-card | StatTile 的数字 + 分段条（BarList 轨道加 25% 刻度）+ 口径说明，用于 Token 用量面板 |
| P3 | StatusDot 状态点 | Watermelon · status-indicator | 7px 圆点加文字，不单靠颜色；运行中复用 `pulse` 关键帧 |
| P3 | Stepper 步骤条 | Watermelon · step-indicator | 当前步 `amber`，完成步 `i-check`，可选步虚线（与图表线型规则一致） |
| P3 | FileTree 文件树 | Watermelon · tree-menu | mono 行，当前项用 SideToc 的 3px 琥珀竖条，展开状态用 `aria-expanded` |

- 万一要复制某个 Watermelon 条目的源码：固定到具体提交，保留 MIT 许可声明，去掉图标库和 motion，把原始色换成 token，再跑一遍验收清单。

## 相关链接

- [Kumo 文档](https://kumo-ui.com) · [cloudflare/kumo 仓库](https://github.com/cloudflare/kumo)（核对时为 npm 2.18.1，提交 `eaa9e17`）
- [Watermelon UI](https://ui.watermelon.sh) · [watermellon-registry 仓库](https://github.com/WatermelonCorp/watermellon-registry)（核对时最新提交 `86052b8`，2026-09-30） · [版权与署名政策](https://ui.watermelon.sh/copyright)
- [Beautiful UI](https://www.beautifului.dev) · [许可证](https://www.beautifului.dev/license)
