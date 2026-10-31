import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import { SiteHeader } from "@/components/site-header";
import "./globals.css";

const inter = Inter({ variable: "--font-inter", subsets: ["latin"] });
const jetbrains = JetBrains_Mono({ variable: "--font-jetbrains", subsets: ["latin"] });

export const metadata: Metadata = {
  title: { default: "Superday Prep · Citadel track", template: "%s · Superday Prep" },
  description:
    "Free, interactive preparation for the Citadel / Citadel Securities quant final round: Python and ML exercises that run in your browser, interviewer follow-ups, and a personalised CV deep dive.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrains.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col">
        <SiteHeader />
        <div className="flex-1 flex flex-col">{children}</div>
      </body>
    </html>
  );
}
