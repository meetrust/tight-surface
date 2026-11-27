全页暂停：页面上有自动开始、持续超过 5 秒的动效（流动的连线、循环播放的演示）时，放一个按钮把它们全部停住（WCAG 2.2.2）。

## 用法
- 一页只放一个：`<button class="act motion-pause" type="button" data-motion-pause>`，36px 操作按钮，放在顶部导航或第一张会动的图上方。图标用 `i-pause` / `i-play`，文字随状态在“暂停动画”和“继续动画”之间切换（不用 `aria-pressed`，可见文字本身就说明了按下后会发生什么）。
- 按下时在 `<html>` 上设置 `data-motion="paused"`：`bundle.css` 里的规则把全页的循环动画（`.flowing`、ThinkingTrace 的脉冲点、StatusRing 的旋转，以及带 `data-loop` 的元素）暂停在当前帧；同时派发 `ts:motion` 事件，脚本驱动的循环（`requestAnimationFrame`、计时器）收到后停下，或改为每秒刷新一次。
- 只停循环，不停入场：暂停时新出现的内容照常播放一个 `dur` 的入场，不会停在半透明的起点。页面自己写的 CSS 循环动画要加 `data-loop`，否则按钮停不住它，`page_check.py` 的 `motion-pause` 会报 FAIL。
- 页面切到后台（`document.visibilityState === "hidden"`）时，脚本循环自己停下，不用等这个按钮。
- 表示“进行中”的状态指示（ThinkingTrace 的脉冲点、StatusRing 的旋转）不另设按钮，但同样受这个按钮控制。
- 连线流动写成 `class="flowing"`：虚线 6 8，周期 `dur-loop`，linear。
- `prefers-reduced-motion: reduce` 下按钮隐藏：这时页面上已经没有会动的东西。

## 不要
- 不要每张图各放一个暂停按钮；一个按钮管全页。
- 不要只靠 `prefers-reduced-motion`：没改过系统设置的人同样需要能停下动效。
- 不要在暂停时隐藏或清空内容：暂停只冻结当前画面，图里的内容仍然可读。
