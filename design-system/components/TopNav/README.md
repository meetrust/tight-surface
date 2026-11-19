地图版式的吸顶导航：品牌两行字 + 带编号的章节链接，当前章节下方 2px 琥珀线。

## 用法
- 高 `nav-h`（60px），底色 `nav-glass` + 12px 背景模糊，底部 1px `rule`。
- 品牌：上行 `brand-mark`（11px、琥珀、字距 0.16em、大写英文），下行中文名（900）。
- 链接 40px 高，编号 11px `faint`；当前项文字 `ink`、编号 `amber`、底部琥珀线，并加 `aria-current`。
- 当前项随滚动更新（IntersectionObserver），平滑滚动在 `prefers-reduced-motion` 下关闭。
- ≤760px：品牌与链接分两行，链接行横向滚动、隐藏滚动条。

## 选择
章节 ≤7 个、单屏信息密度高的“地图 / 仪表”类页面用 TopNav；章节多、正文长的“手册”类页面用 SideToc。
