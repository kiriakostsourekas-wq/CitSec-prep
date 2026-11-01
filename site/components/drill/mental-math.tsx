"use client";
import { useEffect, useRef, useState, useSyncExternalStore } from "react";
import { markVisited } from "@/lib/progress";
import { fmt, isCorrect, nextQuestion, type Question, type Topic, TOPICS } from "@/lib/drill";

const HISTORY_KEY = "citprep:v1:drill-history";
const MAX_QUESTIONS = 80;

type Answered = Question & { given: string; ok: boolean };
type Run = { when: string; minutes: number; topics: Topic[]; right: number; answered: number; seconds: number };

const readHistory = (): Run[] => {
  try {
    return JSON.parse(localStorage.getItem(HISTORY_KEY) ?? "[]");
  } catch {
    return [];
  }
};
const noop = () => () => {};

/** The timed arithmetic drill from 11_mental_math, in the browser. */
export function MentalMath() {
  const hydrated = useSyncExternalStore(noop, () => true, () => false);
  return hydrated ? <Drill /> : <div className="h-72" />;
}

function Drill() {
  const [minutes, setMinutes] = useState(8);
  const [topics, setTopics] = useState<Topic[]>(TOPICS.map((t) => t.id));
  const [phase, setPhase] = useState<"setup" | "running" | "done">("setup");
  const [q, setQ] = useState<Question | null>(null);
  const [input, setInput] = useState("");
  const [answered, setAnswered] = useState<Answered[]>([]);
  const [flash, setFlash] = useState<{ ok: boolean; text: string } | null>(null);
  const [startedAt, setStartedAt] = useState(0);
  const [now, setNow] = useState(0);
  const [history, setHistory] = useState<Run[]>(readHistory);
  const [elapsed, setElapsed] = useState(1);
  const field = useRef<HTMLInputElement>(null);
  const answeredRef = useRef<Answered[]>([]);

  const left = Math.max(0, minutes * 60 - Math.floor((now - startedAt) / 1000));

  const finish = (list: Answered[]) => {
    setPhase("done");
    const seconds = Math.max(1, Math.round((Date.now() - startedAt) / 1000));
    setElapsed(seconds);
    const run: Run = {
      when: new Date().toISOString(),
      minutes,
      topics,
      right: list.filter((a) => a.ok).length,
      answered: list.length,
      seconds,
    };
    if (list.length >= 10) markVisited("mental-math");
    const next = [run, ...readHistory()].slice(0, 50);
    setHistory(next);
    try {
      localStorage.setItem(HISTORY_KEY, JSON.stringify(next));
    } catch {
      /* history is a nice-to-have */
    }
  };

  const finishRef = useRef(finish);
  useEffect(() => {
    finishRef.current = finish;
  });
  useEffect(() => {
    if (phase !== "running") return;
    const id = setInterval(() => {
      const t = Date.now();
      setNow(t);
      if (t - startedAt >= minutes * 60_000) finishRef.current(answeredRef.current);
    }, 250);
    return () => clearInterval(id);
  }, [phase, startedAt, minutes]);

  const start = () => {
    const t = Date.now();
    setStartedAt(t);
    setNow(t);
    setAnswered([]);
    answeredRef.current = [];
    setFlash(null);
    setInput("");
    setQ(nextQuestion(topics));
    setPhase("running");
    setTimeout(() => field.current?.focus(), 0);
  };

  const submit = () => {
    if (!q) return;
    const ok = isCorrect(input, q.answer);
    const list = [...answered, { ...q, given: input.trim(), ok }];
    setAnswered(list);
    answeredRef.current = list;
    setFlash({ ok, text: ok ? "✓" : `✗  ${q.text} = ${fmt(q.answer)}` });
    setInput("");
    if (list.length >= MAX_QUESTIONS) return finish(list);
    setQ(nextQuestion(topics));
  };

  const toggle = (t: Topic) => setTopics((ts) => (ts.includes(t) ? (ts.length > 1 ? ts.filter((x) => x !== t) : ts) : [...ts, t]));

  if (phase === "running" && q) {
    return (
      <div className="rounded-2xl border border-line bg-raised p-6 sm:p-10">
        <div className="flex items-center justify-between text-sm tabular-nums">
          <span className="text-dim">
            Question {answered.length + 1} of {MAX_QUESTIONS}
          </span>
          <span className={left <= 30 ? "text-fail" : "text-muted"}>
            {Math.floor(left / 60)}:{String(left % 60).padStart(2, "0")}
          </span>
        </div>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            submit();
          }}
          className="mt-10 flex flex-col items-center gap-6"
        >
          <div className="text-center font-serif text-4xl font-medium lining-nums tabular-nums text-text sm:text-5xl">{q.text}</div>
          <input
            ref={field}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            inputMode="decimal"
            autoComplete="off"
            aria-label="Your answer"
            className="w-48 border-b-2 border-line-strong bg-transparent pb-1 text-center text-2xl font-medium tabular-nums text-text outline-none focus:border-accent"
          />
          <div className={`h-5 text-sm tabular-nums ${flash?.ok ? "text-pass" : "text-fail"}`}>{flash?.text}</div>
        </form>
        <div className="mt-6 flex justify-center gap-4 text-xs text-dim">
          <span>Enter to answer (empty skips)</span>
          <button type="button" onClick={() => finish(answered)} className="underline underline-offset-4 hover:text-muted">
            End now
          </button>
        </div>
      </div>
    );
  }

  if (phase === "done") {
    const right = answered.filter((a) => a.ok).length;
    const secs = elapsed;
    const byTopic = TOPICS.map((t) => {
      const xs = answered.filter((a) => a.topic === t.id);
      return { ...t, right: xs.filter((a) => a.ok).length, n: xs.length };
    }).filter((t) => t.n);
    const misses = answered.filter((a) => !a.ok);
    return (
      <div className="rounded-2xl border border-line bg-raised p-6 sm:p-8">
        <div className="flex flex-wrap items-baseline gap-x-8 gap-y-2">
          <div className="font-serif text-5xl font-semibold lining-nums tabular-nums text-text">
            {right}
            <span className="text-dim">/{answered.length}</span>
          </div>
          <div className="text-sm text-muted">
            {answered.length ? Math.round((100 * right) / answered.length) : 0}% accuracy, {((answered.length / secs) * 60).toFixed(1)} questions a minute
          </div>
        </div>
        {byTopic.length > 0 && (
          <div className="mt-5 flex flex-wrap gap-x-5 gap-y-1 text-[13px] tabular-nums text-muted">
            {byTopic.map((t) => (
              <span key={t.id}>
                {t.label} <span className={t.right === t.n ? "text-pass" : "text-text"}>{t.right}/{t.n}</span>
              </span>
            ))}
          </div>
        )}
        {misses.length > 0 && (
          <div className="mt-6 border-t border-line pt-4">
            <div className="mb-2 text-sm text-text">Missed</div>
            <ul className="space-y-1 text-sm tabular-nums text-muted">
              {misses.slice(0, 15).map((m, i) => (
                <li key={i}>
                  {m.text} = <span className="text-text">{fmt(m.answer)}</span> <span className="text-dim">(you: {m.given || "skip"})</span>
                </li>
              ))}
            </ul>
          </div>
        )}
        <div className="mt-6 flex gap-3">
          <button type="button" onClick={start} className="rounded-md bg-accent px-4 py-2 text-sm font-semibold text-accent-ink hover:brightness-110">
            Again
          </button>
          <button type="button" onClick={() => setPhase("setup")} className="rounded-md px-3 py-2 text-sm text-muted hover:text-text">
            Change settings
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="grid gap-8 sm:grid-cols-[1fr_220px]">
      <div className="rounded-2xl border border-line bg-raised p-6">
        <div className="text-sm text-text">Length</div>
        <div className="mt-2 flex gap-2">
          {[3, 8].map((m) => (
            <button
              key={m}
              type="button"
              onClick={() => setMinutes(m)}
              className={`rounded-md border px-3 py-1.5 text-sm ${minutes === m ? "border-accent text-text" : "border-line text-muted hover:text-text"}`}
            >
              {m} min{m === 8 ? " (the real test)" : ""}
            </button>
          ))}
        </div>
        <div className="mt-5 text-sm text-text">Topics</div>
        <div className="mt-2 flex flex-wrap gap-2">
          {TOPICS.map((t) => (
            <button
              key={t.id}
              type="button"
              onClick={() => toggle(t.id)}
              className={`rounded-md border px-3 py-1.5 text-sm ${topics.includes(t.id) ? "border-line-strong bg-panel-2 text-text" : "border-line text-dim"}`}
            >
              {t.label}
            </button>
          ))}
        </div>
        <button type="button" onClick={start} className="mt-6 rounded-md bg-accent px-5 py-2 text-sm font-semibold text-accent-ink hover:brightness-110">
          Start
        </button>
        <p className="mt-3 text-xs text-dim">No calculator, no paper. {MAX_QUESTIONS} questions or the clock, whichever comes first.</p>
      </div>
      <div>
        <div className="text-sm text-text">Your last runs</div>
        {history.length ? (
          <ul className="mt-2 space-y-1.5 text-[13px] tabular-nums text-muted">
            {history.slice(0, 8).map((r, i) => (
              <li key={i} className="flex justify-between gap-3">
                <span className="text-dim">{new Date(r.when).toLocaleDateString(undefined, { month: "short", day: "numeric" })}</span>
                <span>
                  {r.right}/{r.answered} in {r.minutes} min
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-2 text-xs text-dim">None yet. Scores are kept in this browser.</p>
        )}
      </div>
    </div>
  );
}
