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
  // Keep the README's order: section titles and topic headings sit between the question cards.
  type CardData = { summary: string; md: string; key: string };
  const items: ({ kind: "heading"; text: string } | { kind: "md"; md: string } | { kind: "card"; card: CardData; index: number })[] = [];
  const cards: CardData[] = [];
  for (const s of sections) {
    if (sections.length > 1 && s.heading) items.push({ kind: "heading", text: s.heading });
    for (const b of s.blocks) {
      if (b.kind === "fold") {
        const card = { summary: b.summary, md: b.md, key: `${folder}:fu:${cards.length}` };
        items.push({ kind: "card", card, index: cards.length });
        cards.push(card);
      } else items.push({ kind: "md", md: b.md });
    }
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
        <div className="mt-3 flex flex-wrap gap-4 text-[13px] tabular-nums">
          <span className="text-pass">{count("nailed")} nailed</span>
          <span className="text-accent">{count("shaky")} shaky</span>
          <span className="text-fail">{count("missed")} missed</span>
          <span className="text-dim">{cards.length - rated.filter(Boolean).length} to do</span>
        </div>
      </div>
      <div className="space-y-3">
        {items.map((it, i) =>
          it.kind === "heading" ? (
            <h2 key={i} className="pt-4 font-serif text-xl font-semibold tracking-[-0.01em] text-text">
              {it.text}
            </h2>
          ) : it.kind === "md" ? (
            <Markdown key={i} md={it.md} className="[&_h3]:mt-6" />
          ) : (
            <Card key={it.card.key} index={it.index} card={it.card} rating={progress.followUps[it.card.key]} />
          ),
        )}
      </div>
    </div>
  );
}

function Card({ index, card, rating }: { index: number; card: { summary: string; md: string; key: string }; rating?: Rating }) {
  const [open, setOpen] = useState(false);
  const question = card.summary.replace(/^\d+[.)]?\s+/, "");
  const rate = (r: Rating) => updateProgress((p) => ({ ...p, followUps: { ...p.followUps, [card.key]: r } }));

  return (
    <div className={`rounded-xl border bg-raised ${open ? "border-line-strong" : "border-line"}`}>
      <div className="flex gap-3 p-4">
        <span className="mt-[3px] w-5 shrink-0 text-right font-serif text-[15px] tabular-nums text-dim">{index + 1}</span>
        <div className="min-w-0 flex-1">
          <div className="font-serif text-[17px] leading-snug text-text">
            <InlineMarkdown md={question} />
          </div>
          {!open ? (
            <button type="button" onClick={() => setOpen(true)} className="mt-3 text-[13px] text-accent hover:underline">
              Show the answer
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
