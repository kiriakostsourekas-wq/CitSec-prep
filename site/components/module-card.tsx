import Link from "next/link";
import { followUpCount, type Module } from "@/lib/content";
import { ModuleProgress } from "./module-progress";

export function ModuleCard({ m }: { m: Module }) {
  const fu = followUpCount(m);
  return (
    <Link
      href={`/modules/${m.slug}`}
      className="group relative flex flex-col rounded-2xl border border-line bg-raised p-5 transition-colors hover:border-line-strong hover:bg-panel"
    >
      <div className="flex items-center gap-2">
        <span className="text-sm tabular-nums text-dim">{m.number}</span>
        {m.star && <span className="rounded-full bg-accent-soft px-2 py-0.5 text-xs font-medium text-accent">Must do</span>}
        <span className="ml-auto text-xs text-dim">{m.time}</span>
      </div>
      <h3 className="mt-3 font-serif text-lg font-semibold text-text group-hover:text-white">{m.title}</h3>
      <p className="mt-1.5 flex-1 text-sm leading-relaxed text-muted">{m.blurb}</p>
      <div className="mt-4 flex gap-3 text-xs tabular-nums text-dim">
        <span>{m.tasks.length} tasks</span>
        {fu > 0 && <span>{fu} follow-ups</span>}
      </div>
      <div className="mt-3">
        <ModuleProgress folder={m.folder} taskIds={m.tasks.map((t) => t.id)} />
      </div>
    </Link>
  );
}
