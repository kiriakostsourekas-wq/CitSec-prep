import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { Suspense } from "react";
import { Workspace } from "@/components/workspace/workspace";
import { getModule, modules } from "@/lib/content";

export function generateStaticParams() {
  return modules.map((m) => ({ slug: m.slug }));
}

export async function generateMetadata({ params }: PageProps<"/modules/[slug]">): Promise<Metadata> {
  const m = getModule((await params).slug);
  return m ? { title: `${m.number} · ${m.title}`, description: m.blurb } : {};
}

async function ModuleWorkspace({ params }: { params: PageProps<"/modules/[slug]">["params"] }) {
  const m = getModule((await params).slug);
  if (!m) notFound();
  return <Workspace module={m} />;
}

export default function ModulePage({ params }: PageProps<"/modules/[slug]">) {
  return (
    <Suspense fallback={<div className="h-[calc(100dvh-3.5rem)] animate-pulse bg-raised" />}>
      <ModuleWorkspace params={params} />
    </Suspense>
  );
}
