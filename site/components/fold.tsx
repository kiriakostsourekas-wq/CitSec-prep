"use client";
import { useState, type ReactNode } from "react";

/** The kit's folded answers (<details>) as a reveal card. */
export function Fold({ summary, children, tone = "default" }: { summary: ReactNode; children: ReactNode; tone?: "default" | "hint" }) {
  const [open, setOpen] = useState(false);
  return (
    <div className={`rounded-xl border transition-colors ${open ? "border-line-strong bg-panel" : "border-line bg-raised hover:border-line-strong"}`}>
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        className="flex w-full items-start gap-3 px-4 py-3 text-left"
      >
        <span
          className={`mt-1 grid size-4 shrink-0 place-items-center rounded-[4px] border text-[11px] leading-none transition-transform ${
            open ? "rotate-90 border-accent text-accent" : "border-line-strong text-dim"
          }`}
          aria-hidden
        >
          ›
        </span>
        <span className={`text-[15px] leading-snug ${tone === "hint" ? "text-muted" : "text-text"}`}>{summary}</span>
      </button>
      {open && <div className="border-t border-line px-4 pb-4 pt-3">{children}</div>}
    </div>
  );
}
