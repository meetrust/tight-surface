图标：默认图标库是 Lucide，固定在 1.71.0（ISC 许可）。24×24 网格，描边 2，圆头圆角，颜色 `currentColor`；页面里只用 Lucide，不混用其他图标库。

## 两种接入方式
- **静态页面、Artifact**：内联 sprite。从 `icons/sprite.svg` 复制页面要用的 `<symbol>`，放进 `<body>` 开头一个隐藏的内联 `<svg>`，上面保留一行 `<!-- @license lucide-static v1.71.0 - ISC -->`；画图标写 `<svg class="i" aria-hidden="true"><use href="#i-play"/></svg>`。symbol 里只有形状，描边由 `.i` 统一提供。不在运行时从 CDN 加载图标。
- **React**：`lucide-react@1.71.0`（精确版本）。根节点包一层 `<LucideProvider className="i">`，每个图标都带上 `.i`，自动套用下面的尺寸和描边。尺寸由 CSS 决定，`size` 属性不生效；不改 `strokeWidth`，不用 `absoluteStrokeWidth`。没有 `aria-label` 的图标，lucide-react 会自动加 `aria-hidden="true"`。

## 命名
sprite 的 id 一律是 `i-` 加 Lucide 图标名，与 lucide-react 组件一一对应：`i-arrow-up-right` 对应 `<ArrowUpRight />`。需要新图标时，在 lucide.dev 查到名字，从 lucide-static 1.71.0 的 `sprite.svg` 复制同名 symbol，把 id 改成 `i-<名字>`，加进 `icons/sprite.svg`。

## 清单
| id | lucide-react | 用途 |
|---|---|---|
| `i-play` | `Play` | 视频 |
| `i-code` | `Code` | 代码仓库 |
| `i-arrow-up-right` | `ArrowUpRight` | 外链 |
| `i-arrow-up` | `ArrowUp` | 回到顶部 |
| `i-menu` | `Menu` | 目录按钮 |
| `i-chevron-right` | `ChevronRight` | 折叠与展开（展开时旋转 90°） |
| `i-check` | `Check` | 建议、成功 |
| `i-x` | `X` | 误区、失败 |
| `i-download` | `Download` | 导出、下载 |
| `i-move-right` | `MoveRight` | 连线图例：必经前置（viewBox 裁成 24×16） |
| `i-move-right-dashed` | — | 连线图例：推荐或可选。唯一的自定义变体，在 `move-right` 的基础上把杆改成虚线 |

## 尺寸（按场景固定）
胶囊、紧凑操作按钮 12px（`icon-xs`）· 外链箭头 / 图例 / 卡片角标 13px（`icon-sm`）· 资源链接按钮和操作按钮 15px（`icon-md`）· 目录按钮 16px（`icon-menu`）· 回到顶部 18px（`icon-lg`）· 连线图例 22×14（`icon-edge`）。

## 规则
- 基础类 `.i`：`width: 1em; height: 1em; vertical-align: -0.14em`，再加 Lucide 的描边样式（`fill: none; stroke: currentColor; stroke-width: 2`，圆头圆角）。具体场景里用上面的尺寸 token 覆盖宽高。
- 装饰图标加 `aria-hidden="true"`，含义由旁边的文字承担；只有图标的按钮必须有 `aria-label`。
- 不使用字符图标：☰ ↑ ↗ ▶ ◆ ▍ ✓ ✕ 都换成 Lucide 图标或 CSS 形状。例外：正文里表示流程的“→”和带 `aria-label` 的 ★ 星级。
- 不用 emoji，不混用其他图标库（Phosphor、Heroicons、Tabler、react-icons 等）。Kumo 组件内部自带的 Phosphor 图标是唯一例外，见“Kumo 适配”。
- 伪元素里需要图标时（如卡片角标），用同一个 Lucide 图标的 SVG 做 `mask`，`background: currentColor`。data URI 里写 `fill='none' stroke='black' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'`，图形与 sprite 一致。
- 判定列表（误区 / 建议）的标记用 `i-x` / `i-check` 的 `mask`，颜色取 `bad` / `good`，并在每条开头加 `.sr-only` 的“误区：”“建议：”，含义不只靠图标和颜色；Markdown 文档里直接写成文字标签“误区”“建议”。

## 从旧图标迁移
v2.3 及更早的页面带着自己的旧 sprite（16×16 网格，1.7–1.8px 描边），不受这次升级影响。升级时换成新 sprite，再按下表改 `href`：

| 旧 id | 新 id |
|---|---|
| `i-play`、`i-code`、`i-menu`、`i-check` | 不变（`i-play` 从实心三角变为描边） |
| `i-ext` | `i-arrow-up-right` |
| `i-up` | `i-arrow-up` |
| `i-cross` | `i-x` |
| `i-to` | `i-move-right` |
| `i-to-opt` | `i-move-right-dashed` |

伪元素里的 `mask` 也要换成 Lucide 的图形。

## 许可
Lucide 采用 ISC 许可，其中 `arrow-up`、`arrow-up-right`、`check`、`chevron-right`、`code`、`download`、`x` 源自 Feather（MIT）。完整声明在 `icons/LICENSE-lucide.txt`。
