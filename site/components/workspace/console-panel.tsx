"use client";
import { useEffect, useRef } from "react";
import type { CheckResult } from "@/lib/python/client";
import { STATUS_STYLE } from "./status";

export type OutputChunk = { kind: "out" | "err" | "info"; text: string };
export type Image = { name: string; png: string };
export type ConsoleTab = "checks" | "output";

type Props = {
  tab: ConsoleTab;
  setTab: (t: ConsoleTab) => void;
  output: OutputChunk[];
  images: Image[];
  checks: CheckResult[] | null;
  fatal: string | null;
  onClear: () => void;
  onRunSolution: () => void;
  onJumpLine: (line: number) => void;
  busy: boolean;
};

export function ConsolePanel({ tab, setTab, output, images, checks, fatal, onClear, onRunSolution, onJumpLine, busy }: Props) {
  const scroller = useRef<HTMLDivElement>(null);
  useEffect(() => {
    // follow the output like a terminal; check results read from the top
    const el = scroller.current;
    if (el) el.scrollTo({ top: tab === "output" ? el.scrollHeight : 0 });
  }, [output, images, checks, tab]);

  const counts = { PASS: 0, FAIL: 0, TODO: 0 };
  for (const r of checks ?? []) counts[r.status === "ERROR" ? "FAIL" : r.status]++;

  return (
    <div className="flex h-full min-h-0 flex-col bg-raised">
      <div className="flex h-9 shrink-0 items-center gap-1 border-b border-line px-2">
        {(["checks", "output"] as const).map((t) => (
          <button
            key={t}
            type="button"
            onClick={() => setTab(t)}
            className={`rounded px-2.5 py-1 text-[13px] ${tab === t ? "bg-panel-2 text-text" : "text-dim hover:text-muted"}`}
          >
            {t === "checks" ? "Checks" : "Output"}
          </button>
        ))}
        {checks && tab === "checks" && (
          <span className="ml-2 flex gap-3 text-[13px] tabular-nums">
            <span className="text-pass">{counts.PASS} passed</span>
            <span className="text-fail">{counts.FAIL} failed</span>
            <span className="text-dim">{counts.TODO} to do</span>
          </span>
        )}
        <div className="ml-auto flex items-center gap-1">
          <button
            type="button"
            disabled={busy}
            onClick={onRunSolution}
            className="rounded px-2 py-1 text-[13px] text-dim hover:text-muted disabled:opacity-40"
            title="Run the reference solution.py and read its analysis"
          >
            Run solution.py
          </button>
          <button type="button" onClick={onClear} className="rounded px-2 py-1 text-[13px] text-dim hover:text-muted">
            Clear
          </button>
        </div>
      </div>

      <div ref={scroller} className="min-h-0 flex-1 overflow-auto px-4 py-3 font-mono text-[12.5px] leading-relaxed">
        {tab === "output" ? (
          output.length || images.length ? (
            <>
              <pre className="w-max min-w-full whitespace-pre">
                {output.map((c, i) => (
                  <span key={i} className={c.kind === "err" ? "text-fail" : c.kind === "info" ? "text-dim" : "text-text"}>
                    {c.text}
                  </span>
                ))}
              </pre>
              {images.map((img, i) => (
                <figure key={i} className="mt-3">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={`data:image/png;base64,${img.png}`} alt={img.name} className="max-w-full rounded-lg border border-line bg-white" />
                  <figcaption className="mt-1 text-[11px] text-dim">{img.name}</figcaption>
                </figure>
              ))}
            </>
          ) : (
            <p className="text-dim">
              Run executes exercise.py like <span className="text-muted">python exercise.py</span>: the playground at the bottom of the file.
              Print anything to explore the data. <span className="text-muted">⌘/Ctrl + Enter</span>
            </p>
          )
        ) : fatal ? (
          <pre className="whitespace-pre-wrap text-fail">{fatal}</pre>
        ) : checks ? (
          <div className="space-y-1.5">
            {checks.map((r) => (
              <div key={r.id}>
                <div className="flex gap-3">
                  <span className={`w-11 shrink-0 ${STATUS_STYLE[r.status].text}`}>{r.status}</span>
                  <span className="w-7 shrink-0 text-dim">{r.id}</span>
                  <span className="text-text">{r.func}</span>
                  <span className="truncate text-dim">{r.title}</span>
                </div>
                {r.message && (
                  <pre className="ml-[4.75rem] whitespace-pre-wrap text-muted">
                    {r.message}
                    {r.line ? (
                      <button type="button" onClick={() => onJumpLine(r.line!)} className="ml-2 text-accent hover:underline">
                        go to line {r.line}
                      </button>
                    ) : null}
                  </pre>
                )}
              </div>
            ))}
          </div>
        ) : (
          <p className="text-dim">
            Check runs the kit&apos;s own tests, like <span className="text-muted">python check.py</span>. You get PASS, FAIL or TODO
            for each task, with an explanation. <span className="text-muted">⇧ + ⌘/Ctrl + Enter</span>
          </p>
        )}
      </div>
    </div>
  );
}
