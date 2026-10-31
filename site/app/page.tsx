import Link from "next/link";
import { ModuleCard } from "@/components/module-card";
import { SiteFooter } from "@/components/site-footer";
import { content, followUpCount, modules } from "@/lib/content";

const totalTasks = modules.reduce((n, m) => n + m.tasks.length, 0);
const totalFollowUps =
  modules.reduce((n, m) => n + followUpCount(m), 0) +
  content.guide.mlStats.sections.reduce((n, s) => n + s.blocks.filter((b) => b.kind === "fold").length, 0);

const STEPS = [
  { k: "01", title: "Read the notes", body: "Short concept notes per topic: the formulas, the intuition, and the traps interviewers like." },
  { k: "02", title: "Write the code", body: "Real Python with numpy, pandas and scikit-learn, running in your browser. Nothing to install." },
  { k: "03", title: "Check it", body: "The kit's own tests give PASS, FAIL or TODO for each task, with a hint ladder and a reference solution." },
  { k: "04", title: "Defend it out loud", body: "Interviewer follow-ups you answer out loud, then rate yourself on. This is what the round actually tests." },
];

const ROUNDS = [
  ["Probability / brainteasers", "EV, conditional probability, Bayes, dice, coins, cards", "08"],
  ["Coding", "Live editor, Python, easy–medium LeetCode with a finance flavour", "01 · 09"],
  ["ML / statistics", "Linear regression (very common), regularisation, evaluation", "03 – 07"],
  ["CV deep dive & behavioural", "“Walk me through your research”, why Citadel, failure", "guide"],
];

function TerminalCard() {
  const rows: [string, string, string, string][] = [
    ["PASS", "A1", "simple_fit", "slope = cov/var"],
    ["PASS", "B2", "fit_ols", "normal equations"],
    ["PASS", "C2", "fit_gd", "gradient descent"],
    ["FAIL", "D2", "coef_standard_errors", "sigma^2 (X^T X)^-1"],
    ["TODO", "D3", "duplicate_data_experiment", "the Citadel question"],
  ];
  const tone = { PASS: "text-pass", FAIL: "text-fail", TODO: "text-dim" } as const;
  return (
    <div className="overflow-hidden rounded-2xl border border-line-strong bg-raised shadow-[0_30px_80px_-20px_rgba(0,0,0,0.8)]">
      <div className="flex items-center gap-2 border-b border-line px-4 py-2.5">
        <span className="size-2.5 rounded-full bg-line-strong" />
        <span className="size-2.5 rounded-full bg-line-strong" />
        <span className="size-2.5 rounded-full bg-line-strong" />
        <span className="ml-3 font-mono text-[11px] text-dim">04_linear_regression · check</span>
      </div>
      <div className="space-y-1.5 px-4 py-4 font-mono text-[12.5px] leading-relaxed">
        <div className="text-dim">$ python check.py</div>
        {rows.map(([s, id, fn, title]) => (
          <div key={id} className="flex gap-3 whitespace-nowrap">
            <span className={`w-9 ${tone[s as keyof typeof tone]}`}>{s}</span>
            <span className="text-dim">[{id}]</span>
            <span className="text-text">{fn}</span>
            <span className="hidden truncate text-dim sm:inline">{title}</span>
          </div>
        ))}
        <div className="pl-[3.75rem] text-muted">standard errors: expected [31.2 0.48 …], got [31.0 0.48 …]</div>
        <div className="pt-2">
          <span className="text-pass">3</span>
          <span className="text-dim">/5 passed · </span>
          <span className="text-fail">1</span>
          <span className="text-dim"> failing · 1 not started</span>
        </div>
      </div>
      <div className="border-t border-line bg-panel px-4 py-3 text-[13px]">
        <span className="label mr-2 text-accent">Follow-up</span>
        <span className="text-muted">You duplicate every row. What happens to β̂, R², the SEs and the t-stats?</span>
      </div>
    </div>
  );
}

export default function Home() {
  return (
    <>
      <section className="relative overflow-hidden border-b border-line">
        <div className="grid-bg pointer-events-none absolute inset-0 opacity-60" />
        <div className="relative mx-auto grid max-w-6xl items-center gap-12 px-4 pb-20 pt-16 sm:px-6 lg:grid-cols-[1.1fr_1fr] lg:pt-24">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border border-line bg-raised px-3 py-1 font-mono text-[11px] text-muted">
              <span className="size-1.5 rounded-full bg-accent" /> Citadel · Citadel Securities · quant final rounds
            </div>
            <h1 className="mt-6 text-4xl font-semibold leading-[1.08] tracking-tight sm:text-5xl lg:text-[3.4rem]">
              Walk into your superday having <span className="text-accent">already done it.</span>
            </h1>
            <p className="mt-6 max-w-xl text-lg leading-relaxed text-muted">
              A free prep track built from one candidate&apos;s actual preparation. You get Python and ML exercises that run in your browser,
              the follow-up questions interviewers really ask, and a CV deep dive to rehearse your own story.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link href="/plan" className="rounded-lg bg-accent px-5 py-2.5 font-semibold text-accent-ink hover:brightness-110">
                Start the roadmap
              </Link>
              <Link
                href="/modules/linear-regression"
                className="rounded-lg border border-line-strong bg-raised px-5 py-2.5 font-medium text-text hover:border-dim"
              >
                Try linear regression →
              </Link>
            </div>
            <dl className="mt-12 grid max-w-lg grid-cols-4 gap-4 border-t border-line pt-6">
              {[
                [modules.length, "modules"],
                [totalTasks, "tested tasks"],
                [totalFollowUps, "follow-ups"],
                [0, "installs"],
              ].map(([n, l]) => (
                <div key={l}>
                  <dt className="font-mono text-2xl text-text">{n}</dt>
                  <dd className="mt-1 text-xs text-dim">{l}</dd>
                </div>
              ))}
            </dl>
          </div>
          <TerminalCard />
        </div>
      </section>

      <section className="mx-auto w-full max-w-6xl px-4 py-20 sm:px-6">
        <div className="label text-accent">How it works</div>
        <h2 className="mt-2 text-2xl font-semibold tracking-tight">The same loop for every topic</h2>
        <div className="mt-8 grid gap-px overflow-hidden rounded-2xl border border-line bg-line sm:grid-cols-2 lg:grid-cols-4">
          {STEPS.map((s) => (
            <div key={s.k} className="bg-raised p-6">
              <div className="font-mono text-xs text-accent">{s.k}</div>
              <h3 className="mt-3 font-semibold">{s.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted">{s.body}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto w-full max-w-6xl px-4 sm:px-6">
        <div className="grid gap-10 rounded-2xl border border-line bg-raised p-6 sm:p-8 lg:grid-cols-[1fr_1.4fr]">
          <div>
            <div className="label text-accent">The final round</div>
            <h2 className="mt-2 text-2xl font-semibold tracking-tight">4–6 back-to-back interviews, 30–45 minutes each</h2>
            <p className="mt-3 text-sm leading-relaxed text-muted">
              Each one is run by a different interviewer focusing on one area. Linear regression comes up again and again. Interviewers care
              about how you think: stating assumptions, explaining trade-offs, and staying calm when pushed.
            </p>
            <Link href="/guide" className="mt-5 inline-block text-sm text-accent hover:underline">
              Read the full interview guide →
            </Link>
          </div>
          <div className="divide-y divide-line">
            {ROUNDS.map(([t, d, where]) => (
              <div key={t} className="flex items-start gap-4 py-3.5 first:pt-0 last:pb-0">
                <div className="min-w-0 flex-1">
                  <div className="font-medium text-text">{t}</div>
                  <div className="mt-0.5 text-sm text-muted">{d}</div>
                </div>
                <span className="shrink-0 rounded-md border border-line px-2 py-0.5 font-mono text-[11px] text-dim">{where}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="modules" className="mx-auto w-full max-w-6xl scroll-mt-20 px-4 py-20 sm:px-6">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <div className="label text-accent">Modules</div>
            <h2 className="mt-2 text-2xl font-semibold tracking-tight">From Python warm-up to a timed mock</h2>
          </div>
          <Link href="/plan" className="text-sm text-accent hover:underline">
            See the session-by-session plan →
          </Link>
        </div>
        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {modules.map((m) => (
            <ModuleCard key={m.slug} m={m} />
          ))}
        </div>
      </section>
      <SiteFooter />
    </>
  );
}
