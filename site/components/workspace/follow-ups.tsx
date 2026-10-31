"use client";
import { useState } from "react";
import type { Section } from "@/lib/content";
import { type Rating, updateProgress, useProgress } from "@/lib/progress";
import { InlineMarkdown, Markdown } from "../markdown";

const RATINGS: { value: Rating; label: string; cls: string }[] = [
  { value: "nailed", label: "Nailed it", cls: "border-pass/40 text-pass hover:bg-pass-soft" },
  { value: "shaky", label: "Shaky", cls: "border-accent/40 text-accent hover:bg-accent-soft" },
  { value: "missed", label: "Missed it", cls: "border-fail/40 text-fail hover:bg-fail-soft" },
];
const BADGE: Record<Rating, string> = { nailed: "bg-pass", shaky: "bg-accent", missed: "bg-fail" };

/** Interviewer follow-ups as say-it-out-loud cards with self-rating. */
export function FollowUps({ folder, sections }: { folder: string; sections: Section[] }) {
  const progress = useProgress();
  const cards: { summary: string; md: string; key: string }[] = [];
  const intro: string[] = [];
  for (const s of sections)
    for (const b of s.blocks) {
      if (b.kind === "fold") cards.push({ summary: b.summary, md: b.md, key: `${folder}:fu:${cards.length}` });
      else intro.push(b.md);
    }
  const rated = cards.map((c) => progress.followUps[c.key]);
  const count = (r: Rating) => rated.filter((x) => x === r).length;

  return (
    <div className="space-y-5">
      <div className="rounded-xl border border-line bg-raised p-4">
        <p className="text-[14px] leading-relaxed text-muted">
          These are the real exam. Read the question, <strong className="text-text">answer it out loud</strong> as if the
          interviewer were listening, then reveal the answer and rate yourself honestly. Re-do the ones you rated shaky or missed
          the day before.
        </p>
        <div className="mt-3 flex flex-wrap gap-4 font-mono text-[11px]">
          <span className="text-pass">● {count("nailed")} nailed</span>
          <span className="text-accent">● {count("shaky")} shaky</span>
          <span className="text-fail">● {count("missed")} missed</span>
          <span className="text-dim">○ {cards.length - rated.filter(Boolean).length} to do</span>
        </div>
      </div>
      {intro.map((md, i) => (
        <Markdown key={i} md={md} />
      ))}
      <div className="space-y-3">
        {cards.map((c, i) => (
          <Card key={c.key} index={i} card={c} rating={progress.followUps[c.key]} />
        ))}
      </div>
    </div>
  );
}

function Card({ index, card, rating }: { index: number; card: { summary: string; md: string; key: string }; rating?: Rating }) {
  const [open, setOpen] = useState(false);
  const question = card.summary.replace(/^\d+\.\s*/, "");
  const rate = (r: Rating) => updateProgress((p) => ({ ...p, followUps: { ...p.followUps, [card.key]: r } }));

  return (
    <div className={`rounded-xl border bg-raised ${open ? "border-line-strong" : "border-line"}`}>
      <div className="flex gap-3 p-4">
        <span className="mt-0.5 font-mono text-xs text-dim">{String(index + 1).padStart(2, "0")}</span>
        <div className="min-w-0 flex-1">
          <div className="text-[15px] leading-snug text-text">
            <InlineMarkdown md={question} />
          </div>
          {!open ? (
            <button type="button" onClick={() => setOpen(true)} className="mt-3 text-[13px] text-accent hover:underline">
              I&apos;ve said my answer: reveal →
            </button>
          ) : (
            <div className="mt-3 space-y-3 border-t border-line pt-3">
              <Markdown md={card.md} className="text-[14px]" />
              <div className="flex flex-wrap items-center gap-2">
                <span className="mr-1 text-xs text-dim">How did you do?</span>
                {RATINGS.map((r) => (
                  <button
                    key={r.value}
                    type="button"
                    onClick={() => rate(r.value)}
                    className={`rounded-md border px-2.5 py-1 text-xs transition-colors ${r.cls} ${rating === r.value ? "bg-panel-2" : ""}`}
                  >
                    {r.label}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
        {rating && <span className={`mt-1.5 size-2 shrink-0 rounded-full ${BADGE[rating]}`} title={rating} />}
      </div>
    </div>
  );
}
