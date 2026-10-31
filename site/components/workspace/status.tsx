"use client";
import type { TaskStatus } from "@/lib/progress";
import { usePythonStatus } from "@/lib/python/client";

export const STATUS_STYLE: Record<TaskStatus | "NONE", { dot: string; text: string; label: string }> = {
  PASS: { dot: "bg-pass", text: "text-pass", label: "pass" },
  FAIL: { dot: "bg-fail", text: "text-fail", label: "fail" },
  ERROR: { dot: "bg-fail", text: "text-fail", label: "error" },
  TODO: { dot: "bg-dim", text: "text-dim", label: "todo" },
  NONE: { dot: "border border-line-strong", text: "text-dim", label: "not run" },
};

export function StatusDot({ status }: { status?: TaskStatus }) {
  return <span className={`inline-block size-2 shrink-0 rounded-full ${STATUS_STYLE[status ?? "NONE"].dot}`} />;
}

export function Spinner({ className = "" }: { className?: string }) {
  return (
    <span
      className={`inline-block size-3 animate-spin rounded-full border-[1.5px] border-current border-r-transparent ${className}`}
      aria-hidden
    />
  );
}

export function PythonPill() {
  const { status, detail } = usePythonStatus();
  const map = {
    idle: { cls: "text-dim", text: "Python idle" },
    loading: { cls: "text-accent", text: detail || "Loading Python…" },
    ready: { cls: "text-pass", text: "Python 3.14 · ready" },
    running: { cls: "text-info", text: "Running…" },
    error: { cls: "text-fail", text: detail || "Python failed to load" },
  }[status];
  return (
    <span className={`flex min-w-0 items-center gap-2 font-mono text-[11px] ${map.cls}`} title={map.text}>
      {status === "loading" || status === "running" ? <Spinner /> : <span className="size-1.5 shrink-0 rounded-full bg-current" />}
      <span className="truncate">{map.text}</span>
    </span>
  );
}

export function ProgressBar({ value, total, className = "" }: { value: number; total: number; className?: string }) {
  const pct = total ? Math.round((100 * value) / total) : 0;
  return (
    <div className={`h-1 overflow-hidden rounded-full bg-line ${className}`}>
      <div className="h-full rounded-full bg-pass transition-[width] duration-500" style={{ width: `${pct}%` }} />
    </div>
  );
}
