# 交互状态

图形里的“聚焦高亮”（悬停或选中一个节点，相关的线、节点、标签保持高亮，其余淡出）是本系统的标志性交互。这一节的规则来自《斯坦福 AI 课程地图》依赖图谱的一次修复：点击节点后，所有连线标签一起变灰，触屏上还会闪现重叠的文字。

## 聚焦 + 上下文
- 相关项保持原样，有效不透明度必须是 1。无关项淡出：连线 12%，节点图形 30%，节点文字降到 `ink` 30%。
- 连线标签淡出时只调暗文字和描边颜色（文字取标签文字色的 24%：Night 为 #eef2f8，Day 为 `ink`；描边取连线色的 30%），标签芯片的底色保持不透明，继续遮住下面的连线。
- 用于淡出的选择器必须限定到图形自己的 SVG 分组（例如 `g.edgeLabel`），不要用裸类名。Mermaid 在外层 `<g>` 和内部的 HTML `<span>` 上用的是同一个类名，裸类名会让淡出效果叠加（0.15 × 0.15 = 0.02），还会把本该高亮的标签一起调暗。

## foreignObject 里的 HTML
- SVG `<foreignObject>` 里的 HTML 元素（Mermaid 开启 htmlLabels 时的节点文字和连线标签）一律不加 `opacity`、`transform`、`filter`、`transition`、`will-change`。
- 需要变化状态时，二选一：直接改颜色（`color`、`border-color`），或者把效果加在纯 SVG 图形上（`rect.label-container`、`path`）。
- 原因：WebKit（Safari、iOS 内置浏览器、App 内的 WebView）会把带这些属性的 HTML 提升为合成层，然后画到错误的位置，表现为图的左上角闪现一团重叠的文字。Chromium 上看不出这个问题，所以只能靠规则预防。
- 悬停效果同理：`filter: brightness()` 加在节点的 `.label-container` 上，不加在整个 `g.node` 上。

## 指针类型
- 悬停类高亮只响应鼠标：`pointerenter` / `pointerleave` 的处理函数先判断 `e.pointerType === "mouse"`。
- 键盘聚焦只在 `:focus-visible` 时高亮，这样键盘用户能看到依赖链，点击和轻点不会触发。
- 点击或轻点节点去往详情前，先清除高亮。
- 原因：触屏上的一次轻点会依次触发 pointerenter、pointerleave、focus、click，高亮状态在约 10ms 内经历亮、灭、再亮，离开后还一直停在淡出状态。
- 触屏上，节点的主要操作就是“点击进入详情”；完整的依赖链由图旁边的文字列表（连线说明）来呈现。
- 点击或轻点用来“固定”某一项时（图例、连线列表），它必须是可切换按钮：`aria-pressed` 与状态一致，再按一次取消；悬停和键盘聚焦只做预览，离开后回到固定项或清空。不要靠 `blur` 来清除——iOS Safari 轻点按钮时不会让它获得焦点，淡出状态会一直留着（《斯坦福 AI 课程地图》的连线列表曾经如此）。

## 验收
- 用桌面悬停、键盘 Tab、触屏轻点三种方式各操作一遍图形。
- 用 MutationObserver 记录状态类名（如 `is-focus`）的变化：一次轻点最多只能有一次变化，操作结束后不能残留淡出状态；可切换的固定按钮例外，但再轻点一次必须恢复，且 `aria-pressed` 与状态一致。
- 在聚焦状态下逐项测量：相关标签的有效不透明度 = 1；`foreignObject` 内带 opacity、transform、filter、transition 的元素数量 = 0。
- 有条件时，在 Safari 或 iOS 真机上点一次节点看看。
