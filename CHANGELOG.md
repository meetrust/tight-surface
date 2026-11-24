# 更新记录 · Changelog

版本号遵循语义化版本。v2.3.0 是迁入 GitHub 时的第一个标签；更早的版本按 Design System artifact 的修改记录补记，没有对应的 Git 标签。

## [2.4.1] · 2026-11-24

### 修正
- `tokens.json` 里 `bad` 的用途说明仍写着 `i-cross`，改为 `i-x`。
- React 的描边规则补上 `nonScalingStroke`：lucide-react 1.71.0 里它取代了已弃用的 `absoluteStrokeWidth`，两个都不用。
- 连线图例的 `i-move-right`（裁剪过 viewBox）和 `i-move-right-dashed`（自定义变体）没有对应的 lucide-react 组件，React 页面里也用 sprite 画；Icon 说明、预览、设计说明、sprite 注释和技能都写明了这一点。
- Icon 预览：390px 下 `i-move-right-dashed` 的 id 折成两行，内联间距 10px、6px 也不在 4px 刻度上。改为 8px 间距、id 不换行、列宽至少 164px，320–1000px 下 id 和说明都在一行内。
- 2.4.0 的验收记录改为准确表述：9 个取自官方的图标与 lucide-static 1.71.0 逐字一致，连线图例的两个图标是有意的改动。

### 验收
- 从 GitHub 重新克隆后复查：22 个预览在 Night / Day、1000 / 390 / 320px 下全部通过（含 axe-core 与图标检查），README 检查 0 项；Kumo 对照页 lint、构建与 `kumo/qa/probe.py` 全部为 0，按钮图标实测 15 / 12px、描边 2；Artifact 与仓库文件逐个哈希一致。

## [2.4.0] · 2026-11-24

### 新增
- 默认图标库改为 Lucide，固定在 1.71.0（ISC 许可）：24×24 网格，描边 2，圆头圆角。静态页面从新增的 `icons/sprite.svg` 复制图标，React 项目用 `lucide-react@1.71.0` 并在根节点包 `<LucideProvider className="i">`；许可声明在 `icons/LICENSE-lucide.txt`。
- 图标 id 统一为 `i-` 加 Lucide 名，与 lucide-react 组件一一对应；新增 `i-chevron-right`、`i-download`。
- 操作按钮里的图标统一为 15px，`.act.sm` 里 12px；Kumo 按钮同样处理（`TsButton` 新增 `data-ts-size`）。
- `tools/check_components.py` 检查每个预览的 sprite 与 `icons/sprite.svg` 逐字一致、带 Lucide 许可注释；Kumo 的 ESLint 规则禁止应用代码引入其他图标库。

### 变更
- 旧图标换成 Lucide 图形，部分 id 改名：`i-ext` → `i-arrow-up-right`、`i-up` → `i-arrow-up`、`i-cross` → `i-x`、`i-to` → `i-move-right`、`i-to-opt` → `i-move-right-dashed`；`i-play`、`i-code`、`i-menu`、`i-check` 不改名，`i-play` 从实心变为描边。已交付的页面带着自己的旧 sprite，不受影响，迁移对照见 Icon 组件。
- `.i` 自带 Lucide 的描边样式；ThinkingTrace 的折叠箭头改用 `i-chevron-right`。

### 验收
- 22 个预览在 Night / Day、1000 / 390 / 320px 下全部通过（`tools/check_components.py`，含 axe-core 与新的图标检查）；sprite 里 9 个取自官方的图标与 lucide-static 1.71.0 逐字一致，连线图例的两个图标是有意的裁剪和变体。
- Kumo 对照页加入带图标的按钮后，`kumo/qa/probe.py` 在 Night / Day、1440 / 390px 下全部为 0；ESLint 规则测试通过。

## [2.3.1] · 2026-11-23

### 修正
- ApprovalCard 与 SideToc 的用法说明不再用“+”串联两项，行内代码与引号之间的间距统一。

### 验收
- 22 个预览在 Night / Day、1000 / 390 / 320px 下全部通过（`tools/check_components.py`，含 axe-core 扫描）。

## [2.3.0] · 2026-11-16

### 新增
- Kumo（`@cloudflare/kumo` 2.18.1）适配层：`kumo/` 目录与“Kumo 适配”一节，Kumo 的 54 个语义颜色 token 全部指向 Tight Surface token。
- `warn` 与 `pop` 两个 token；36px 操作按钮 `.act` 与 26px 紧凑版 `.act.sm`。
- 4 个 Agent 组件：ThinkingTrace、ToolCall、TaskRow、ApprovalCard。

### 修正
- 资源链接按钮的标签不换行；TaskRow 在窄屏重排；强调按钮悬停时的对比度；`pulse` 光晕随主题取色。
- Badge 必须写 `variant`；更正 `warn` 淡底与圆角的说明。

### 验收
- 22 个预览在 Night / Day、960 / 390 / 320px 下全部通过。

## [2.2.0] · 2026-11-08

### 新增
- 验收清单加入 320px 重排、axe-core 扫描和 `forced-colors` 截图三项。
- 会横向滚动的表格和代码块可以用键盘滚动；复制按钮在异步剪贴板被拦截时退回 `execCommand("copy")`。
- `i-check` / `i-cross` 图标，以及样式表里的字符图标扫描。

### 修正
- 手机单列网格改为 `minmax(0, 1fr)`，宽表不再在 320px 下撑出横向滚动。
- Windows 对比度主题下保留条形、图例色块和里程碑菱形。
- 视频按钮第二行与节点内虚线标签改用 `dim`，“暂无”胶囊改用 `faint`；用来固定某一项的按钮必须可切换（`aria-pressed`）。

## [2.1.0] · 2026-11-08

### 新增
- 白昼（Day）浅色主题：在 `<html>` 上加 `data-theme="day"` 切换。全部颜色 token 提供 Night / Day 两套取值，组件和尺寸不变，Night 仍是默认主题。

## [2.0.0] · 2026-11-04

### 新增
- 设计原则 v2：原有五条落成可检验的规则，新增“同一系列不同版式”“可验证”“中文排版优先”“原生实现优先”“README 原生可读”五条。
- 交互状态规范、交付验收清单、GitHub README 规则与检查脚本。
- Design System artifact「Tight Surface」。

## [1.0.0] · 2026-09-08

- 初版方向：紧凑、平静、具触感、信息优先、可访问性良好；包含 DESIGN.md、SKILL.md 与 tokens.css。
