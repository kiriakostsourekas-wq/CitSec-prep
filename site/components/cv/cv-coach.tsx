"use client";
import Link from "next/link";
import { useRef, useState, useSyncExternalStore } from "react";
import { type OfflineBank, offlinePlan, pdfToText, redact } from "@/lib/cv/offline";
import { type CvItem, type CvQuestion, type Feedback, type SavedPlan, TARGETS, type Target } from "@/lib/cv/types";
import { markVisited } from "@/lib/progress";
import { Spinner } from "../workspace/status";

const PLAN_KEY = "citprep:v1:cv-plan";
const ANSWERS_KEY = "citprep:v1:cv-answers";
const WHY_KEY = "citprep:v1:cv-why";

const read = <T,>(key: string, fallback: T): T => {
  try {
    const v = localStorage.getItem(key);
    return v ? (JSON.parse(v) as T) : fallback;
  } catch {
    return fallback;
  }
};
const write = (key: string, value: unknown) => {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch {
    /* storage unavailable: still works for this visit */
  }
};

async function callApi<T>(body: object): Promise<{ ok: true; data: T } | { ok: false; status: number; error: string }> {
  try {
    const res = await fetch("/api/cv", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) return { ok: false, status: res.status, error: data.error ?? `Request failed (${res.status}).` };
    return { ok: true, data };
  } catch {
    return { ok: false, status: 0, error: "Couldn't reach the server." };
  }
}

const noop = () => () => {};

export function CvCoach(props: { bank: OfflineBank; moduleTitles: Record<string, string> }) {
  // Everything here lives in localStorage, so render only once we're in the browser.
  const hydrated = useSyncExternalStore(noop, () => true, () => false);
  return hydrated ? <Coach {...props} /> : <div className="mx-auto h-[70vh] w-full max-w-6xl" />;
}

function Coach({ bank, moduleTitles }: { bank: OfflineBank; moduleTitles: Record<string, string> }) {
  const [saved, setSaved] = useState<SavedPlan | null>(() => read<SavedPlan | null>(PLAN_KEY, null));

  const save = (p: SavedPlan | null) => {
    setSaved(p);
    if (p) {
      write(PLAN_KEY, p);
      markVisited("guide/cv");
    }
    else [PLAN_KEY, ANSWERS_KEY, WHY_KEY].forEach((k) => localStorage.removeItem(k));
    window.scrollTo({ top: 0 });
  };

  return saved ? (
    <Results saved={saved} moduleTitles={moduleTitles} onReset={() => save(null)} />
  ) : (
    <Intake bank={bank} onDone={save} />
  );
}

// ================================================================== step 1: the CV
function Intake({ bank, onDone }: { bank: OfflineBank; onDone: (p: SavedPlan) => void }) {
  const [target, setTarget] = useState<Target>("securities");
  const [text, setText] = useState("");
  const [fileName, setFileName] = useState("");
  const [reading, setReading] = useState(false);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState("");
  const [drag, setDrag] = useState(false);
  const input = useRef<HTMLInputElement>(null);

  const onFile = async (file?: File) => {
    if (!file) return;
    setNotice("");
    if (file.type !== "application/pdf" && !file.name.toLowerCase().endsWith(".pdf")) {
      if (file.type.startsWith("text/") || /\.(txt|md)$/i.test(file.name)) {
        setText(await file.text());
        setFileName(file.name);
      } else setNotice("Use a PDF (or paste the text below).");
      return;
    }
    setReading(true);
    try {
      const t = await pdfToText(file);
      setFileName(file.name);
      setText(t);
      if (t.length < 200) setNotice("Very little text came out of that PDF (is it a scanned image?). Paste the text instead.");
    } catch {
      setNotice("Couldn't read that PDF. Paste the text below instead.");
    } finally {
      setReading(false);
    }
  };

  const generate = async () => {
    const cvText = redact(text).slice(0, 15000);
    setBusy(true);
    setNotice("");
    const res = await callApi<{ plan: SavedPlan["plan"] }>({ mode: "plan", target, cvText });
    setBusy(false);
    if (res.ok) return onDone({ plan: res.data.plan, mode: "ai", target, createdAt: new Date().toISOString() });
    if (res.status === 400) return setNotice(res.error);
    // AI not configured, over the free quota, or down: fall back to the guide's question bank.
    onDone({ plan: offlinePlan(cvText, bank), mode: "offline", target, createdAt: new Date().toISOString() });
  };

  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-12 sm:px-6">
      <div className="grid gap-12 lg:grid-cols-[1fr_380px]">
        <div>
          <div className="label text-accent">CV coach</div>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight sm:text-4xl">Every line of your CV is fair game.</h1>
          <p className="mt-4 max-w-2xl text-lg leading-relaxed text-muted">
            Drop your CV and get the deep-dive questions an interviewer is likely to ask about <em>your</em> projects, what a strong answer
            contains, and the follow-up that comes next. Then type your answers and get feedback.
          </p>

          <div className="mt-8">
            <div className="label mb-2">Interviewing with</div>
            <div className="grid gap-2 sm:grid-cols-2">
              {(Object.keys(TARGETS) as Target[]).map((t) => (
                <button
                  key={t}
                  type="button"
                  onClick={() => setTarget(t)}
                  className={`rounded-xl border px-4 py-3 text-left text-sm transition-colors ${
                    target === t ? "border-accent bg-accent-soft text-text" : "border-line bg-raised text-muted hover:border-line-strong"
                  }`}
                >
                  {TARGETS[t]}
                </button>
              ))}
            </div>
          </div>

          <div
            onDragOver={(e) => {
              e.preventDefault();
              setDrag(true);
            }}
            onDragLeave={() => setDrag(false)}
            onDrop={(e) => {
              e.preventDefault();
              setDrag(false);
              onFile(e.dataTransfer.files[0]);
            }}
            onClick={() => input.current?.click()}
            className={`mt-6 grid cursor-pointer place-items-center rounded-2xl border border-dashed px-6 py-10 text-center transition-colors ${
              drag ? "border-accent bg-accent-soft" : "border-line-strong bg-raised hover:border-dim"
            }`}
          >
            <input ref={input} type="file" accept="application/pdf,.pdf,.txt,.md" className="hidden" onChange={(e) => onFile(e.target.files?.[0])} />
            <div className="grid size-11 place-items-center rounded-xl border border-line bg-panel font-mono text-accent">CV</div>
            <div className="mt-3 font-medium text-text">{reading ? "Reading your PDF…" : fileName || "Drop your CV here, or click to choose"}</div>
            <div className="mt-1 text-sm text-dim">PDF, read in your browser. Or paste the text below.</div>
          </div>

          <div className="mt-6">
            <div className="mb-2 flex items-baseline justify-between">
              <span className="label">CV text {text ? "· check it, remove anything you don't want to share" : ""}</span>
              <span className="font-mono text-[11px] text-dim">{text.length.toLocaleString()} chars</span>
            </div>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              rows={10}
              placeholder="…or paste your CV here"
              className="w-full rounded-xl border border-line bg-raised px-4 py-3 font-mono text-[13px] leading-relaxed text-text outline-none placeholder:text-dim focus:border-line-strong"
            />
          </div>

          {notice && <div className="mt-3 rounded-lg border border-fail/30 bg-fail-soft px-4 py-2.5 text-sm text-text">{notice}</div>}

          <button
            type="button"
            onClick={generate}
            disabled={busy || reading || text.trim().length < 200}
            className="mt-5 flex items-center gap-2 rounded-lg bg-accent px-5 py-2.5 font-semibold text-accent-ink hover:brightness-110 disabled:opacity-40"
          >
            {busy && <Spinner />}
            {busy ? "Reading it like an interviewer… (≈ 20 s)" : "Generate my interview questions"}
          </button>
        </div>

        <aside className="space-y-4 lg:pt-20">
          <div className="rounded-2xl border border-line bg-raised p-5 text-sm leading-relaxed text-muted">
            <div className="label mb-3 text-accent">Your privacy</div>
            <ul className="space-y-2.5">
              <li>Your PDF is read <strong className="text-text">in your browser</strong>. The file is never uploaded.</li>
              <li>Emails, phone numbers and links are removed before anything is sent.</li>
              <li>
                The remaining text goes once to an AI model (via Groq) to write the questions. This site doesn&apos;t store it, and there&apos;s no
                account.
              </li>
              <li>Your questions and answers are saved only in this browser.</li>
            </ul>
          </div>
          <div className="rounded-2xl border border-line bg-raised p-5 text-sm leading-relaxed text-muted">
            <div className="label mb-3">What you get</div>
            <ul className="space-y-2">
              <li>→ The 4–6 lines of your CV they&apos;ll push hardest on</li>
              <li>→ For each: the questions, what a strong answer contains, and the follow-up</li>
              <li>→ Feedback on answers you type, with the next pushback question</li>
              <li>→ Behavioural stories mapped to your CV, and a draft &ldquo;why us&rdquo;</li>
            </ul>
          </div>
        </aside>
      </div>
    </div>
  );
}

// ================================================================== step 2: the questions
const RISK = {
  high: "border-fail/40 text-fail",
  medium: "border-accent/40 text-accent",
  low: "border-line-strong text-muted",
};

function Results({ saved, moduleTitles, onReset }: { saved: SavedPlan; moduleTitles: Record<string, string>; onReset: () => void }) {
  const { plan, mode, target } = saved;
  const [answers, setAnswers] = useState<Record<string, string>>(() => read(ANSWERS_KEY, {}));
  const [why, setWhy] = useState(() => read(WHY_KEY, plan.whyTarget) || plan.whyTarget);

  const setAnswer = (key: string, v: string) =>
    setAnswers((a) => {
      const next = { ...a, [key]: v };
      write(ANSWERS_KEY, next);
      return next;
    });

  const firm = target === "citadel" ? "Citadel" : "Citadel Securities";
  const total = plan.items.reduce((n, it) => n + it.questions.length, 0);
  const done = plan.items.reduce((n, it, i) => n + it.questions.filter((_, j) => (answers[`${i}:${j}`] ?? "").trim().length > 20).length, 0);

  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-12 sm:px-6">
      <div className="flex flex-wrap items-center gap-3">
        <span className="label text-accent">CV coach · {TARGETS[target]}</span>
        <span
          className={`rounded-full px-2.5 py-0.5 font-mono text-[10px] uppercase tracking-wider ${
            mode === "ai" ? "bg-pass-soft text-pass" : "bg-accent-soft text-accent"
          }`}
        >
          {mode === "ai" ? "personalised by AI" : "offline question bank"}
        </span>
        <button
          type="button"
          onClick={() => confirm("Start over with a new CV? Your current questions will be replaced.") && onReset()}
          className="ml-auto rounded-md border border-line-strong px-3 py-1.5 text-sm text-muted hover:text-text"
        >
          New CV
        </button>
      </div>
      <h1 className="mt-3 text-3xl font-semibold tracking-tight">Your deep-dive round</h1>

      <div className="mt-8 grid gap-10 lg:grid-cols-[minmax(0,1fr)_340px]">
        <div className="space-y-6">
          <div className="rounded-2xl border border-line bg-raised p-5">
            <div className="label mb-2">How an interviewer reads your CV</div>
            <p className="leading-relaxed text-text">{plan.summary}</p>
            <div className="mt-4 flex items-center gap-3 font-mono text-[11px] text-dim">
              <span>
                {done}/{total} questions practised
              </span>
            </div>
          </div>

          {plan.items.length === 0 && (
            <p className="text-muted">
              Nothing in the CV matched the question bank. Check the CV text has your projects and experience, then try again.
            </p>
          )}

          {plan.items.map((item, i) => (
            <ItemCard key={i} index={i} item={item} target={target} mode={mode} answers={answers} setAnswer={setAnswer} />
          ))}

          <section className="rounded-2xl border border-line bg-raised p-5">
            <div className="label mb-1 text-accent">Behavioural</div>
            <p className="mb-4 text-sm text-muted">Prepare one 2-minute STAR story for each (Situation, Task, Action, Result). The same story can serve several questions.</p>
            <ul className="divide-y divide-line">
              {plan.behavioural.map((b, i) => (
                <li key={i} className="py-3 first:pt-0 last:pb-0">
                  <div className="text-text">{b.q}</div>
                  {b.storyHint && <div className="mt-1 text-sm text-muted">↳ {b.storyHint}</div>}
                </li>
              ))}
            </ul>
          </section>

          <section className="rounded-2xl border border-line bg-raised p-5">
            <div className="label mb-1 text-accent">Why {firm}?</div>
            <p className="mb-3 text-sm text-muted">
              {plan.whyTarget
                ? "A first draft built from your CV. Fill in the [brackets] with things that are genuinely yours, then say it out loud until it sounds like you."
                : "Write your answer here: be specific (research culture, the people, the speed of feedback from markets, what you've read about the firm)."}
            </p>
            <textarea
              value={why}
              onChange={(e) => {
                setWhy(e.target.value);
                write(WHY_KEY, e.target.value);
              }}
              rows={7}
              className="w-full rounded-xl border border-line bg-bg px-4 py-3 text-[15px] leading-relaxed text-text outline-none focus:border-line-strong"
            />
          </section>
        </div>

        <aside className="space-y-4 lg:sticky lg:top-24 lg:self-start">
          {plan.focus.length > 0 && (
            <div className="rounded-2xl border border-line bg-raised p-5">
              <div className="label mb-3 text-accent">Drill these modules</div>
              <ul className="space-y-3">
                {plan.focus.map((f) => (
                  <li key={f.module}>
                    <Link href={`/modules/${f.module}`} className="font-medium text-text hover:text-accent">
                      {moduleTitles[f.module] ?? f.module} →
                    </Link>
                    <p className="mt-0.5 text-sm text-muted">{f.reason}</p>
                  </li>
                ))}
              </ul>
            </div>
          )}
          {plan.askThem.length > 0 && (
            <div className="rounded-2xl border border-line bg-raised p-5">
              <div className="label mb-3">Questions to ask them</div>
              <ul className="space-y-2.5 text-sm text-muted">
                {plan.askThem.map((q, i) => (
                  <li key={i}>&ldquo;{q}&rdquo;</li>
                ))}
              </ul>
            </div>
          )}
          <div className="rounded-2xl border border-line bg-raised p-5 text-sm text-muted">
            <div className="label mb-2">Ground rules</div>
            <ul className="space-y-1.5">
              <li>Know your own numbers exactly.</li>
              <li>Name the limitations before they do.</li>
              <li>&ldquo;We built…, and my part was…&rdquo;: never overclaim.</li>
            </ul>
            <Link href="/guide/cv" className="mt-3 inline-block text-accent hover:underline">
              Full CV guide →
            </Link>
          </div>
        </aside>
      </div>
    </div>
  );
}

function ItemCard({
  index,
  item,
  target,
  mode,
  answers,
  setAnswer,
}: {
  index: number;
  item: CvItem;
  target: Target;
  mode: SavedPlan["mode"];
  answers: Record<string, string>;
  setAnswer: (k: string, v: string) => void;
}) {
  return (
    <section className="overflow-hidden rounded-2xl border border-line bg-raised">
      <div className="border-b border-line p-5">
        <div className="flex flex-wrap items-center gap-2">
          <span className="font-mono text-xs text-dim">{String(index + 1).padStart(2, "0")}</span>
          <span className="rounded-md border border-line px-2 py-0.5 font-mono text-[10px] uppercase tracking-wider text-muted">{item.kind}</span>
          <span className={`rounded-md border px-2 py-0.5 font-mono text-[10px] uppercase tracking-wider ${RISK[item.risk]}`}>
            {item.risk} pressure
          </span>
        </div>
        <blockquote className="mt-3 border-l-2 border-accent pl-3 text-[15px] leading-relaxed text-text">{item.cvLine}</blockquote>
        {item.why && <p className="mt-2 text-sm text-muted">{item.why}</p>}
      </div>
      <div className="divide-y divide-line">
        {item.questions.map((q, j) => (
          <QuestionCard
            key={j}
            q={q}
            cvLine={item.cvLine}
            target={target}
            mode={mode}
            answer={answers[`${index}:${j}`] ?? ""}
            setAnswer={(v) => setAnswer(`${index}:${j}`, v)}
          />
        ))}
      </div>
    </section>
  );
}

function QuestionCard({
  q,
  cvLine,
  target,
  mode,
  answer,
  setAnswer,
}: {
  q: CvQuestion;
  cvLine: string;
  target: Target;
  mode: SavedPlan["mode"];
  answer: string;
  setAnswer: (v: string) => void;
}) {
  const [open, setOpen] = useState(false);
  const [reveal, setReveal] = useState(false);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);
  const practised = answer.trim().length > 20;

  const getFeedback = async () => {
    setBusy(true);
    setErr("");
    const res = await callApi<{ feedback: Feedback }>({ mode: "feedback", target, question: q.q, lookingFor: q.lookingFor, cvLine, answer });
    setBusy(false);
    if (res.ok) setFeedback(res.data.feedback);
    else setErr(res.status === 503 ? "AI feedback isn't switched on for this site yet." : res.error);
  };

  return (
    <div className="p-5">
      <div className="flex gap-3">
        <span className={`mt-2 size-2 shrink-0 rounded-full ${practised ? "bg-pass" : "border border-line-strong"}`} />
        <div className="min-w-0 flex-1">
          <p className="text-[15px] leading-snug text-text">{q.q}</p>
          <div className="mt-3 flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => setOpen((o) => !o)}
              className="rounded-md border border-line-strong px-3 py-1 text-[13px] text-muted hover:text-text"
            >
              {open ? "Hide answer box" : practised ? "Edit my answer" : "Practise"}
            </button>
            {(q.lookingFor.length > 0 || q.followUp) && (
              <button type="button" onClick={() => setReveal((r) => !r)} className="rounded-md px-3 py-1 text-[13px] text-accent hover:underline">
                {reveal ? "Hide" : "What they look for"}
              </button>
            )}
          </div>

          {reveal && (
            <div className="mt-3 rounded-lg border border-line bg-bg p-3.5 text-sm">
              {q.lookingFor.length > 0 && (
                <ul className="space-y-1 text-muted">
                  {q.lookingFor.map((l, i) => (
                    <li key={i}>✓ {l}</li>
                  ))}
                </ul>
              )}
              {q.followUp && (
                <p className="mt-2.5 text-text">
                  <span className="label mr-2 text-accent">then</span>
                  {q.followUp}
                </p>
              )}
            </div>
          )}

          {open && (
            <div className="mt-3 space-y-3">
              <textarea
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                rows={5}
                placeholder="Type your answer the way you'd say it out loud (about 1–2 minutes)."
                className="w-full rounded-xl border border-line bg-bg px-3.5 py-3 text-[14px] leading-relaxed text-text outline-none placeholder:text-dim focus:border-line-strong"
              />
              <div className="flex items-center gap-3">
                <button
                  type="button"
                  onClick={getFeedback}
                  disabled={busy || answer.trim().length < 20}
                  className="flex items-center gap-2 rounded-md bg-text px-3 py-1.5 text-[13px] font-medium text-bg hover:bg-white disabled:opacity-40"
                >
                  {busy && <Spinner />} Get interviewer feedback
                </button>
                {mode === "offline" && <span className="text-xs text-dim">uses the AI if it&apos;s available</span>}
              </div>
              {err && <p className="text-sm text-fail">{err}</p>}
              {feedback && <FeedbackView f={feedback} />}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function FeedbackView({ f }: { f: Feedback }) {
  const tone = { strong: "text-pass", solid: "text-accent", weak: "text-fail" }[f.verdict];
  return (
    <div className="rounded-xl border border-line-strong bg-panel p-4 text-sm">
      <div className="flex items-center gap-3">
        <span className={`font-mono text-xs uppercase tracking-wider ${tone}`}>{f.verdict}</span>
        <span className="flex gap-1">
          {[1, 2, 3, 4, 5].map((n) => (
            <span key={n} className={`size-2 rounded-full ${n <= f.score ? "bg-current " + tone : "bg-line-strong"}`} />
          ))}
        </span>
      </div>
      <div className="mt-3 grid gap-3 sm:grid-cols-2">
        {f.good.length > 0 && (
          <div>
            <div className="label mb-1 text-pass">Landed</div>
            <ul className="space-y-1 text-muted">
              {f.good.map((g, i) => (
                <li key={i}>+ {g}</li>
              ))}
            </ul>
          </div>
        )}
        {f.missing.length > 0 && (
          <div>
            <div className="label mb-1 text-fail">Missing</div>
            <ul className="space-y-1 text-muted">
              {f.missing.map((g, i) => (
                <li key={i}>− {g}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
      {f.followUp && (
        <p className="mt-3 border-t border-line pt-3 text-text">
          <span className="label mr-2 text-accent">they push</span>
          {f.followUp}
        </p>
      )}
      {f.tip && <p className="mt-2 text-muted">Tip: {f.tip}</p>}
    </div>
  );
}
