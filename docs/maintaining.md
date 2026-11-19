# 维护与同步

这个仓库是 Tight Surface 唯一的修改入口。Design System artifact「Tight Surface」是可浏览的组件展示页，`skill/SKILL.md` 是给 Claude 用的技能版本，三处内容要保持一致。

## 对应关系

| 仓库 | 同步到 |
|---|---|
| `design-system/<路径>` | Design System artifact 的 `project/<路径>` |
| `skill/SKILL.md` | tight-surface-ui 技能 |

Artifact 里由类型提供的文件（`SKILL.md`、`artifact-type/`、`index.html`）不进仓库，也不需要同步。

## 发布一个版本

1. 在 `design-system/` 里修改；新增或改动的规则同时写进 `skill/SKILL.md`。
2. 运行 `python3 tools/check_components.py` 和 `python3 tools/readme_check.py README.md`，两者都是零问题。
3. 按语义化版本定版本号：在 `CHANGELOG.md` 顶部写本次变化，更新 README 的版本徽章，把 `design-system/design-system.json` 的 `lastChange` 改成本次说明。
4. 提交，打带说明的标签（`git tag -a v2.4.0 -m "..."`），推送分支和标签。
5. 同步 artifact：把改动的文件发布到 `project/` 下的同名路径，`design-system.json` 最后发布。
6. 运行 `python3 tools/manifest.py`，把输出的 sha256 与 artifact 的文件清单逐行对照，全部一致才算同步完成。
7. `skill/SKILL.md` 有改动时，通过技能更新卡片保存。

## 反向同步

如果直接在 artifact 里改过文件，先把这些文件取回仓库（同样按 sha256 核对），提交之后再开始下一次修改，避免两边分叉。
