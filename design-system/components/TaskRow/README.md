任务行：Agent 的多步任务清单，每行一个任务，带编号、标题、说明、状态胶囊，进行中的任务显示进度条。

## 用法
- 结构：`<ol class="tasks">` > `<li class="task" data-state="done|running|failed|queued">`：编号 `.task-no`（两位数，Display）+ `.task-main`（标题 `.task-title`、说明 `.task-note`、可选进度条 `.task-bar`）+ `.task-side`（状态胶囊和操作）。
- 状态胶囊（26px）：完成 `.st.ok`（`good`），进行中 `.st.v`（琥珀，写“进行中 68%”），失败 `.st.bad`（`bad`），排队 `.st.no`（虚线、`faint`）。胶囊里的图标是 StatusRing（12px，`data-state` 与任务一致，进行中写 `--p`），状态变化时只改 `data-state` 和 `--p`，环会逐段过渡。胶囊里一定有文字，颜色不单独表达状态。
- 进行中：编号变 `amber`；进度条 8px，琥珀填充，`role="progressbar"` 加 `aria-valuenow` 和含任务名的 `aria-label`，宽度写 `style="--v: 68"`，数值变化时宽度过渡 `dur`；进度条、进度弧和胶囊里的百分比取同一个数，百分比可以用 NumberRoll。
- 失败：说明里写清原因和已重试次数，旁边放 26px 的 `.act.sm`“重试”。
- 标题单行省略；说明写数量时带单位（“12 个模型 · 1,284 条记录”）。
- 窄屏（≤760px）：状态胶囊和操作移到说明下方，标题占满整行，避免被截断。

## 不要
- 不要用进度条和状态环以外的动画表示进行中；状态点的 `pulse` 只用在 ThinkingTrace。
- 不要在同一列表里混用 26px 以外的状态胶囊。
- 不要把子任务嵌套成第二层列表；需要时拆成两组 TaskRow，组名用 SectionHead。
