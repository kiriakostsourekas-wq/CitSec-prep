import type { Metadata } from "next";
import { ModuleCard } from "@/components/module-card";
import { SiteFooter } from "@/components/site-footer";
import { modules } from "@/lib/content";

export const metadata: Metadata = { title: "Modules" };

export default function ModulesPage() {
  return (
    <>
      <div className="mx-auto w-full max-w-6xl px-4 py-12 sm:px-6">
        <div className="label text-accent">Citadel track · 10 modules</div>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight">Modules</h1>
        <p className="mt-3 max-w-2xl text-muted">
          Each module has concept notes, coding tasks that go from A (easy) to D (interview-style), hints you open one at a time,
          and a reference solution. Do them in order. Your code and progress stay in this browser.
        </p>
        <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {modules.map((m) => (
            <ModuleCard key={m.slug} m={m} />
          ))}
        </div>
      </div>
      <SiteFooter />
    </>
  );
}
