滑动选中块：单选的标签和分段控件。切换时，选中底块从旧位置滑到新位置，让人看清选中项从哪里移到了哪里。静态页面用这个组件；React 应用用 Kumo Tabs（适配层已把它的指示块改成同样的缓动和时长）。

## 用法
- 结构：`<div class="seg" role="tablist" aria-label="…">` > 一个 `<span class="seg-thumb" aria-hidden="true">` + 若干 `<button role="tab">`，每个按钮有 `id`、`aria-selected` 和 `aria-controls`；面板 `role="tabpanel"`，`aria-labelledby` 指向当前标签。
- 尺寸：外框 36px（`h-filter`），紧凑版 `.seg.sm` 26px（`h-pill`），用在表格和工具栏里。外框 `void` 底、`rule` 描边；底块 `panel` 底、`rule-2` 描边；未选中文字 `dim`，选中 `ink`，字重都是 400（字重不变，底块宽度才不会在切换时跳动）。与 Kumo Tabs 的分段样式一致。
- 键盘：只有选中的标签在 Tab 顺序里（其余 `tabindex="-1"`）；左右方向键切换并选中，Home / End 到首尾。
- 底块位置由脚本读取选中项的 `offsetLeft`、`offsetTop` 和尺寸，写进 `--x`、`--y`、`--w`、`--h`；加上 `data-ready` 之后才开始过渡，所以首次显示和窗口尺寸变化时直接对齐，不会从左上角滑过来。窄屏换行时底块同样能滑到第二行。
- 没有脚本时（没有 `data-ready`），由选中的标签自己画底色，仍然可用。
- Windows 对比度主题：底块隐藏，选中的标签改用系统色 `Highlight`。

## 不要
- 不要用于多选：多选的筛选用 `.fbtn` 和 `aria-pressed`。
- 不要给底块加拉伸、回弹或黏液效果；从旧位置平移到新位置就够了。
- 不要在切换时改变标签的字重或字号。
