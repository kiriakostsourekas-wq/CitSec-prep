import type { Section } from "@/lib/content";
import { Fold } from "./fold";
import { InlineMarkdown, Markdown } from "./markdown";

export const anchor = (heading: string) =>
  heading.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

/** A list of markdown sections where folded answers become reveal cards. */
export function SectionsView({ sections, headingLevel = 2 }: { sections: Section[]; headingLevel?: 2 | 3 }) {
  const H = headingLevel === 2 ? "h2" : "h3";
  return (
    <div className="space-y-10">
      {sections.map((s, i) => (
        <section key={i} id={s.heading ? anchor(s.heading) : undefined} className="scroll-mt-24">
          {s.heading && (
            <H className={`mb-4 font-semibold tracking-tight text-text ${H === "h2" ? "text-xl" : "text-lg"}`}>{s.heading}</H>
          )}
          <div className="space-y-3">
            {s.blocks.map((b, j) =>
              b.kind === "md" ? (
                <Markdown key={j} md={b.md} />
              ) : (
                <Fold key={j} summary={<InlineMarkdown md={b.summary} />}>
                  <Markdown md={b.md} />
                </Fold>
              ),
            )}
          </div>
        </section>
      ))}
    </div>
  );
}
