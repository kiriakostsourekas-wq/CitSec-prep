"use client";
import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";
import type { Module, Task } from "@/lib/content";
import { loadCode, saveCode, taskKey, updateProgress, useProgress } from "@/lib/progress";
import { type CheckResult, getPython } from "@/lib/python/client";
import { SectionsView } from "../doc-view";
import { CodeEditor, type CodeEditorHandle } from "./code-editor";
import { ConsolePanel, type ConsoleTab, type Image, type OutputChunk } from "./console-panel";
import { FollowUps } from "./follow-ups";
import { MockTimer } from "./mock-timer";
import { ProgressBar, PythonPill, Spinner } from "./status";
import { TaskList } from "./task-list";

type Tab = "learn" | "tasks" | "followups";
const BACKUP_KEY = (folder: string) => `citprep:v1:backup:${folder}`;

export function Workspace({ module: m }: { module: Module }) {
  const progress = useProgress();
  const [tab, setTab] = useState<Tab>("tasks");
  const [code, setCode] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [consoleTab, setConsoleTab] = useState<ConsoleTab>("checks");
  const [output, setOutput] = useState<OutputChunk[]>([]);
  const [images, setImages] = useState<Image[]>([]);
  const [checks, setChecks] = useState<CheckResult[] | null>(null);
  const [fatal, setFatal] = useState<string | null>(null);
  const [results, setResults] = useState<Record<string, CheckResult>>({});
  const [hasBackup, setHasBackup] = useState(false);
  const editor = useRef<CodeEditorHandle>(null);
  const saveTimer = useRef<ReturnType<typeof setTimeout>>(undefined);

  const passed = m.tasks.filter((t) => progress.tasks[taskKey(m.folder, t.id)] === "PASS").length;
  const allPassed = passed === m.tasks.length && m.tasks.length > 0;
  const exercisePath = `${m.folder}/exercise.py`;

  useEffect(() => {
    setCode(loadCode(m.folder) ?? m.starter);
    setHasBackup(!!localStorage.getItem(BACKUP_KEY(m.folder)));
    getPython().warmUp();
  }, [m.folder, m.starter]);

  const onChange = (v: string) => {
    setCode(v);
    clearTimeout(saveTimer.current);
    saveTimer.current = setTimeout(() => saveCode(m.folder, v), 300);
  };

  const run = useCallback(
    async (filename: "exercise.py" | "solution.py") => {
      if (code == null || busy) return;
      setBusy(true);
      setConsoleTab("output");
      setImages([]);
      setOutput([{ kind: "info", text: `$ python ${filename}\n` }]);
      const files = filename === "solution.py" ? [...m.files, m.solutionFile] : m.files;
      try {
        const res = await getPython().runScript(m.folder, filename, files, { [exercisePath]: code }, (text) =>
          setOutput((o) => [...o, { kind: "out", text }]),
        );
        if (res.error) setOutput((o) => [...o, { kind: "err", text: res.error! }]);
        setImages(res.images);
      } catch (e) {
        setOutput((o) => [...o, { kind: "err", text: String((e as Error).message) + "\n" }]);
      } finally {
        setBusy(false);
      }
    },
    [busy, code, exercisePath, m.files, m.folder, m.solutionFile],
  );

  const check = useCallback(
    async (ids?: string[]) => {
      if (code == null || busy) return;
      setBusy(true);
      setConsoleTab("checks");
      setFatal(null);
      try {
        const res = await getPython().runChecks(m.folder, "exercise", m.files, { [exercisePath]: code }, ids);
        if (res.fatal) {
          setFatal(res.fatal);
          setChecks(null);
          return;
        }
        const list = res.results ?? [];
        setChecks((prev) => (ids && prev ? prev.map((r) => list.find((x) => x.id === r.id) ?? r) : list));
        setResults((prev) => ({ ...prev, ...Object.fromEntries(list.map((r) => [r.id, r])) }));
        updateProgress((p) => ({
          ...p,
          tasks: { ...p.tasks, ...Object.fromEntries(list.map((r) => [taskKey(m.folder, r.id), r.status])) },
        }));
      } catch (e) {
        setFatal(String((e as Error).message));
      } finally {
        setBusy(false);
      }
    },
    [busy, code, exercisePath, m.files, m.folder],
  );

  const lineOf = (t: Task) => {
    const lines = (code ?? "").split("\n");
    const i = lines.findIndex((l) => new RegExp(`^(def|class) ${t.func}\\b`).test(l));
    return i + 1;
  };

  const reset = () => {
    if (!confirm("Start this exercise again from the blank template? Your current code is kept as a backup you can restore.")) return;
    localStorage.setItem(BACKUP_KEY(m.folder), code ?? "");
    setHasBackup(true);
    onChange(m.starter);
    setResults({});
    setChecks(null);
  };
  const restore = () => {
    const backup = localStorage.getItem(BACKUP_KEY(m.folder));
    if (backup == null || !confirm("Swap your current code with the saved backup?")) return;
    localStorage.setItem(BACKUP_KEY(m.folder), code ?? "");
    onChange(backup);
  };

  const tabs: { id: Tab; label: string; badge?: string }[] = [
    { id: "learn", label: "Learn" },
    { id: "tasks", label: "Tasks", badge: `${passed}/${m.tasks.length}` },
    ...(m.followUps.length
      ? [{ id: "followups" as Tab, label: m.followUps.some((s) => /problem|questions/i.test(s.heading)) ? "Questions" : "Follow-ups" }]
      : []),
  ];

  return (
    <div className="flex flex-col lg:h-[calc(100dvh-3.5rem)] lg:flex-row">
      {/* ---------------- left: notes / tasks / follow-ups */}
      <aside className="flex min-h-0 flex-col border-line lg:w-[46%] lg:max-w-[720px] lg:border-r">
        <div className="shrink-0 border-b border-line px-5 pb-0 pt-4">
          <div className="flex items-center gap-2 text-xs text-dim">
            <Link href="/modules" className="hover:text-muted">
              Modules
            </Link>
            <span>/</span>
            <span className="font-mono">{m.number}</span>
            {m.time && <span className="ml-auto font-mono">{m.time}</span>}
          </div>
          <h1 className="mt-1.5 text-xl font-semibold tracking-tight">{m.title}</h1>
          <div className="mt-3 flex items-center gap-3">
            <ProgressBar value={passed} total={m.tasks.length} className="flex-1" />
            <span className="font-mono text-[11px] text-dim">
              {passed}/{m.tasks.length} tasks
            </span>
          </div>
          {m.folder === "10_mock_interview" && <MockTimer />}
          <div className="-mb-px mt-3 flex gap-1">
            {tabs.map((t) => (
              <button
                key={t.id}
                type="button"
                onClick={() => setTab(t.id)}
                className={`border-b-2 px-3 py-2 text-sm transition-colors ${
                  tab === t.id ? "border-accent text-text" : "border-transparent text-muted hover:text-text"
                }`}
              >
                {t.label}
                {t.badge && <span className="ml-1.5 font-mono text-[11px] text-dim">{t.badge}</span>}
              </button>
            ))}
          </div>
        </div>

        <div key={tab} className="min-h-0 flex-1 overflow-y-auto px-5 py-5">
          {allPassed && tab === "tasks" && m.followUps.length > 0 && (
            <div className="mb-5 rounded-xl border border-pass/30 bg-pass-soft p-4 text-sm">
              <div className="font-medium text-pass">Every task passes.</div>
              <p className="mt-1 text-muted">
                Now the part that matters most: answer the interviewer follow-ups out loud.{" "}
                <button type="button" onClick={() => setTab("followups")} className="text-accent hover:underline">
                  Open follow-ups →
                </button>
              </p>
            </div>
          )}
          {tab === "learn" && (
            <>
              <div className="mb-6 rounded-xl border border-line bg-raised px-4 py-3 text-[13px] text-muted">
                In the browser, <span className="font-mono text-text">Run</span> is <span className="font-mono">python exercise.py</span> and{" "}
                <span className="font-mono text-text">Check</span> is <span className="font-mono">python check.py</span>. Your code is saved in this
                browser as you type.
              </div>
              <SectionsView sections={m.notes} />
            </>
          )}
          {tab === "tasks" && (
            <TaskList
              module={m}
              results={results}
              busy={busy || code == null}
              onCheck={(ids) => check(ids)}
              onJump={(t) => editor.current?.revealLine(lineOf(t))}
              onJumpLine={(l) => editor.current?.revealLine(l)}
            />
          )}
          {tab === "followups" && <FollowUps folder={m.folder} sections={m.followUps} />}
        </div>
      </aside>

      {/* ---------------- right: editor + console */}
      <main className="flex min-h-0 min-w-0 flex-1 flex-col">
        <div className="flex h-11 shrink-0 items-center gap-2 border-b border-line bg-raised px-3">
          <span className="rounded-md border border-line bg-panel px-2.5 py-1 font-mono text-[12px] text-text">exercise.py</span>
          <div className="ml-1 min-w-0 flex-1">
            <PythonPill />
          </div>
          <button type="button" onClick={reset} className="hidden rounded-md px-2 py-1 text-xs text-dim hover:text-muted sm:block">
            Reset
          </button>
          {hasBackup && (
            <button type="button" onClick={restore} className="hidden rounded-md px-2 py-1 text-xs text-dim hover:text-muted sm:block">
              Restore backup
            </button>
          )}
          {busy && (
            <button
              type="button"
              onClick={() => getPython().stop()}
              className="rounded-md border border-fail/40 px-2.5 py-1 text-xs text-fail hover:bg-fail-soft"
              title="Stop a runaway program (restarts Python)"
            >
              Stop
            </button>
          )}
          <button
            type="button"
            onClick={() => run("exercise.py")}
            disabled={busy || code == null}
            className="flex items-center gap-1.5 rounded-md border border-line-strong px-3 py-1.5 text-[13px] text-text hover:border-dim disabled:opacity-50"
            title="Run exercise.py (⌘/Ctrl + Enter)"
          >
            {busy && consoleTab === "output" ? <Spinner /> : <span className="text-[10px]">▶</span>} Run
          </button>
          <button
            type="button"
            onClick={() => check()}
            disabled={busy || code == null}
            className="flex items-center gap-1.5 rounded-md bg-accent px-3 py-1.5 text-[13px] font-semibold text-accent-ink hover:brightness-110 disabled:opacity-50"
            title="Check all tasks (⇧ + ⌘/Ctrl + Enter)"
          >
            {busy && consoleTab === "checks" ? <Spinner /> : "✓"} Check all
          </button>
        </div>

        <div className="h-[60vh] min-h-0 overflow-hidden lg:h-auto lg:flex-[3]">
          {code == null ? (
            <div className="h-full animate-pulse bg-raised" />
          ) : (
            <CodeEditor ref={editor} value={code} onChange={onChange} onRun={() => run("exercise.py")} onCheck={() => check()} />
          )}
        </div>
        <div className="h-[45vh] min-h-0 border-t border-line lg:h-auto lg:flex-[2]">
          <ConsolePanel
            tab={consoleTab}
            setTab={setConsoleTab}
            output={output}
            images={images}
            checks={checks}
            fatal={fatal}
            busy={busy}
            onClear={() => {
              setOutput([]);
              setImages([]);
              setChecks(null);
              setFatal(null);
            }}
            onRunSolution={() => run("solution.py")}
            onJumpLine={(l) => editor.current?.revealLine(l)}
          />
        </div>
      </main>
    </div>
  );
}
