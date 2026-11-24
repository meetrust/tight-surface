胶囊家族：内容胶囊统一 26px（`h-pill`），图形节点里的微型标签统一 20px（`h-tag`）。

## 种类
- `.lvl`：层级 / 抽象层，实线描边 + 12% 淡底，颜色取该层数据色。
- `.rel`：课程或模块之间的关系（等宽字体，“A → B”），可点击。
- `.tk`：轨道标签，前面一个 7px 实心圆点。
- `.k-chip`：卡片小节的英文标签（MECHANISM / HIGHLIGHTS / OUTPUT），大写、字距 0.14em。
- `.st.v` / `.st.g` / `.st.no`：视频 / 代码 / 暂无，三种资源状态；`.st.no` 用虚线和 `faint` 文字。
- `.st.ok` / `.st.bad`：任务完成 / 失败（`good` / `bad` 文字加 45% 描边），配 `i-check` / `i-x` 和文字，用法见 TaskRow。
- `.specs`：键值规格条（LANG / SIZE / STARS），8px 圆角，不是胶囊。
- `.dn-badge` / `.dn-need`：节点内 20px 微型标签，前者实线着色，后者虚线、`dim` 文字（节点底是着色的，faint 在上面不到 4.5:1）。

## 规则
- 都要 `white-space: nowrap`，空间不够就截断加省略号，不能换行把高度撑高。
- 颜色只来自数据色 `l0`–`l7` 或 amber / ice；不要为胶囊另造颜色。
- 胶囊里的图标 12px。
