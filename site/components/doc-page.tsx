import Link from "next/link";
import type { Doc } from "@/lib/content";
import { anchor, SectionsView } from "./doc-view";
import { SiteFooter } from "./site-footer";

type NavLink = { href: string; label: string; active?: boolean };

/** Reading layout: side navigation, the document, and an on-page table of contents. */
export function DocPage({ doc, eyebrow, nav, intro }: { doc: Doc; eyebrow: string; nav: NavLink[]; intro?: React.ReactNode }) {
  const toc = doc.sections.filter((s) => s.heading);
  return (
    <>
      <div className="mx-auto grid w-full max-w-6xl gap-10 px-4 py-10 sm:px-6 lg:grid-cols-[200px_minmax(0,1fr)_200px]">
        <nav className="flex gap-1 overflow-x-auto lg:sticky lg:top-24 lg:flex-col lg:self-start">
          {nav.map((n) => (
            <Link
              key={n.href}
              href={n.href}
              className={`whitespace-nowrap rounded-md px-3 py-1.5 text-sm ${n.active ? "bg-panel-2 text-text" : "text-muted hover:text-text"}`}
            >
              {n.label}
            </Link>
          ))}
        </nav>
        <article className="min-w-0">
          <div className="label text-accent">{eyebrow}</div>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight">{doc.title}</h1>
          {intro}
          <div className="mt-8">
            <SectionsView sections={doc.sections} />
          </div>
        </article>
        <aside className="hidden lg:sticky lg:top-24 lg:block lg:self-start">
          {toc.length > 1 && (
            <>
              <div className="label mb-2">On this page</div>
              <ul className="space-y-1.5 text-[13px]">
                {toc.map((s) => (
                  <li key={s.heading}>
                    <a href={`#${anchor(s.heading)}`} className="line-clamp-2 text-dim hover:text-muted">
                      {s.heading}
                    </a>
                  </li>
                ))}
              </ul>
            </>
          )}
        </aside>
      </div>
      <SiteFooter />
    </>
  );
}
