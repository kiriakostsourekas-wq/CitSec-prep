import { redirect } from "next/navigation";
import { content } from "@/lib/content";

export default function CheatsheetsIndex() {
  redirect(`/cheatsheets/${content.cheatsheets.find((c) => c.slug === "python")?.slug ?? content.cheatsheets[0].slug}`);
}
