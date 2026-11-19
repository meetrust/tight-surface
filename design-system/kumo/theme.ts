/**
 * theme.ts · 同时维护 Tight Surface 的 data-theme 与 Kumo 的 data-mode。
 * Night 是默认值：<html data-mode="dark">；Day：<html data-theme="day" data-mode="light">。
 * 只改属性，不改任何尺寸（TS QA 第 2、3 组要求切主题后布局不变）。
 */
export type TsTheme = "night" | "day";

export function applyTheme(theme: TsTheme, root: HTMLElement = document.documentElement) {
  if (theme === "day") root.setAttribute("data-theme", "day");
  else root.removeAttribute("data-theme");
  root.setAttribute("data-mode", theme === "day" ? "light" : "dark");
}

/** 首次加载：页面同时提供两套主题时，按系统偏好决定初始主题。 */
export function initialTheme(): TsTheme {
  return window.matchMedia?.("(prefers-color-scheme: light)").matches ? "day" : "night";
}
