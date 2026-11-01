"use client";
import { useEffect } from "react";
import { markVisited } from "@/lib/progress";

/** Lights up this page's stop on the plan map once it has been opened. */
export function MarkVisited({ id }: { id: string }) {
  useEffect(() => markVisited(id), [id]);
  return null;
}
