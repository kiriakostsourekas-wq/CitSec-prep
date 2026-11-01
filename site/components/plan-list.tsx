"use client";
import Link from "next/link";
import { Fragment } from "react";
import { type Progress, taskKey, useProgress } from "@/lib/progress";

export type PlanEntry = { href: string; label: string; note: string; folder?: string; taskIds?: string[] };
export type PlanRow = { key: string; when: string; hours: string; entries: PlanEntry[] };

const complete = (p: Progress, e: PlanEntry) =>
  !!e.folder && !!e.taskIds?.length && e.taskIds.every((id) => p.tasks[taskKey(e.folder!, id)] === "PASS");

/** The study plan as a plain list; an item turns green once every task in its module passes. */
export function PlanList({ rows }: { rows: PlanRow[] }) {
  const p = useProgress();
  return (
    <ol className="divide-y divide-line border-y border-line">
      {rows.map((r) => {
        const modules = r.entries.filter((e) => e.folder);
        const sessionDone = modules.length > 0 && modules.every((e) => complete(p, e));
        return (
          <li key={r.key} className="grid grid-cols-[3.25rem_1fr_auto] items-baseline gap-x-4 py-4">
            <span className={`font-mono text-sm ${sessionDone ? "text-pass" : "text-dim"}`}>{sessionDone ? "✓" : r.when}</span>
            <span className="leading-relaxed">
              {r.entries.map((e, i) => (
                <Fragment key={i}>
                  {i > 0 && <span className="text-dim"> · </span>}
                  <Link
                    href={e.href}
                    className={`underline decoration-line-strong underline-offset-4 hover:decoration-accent ${complete(p, e) ? "text-pass" : "text-text"}`}
                  >
                    {e.label}
                  </Link>
                  {e.note && <span className="text-sm text-dim"> {e.note}</span>}
                </Fragment>
              ))}
            </span>
            <span className="font-mono text-xs text-dim">{r.hours}</span>
          </li>
        );
      })}
    </ol>
  );
}
