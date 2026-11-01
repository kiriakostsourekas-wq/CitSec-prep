"use client";
import { taskKey, useProgress } from "@/lib/progress";
import { ProgressBar } from "./workspace/status";

export function ModuleProgress({ folder, taskIds }: { folder: string; taskIds: string[] }) {
  const p = useProgress();
  const done = taskIds.filter((id) => p.tasks[taskKey(folder, id)] === "PASS").length;
  return (
    <div className="flex items-center gap-3">
      <ProgressBar value={done} total={taskIds.length} className="flex-1" />
      <span className={`text-xs tabular-nums ${done === taskIds.length && done ? "text-pass" : "text-dim"}`}>
        {done}/{taskIds.length}
      </span>
    </div>
  );
}
