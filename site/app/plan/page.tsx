import type { Metadata } from "next";
import { SiteFooter } from "@/components/site-footer";
import { content, moduleByFolder, planHref, planLabel } from "@/lib/content";
import { Roadmap, type RoadmapItem } from "./roadmap";

export const metadata: Metadata = { title: "Roadmap" };

const toItem = ([key, note]: [string] | [string, string]): RoadmapItem => {
  const m = moduleByFolder(key);
  return { key, note: note ?? "", href: planHref(key), label: planLabel(key), folder: m?.folder, taskIds: m?.tasks.map((t) => t.id) };
};

export default function PlanPage() {
  const day = content.guide.main.sections.find((s) => s.heading.startsWith("5."));
  const checklist = (day?.blocks ?? [])
    .flatMap((b) => (b.kind === "md" ? b.md.split("\n") : []))
    .filter((l) => l.startsWith("- [ ]"))
    .map((l) => l.slice(5).trim());

  return (
    <>
      <div className="mx-auto w-full max-w-6xl px-4 py-12 sm:px-6">
        <div className="label text-accent">Study plan · Citadel track</div>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight">Your roadmap to the superday</h1>
        <p className="mt-3 max-w-2xl text-muted">
          Six sessions of about three hours each (≈ 13 h core). Short on time? Switch to the 6-hour fast track. The evening before,
          go through the checklist.
        </p>
        <Roadmap
          sessions={content.plan.sessions.map((s) => ({ n: s.n, hours: s.hours, items: s.items.map(toItem) }))}
          fastTrack={content.plan.fastTrack.map(toItem)}
          checklist={checklist}
        />
      </div>
      <SiteFooter />
    </>
  );
}
