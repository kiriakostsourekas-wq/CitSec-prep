import type { Metadata } from "next";
import { DocPage } from "@/components/doc-page";
import { content } from "@/lib/content";
import { guideNav } from "../nav";

export const metadata: Metadata = { title: "CV deep dive & behavioural" };

export default function CvPage() {
  return <DocPage doc={content.guide.cv} eyebrow="Interview guide · every line of your CV is fair game" nav={guideNav("/guide/cv")} />;
}
