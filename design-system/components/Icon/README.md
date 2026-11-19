图标：一份内联 SVG sprite（`<symbol>` + `<use>`），16×16 网格（连线箭头 24×16），1.7–1.8px 圆头描边，颜色 `currentColor`。

## 清单
`i-play` 视频 · `i-code` 代码 · `i-ext` 外链 · `i-up` 回到顶部 · `i-menu` 目录 · `i-to` 必经前置 · `i-to-opt` 推荐 / 可选（虚线） · `i-check` 建议 / 正确做法 · `i-cross` 误区 / 错误做法。

## 尺寸（按场景固定）
胶囊 12px（`icon-xs`）· 外链箭头 / 图例 / 卡片角标 13px（`icon-sm`）· 按钮主图标 15px（`icon-md`）· 目录按钮 16px（`icon-menu`）· 回到顶部 18px（`icon-lg`）· 连线图例 22×14（`icon-edge`）。

## 规则
- 基础类 `.i { width: 1em; height: 1em; vertical-align: -0.14em }`，在具体场景里用上面的 token 覆盖宽高。
- 装饰图标加 `aria-hidden="true"`，含义由旁边的文字承担；只有图标的按钮必须有 `aria-label`。
- 不使用字符图标：☰ ↑ ↗ ▶ ◆ ▍ ✓ ✕ 都换成 SVG 或 CSS 形状。例外：正文里表示流程的“→”和带 `aria-label` 的 ★ 星级。
- 不用 emoji。
- 伪元素里需要图标时（如卡片角标），用同一路径的 SVG 做 `mask`，`background: currentColor`。
- 判定列表（误区 / 建议）的标记用 `i-cross` / `i-check` 的 `mask`，颜色取 `bad` / `good`，并在每条开头加 `.sr-only` 的“误区：”“建议：”，含义不只靠图标和颜色；Markdown 文档里直接写成文字标签“误区”“建议”。
