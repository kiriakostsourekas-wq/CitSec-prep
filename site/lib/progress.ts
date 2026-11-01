"use client";
// Everything a learner does is kept in this browser only (localStorage). No accounts, nothing sent anywhere.
import { useSyncExternalStore } from "react";

export type TaskStatus = "PASS" | "FAIL" | "TODO" | "ERROR";
export type Rating = "nailed" | "shaky" | "missed";

export type Progress = {
  tasks: Record<string, TaskStatus>; // "04_linear_regression:A1"
  hints: Record<string, number>; // hints opened per task
  solutions: Record<string, true>; // solutions revealed per task
  followUps: Record<string, Rating>; // "04_linear_regression:3"
  checklist: Record<string, boolean>;
  visited: Record<string, true>; // non-coding stops on the map: "guide", "guide/cv", "mental-math", …
  fastTrack: boolean;
};

const KEY = "citprep:v1:progress";
const CODE_KEY = (folder: string) => `citprep:v1:code:${folder}`;
const EMPTY: Progress = { tasks: {}, hints: {}, solutions: {}, followUps: {}, checklist: {}, visited: {}, fastTrack: false };

const listeners = new Set<() => void>();
let cache: Progress | null = null;

function load(): Progress {
  if (cache) return cache;
  try {
    cache = { ...EMPTY, ...JSON.parse(localStorage.getItem(KEY) ?? "{}") };
  } catch {
    cache = { ...EMPTY };
  }
  return cache!;
}

export function updateProgress(fn: (p: Progress) => Progress) {
  cache = fn(load());
  try {
    localStorage.setItem(KEY, JSON.stringify(cache));
  } catch {
    /* private mode or storage full: progress still works for this visit */
  }
  listeners.forEach((l) => l());
}

function subscribe(fn: () => void) {
  listeners.add(fn);
  const onStorage = (e: StorageEvent) => {
    if (e.key === KEY) {
      cache = null;
      fn();
    }
  };
  window.addEventListener("storage", onStorage);
  return () => {
    listeners.delete(fn);
    window.removeEventListener("storage", onStorage);
  };
}

export function useProgress(): Progress {
  return useSyncExternalStore(subscribe, load, () => EMPTY);
}

/** Mark a non-coding stop of the plan as done (reading a guide page, finishing a drill run). */
export function markVisited(key: string) {
  if (load().visited[key]) return;
  updateProgress((p) => ({ ...p, visited: { ...p.visited, [key]: true } }));
}

export const taskKey = (folder: string, id: string) => `${folder}:${id}`;

export function loadCode(folder: string): string | null {
  try {
    return localStorage.getItem(CODE_KEY(folder));
  } catch {
    return null;
  }
}

export function saveCode(folder: string, code: string) {
  try {
    localStorage.setItem(CODE_KEY(folder), code);
  } catch {
    /* ignore */
  }
}

/** Download everything (progress + code) as one JSON file, and load it back on another device. */
export function exportAll(): string {
  const out: Record<string, string> = {};
  for (let i = 0; i < localStorage.length; i++) {
    const k = localStorage.key(i)!;
    if (k.startsWith("citprep:")) out[k] = localStorage.getItem(k)!;
  }
  return JSON.stringify(out, null, 1);
}

export function importAll(json: string) {
  const data = JSON.parse(json) as Record<string, string>;
  for (const [k, v] of Object.entries(data)) if (k.startsWith("citprep:")) localStorage.setItem(k, v);
  cache = null;
  listeners.forEach((l) => l());
}
