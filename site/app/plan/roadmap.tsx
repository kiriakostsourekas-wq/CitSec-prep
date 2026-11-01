"use client";
import Link from "next/link";
import { Markdown } from "@/components/markdown";
import { ProgressBar } from "@/components/workspace/status";
import { type Progress, taskKey, updateProgress, useProgress } from "@/lib/progress";

export type RoadmapItem = { key: string; note: string; href: string; label: string; folder?: string; taskIds?: string[] };

const done = (p: Progress, it: RoadmapItem) =>
  it.folder && it.taskIds ? it.taskIds.filter((id) => p.tasks[taskKey(it.folder!, id)] === "PASS").length : 0;

function Item({ it }: { it: RoadmapItem }) {
  const p = useProgress();
  const n = done(p, it);
  const total = it.taskIds?.length ?? 0;
  return (
    <Link href={it.href} className="group flex items-center gap-4 rounded-lg px-3 py-2.5 hover:bg-panel">
      <span
        className={`grid size-5 shrink-0 place-items-center rounded-full border text-[10px] ${
          total && n === total ? "border-pass bg-pass text-bg" : "border-line-strong text-transparent"
        }`}
      >
        ✓
      </span>
      <span className="min-w-0 flex-1">
        <span className="block text-[15px] text-text group-hover:text-white">{it.label}</span>
        {it.note && <span className="block text-[13px] text-dim">{it.note}</span>}
      </span>
      {total > 0 && (
        <span className="flex w-28 shrink-0 items-center gap-2">
          <ProgressBar value={n} total={total} className="flex-1" />
          <span className="text-xs tabular-nums text-dim">
            {n}/{total}
          </span>
        </span>
      )}
    </Link>
  );
}

export function Roadmap({
  sessions,
  daily,
  fastTrack,
  checklist,
}: {
  sessions: { n: number; hours: number; items: RoadmapItem[] }[];
  daily: RoadmapItem[];
  fastTrack: RoadmapItem[];
  checklist: string[];
}) {
  const p = useProgress();
  const setFast = (fast: boolean) => updateProgress((x) => ({ ...x, fastTrack: fast }));

  return (
    <div className="mt-10 grid gap-10 lg:grid-cols-[minmax(0,1fr)_320px]">
      <div>
        <div className="mb-6 inline-flex rounded-lg border border-line bg-raised p-1 text-sm">
          {[
            [false, `Full plan, about ${sessions.reduce((h, s) => h + s.hours, 0)} h`],
            [true, "Fast track, about 7 h"],
          ].map(([v, label]) => (
            <button
              key={String(v)}
              type="button"
              onClick={() => setFast(v as boolean)}
              className={`rounded-md px-3 py-1.5 ${p.fastTrack === v ? "bg-panel-2 text-text" : "text-muted hover:text-text"}`}
            >
              {label as string}
            </button>
          ))}
        </div>

        {p.fastTrack ? (
          <div className="rounded-2xl border border-line bg-raised p-2">
            {fastTrack.map((it, i) => (
              <Item key={i} it={it} />
            ))}
          </div>
        ) : (
          <ol className="relative space-y-5 border-l border-line pl-6">
            {sessions.map((s) => (
              <li key={s.n} className="relative">
                <span className="absolute -left-[33px] top-3 grid size-4 place-items-center rounded-full border border-line-strong bg-bg text-[10px] tabular-nums text-muted">
                  {s.n}
                </span>
                <div className="rounded-2xl border border-line bg-raised p-2">
                  <div className="flex items-baseline justify-between px-3 pb-1 pt-2">
                    <span className="label">Session {s.n}</span>
                    <span className="text-xs tabular-nums text-dim">{s.hours} h</span>
                  </div>
                  {s.items.map((it, i) => (
                    <Item key={i} it={it} />
                  ))}
                </div>
              </li>
            ))}
          </ol>
        )}
        <div className="mt-5 rounded-2xl border border-line bg-raised p-2">
          <div className="px-3 pb-1 pt-2">
            <span className="label">Every day</span>
          </div>
          {daily.map((it, i) => (
            <Item key={i} it={it} />
          ))}
        </div>
        <p className="mt-6 text-sm text-dim">
          Extra time? Do the bonuses (06 D2–D3, 09 D1–D2), reset whatever felt hardest and redo it, then redo the mock.
        </p>
      </div>

      <aside className="space-y-4 lg:sticky lg:top-24 lg:self-start">
        <div className="rounded-2xl border border-line bg-raised p-5">
          <div className="label text-accent">The day before / the day of</div>
          <ul className="mt-3 space-y-2.5">
            {checklist.map((c, i) => {
              const k = `day:${i}`;
              const on = !!p.checklist[k];
              return (
                <li key={k}>
                  <label className="flex cursor-pointer gap-3 text-sm">
                    <input
                      type="checkbox"
                      checked={on}
                      onChange={() => updateProgress((x) => ({ ...x, checklist: { ...x.checklist, [k]: !on } }))}
                      className="mt-1 size-4 shrink-0 accent-[var(--accent)]"
                    />
                    <span className={on ? "text-dim line-through" : "text-muted"}>
                      <Markdown md={c} className="text-sm [&_p]:inline" />
                    </span>
                  </label>
                </li>
              );
            })}
          </ul>
        </div>
      </aside>
    </div>
  );
}
