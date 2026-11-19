/**
 * eslint-rules.js · Kumo × Tight Surface 的 ESLint 规则（flat config）
 * 用法：在 eslint.config.js 里 `import { kumoTightSurface } from "./src/kumo-ts/eslint-rules.js";`
 *       然后把它放进导出的数组；adapters.tsx 自身用 ignores 排除。
 */
const banned = [
  "Chart", "TimeseriesChart", "SankeyChart", "BubbleMap", "ChoroplethMap", "GlobeMap",
  "CloudflareLogo", "Empty", "TableOfContents", "Code",
];

export const kumoTightSurface = {
  files: ["**/*.{jsx,tsx}"],
  ignores: ["**/kumo-ts/adapters.tsx"],
  rules: {
    "no-restricted-imports": ["error", {
      paths: [{
        name: "@cloudflare/kumo",
        importNames: banned,
        message: "Tight Surface：图表按原则 9 原生实现；Empty / TableOfContents / Code 改用 TS 的 EmptyState / SideToc / CodeBlock；不用品牌组件。",
      }],
      patterns: [
        { group: ["@cloudflare/kumo/components/chart*", "@cloudflare/kumo/components/{empty,table-of-contents,code,cloudflare-logo}"], message: "同上：这些 Kumo 组件不进入 Tight Surface 项目。" },
        { group: ["@cloudflare/kumo/styles/standalone"], message: "只用 Tailwind 路径（@cloudflare/kumo/styles/tailwind），适配层的构建期主题才会生效。" },
      ],
    }],
    "no-restricted-syntax": ["error",
      {
        selector: "JSXOpeningElement[name.name='Button'] > JSXAttribute[name.name='variant'][value.value=/^(primary|destructive|secondary-destructive)$/]",
        message: "强调与危险操作用 TsButton tone=\"primary\" / \"danger\"（琥珀 / bad 淡底）。",
      },
      {
        selector: "JSXOpeningElement[name.name='Badge']:not(:has(JSXAttribute[name.name='variant']))",
        message: "Badge 必须写 variant：不写时默认 primary（实底反色），只用 success / warning / error / info / secondary。",
      },
      {
        selector: "JSXOpeningElement[name.name='Badge'] > JSXAttribute[name.name='variant'][value.value=/^(primary|destructive|beta|outline|red|green|neutral|orange|purple|teal|teal-subtle|blue)$/]",
        message: "分类胶囊用 Chip（c=\"l0\"–\"l7\"）；Badge 只用 success / warning / error / info / secondary 这些状态变体。",
      },
    ],
  },
};
