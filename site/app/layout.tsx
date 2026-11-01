import type { Metadata } from "next";
import { IBM_Plex_Mono, IBM_Plex_Sans, Source_Serif_4 } from "next/font/google";
import { SiteHeader } from "@/components/site-header";
import "./globals.css";

// Source Serif for reading and headings, Plex Sans for the interface, Plex Mono only for code.
const serif = Source_Serif_4({ variable: "--font-source-serif", subsets: ["latin"], axes: ["opsz"] });
const sans = IBM_Plex_Sans({ variable: "--font-plex-sans", subsets: ["latin"] });
const mono = IBM_Plex_Mono({ variable: "--font-plex-mono", subsets: ["latin"], weight: ["400", "500"] });

export const metadata: Metadata = {
  title: { default: "Superday Prep · Citadel track", template: "%s · Superday Prep" },
  description:
    "Free, interactive preparation for the Citadel / Citadel Securities quant final round: Python and ML exercises that run in your browser, interviewer follow-ups, and a personalised CV deep dive.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${serif.variable} ${sans.variable} ${mono.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col">
        <SiteHeader />
        <div className="flex-1 flex flex-col">{children}</div>
      </body>
    </html>
  );
}
