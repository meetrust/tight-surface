人工确认卡：Agent 需要人来做决定时，把问题、可选方案和各自的置信度放在一张卡里，确认后才继续。

## 用法
- 结构：`<form class="approve" aria-labelledby>`：头部（eyebrow 写“NEEDS APPROVAL”，步数 `.approve-step` 写“1 / 3”）、问题 `.approve-q`（18px 700，一句话写清要决定什么）、选项组 `<fieldset class="approve-opts">`（带 `.sr-only` 的 `legend`）、底部按钮 `.approve-foot`。
- 选项 `.opt` 是 `<label>` 包住原生单选：方案名 `<b>`、影响说明 `<small>`、置信度 `.opt-conf`（Display，“置信度 82%”）。选中项：单选为琥珀实底加 `on-amber` 圆心，整张选项卡 9% 琥珀淡底、55% 琥珀描边。默认选中 Agent 推荐的方案，并排在第一位。
- 按钮用 36px 的 `.act`：“跳过”为 `.act.ghost`，次要操作为 `.act`，“确认”为 `.act.primary`（琥珀淡底）。会删除数据或花钱的决定，确认按钮用 `.act.danger` 并在问题里写明后果。
- 置信度只作参考：至少两个方案时才显示，按从高到低排列。
- React 项目里选项可以用 Kumo 的 `Radio.Group`，按钮用 `TsButton`，外观由适配层保持一致。

## 不要
- 不要用确认卡做纯信息提示；不需要人做决定时用 Banner。
- 不要超过 4 个选项；更多时先让 Agent 收窄。
- 不要把“确认”做成琥珀实底按钮；琥珀实底只表示选中。
