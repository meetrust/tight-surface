<div align="center">

<sub><b>DESIGN SYSTEM</b></sub>

# Tight Surface

**暗夜与白昼两套主题的界面设计语言**

单一琥珀强调、信息优先，<br>用于 AI 应用、开发工具与数据叙事页面。<br>
*An info-first interface language with Night and Day themes and a single amber accent.*

![版本 v2.5.0](https://img.shields.io/badge/version-v2.5.0-ffb347?style=flat-square&labelColor=111723)

[原则 Principles](#设计原则--principles)&nbsp;· [概览 Overview](#概览--overview)&nbsp;· [目录 Contents](#目录--contents)&nbsp;· [使用 Usage](#使用--usage)&nbsp;· [版本 Versioning](#版本--versioning)

</div>

## 设计原则 · Principles

| # | 原则 Principle | 落成的规则 Rule |
|---|---|---|
| 1 | 信息优先<br><sub>Information first</sub> | 每个视觉元素都编码信息，每个数字都有出处<br><sub>Every mark encodes data, every number has a source</sub> |
| 2 | 紧凑<br><sub>Compact</sub> | 4px 间距阶梯，同类元素同一尺寸<br><sub>A 4px spacing scale and one size per element type</sub> |
| 3 | 平静<br><sub>Calm</sub> | 界面强调色只有琥珀和冰蓝，不用投影<br><sub>Amber and ice are the only UI accents, no shadows</sub> |
| 4 | 具触感<br><sub>Tactile</sub> | 悬停位移只给精确指针，触控目标不小于 24px<br><sub>Hover lift for fine pointers only, targets of 24px or more</sub> |
| 5 | 可访问性良好<br><sub>Accessible</sub> | 文字对比度 ≥4.5:1，axe-core 零违规<br><sub>Text contrast of 4.5:1 or more, zero axe-core violations</sub> |
| 6 | 同一系列，不同版式<br><sub>One family, many layouts</sub> | token、字体和尺寸相同，骨架和首屏可以不同<br><sub>Shared tokens, fonts and sizes with a free skeleton and hero</sub> |
| 7 | 可验证<br><sub>Verifiable</sub> | 每条规则都有脚本检查，320–1440px 全宽度验收<br><sub>Every rule is scripted and checked from 320 to 1440px</sub> |
| 8 | 中文排版优先<br><sub>Chinese typography first</sub> | 中英文之间加空格，全角标点，不留单字孤行<br><sub>Spaces between Chinese and Latin, full-width punctuation, no orphans</sub> |
| 9 | 原生实现优先<br><sub>Native first</sub> | 图表用 HTML、CSS 和内联 SVG，不引入图表库<br><sub>Charts in HTML, CSS and inline SVG, no chart libraries</sub> |
| 10 | README 原生可读<br><sub>Native README</sub> | 只用 GitHub 能渲染的写法，不放图片，中英对照<br><sub>GitHub-native markup, no images, bilingual</sub> |

<sub>每条原则在 [design-system/README.md](design-system/README.md) 里展开为可检验的规则。<br>Each principle expands into checkable rules in the design system README.</sub>

## 概览 · Overview

Tight Surface 是一套跨产品的界面设计语言：同一套 token 和组件，可以搭出手册、地图、仪表盘和 Agent 应用等不同版式，但一眼就能认出是同一个系列。默认主题是暗夜（Night）；在 `<html>` 上加 `data-theme="day"` 就切换到浅色的白昼（Day），组件和尺寸不变，只换颜色。

Tight Surface is a cross-product interface language. One set of tokens and components builds handbooks, maps, dashboards and agent apps that still read as one family. Night is the default theme; add `data-theme="day"` to `<html>` for the light Day theme, which changes colours only.

| **10** | **2** | **45** | **21** | **24** |
|---|---|---|---|---|
| 设计原则<br><sub>Principles</sub> | 主题<br><sub>Themes</sub> | 颜色 token<br><sub>Colour tokens</sub> | 组件<br><sub>Components</sub> | 已适配的 Kumo 组件<br><sub>Kumo components adapted</sub> |

## 目录 · Contents

| 文档 Document | 内容 What it covers |
|---|---|
| [README.md](design-system/README.md) | 设计原则、文案、颜色、字体、间距、图标、组件选择<br><sub>Principles, copy, colour, type, spacing, icons, component choice</sub> |
| [day-theme.md](design-system/day-theme.md) | 白昼主题的取值规则与对比度<br><sub>Day theme values and contrast</sub> |
| [interaction.md](design-system/interaction.md) | 聚焦高亮、指针类型与固定按钮<br><sub>Focus highlight, pointer types and pin toggles</sub> |
| [charts.md](design-system/charts.md) · [data-viz.md](design-system/data-viz.md) | 原生图表与数据可视化规则<br><sub>Native charts and data visualization rules</sub> |
| [qa.md](design-system/qa.md) | 交付验收清单，共七组<br><sub>The delivery checklist in seven groups</sub> |
| [github-readme.md](design-system/github-readme.md) | README 写法与检查脚本<br><sub>README rules and the checker script</sub> |
| [kumo.md](design-system/kumo.md) | Kumo 应用控件的适配层<br><sub>The Kumo adapter for app controls</sub> |
| [icons](design-system/icons) | Lucide 图标 sprite 与许可声明<br><sub>The Lucide icon sprite and its licence</sub> |
| [components](design-system/components) | 21 个组件的说明与预览<br><sub>Notes and previews for 21 components</sub> |
| [SKILL.md](skill/SKILL.md) | 同一套规则的 Claude 技能版本<br><sub>The same rules as a Claude skill</sub> |

## 使用 · Usage

在页面里依次引入 `tokens.css` 和 `components/bundle.css` 两个文件，组件的类名和写法见各组件的说明。用 React 写表单、浮层这类应用控件时，按 [kumo.md](design-system/kumo.md) 接入 Kumo 和适配层。图标统一用 Lucide 1.71.0：静态页面从 `icons/sprite.svg` 复制需要的图标，React 项目用 `lucide-react`，写法见 Icon 组件的说明。

Load `tokens.css` first, then `components/bundle.css`; class names and markup are in each component's notes. For app controls such as forms and overlays in React, add Kumo and the adapter as described in kumo.md. Icons are Lucide 1.71.0: static pages copy what they need from `icons/sprite.svg`, React projects use `lucide-react`, as the Icon notes describe.

```html
<!-- Night 是默认主题；加 data-theme="day" 切换到 Day -->
<html lang="zh-CN" data-theme="day">
<link rel="stylesheet" href="tight-surface/tokens.css">
<link rel="stylesheet" href="tight-surface/components/bundle.css">
```

修改组件或 token 后，在仓库根目录运行检查，全部零问题再提交：

After changing a component or a token, run the checks from the repository root and commit only when they report zero problems:

```bash
pip install playwright && python3 -m playwright install chromium
npm install                               # axe-core
python3 tools/check_components.py         # 22 previews, Night and Day, 1000 / 390 / 320 px
python3 tools/readme_check.py README.md   # README rules
```

交付用 Tight Surface 做的页面前，再跑一遍页面检查：占位内容、按钮文案、可见标签、主操作、并排对齐、行长、贴边、空白和章节间距，FAIL 为 0 才交付。

Before delivering a page built with Tight Surface, run the page check for leftover placeholders, generic button labels, visible field labels, one primary action per group, row alignment, line length, edge gaps, blank bands and section spacing; deliver only with zero FAILs.

```bash
python3 tools/page_check.py path/to/index.html   # or a URL such as http://localhost:5173/
```

## 版本 · Versioning

版本号遵循语义化版本：新增或修改规则和组件升次版本号，修正升修订号，删除或改名 token 升主版本号。每个版本的变化写在 [CHANGELOG.md](CHANGELOG.md)，同步到 Design System artifact 和技能的步骤见[维护与同步](docs/maintaining.md)。

Versions follow semantic versioning: new or changed rules and components bump the minor version, fixes bump the patch, and removing or renaming a token bumps the major version. Release notes are in the changelog, and the steps for syncing the artifact and the skill are in the maintenance guide.

## 项目结构 · Structure

```text
design-system/        设计系统本体，与 artifact 的 project/ 一一对应 · The design system, mirroring the artifact
  README.md           设计原则与视觉基础 · Principles and foundations
  tokens.json / .css  两套主题的 token · Tokens for both themes
  components/         bundle.css 与 21 个组件 · bundle.css and 21 components
  kumo/               Kumo 适配层与对照页 · Kumo adapter and demo
  icons/              Lucide 图标 sprite 与许可 · Lucide sprite and licence
  *.md                白昼主题、交互、图表、验收、README 规则 · Day, interaction, charts, QA, README rules
skill/SKILL.md        tight-surface-ui 技能 · The Claude skill
tools/                组件、页面和 README 检查，文件清单 · Component, page and README checks, manifest
docs/maintaining.md   版本与同步流程 · Release and sync steps
CHANGELOG.md          版本记录 · Release notes
```

## 同系列 · Companion projects

| 页面 Page | 版式 Layout | 仓库 Repository |
|---|---|---|
| [大模型可视化学习指南](https://meetrust.github.io/llm-visual-guide/)<br><sub>LLM Visual Guide</sub> | 手册版式，左侧目录<br><sub>Handbook layout with a side TOC</sub> | [llm-visual-guide](https://github.com/meetrust/llm-visual-guide) |
| [斯坦福 AI 课程地图](https://meetrust.github.io/stanford-ai-courses/)<br><sub>Stanford AI Course Map</sub> | 地图版式，顶部导航<br><sub>Map layout with a top nav</sub> | [stanford-ai-courses](https://github.com/meetrust/stanford-ai-courses) |

## 许可证 · License

代码、样式表、token 和脚本采用 [MIT](LICENSE) 许可；README、设计说明等原创文档采用 [CC BY 4.0](LICENSE-DOCS.md) 许可。图标来自 [Lucide](https://lucide.dev)，采用 ISC 许可，声明见 [LICENSE-lucide.txt](design-system/icons/LICENSE-lucide.txt)。

Code, stylesheets, tokens and scripts are under the MIT license; original documentation such as this README and the design notes is under CC BY 4.0. Icons come from Lucide under the ISC license; see the Lucide notice in the icons folder.
