# 更新记录 · Changelog

版本号遵循语义化版本。v2.3.0 是迁入 GitHub 时的第一个标签；更早的版本按 Design System artifact 的修改记录补记，没有对应的 Git 标签。

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
