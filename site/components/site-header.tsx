"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV = [
  { href: "/plan", label: "Roadmap" },
  { href: "/modules", label: "Modules" },
  { href: "/cv", label: "CV coach" },
  { href: "/guide", label: "Guide" },
  { href: "/cheatsheets", label: "Cheatsheets" },
];

export function Logo() {
  return (
    <span className="flex items-center gap-2.5">
      <span className="grid size-7 place-items-center rounded-md bg-accent font-mono text-[13px] font-bold text-accent-ink">SD</span>
      <span className="hidden font-semibold tracking-tight text-text sm:inline">
        Superday<span className="text-dim">/</span>prep
      </span>
    </span>
  );
}

export function SiteHeader() {
  const path = usePathname();
  const inWorkspace = path.startsWith("/modules/");
  return (
    <header className="sticky top-0 z-40 border-b border-line bg-bg/85 backdrop-blur-md">
      <div className={`mx-auto flex h-14 items-center gap-3 px-4 sm:gap-6 sm:px-6 ${inWorkspace ? "" : "max-w-6xl"}`}>
        <Link href="/" aria-label="Home">
          <Logo />
        </Link>
        <nav className="flex min-w-0 items-center gap-1 overflow-x-auto text-sm no-scrollbar">
          {NAV.map((n) => {
            const active = path === n.href || path.startsWith(n.href + "/");
            return (
              <Link
                key={n.href}
                href={n.href}
                className={`whitespace-nowrap rounded-md px-2.5 py-1.5 transition-colors ${
                  active ? "bg-panel-2 text-text" : "text-muted hover:text-text"
                }`}
              >
                {n.label}
              </Link>
            );
          })}
        </nav>
        <span className="ml-auto hidden items-center gap-2 font-mono text-[11px] text-dim md:flex">
          <span className="size-1.5 rounded-full bg-pass" /> runs in your browser · no sign-up
        </span>
      </div>
    </header>
  );
}
