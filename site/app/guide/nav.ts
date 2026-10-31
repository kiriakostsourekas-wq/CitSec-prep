export const guideNav = (active: string) =>
  [
    { href: "/guide", label: "Final-round format" },
    { href: "/guide/ml-stats", label: "ML & stats rapid-fire" },
    { href: "/guide/cv", label: "CV & behavioural" },
  ].map((n) => ({ ...n, active: n.href === active }));
