import Link from "next/link";
import { ModuleCount } from "@/components/module-progress";
import { SiteFooter } from "@/components/site-footer";
import { content, followUpCount, modules } from "@/lib/content";

const totalTasks = modules.reduce((n, m) => n + m.tasks.length, 0);
const totalFollowUps =
  modules.reduce((n, m) => n + followUpCount(m), 0) +
  content.guide.mlStats.sections.reduce((n, s) => n + s.blocks.filter((b) => b.kind === "fold").length, 0);

const INSIDE = [
  { href: "/modules", title: "Modules", body: "Concept notes, coding tasks with hints, and the kit's own tests." },
  { href: "/cv", title: "CV coach", body: "The questions your CV will get, and feedback on your answers." },
  { href: "/guide", title: "Guide", body: "The final-round format, ML & stats rapid-fire, behavioural." },
  { href: "/plan", title: "Roadmap", body: "Six sessions of about three hours, or a 6-hour fast track." },
];

function SectionLabel({ children }: { children: React.ReactNode }) {
  return <h2 className="label mb-4">{children}</h2>;
}

export default function Home() {
  return (
    <>
      <main className="mx-auto w-full max-w-3xl px-6">
        <section className="pb-20 pt-20 sm:pt-28">
          <p className="font-mono text-xs text-accent">Citadel · Citadel Securities · quant final rounds</p>
          <h1 className="mt-5 text-4xl font-semibold leading-[1.1] tracking-tight sm:text-5xl">
            Walk into your superday
            <br className="hidden sm:block" />{" "}
            having <span className="text-accent">already done it.</span>
          </h1>
          <p className="mt-6 max-w-xl text-lg leading-relaxed text-muted">
            Free prep built from one candidate&apos;s real preparation: Python and ML exercises that run in your browser, the follow-ups
            interviewers ask, and a CV coach.
          </p>
          <div className="mt-9 flex flex-wrap items-center gap-x-6 gap-y-3">
            <Link href="/plan" className="rounded-md bg-accent px-4 py-2 text-sm font-semibold text-accent-ink hover:brightness-110">
              Start the roadmap
            </Link>
            <Link href="/modules/linear-regression" className="text-sm text-muted hover:text-text">
              Try linear regression →
            </Link>
          </div>
          <p className="mt-12 font-mono text-xs text-dim">
            {modules.length} modules · {totalTasks} tested tasks · {totalFollowUps} follow-ups · nothing to install
          </p>
        </section>

        <section className="pb-20">
          <SectionLabel>Inside</SectionLabel>
          <ul className="divide-y divide-line border-y border-line">
            {INSIDE.map((i) => (
              <li key={i.href}>
                <Link href={i.href} className="group flex items-baseline gap-6 py-4">
                  <span className="w-24 shrink-0 text-text">{i.title}</span>
                  <span className="min-w-0 flex-1 text-sm text-muted">{i.body}</span>
                  <span className="text-dim transition-colors group-hover:text-accent">→</span>
                </Link>
              </li>
            ))}
          </ul>
        </section>

        <section className="pb-8">
          <SectionLabel>Modules</SectionLabel>
          <ul className="divide-y divide-line border-y border-line">
            {modules.map((m) => (
              <li key={m.slug}>
                <Link href={`/modules/${m.slug}`} className="group flex items-baseline gap-4 py-3">
                  <span className="w-6 shrink-0 font-mono text-xs text-dim">{m.number}</span>
                  <span className="min-w-0 flex-1 truncate text-text group-hover:text-white">{m.title}</span>
                  <ModuleCount folder={m.folder} taskIds={m.tasks.map((t) => t.id)} fallback={m.time} />
                </Link>
              </li>
            ))}
          </ul>
        </section>
      </main>
      <SiteFooter />
    </>
  );
}
