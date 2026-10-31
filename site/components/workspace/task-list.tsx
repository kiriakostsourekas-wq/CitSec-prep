"use client";
import { useState } from "react";
import type { Module, Task } from "@/lib/content";
import { taskKey, updateProgress, useProgress } from "@/lib/progress";
import type { CheckResult } from "@/lib/python/client";
import { Markdown } from "../markdown";
import { STATUS_STYLE, StatusDot } from "./status";

type Props = {
  module: Module;
  results: Record<string, CheckResult>;
  busy: boolean;
  onCheck: (ids: string[]) => void;
  onJump: (task: Task) => void;
  onJumpLine: (line: number) => void;
};

export function TaskList({ module, results, busy, onCheck, onJump, onJumpLine }: Props) {
  const progress = useProgress();
  const [open, setOpen] = useState<string | null>(module.tasks[0]?.id ?? null);
  const groups: { part: string; tasks: Task[] }[] = [];
  for (const t of module.tasks) {
    const g = groups.at(-1);
    if (g && g.part === t.part) g.tasks.push(t);
    else groups.push({ part: t.part, tasks: [t] });
  }

  return (
    <div className="space-y-6">
      {groups.map((g) => {
        const passed = g.tasks.filter((t) => progress.tasks[taskKey(module.folder, t.id)] === "PASS").length;
        return (
          <section key={g.part}>
            <div className="mb-2 flex items-baseline gap-3">
              <span className="label shrink-0 whitespace-nowrap">{g.part.length === 1 ? `Part ${g.part}` : g.part.replace("S", "Stage ")}</span>
              <span className="truncate text-sm text-muted">{module.parts[g.part]}</span>
              <span className="ml-auto font-mono text-[11px] text-dim">
                {passed}/{g.tasks.length}
              </span>
            </div>
            <div className="divide-y divide-line overflow-hidden rounded-xl border border-line bg-raised">
              {g.tasks.map((t) => (
                <TaskRow
                  key={t.id}
                  module={module}
                  task={t}
                  result={results[t.id]}
                  open={open === t.id}
                  busy={busy}
                  onToggle={() => setOpen(open === t.id ? null : t.id)}
                  onCheck={() => onCheck([t.id])}
                  onJump={() => onJump(t)}
                  onJumpLine={onJumpLine}
                />
              ))}
            </div>
          </section>
        );
      })}
    </div>
  );
}

function TaskRow({
  module,
  task,
  result,
  open,
  busy,
  onToggle,
  onCheck,
  onJump,
  onJumpLine,
}: {
  module: Module;
  task: Task;
  result?: CheckResult;
  open: boolean;
  busy: boolean;
  onToggle: () => void;
  onCheck: () => void;
  onJump: () => void;
  onJumpLine: (line: number) => void;
}) {
  const progress = useProgress();
  const key = taskKey(module.folder, task.id);
  const status = result?.status ?? progress.tasks[key];
  const hintsShown = progress.hints[key] ?? 0;
  const solutionShown = !!progress.solutions[key];
  const failing = result && (result.status === "FAIL" || result.status === "ERROR");

  const revealSolution = () => {
    if (status !== "PASS" && !confirm("Try it for ~10 minutes and use the hints first. Reveal the reference solution anyway?")) return;
    updateProgress((p) => ({ ...p, solutions: { ...p.solutions, [key]: true } }));
  };

  return (
    <div className={open ? "bg-panel" : ""}>
      <button type="button" onClick={onToggle} className="flex w-full items-center gap-3 px-3.5 py-2.5 text-left hover:bg-panel">
        <StatusDot status={status} />
        <span className="w-7 shrink-0 font-mono text-xs text-dim">{task.id}</span>
        <span className="min-w-0 truncate font-mono text-[13px] text-text">{task.func}</span>
        <span className="hidden min-w-0 truncate text-[13px] text-dim sm:inline">{task.title}</span>
        <span className={`ml-auto shrink-0 font-mono text-[10px] uppercase ${STATUS_STYLE[status ?? "NONE"].text}`}>
          {status ? STATUS_STYLE[status].label : ""}
        </span>
      </button>

      {open && (
        <div className="space-y-4 px-3.5 pb-4 pt-1">
          {task.doc && (
            <pre className="overflow-x-auto whitespace-pre-wrap break-words rounded-lg border border-line bg-bg px-3 py-2.5 font-mono text-[12.5px] leading-relaxed text-muted">
              {task.doc}
            </pre>
          )}

          {failing && (
            <div className="rounded-lg border border-fail/30 bg-fail-soft px-3 py-2.5">
              <div className="mb-1 font-mono text-[11px] uppercase text-fail">{result.status}</div>
              <pre className="whitespace-pre-wrap font-mono text-[12.5px] text-text">{result.message}</pre>
              {result.line ? (
                <button type="button" onClick={() => onJumpLine(result.line!)} className="mt-2 text-xs text-accent hover:underline">
                  Go to line {result.line} →
                </button>
              ) : null}
            </div>
          )}
          {result?.output && (
            <pre className="max-h-40 overflow-auto rounded-lg border border-line bg-bg px-3 py-2 font-mono text-[12px] text-muted">
              {result.output}
            </pre>
          )}

          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              onClick={onCheck}
              disabled={busy}
              className="rounded-md bg-text px-3 py-1.5 text-[13px] font-medium text-bg hover:bg-white disabled:opacity-50"
            >
              Check {task.id}
            </button>
            <button type="button" onClick={onJump} className="rounded-md border border-line-strong px-3 py-1.5 text-[13px] text-muted hover:text-text">
              Go to code
            </button>
          </div>

          {(task.hints.length > 0 || task.hintNote) && (
            <div className="space-y-2">
              <div className="label">Hints · {hintsShown}/{task.hints.length} opened</div>
              {task.hintNote && <Markdown md={task.hintNote} className="text-[13.5px]" />}
              {task.hints.slice(0, hintsShown).map((h, i) => (
                <div key={i} className="rounded-lg border border-line bg-bg px-3 py-2">
                  <div className="mb-1 font-mono text-[10px] uppercase text-accent">Hint {i + 1}</div>
                  <Markdown md={h} className="text-[13.5px]" />
                </div>
              ))}
              {hintsShown < task.hints.length && (
                <button
                  type="button"
                  onClick={() => updateProgress((p) => ({ ...p, hints: { ...p.hints, [key]: hintsShown + 1 } }))}
                  className="rounded-md border border-dashed border-line-strong px-3 py-1.5 text-[13px] text-muted hover:border-accent hover:text-accent"
                >
                  Show hint {hintsShown + 1}
                </button>
              )}
            </div>
          )}

          {task.solution && (
            <div className="space-y-2">
              <div className="label">Reference solution</div>
              {solutionShown ? (
                <Markdown md={"```python\n" + task.solution + "\n```"} className="text-[13px]" />
              ) : (
                <button type="button" onClick={revealSolution} className="text-[13px] text-dim underline decoration-line-strong underline-offset-4 hover:text-muted">
                  {status === "PASS" ? "Compare with the reference solution" : "Reveal the solution"}
                </button>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
