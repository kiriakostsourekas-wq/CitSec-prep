import type { Metadata } from "next";
import Link from "next/link";
import { ModuleCard } from "@/components/module-card";
import { SiteFooter } from "@/components/site-footer";
import { modules } from "@/lib/content";

export const metadata: Metadata = { title: "Modules" };

export default function ModulesPage() {
  return (
    <>
      <div className="mx-auto w-full max-w-6xl px-4 py-12 sm:px-6">
        <div className="label text-accent">Citadel track · 12 modules</div>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight">Modules</h1>
        <p className="mt-3 max-w-2xl text-muted">
          Each module has concept notes, coding tasks that go from A (easy) to D (interview-style), hints you open one at a time,
          and a reference solution. Do them in order. Your code and progress stay in this browser.
        </p>
        <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {modules.map((m) => (
            <ModuleCard key={m.slug} m={m} />
          ))}
          <Link
            href="/mental-math"
            className="flex flex-col rounded-2xl border border-line bg-raised p-5 transition-colors hover:border-line-strong hover:bg-panel"
          >
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs text-accent">11</span>
              <span className="ml-auto font-mono text-[11px] text-dim">8 min a day</span>
            </div>
            <h3 className="mt-3 font-semibold tracking-tight text-text">Mental math</h3>
            <p className="mt-1.5 flex-1 text-sm leading-relaxed text-muted">
              A timed arithmetic drill: multiplication, percentages, fractions, squares and quick expected values.
            </p>
          </Link>
        </div>
      </div>
      <SiteFooter />
    </>
  );
}
