思考轨迹：把 Agent 的推理、检索、编码步骤收在一个可折叠的面板里，进行中展开，完成后收起成一行。

## 用法
- 结构：`<details class="trace">` > `<summary>`（状态点 `.trace-dot` + 标题 `.trace-title` + 用时 `.trace-time` + 摘要 `.trace-meta` + 箭头 `.trace-caret`）+ `<ol class="trace-steps">`。
- 状态：进行中写 `data-state="running"` 和 `open`，标题写“思考中”，状态点是带 `pulse` 的琥珀点；完成后去掉 `data-state` 和 `open`，标题改为“已思考”，状态点变 `faint`。
- 每一步：分类胶囊 `.tk`（步骤 `l0`、检索 `l1`、推理 `l2`、编码 `l6`，整个产品固定）+ 一句话 + 用时 `.t`。分类名固定两个字，胶囊列宽 64px。各步用时之和等于标题里的总用时。
- 用时用 Display 字体和 tabular-nums，格式“12.4 s”；摘要写“4 步 · 1 次检索”。
- 流式更新：用时文字每秒最多改一次；完成时在页面已有的 `role="status"` 区域里报一次“思考完成，用时 12.4 秒”，不要给 `summary` 加 `aria-live`。
- React 项目可以用 Kumo 的 Collapsible 做外壳，样式仍用本组件的类名。

## 不要
- 不要把思考轨迹和最终回答放在同一个面板里；回答是正文，轨迹是附注。
- 不要逐字流式刷新步骤文字导致高度跳动；一步完成后再整句插入。
- 分类色只编码步骤类型，不表示成功或失败。
