"use client";
import { useEffect, useState } from "react";

const TOTAL = 60 * 60;

/** The 60-minute clock for the mock interview. */
export function MockTimer() {
  const [left, setLeft] = useState(TOTAL);
  const [running, setRunning] = useState(false);

  useEffect(() => {
    if (!running) return;
    const id = setInterval(() => setLeft((s) => Math.max(0, s - 1)), 1000);
    return () => clearInterval(id);
  }, [running]);

  const mm = String(Math.floor(left / 60)).padStart(2, "0");
  const ss = String(left % 60).padStart(2, "0");
  const tone = left === 0 ? "text-fail" : left < 10 * 60 ? "text-accent" : "text-text";

  return (
    <div className="mt-3 flex items-center gap-3 rounded-lg border border-line bg-raised px-3 py-2">
      <span className="label">Mock clock</span>
      <span className={`font-mono text-lg tabular-nums ${tone}`}>
        {mm}:{ss}
      </span>
      <div className="ml-auto flex gap-1.5">
        <button
          type="button"
          onClick={() => setRunning((r) => !r)}
          className="rounded-md bg-accent px-2.5 py-1 text-xs font-semibold text-accent-ink hover:brightness-110"
        >
          {running ? "Pause" : left === TOTAL ? "Start 60 min" : "Resume"}
        </button>
        <button
          type="button"
          onClick={() => {
            setRunning(false);
            setLeft(TOTAL);
          }}
          className="rounded-md border border-line-strong px-2.5 py-1 text-xs text-muted hover:text-text"
        >
          Reset
        </button>
      </div>
    </div>
  );
}
