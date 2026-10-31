import Link from "next/link";
import ReactMarkdown from "react-markdown";
import rehypeHighlight from "rehype-highlight";
import remarkGfm from "remark-gfm";

/** Renders the kit's markdown. Internal links use client-side navigation. */
export function Markdown({ md, className = "" }: { md: string; className?: string }) {
  return (
    <div className={`md ${className}`}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[[rehypeHighlight, { detect: false, ignoreMissing: true }]]}
        components={{
          a: ({ href = "", children }) =>
            href.startsWith("/") ? (
              <Link href={href}>{children}</Link>
            ) : (
              <a href={href} target="_blank" rel="noreferrer">
                {children}
              </a>
            ),
        }}
      >
        {md}
      </ReactMarkdown>
    </div>
  );
}

/** Inline markdown for one-liners such as fold summaries (no wrapping paragraph). */
export function InlineMarkdown({ md }: { md: string }) {
  return (
    <span className="md [&_p]:inline">
      <ReactMarkdown remarkPlugins={[remarkGfm]} allowedElements={["p", "code", "strong", "em", "a"]} unwrapDisallowed>
        {md}
      </ReactMarkdown>
    </span>
  );
}
