import type { Metadata } from "next";
import { DocPage } from "@/components/doc-page";
import { MarkVisited } from "@/components/mark-visited";
import { content } from "@/lib/content";
import { guideNav } from "./nav";

export const metadata: Metadata = { title: "Interview guide" };

export default function GuidePage() {
  return (
    <>
      <MarkVisited id="guide" />
      <DocPage doc={content.guide.main} nav={guideNav("/guide")} />
    </>
  );
}
