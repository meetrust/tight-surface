四种按钮：48px 资源链接按钮（`.btn`）、36px 操作按钮（`.act`，紧凑版 `.act.sm` 26px）、36px 筛选按钮（`.fbtn`）、28px 复制按钮（`.copy`）。

## 用法
- `.btn`：左图标（`.ic`，15px，faint）+ 两行标签（`fs-sm` 600 + `fs-2xs` 12px 说明，两行都不换行，放不下时加省略号）+ 右侧外链箭头（13px）。外链一律 `target="_blank" rel="noopener"`。
- `.btn.video`：琥珀淡底，文字 `amber-ink`，第二行说明 `dim`（faint 在琥珀淡底上只有 4.2:1），图标 `amber`——每张卡片最多一个，标记最主要的去处。
- `.btn.off`：虚线 `rule` 描边、透明底、`faint` 文字，渲染成 `<span aria-disabled="true">`，不是链接。用于“暂无公开链接”，保留占位，不隐藏。
- `.act`：页面里的操作（保存、导出、重试、确认），写成 `<button type="button">`。默认 `panel` 底、`rule-2` 描边、`fs-sm` 500 字重。
  - `.act.primary` 是主操作：琥珀淡底，与 `.btn.video` 同款，一组最多一个；不用琥珀实底，实底只表示“选中”。
  - `.act.danger` 是危险操作：`bad` 淡底，写法同 primary。
  - `.act.ghost` 没有描边和底色，用于“取消”“跳过”这类次要操作。
  - `.act.sm`（26px，与胶囊同高）用在表格行、任务行等紧凑位置。
  - 禁用写 `disabled` 或 `aria-disabled="true"`：虚线 `rule` 描边、`faint` 文字，保留占位。
  - 用了 Kumo 的页面，同样的按钮用适配层的 `TsButton`（`tone` 对应 primary / danger / ghost），两者视觉一致，见“Kumo 适配”。
- `.fbtn`：胶囊形，`aria-pressed` 表示选中，选中为琥珀实底 + `on-amber` 文字。
- `.copy`：代码块顶栏里的复制按钮，成功后加 `.ok` 并把文字改为“已复制”。
- 悬停：上浮 2px（`lift`），描边变 `ice`；`.act.primary` / `.act.danger` 悬停时描边变实色 `amber` / `bad`，底色不变（与 Kumo 的 `TsButton` 一致，也保证 Day 下文字对比度）；只在精确指针设备上生效。

## 不要
- 不要用 ▶ ↗ 等字符做图标，只用 SVG（见 Icon）。
- 同一组按钮的高度必须一致。按钮只有 48（`.btn`）、36（`.act`、`.fbtn`）、28（`.copy`）、26（`.act.sm`）四档，不再增加。
- `.btn` 只用于去往外部资源的链接；页面内的操作用 `.act`，不要把 `.act` 做成两行标签。
