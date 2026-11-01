import type { Metadata } from "next";
import { CvCoach } from "@/components/cv/cv-coach";
import { SiteFooter } from "@/components/site-footer";
import { content, modules } from "@/lib/content";
import { buildOfflineBank } from "@/lib/cv/offline";

export const metadata: Metadata = {
  title: "CV coach",
  description: "Drop your CV and get the deep-dive questions a Citadel interviewer is likely to ask about it, then practise your answers.",
};

export default function CvPage() {
  const bank = buildOfflineBank(content.guide.cv.sections);
  const moduleTitles = Object.fromEntries(modules.map((m) => [m.slug, m.title]));
  return (
    <>
      <CvCoach bank={bank} moduleTitles={moduleTitles} />
      <SiteFooter />
    </>
  );
}
