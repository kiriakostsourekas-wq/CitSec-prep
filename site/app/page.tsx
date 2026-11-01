import Link from "next/link";
import { type MapStop, PlanMap } from "@/components/plan-map";
import { SiteFooter } from "@/components/site-footer";
import { content, moduleByFolder, planHref, planLabel } from "@/lib/content";
import { STOPS } from "@/lib/plan-map";

// Notes for each stop, gathered from every place it appears in the plan ("part A (numpy)", "parts B–D (pandas)").
const notes = new Map<string, string[]>();
for (const item of [...content.plan.sessions.flatMap((s) => s.items), ...content.plan.daily])
  if (item[1]) notes.set(item[0], [...(notes.get(item[0]) ?? []), item[1]]);

const stops: MapStop[] = STOPS.map((s) => {
  const m = moduleByFolder(s.key);
  return {
    ...s,
    title: m ? m.title : planLabel(s.key),
    href: planHref(s.key),
    time: m?.time ?? "",
    note: (notes.get(s.key) ?? []).join(", then "),
    folder: m?.folder,
    taskIds: m?.tasks.map((t) => t.id),
  };
});
const totalHours = content.plan.sessions.reduce((h, s) => h + s.hours, 0);

const A = ({ href, children }: { href: string; children: React.ReactNode }) => (
  <Link href={href} className="text-text underline decoration-line-strong underline-offset-4 hover:decoration-accent">
    {children}
  </Link>
);

export default function Home() {
  return (
    <>
      <main className="mx-auto w-full max-w-2xl px-6 pt-16 sm:pt-24">
        <h1 className="font-serif text-[2.2rem] font-semibold leading-[1.1] tracking-[-0.015em] sm:text-[2.75rem]">Citadel quant final round prep</h1>

        <div className="mt-7 space-y-5 font-serif text-[19px] leading-[1.6] text-reading">
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
            Short on time? Use the fast track
          </Link>
        </div>

      </main>

      <section className="mx-auto w-full max-w-5xl px-6 pb-8 pt-14">
        <div className="mb-4 flex items-baseline justify-between">
          <h2 className="shrink-0 font-serif text-2xl font-semibold tracking-[-0.01em] text-text">The plan</h2>
          <span className="text-sm tabular-nums text-dim">
            About {totalHours} hours over {content.plan.sessions.length} sessions
          </span>
        </div>
        <PlanMap stops={stops} sessions={content.plan.sessions.map((s) => ({ n: s.n, hours: s.hours }))} />
        <p className="mt-4 text-sm leading-relaxed text-dim">
          Each line is one interview round. A station lights up when you finish it, and your progress stays in this browser.
        </p>
      </section>
      <SiteFooter />
    </>
  );
}
