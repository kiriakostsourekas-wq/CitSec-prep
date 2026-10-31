import type { Metadata } from "next";
import { DocPage } from "@/components/doc-page";
import { content } from "@/lib/content";
import { guideNav } from "../nav";

export const metadata: Metadata = { title: "ML & stats rapid-fire" };

export default function MlStatsPage() {
  return <DocPage doc={content.guide.mlStats} eyebrow="Interview guide · answer out loud, then open" nav={guideNav("/guide/ml-stats")} />;
}
