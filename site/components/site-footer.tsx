export const REPO_URL = "https://github.com/kiriakostsourekas-wq/CitSec-prep";

export function SiteFooter() {
  return (
    <footer className="mt-24 border-t border-line">
      <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-8 text-xs leading-relaxed text-dim sm:px-6 md:flex-row md:items-start md:justify-between">
        <p className="max-w-2xl">
          Unofficial, community-made study material. Not affiliated with, endorsed by, or connected to Citadel LLC or Citadel Securities. The interview
          format is summarised from public candidate reports and may differ from your own process.
        </p>
        <p className="flex gap-4 whitespace-nowrap">
          <a href={REPO_URL} target="_blank" rel="noreferrer" className="hover:text-muted">
            Source on GitHub
          </a>
          <span>Code runs locally in your browser</span>
        </p>
      </div>
    </footer>
  );
}
