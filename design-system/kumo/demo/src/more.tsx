import * as React from "react";
import {
  Autocomplete, Breadcrumbs, Combobox, CommandPalette, DatePicker, Pagination, Sidebar, Slider, TagInput, Toasty,
  useKumoToastManager,
} from "@cloudflare/kumo";
import { zhCN } from "react-day-picker/locale";
import { TsButton } from "./kumo-ts/adapters";

const params = new URLSearchParams(location.search);
const open = params.get("open");
const PAGINATION_LABELS = { navigation: "分页", firstPage: "第一页", previousPage: "上一页", nextPage: "下一页", lastPage: "最后一页", pageNumber: "页码", pageSize: "每页条数" };
const models = ["claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5", "glm-5.3", "deepseek-v4"];

type Cmd = { id: string; title: string };
type Grp = { id: string; label: string; items: Cmd[] };
const groups: Grp[] = [
  { id: "c", label: "命令", items: [{ id: "n", title: "新建会话" }, { id: "s", title: "打开设置" }] },
  { id: "p", label: "页面", items: [{ id: "u", title: "用量面板" }, { id: "l", title: "调用记录" }] },
];

function ToastButton() {
  const m = useKumoToastManager();
  const fired = React.useRef(false);
  const fire = () => {
    m.add({ title: "额度将尽", description: "本月 Token 额度已用 86%。", variant: "warning" });
    m.add({ title: "已保存", description: "路由策略已更新。", variant: "success" });
  };
  React.useEffect(() => { if (open === "toast" && !fired.current) { fired.current = true; fire(); } });
  return <TsButton onClick={fire}>弹出通知</TsButton>;
}

export function MoreKumo() {
  const [combo, setCombo] = React.useState<string | null>("claude-opus-5-5");
  const [page, setPage] = React.useState(2);
  const [tags, setTags] = React.useState<string[]>(["检索", "评测"]);
  const [date, setDate] = React.useState<Date>(new Date(2026, 10, 16));
  const [palette, setPalette] = React.useState(open === "palette");
  const [q, setQ] = React.useState("");
  const filtered = groups
    .map((g) => ({ ...g, items: g.items.filter((i) => i.title.includes(q)) }))
    .filter((g) => g.items.length);

  return (
    <section id="more">
      <p className="eyebrow">MORE CONTROLS</p>
      <div className="grid2">
        <div className="cardp" style={{ display: "grid", gap: 16, alignContent: "start" }}>
          <Breadcrumbs>
            <Breadcrumbs.Link href="#more">工作台</Breadcrumbs.Link>
            <Breadcrumbs.Separator />
            <Breadcrumbs.Link href="#more">模型路由</Breadcrumbs.Link>
            <Breadcrumbs.Separator />
            <Breadcrumbs.Current>调用记录</Breadcrumbs.Current>
          </Breadcrumbs>
          <Combobox label="模型" value={combo} onValueChange={(v) => setCombo(v as string | null)} items={models} defaultOpen={open === "combobox"}>
            <Combobox.TriggerInput placeholder="如 claude-sonnet-5-5" clearLabel="清除选择" showOptionsLabel="展开选项" />
            <Combobox.Content>
              <Combobox.Empty>没有匹配的模型。</Combobox.Empty>
              <Combobox.List>
                {(item: string) => <Combobox.Item key={item} value={item}>{item}</Combobox.Item>}
              </Combobox.List>
            </Combobox.Content>
          </Combobox>
          <Autocomplete items={models} label="搜索模型" defaultOpen={open === "autocomplete"}>
            <Autocomplete.InputGroup placeholder="输入模型名称" />
            <Autocomplete.Content>
              <Autocomplete.List>
                {(item: string) => <Autocomplete.Item key={item} value={item}>{item}</Autocomplete.Item>}
              </Autocomplete.List>
            </Autocomplete.Content>
          </Autocomplete>
          <TagInput label="标签" description="回车添加，最多 5 个。" placeholder="添加标签" value={tags} onValueChange={setTags} maxValues={5} />
          <Slider label="温度" defaultValue={40} className="w-full max-w-72" />
          <Pagination page={page} setPage={setPage} perPage={10} totalCount={86} labels={PAGINATION_LABELS} text={() => `第 ${(page - 1) * 10 + 1}–${Math.min(page * 10, 86)} 条，共 86 条`} />
          <div className="row">
            <Toasty><ToastButton /></Toasty>
            <TsButton onClick={() => setPalette(true)}>命令面板</TsButton>
          </div>
        </div>
        <div className="cardp" style={{ display: "grid", gap: 16, alignContent: "start" }}>
          <DatePicker className="p-3" mode="single" locale={zhCN} selected={date} onChange={(d) => d && setDate(d)} />
          <div style={{ height: 260, position: "relative", border: "1px solid var(--rule)", borderRadius: 12, overflow: "hidden" }}>
            <Sidebar.Provider contained defaultOpen className="h-full min-h-0!">
              <Sidebar>
                <Sidebar.Content>
                  <Sidebar.Group>
                    <Sidebar.GroupLabel>工作台</Sidebar.GroupLabel>
                    <Sidebar.Menu>
                      <Sidebar.MenuButton active>会话</Sidebar.MenuButton>
                      <Sidebar.MenuButton>用量</Sidebar.MenuButton>
                      <Sidebar.MenuButton>设置</Sidebar.MenuButton>
                    </Sidebar.Menu>
                  </Sidebar.Group>
                </Sidebar.Content>
              </Sidebar>
            </Sidebar.Provider>
          </div>
        </div>
      </div>
      <CommandPalette.Root
        open={palette}
        onOpenChange={setPalette}
        items={filtered}
        value={q}
        onValueChange={setQ}
        itemToStringValue={(g: Grp) => g.label}
        onSelect={() => setPalette(false)}
        getSelectableItems={(gs: Grp[]) => gs.flatMap((g) => g.items)}
      >
        <CommandPalette.Input placeholder="输入命令或搜索" />
        <CommandPalette.List>
          <CommandPalette.Results>
            {(g: Grp) => (
              <CommandPalette.Group key={g.id} items={g.items}>
                <CommandPalette.GroupLabel>{g.label}</CommandPalette.GroupLabel>
                <CommandPalette.Items>
                  {(i: Cmd) => <CommandPalette.Item key={i.id} value={i}>{i.title}</CommandPalette.Item>}
                </CommandPalette.Items>
              </CommandPalette.Group>
            )}
          </CommandPalette.Results>
        </CommandPalette.List>
      </CommandPalette.Root>
    </section>
  );
}
