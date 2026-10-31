import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Suspense } from "react";
import { DocPage } from "@/components/doc-page";
import { content } from "@/lib/content";

export function generateStaticParams() {
  return content.cheatsheets.map((c) => ({ slug: c.slug }));
}

export async function generateMetadata({ params }: PageProps<"/cheatsheets/[slug]">): Promise<Metadata> {
  const { slug } = await params;
  const c = content.cheatsheets.find((x) => x.slug === slug);
  return c ? { title: c.title } : {};
}

export default function CheatsheetPage({ params }: PageProps<"/cheatsheets/[slug]">) {
  return (
    <Suspense>
      <Cheatsheet params={params} />
    </Suspense>
  );
}

async function Cheatsheet({ params }: { params: PageProps<"/cheatsheets/[slug]">["params"] }) {
  const { slug } = await params;
  const doc = content.cheatsheets.find((c) => c.slug === slug);
  if (!doc) notFound();
  const nav = content.cheatsheets.map((c) => ({ href: `/cheatsheets/${c.slug}`, label: c.title.replace(/\s*\(.*\)$/, ""), active: c.slug === slug }));
  return <DocPage doc={doc} eyebrow="Cheatsheet" nav={nav} />;
}
