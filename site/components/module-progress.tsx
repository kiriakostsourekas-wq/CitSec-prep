"use client";
import { taskKey, useProgress } from "@/lib/progress";
import { ProgressBar } from "./workspace/status";

export function ModuleProgress({ folder, taskIds }: { folder: string; taskIds: string[] }) {
  const p = useProgress();
  const done = taskIds.filter((id) => p.tasks[taskKey(folder, id)] === "PASS").length;
  return (
    <div className="flex items-center gap-3">
      <ProgressBar value={done} total={taskIds.length} className="flex-1" />
      <span className={`font-mono text-[11px] ${done === taskIds.length && done ? "text-pass" : "text-dim"}`}>
        {done}/{taskIds.length}
      </span>
    </div>
  );
}

/** Compact "3/11" for list rows; shows the fallback (e.g. the time estimate) until something passes. */
export function ModuleCount({ folder, taskIds, fallback }: { folder: string; taskIds: string[]; fallback: string }) {
  const p = useProgress();
  const done = taskIds.filter((id) => p.tasks[taskKey(folder, id)] === "PASS").length;
  if (!done) return <span className="shrink-0 font-mono text-xs text-dim">{fallback}</span>;
  return (
    <span className={`shrink-0 font-mono text-xs ${done === taskIds.length ? "text-pass" : "text-muted"}`}>
      {done}/{taskIds.length} tasks
    </span>
  );
}
