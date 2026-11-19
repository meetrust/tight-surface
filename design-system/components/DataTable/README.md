数据表：琥珀表头、首列吊住、表格内横向滚动，可叠加 1–5 级热力格。

## 用法
- 外层 `.tbl`（16px 圆角、`panel` 底），宽表加 `.sticky-first`：首列 `position: sticky`，右侧 1px `rule` 阴影线。
- 表头 `t-table-head`：`amber`、大写字距、nowrap；数字列 tabular-nums。
- 行首 `<th scope="row">` 用等宽字体，颜色取该行的数据色（`--c`）。
- 热力格：`.heat` 表里的 `td.h.h1`–`.h5`，底色 / 文字成对使用 `heat-N` / `heat-N-ink`（Night ≥7.2:1、Day ≥7.1:1），格内主数字 + `small` 原始值。
- 星级 `.stars` 用 ★☆ 字符，必须带 `aria-label="N 星"`——这是唯一允许的字符图形。
- 手机端只在 `.tbl` 内横向滚动，页面宽度不得超过视口（320px 也不行）。
- 会横向滚动的 `.tbl` 必须能用键盘滚动：加 `tabindex="0"`、`role="region"` 和全页唯一的 `aria-label`（“<表名>（可横向滚动）”）。是否溢出随视口变化时，用脚本在溢出时加上、不溢出时去掉（《大模型可视化学习指南》的 `markScrollers()`），表名写在 `data-scroll-name` 里。

## 不要
- 不要纵向斑马纹；用 1px 横线 + 悬停行高亮（ice 5%）。
