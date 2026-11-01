// Typed access to content/generated/content.json (built from the repo by scripts/build-content.mjs).
import raw from "@/content/generated/content.json";

export type Block = { kind: "md"; md: string } | { kind: "fold"; summary: string; md: string };
export type Section = { heading: string; blocks: Block[] };
export type Doc = { slug: string; title: string; sections: Section[] };

export type Task = {
  id: string;
  func: string;
  title: string;
  part: string;
  doc: string;
  solution: string;
  hints: string[];
  hintNote: string;
};

export type Module = {
  folder: string;
  slug: string;
  number: string;
  title: string;
  short: string;
  time: string;
  blurb: string;
  tags: string[];
  star?: boolean;
  notes: Section[];
  followUps: Section[];
  parts: Record<string, string>;
  tasks: Task[];
  starter: string;
  files: string[];
  solutionFile: string;
};

type PlanItem = [string] | [string, string];
export type Content = {
  modules: Module[];
  guide: { main: Doc; cv: Doc; mlStats: Doc };
  cheatsheets: Doc[];
  mentalMath: Doc;
  plan: { sessions: { n: number; hours: number; items: PlanItem[] }[]; daily: PlanItem[]; fastTrack: PlanItem[] };
};

export const content = raw as unknown as Content;
export const modules = content.modules;

export const getModule = (slug: string) => modules.find((m) => m.slug === slug);
export const moduleByFolder = (folder: string) => modules.find((m) => m.folder === folder);

/** Questions folded in a module's follow-up sections. */
export const followUpCount = (m: Module) =>
  m.followUps.reduce((n, s) => n + s.blocks.filter((b) => b.kind === "fold").length, 0);

/** Where a study-plan item points on the site. */
export function planHref(key: string) {
  if (key === "guide") return "/guide";
  if (key === "mental-math") return "/mental-math";
  if (key.startsWith("guide/")) return "/" + key;
  const m = moduleByFolder(key);
  return m ? `/modules/${m.slug}` : "/";
}
export function planLabel(key: string) {
  if (key === "guide") return "Interview guide";
  if (key === "guide/cv") return "CV deep dive";
  if (key === "guide/ml-stats") return "ML & stats rapid-fire";
  if (key === "mental-math") return "Mental math";
  const m = moduleByFolder(key);
  return m ? `${m.number} · ${m.title}` : key;
}
