/**
 * adapters.tsx · Kumo × Tight Surface 薄适配组件
 * 只做两件事：把 TS 语义映射到 Kumo 的公开 props，再打上 data-ts-variant，
 * 视觉全部由 kumo-tight-surface.css 决定。不复制、不改写 Kumo 源码。
 */
import * as React from "react";
import { Badge, Button, LinkButton } from "@cloudflare/kumo";

type KumoButtonProps = React.ComponentProps<typeof Button>;

/** 操作按钮：tone 对应 TS 的三种强调。尺寸只用 sm(26) / base(36)。 */
export function TsButton({
  tone = "default",
  size = "base",
  ...props
}: Omit<KumoButtonProps, "variant" | "size"> & {
  tone?: "default" | "primary" | "danger" | "ghost";
  size?: "sm" | "base";
}) {
  const variant =
    tone === "primary" ? "primary" : tone === "danger" ? "destructive" : tone === "ghost" ? "ghost" : "secondary";
  const ts = tone === "primary" ? "primary" : tone === "danger" ? "danger" : undefined;
  return <Button {...(props as KumoButtonProps)} variant={variant} size={size} data-ts-variant={ts} data-ts-size={size} />;
}

/** 筛选按钮 = TS .fbtn：36px 胶囊，aria-pressed 表示选中。 */
export function FilterButton({
  pressed,
  onPressedChange,
  children,
  ...props
}: Omit<KumoButtonProps, "variant" | "size" | "shape" | "onClick"> & {
  pressed: boolean;
  onPressedChange: (next: boolean) => void;
}) {
  return (
    <Button
      {...(props as KumoButtonProps)}
      variant="outline"
      size="base"
      aria-pressed={pressed}
      data-ts-variant="filter"
      onClick={() => onPressedChange(!pressed)}
    >
      {children}
    </Button>
  );
}

/** 资源链接按钮 = TS .btn：48px，两行标签（主标题 + small 说明）。 */
export function ResourceButton({
  title,
  note,
  href,
  external = true,
}: {
  title: string;
  note?: string;
  href: string;
  external?: boolean;
}) {
  return (
    <LinkButton
      href={href}
      variant="secondary"
      data-ts-variant="resource"
      {...(external ? { target: "_blank", rel: "noopener" } : {})}
    >
      <span className="flex min-w-0 flex-col items-start">
        <span>{title}</span>
        {note ? (
          <small className="truncate text-[12px] leading-[1.3] font-normal text-(--faint)">{note}</small>
        ) : null}
      </span>
    </LinkButton>
  );
}

/** 内容胶囊 = TS .lvl：26px，12% 淡底 + 同色描边与文字。c 取 l0–l7。 */
export function Chip({
  c = "l1",
  children,
}: {
  c?: "l0" | "l1" | "l2" | "l3" | "l4" | "l5" | "l6" | "l7";
  children: React.ReactNode;
}) {
  return (
    <span style={{ "--c": `var(--${c})` } as React.CSSProperties} className="inline-flex">
      <Badge
        variant="outline"
        className="h-(--h-pill) gap-1.5 border-(--c) bg-[color-mix(in_srgb,var(--c)_12%,transparent)] px-[10px] py-0 text-[12px] leading-[1.2] font-normal text-(--c)"
      >
        {children}
      </Badge>
    </span>
  );
}
