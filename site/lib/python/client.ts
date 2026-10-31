"use client";
// One shared Python runtime per tab. Pyodide lives in public/runtime/py-worker.mjs; this file talks to it.
import { useSyncExternalStore } from "react";

export type PyStatus = { status: "idle" | "loading" | "ready" | "running" | "error"; detail: string };

export type CheckResult = {
  id: string;
  func: string;
  title: string;
  status: "PASS" | "FAIL" | "TODO" | "ERROR";
  message: string;
  output: string;
  line?: number | null;
};
export type ChecksResponse = { fatal?: string; results?: CheckResult[]; importOutput?: string };
export type ScriptResponse = { error: string | null; images: { name: string; png: string }[] };

type Pending = { resolve: (v: unknown) => void; reject: (e: Error) => void; onOutput?: (t: string) => void };

class PythonRuntime {
  private worker: Worker | null = null;
  private pending = new Map<number, Pending>();
  private nextId = 1;
  private listeners = new Set<() => void>();
  state: PyStatus = { status: "idle", detail: "" };

  subscribe = (fn: () => void) => {
    this.listeners.add(fn);
    return () => this.listeners.delete(fn);
  };

  private set(state: PyStatus) {
    this.state = state;
    this.listeners.forEach((fn) => fn());
  }

  private ensure() {
    if (this.worker) return this.worker;
    const w = new Worker("/runtime/py-worker.mjs", { type: "module" });
    w.onmessage = ({ data }) => {
      if (data.type === "status") return this.set({ status: data.status, detail: data.detail ?? "" });
      if (data.type === "stdout") return this.pending.get(data.id)?.onOutput?.(data.text + "\n");
      const p = this.pending.get(data.id);
      if (!p) return;
      this.pending.delete(data.id);
      if (data.ok) p.resolve(data.result);
      else p.reject(new Error(data.error));
    };
    w.onerror = (e) => this.set({ status: "error", detail: e.message || "Python worker crashed" });
    this.worker = w;
    this.call({ type: "init" }).catch(() => {});
    return w;
  }

  private call<T>(msg: Record<string, unknown>, onOutput?: (t: string) => void): Promise<T> {
    const w = this.ensure();
    const id = this.nextId++;
    return new Promise<T>((resolve, reject) => {
      this.pending.set(id, { resolve: resolve as (v: unknown) => void, reject, onOutput });
      w.postMessage({ id, ...msg });
    });
  }

  /** Start downloading Python in the background (call when a workspace opens). */
  warmUp() {
    this.ensure();
  }

  private async job<T>(files: string[], writes: Record<string, string>, msg: Record<string, unknown>, onOutput?: (t: string) => void) {
    await this.call({ type: "mount", files });
    for (const [path, content] of Object.entries(writes)) await this.call({ type: "write", path, content });
    this.set({ status: "running", detail: "" });
    try {
      return await this.call<T>(msg, onOutput);
    } finally {
      if (this.state.status === "running") this.set({ status: "ready", detail: "" });
    }
  }

  runScript(folder: string, filename: string, files: string[], writes: Record<string, string>, onOutput: (t: string) => void) {
    return this.job<ScriptResponse>(files, writes, { type: "script", folder, filename }, onOutput);
  }

  runChecks(folder: string, which: "exercise" | "solution", files: string[], writes: Record<string, string>, wanted?: string[]) {
    return this.job<ChecksResponse>(files, writes, { type: "checks", folder, which, wanted });
  }

  /** Kill a runaway program (infinite loop): restart the worker. Python reloads from the browser cache. */
  stop() {
    this.worker?.terminate();
    this.worker = null;
    for (const p of this.pending.values()) p.reject(new Error("Stopped."));
    this.pending.clear();
    this.set({ status: "idle", detail: "" });
    this.ensure();
  }
}

let runtime: PythonRuntime | null = null;
export function getPython() {
  runtime ??= new PythonRuntime();
  return runtime;
}

const idle: PyStatus = { status: "idle", detail: "" };
export function usePythonStatus(): PyStatus {
  const py = getPython();
  return useSyncExternalStore(py.subscribe, () => py.state, () => idle);
}
