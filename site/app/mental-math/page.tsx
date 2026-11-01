import type { Metadata } from "next";
import { SectionsView } from "@/components/doc-view";
import { MentalMath } from "@/components/drill/mental-math";
import { SiteFooter } from "@/components/site-footer";
import { content } from "@/lib/content";

export const metadata: Metadata = {
  title: "Mental math",
  description: "A timed arithmetic drill for quant interviews: multiplication, division, percentages, fractions, squares and quick expected values.",
};

export default function MentalMathPage() {
  return (
    <>
      <main className="mx-auto w-full max-w-3xl px-6 py-14">
        <h1 className="font-serif text-[2.2rem] font-semibold leading-[1.15] tracking-[-0.015em]">Mental math</h1>
        <p className="mt-4 max-w-2xl leading-relaxed text-muted">
          Eight minutes a day until the interview. Some trading firms screen with a timed arithmetic test (about 60–80 questions in 8
          minutes), and in probability rounds fast arithmetic is what lets you keep talking while you think. Go for accuracy first, then
          speed.
        </p>
        <div className="mt-10">
          <MentalMath />
        </div>
        <div className="mt-16">
          <SectionsView sections={content.mentalMath.sections} />
        </div>
      </main>
      <SiteFooter />
    </>
  );
}
