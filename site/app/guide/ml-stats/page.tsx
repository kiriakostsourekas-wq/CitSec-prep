import type { Metadata } from "next";
import { DocPage } from "@/components/doc-page";
import { MarkVisited } from "@/components/mark-visited";
import { content } from "@/lib/content";
import { guideNav } from "../nav";

export const metadata: Metadata = { title: "ML & stats rapid-fire" };

export default function MlStatsPage() {
  return (
    <>
      <MarkVisited id="guide/ml-stats" />
      <DocPage doc={content.guide.mlStats} eyebrow="Interview guide · answer out loud, then open" nav={guideNav("/guide/ml-stats")} />
    </>
  );
}
