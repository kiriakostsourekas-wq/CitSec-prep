import type { Metadata } from "next";
import { DocPage } from "@/components/doc-page";
import { content } from "@/lib/content";
import { guideNav } from "./nav";

export const metadata: Metadata = { title: "Interview guide" };

export default function GuidePage() {
  return <DocPage doc={content.guide.main} eyebrow="Interview guide · read first" nav={guideNav("/guide")} />;
}
