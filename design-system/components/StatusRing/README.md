状态环：任务和工具调用的状态图标。排队时是虚线环，进行中画进度弧（不知道进度时匀速旋转），完成时弧画满后画出对勾，失败时画出叉。状态改变时逐段过渡，不整体替换。

## 用法
- 结构：一个 24 网格的内联 `<svg class="ring" viewBox="0 0 24 24" data-state="queued|running|done|failed" aria-hidden="true">`，里面依次是 `.ring-track`、`.ring-arc` 两个圆（`r="10"`、`pathLength="100"`），对勾 `.ring-mark.ring-ok`、叉的两笔 `.ring-mark.ring-no`（`pathLength="1"`）。完整写法见预览。几何取自 Lucide 的 circle-dashed、circle-check、circle-x（描边 2，圆头圆角），自绘是为了能逐段过渡。
- 进度：`style="--p: 68"` 让弧画到 68%；不写 `--p` 时弧长 25%，以 `dur-loop` 匀速旋转，表示进行中但不知道进度。
- 状态切换只改 `data-state` 和 `--p`，过渡由 CSS 完成：弧长 `dur`；完成或失败时，记号等弧画满（延迟一个 `dur`）再用一个 `dur` 画出。
- 颜色：排队 `faint`、进行中 `amber`、完成 `good`、失败 `bad`；放在状态胶囊 `.st` 里时跟随胶囊的文字色。尺寸：胶囊和工具胶囊里 12px，单独使用 15px。
- 状态图标只是辅助：旁边一定有文字（“排队”“进行中 68%”“已完成”“失败”），或 ToolCall 里的 `.sr-only` 状态文字。状态变化需要播报时，用页面里已有的 `role="status"` 播报一次。
- 旋转受全页暂停（PauseMotion）控制；减弱动效下弧停在 25%，状态切换直接到位。

## 不要
- 不要只靠环的颜色表达状态。
- 不要在失败时抖动、完成时撒花；画出记号就是全部反馈。
- 不要把进度弧和 TaskRow 的进度条写成不同的数值：两者取同一个百分比。
