终端式代码块：顶栏（语言 · 标题 + 复制按钮）+ 代码正文；以及行内 `code`。

## 用法
- `.term` 底色 `code-bg`，顶栏 `code-bar`；顶栏标题前的 3px 色条取该模块的数据色（`--c`）。
- 正文 `t-code`（13px，行高 1.6，`code-ink`）；高亮四色：注释 `.c`（code-comment）、关键字 `.k`（l2）、函数 `.f`（l1）、要点 `.hl`（amber）。
- 超长行在 `pre` 内横向滚动，不折行、不撑破页面。会滚动的 `pre` 加 `tabindex="0"`、`role="region"` 和 `aria-label="代码 <顶栏标题>（可横向滚动）"`，键盘才能滚动到行尾（规则同 DataTable）。
- 行内 `code`：0.86em（不小于 12px），ice 10% 底（Day 8%），`inline-code-ink` 文字，允许任意位置断行。
- 复制成功：按钮加 `.ok`，文字改“已复制”，1.6s 后复原。
- 复制先用 `navigator.clipboard.writeText`；它不存在或被拒绝时（嵌入页的权限策略常会拦截），退回隐藏 `textarea` + `document.execCommand("copy")`，两者都失败才显示“复制失败”，并把焦点还给按钮。
