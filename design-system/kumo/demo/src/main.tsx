import * as React from "react";
import { createRoot } from "react-dom/client";
import { LucideProvider, Download, RotateCcw } from "lucide-react";
import {
  Badge, Banner, Button, Checkbox, Dialog, DropdownMenu, Input, Meter, Radio, Select, Switch, Table, Tabs,
} from "@cloudflare/kumo";
import "./app.css";
import { Chip, FilterButton, ResourceButton, TsButton } from "./kumo-ts/adapters";
import { applyTheme, type TsTheme } from "./kumo-ts/theme";
import { MoreKumo } from "./more";

const params = new URLSearchParams(location.search);
const startTheme: TsTheme = params.get("theme") === "day" ? "day" : "night";
applyTheme(startTheme);

const rows = [
  { id: "M01", name: "检索增强", owner: "Agent 组", tok: "1,240", st: "ok" },
  { id: "M02", name: "工具调用", owner: "平台组", tok: "860", st: "warn" },
  { id: "M03", name: "长上下文", owner: "研究组", tok: "2,015", st: "bad" },
];

function App() {
  const [theme, setTheme] = React.useState<TsTheme>(startTheme);
  const [f1, setF1] = React.useState(true);
  const [f2, setF2] = React.useState(false);
  const [chk, setChk] = React.useState(true);
  const [chk2, setChk2] = React.useState(false);
  const [sw, setSw] = React.useState(true);
  const [sw2, setSw2] = React.useState(false);
  const [radio, setRadio] = React.useState("night");
  const [sel, setSel] = React.useState("a");

  return (
    <div className="isolate ts-grid-bg min-h-dvh">
      <main className="demo">
        <h1 className="sr-only">Kumo × Tight Surface 适配验证</h1>
        <header className="sh">
          <span className="sh-idx">00</span>
          <h2>Kumo × Tight Surface 适配验证</h2>
          <button
            className="fbtn"
            aria-pressed={theme === "day"}
            onClick={() => { const t = theme === "day" ? "night" : "day"; applyTheme(t); setTheme(t); }}
          >
            白昼主题
          </button>
        </header>

        <section id="buttons">
          <p className="eyebrow">BUTTONS</p>
          <div className="grid2">
            <div className="cardp" data-col="ts">
              <p className="lab">TIGHT SURFACE NATIVE</p>
              <div className="row">
                <a className="btn" href="#x" data-probe="ts-btn"><span className="lbl">课程主页<small>官方站点</small></span></a>
                <a className="btn video" href="#x" data-probe="ts-btn-video"><span className="lbl">观看视频<small>2024 版</small></span></a>
              </div>
              <div className="row" style={{ marginTop: 12 }}>
                <button className="fbtn" aria-pressed="true" data-probe="ts-fbtn-on">全部</button>
                <button className="fbtn" aria-pressed="false" data-probe="ts-fbtn-off">进行中</button>
              </div>
            </div>
            <div className="cardp" data-col="kumo">
              <p className="lab">KUMO + ADAPTER</p>
              <div className="row">
                <ResourceButton title="课程主页" note="官方站点" href="#x" />
                <TsButton tone="primary" data-probe="k-primary">保存更改</TsButton>
                <TsButton data-probe="k-secondary">取消</TsButton>
                <TsButton tone="danger" data-probe="k-danger">删除</TsButton>
                <TsButton tone="ghost">更多</TsButton>
                <TsButton icon={<Download />} data-probe="k-icon">导出 CSV</TsButton>
                <TsButton size="sm" icon={<RotateCcw />} data-probe="k-icon-sm">重试</TsButton>
                <TsButton size="sm" data-probe="k-sm">小号</TsButton>
                <TsButton disabled>禁用</TsButton>
              </div>
              <div className="row" style={{ marginTop: 12 }}>
                <FilterButton pressed={f1} onPressedChange={setF1} data-probe="k-filter-on">全部</FilterButton>
                <FilterButton pressed={f2} onPressedChange={setF2} data-probe="k-filter-off">进行中</FilterButton>
                {/* eslint-disable-next-line no-restricted-syntax -- 故意保留未适配写法，检查适配层的兜底规则 */}
                <Button variant="primary" data-probe="k-raw-primary">未适配 primary</Button>
              </div>
            </div>
          </div>
        </section>

        <section id="forms">
          <p className="eyebrow">FORMS</p>
          <div className="grid2">
            <div className="cardp">
              <Input label="模型名称" placeholder="例如 claude-opus-5-5" description="用于路由与计费口径" data-probe="k-input" />
              <div style={{ marginTop: 16 }}>
                <Select label="部署区域" className="w-[240px]" value={sel} onValueChange={(v) => setSel((v as string) ?? "a")}
                  items={{ a: "欧洲 · 马德里", b: "美国 · 俄勒冈", c: "亚洲 · 东京" }} />
              </div>
            </div>
            <div className="cardp">
              <div className="row" style={{ gap: 24 }}>
                <Checkbox label="启用缓存" checked={chk} onCheckedChange={setChk} />
                <Checkbox label="记录日志" checked={chk2} onCheckedChange={setChk2} />
              </div>
              <div className="row" style={{ gap: 24, marginTop: 16 }}>
                <Switch label="流式输出" checked={sw} onCheckedChange={setSw} />
                <Switch label="自动重试" checked={sw2} onCheckedChange={setSw2} />
              </div>
              <div style={{ marginTop: 16 }}>
                <Radio.Group legend="界面主题" value={radio} onValueChange={(v) => setRadio(v as string)}>
                  <Radio.Item label="暗夜" value="night" />
                  <Radio.Item label="白昼" value="day" />
                </Radio.Group>
              </div>
            </div>
          </div>
          <div className="cardp" style={{ marginTop: 24 }}>
            <Tabs variant="underline" selectedValue="t1" tabs={[{ value: "t1", label: "概览" }, { value: "t2", label: "调用记录" }, { value: "t3", label: "设置" }]} />
            <div style={{ marginTop: 16 }}>
              <Tabs variant="segmented" selectedValue="d" tabs={[{ value: "d", label: "日" }, { value: "w", label: "周" }, { value: "m", label: "月" }]} />
            </div>
          </div>
        </section>

        <section id="status">
          <p className="eyebrow">STATUS</p>
          <div className="grid2">
            <div className="cardp" style={{ display: "grid", gap: 12 }}>
              <Banner title="版本更新" description="新的路由策略已就绪，可以在设置中启用。" />
              <Banner variant="alert" title="额度将尽" description="本月 Token 额度已用 86%。" />
              <Banner variant="error" title="保存失败" description="网络中断，请重试。" />
            </div>
            <div className="cardp">
              <p className="lab">STATUS BADGE</p>
              <div className="row">
                <Badge variant="success">运行中</Badge>
                <Badge variant="warning">排队</Badge>
                <Badge variant="error">失败</Badge>
                <Badge variant="secondary">草稿</Badge>
              </div>
              <p className="lab" style={{ marginTop: 16 }}>CHIP · NATIVE VS ADAPTER</p>
              <div className="row">
                <span className="lvl" style={{ "--c": "var(--l3)" } as React.CSSProperties} data-probe="ts-lvl">L3 · 中级</span>
                <span data-probe="k-chip"><Chip c="l3">L3 · 中级</Chip></span>
                <Chip c="l1">检索</Chip>
                <Chip c="l6">评测</Chip>
              </div>
              <div style={{ marginTop: 16 }}>
                <Meter label="Token 额度" value={86} showValue />
              </div>
            </div>
          </div>
        </section>

        <section id="tables">
          <p className="eyebrow">TABLES</p>
          <div className="grid2">
            <div className="tbl" data-probe="ts-tbl">
              <table>
                <thead><tr><th>编号</th><th>模块</th><th>Token</th></tr></thead>
                <tbody>{rows.map((r) => <tr key={r.id}><th>{r.id}</th><td>{r.name}</td><td>{r.tok}</td></tr>)}</tbody>
              </table>
            </div>
            <div className="tbl" data-probe="k-tbl">
              <Table>
                <Table.Header><Table.Row><Table.Head>编号</Table.Head><Table.Head>模块</Table.Head><Table.Head>Token</Table.Head></Table.Row></Table.Header>
                <Table.Body>{rows.map((r) => <Table.Row key={r.id}><Table.Cell>{r.id}</Table.Cell><Table.Cell>{r.name}</Table.Cell><Table.Cell>{r.tok}</Table.Cell></Table.Row>)}</Table.Body>
              </Table>
            </div>
          </div>
        </section>

        <section id="overlays">
          <p className="eyebrow">OVERLAYS</p>
          <div className="row">
            <Dialog.Root defaultOpen={params.get("open") === "dialog"}>
              <Dialog.Trigger render={(p) => <Button {...p}>打开对话框</Button>} />
              <Dialog className="p-8" data-probe="k-dialog">
                <Dialog.Title className="text-xl font-bold">删除模块 M03？</Dialog.Title>
                <Dialog.Description className="mt-2 text-kumo-subtle">删除后调用记录保留 30 天，可以在回收站恢复。</Dialog.Description>
                <div className="row" style={{ marginTop: 24, justifyContent: "flex-end" }}>
                  <Dialog.Close render={(p) => <TsButton {...(p as object)}>取消</TsButton>} />
                  <TsButton tone="danger">删除</TsButton>
                </div>
              </Dialog>
            </Dialog.Root>
            <DropdownMenu defaultOpen={params.get("open") === "menu"}>
              <DropdownMenu.Trigger render={<Button>视图选项</Button>} />
              <DropdownMenu.Content>
                <DropdownMenu.Item>按时间排序</DropdownMenu.Item>
                <DropdownMenu.Item>按用量排序</DropdownMenu.Item>
                <DropdownMenu.Item>导出 CSV</DropdownMenu.Item>
              </DropdownMenu.Content>
            </DropdownMenu>
          </div>
        </section>

        <MoreKumo />

        <footer style={{ marginTop: 64, paddingTop: 16, borderTop: "1px solid var(--rule)", fontSize: 12, color: "var(--faint)", lineHeight: 1.7 }}>
          核对日期 2026-11-16 · @cloudflare/kumo 2.18.1 · Tailwind CSS 4.3.5 · 左列为 Tight Surface 原生组件，右列为 Kumo 组件加适配层
          <br />与 Tight Surface 设计系统同一系列
        </footer>
      </main>
    </div>
  );
}

createRoot(document.getElementById("root")!).render(
  <LucideProvider className="i">
    <App />
  </LucideProvider>,
);
