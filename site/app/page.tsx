import Link from "next/link";
import { type PlanEntry, PlanList, type PlanRow } from "@/components/plan-list";
import { SiteFooter } from "@/components/site-footer";
import { content, moduleByFolder, planHref, planLabel } from "@/lib/content";

const entry = ([key, note]: [string] | [string, string]): PlanEntry => {
  const m = moduleByFolder(key);
  return {
    href: planHref(key),
    label: m ? m.short : planLabel(key),
    note: note ?? "",
    folder: m?.folder,
    taskIds: m?.tasks.map((t) => t.id),
  };
};

const rows: PlanRow[] = [
  ...content.plan.sessions.map((s) => ({ key: `s${s.n}`, when: String(s.n), hours: `${s.hours} h`, entries: s.items.map(entry) })),
  ...content.plan.daily.map((d, i) => ({ key: `d${i}`, when: "daily", hours: "8 min", entries: [entry(d)] })),
];
const totalHours = content.plan.sessions.reduce((h, s) => h + s.hours, 0);

const A = ({ href, children }: { href: string; children: React.ReactNode }) => (
  <Link href={href} className="text-text underline decoration-line-strong underline-offset-4 hover:decoration-accent">
    {children}
  </Link>
);

export default function Home() {
  return (
    <>
      <main className="mx-auto w-full max-w-2xl px-6 pb-8 pt-16 sm:pt-24">
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Citadel quant final round prep</h1>

        <div className="mt-8 space-y-5 text-[17px] leading-relaxed text-muted">
          <p>
            I put this together while preparing for the final round of the Citadel Securities quant research internship. It&apos;s
            the material from my GitHub repo, made easier to use: the exercises run here in the browser, and hints and answers stay
            folded until you ask for them.
          </p>
          <p>
            The final round is four to six interviews of 30–45 minutes each. Expect <A href="/modules/probability-ev">probability and
            brainteasers</A>, <A href="/modules/algorithms">live coding in Python</A>, <A href="/modules/linear-regression">ML and
            statistics</A> (linear regression comes up a lot), and a <A href="/cv">deep dive on your CV</A>. The plan below covers
            all of them.
          </p>
        </div>

        <div className="mt-8 flex flex-wrap items-center gap-x-6 gap-y-3">
          <Link href="/guide" className="rounded-md bg-accent px-4 py-2 text-sm font-semibold text-accent-ink hover:brightness-110">
            Start with session 1
          </Link>
          <Link href="/plan" className="text-sm text-muted hover:text-text">
            Short on time? The fast track →
          </Link>
        </div>

        <section className="mt-16">
          <div className="mb-3 flex items-baseline justify-between">
            <h2 className="font-medium text-text">The plan</h2>
            <span className="font-mono text-xs text-dim">≈ {totalHours} h over {content.plan.sessions.length} sessions</span>
          </div>
          <PlanList rows={rows} />
          <p className="mt-4 text-sm leading-relaxed text-dim">
            Each module has short notes, coding tasks checked by tests, and the follow-up questions an interviewer asks once your code
            works. Your code and progress stay in this browser.
          </p>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
