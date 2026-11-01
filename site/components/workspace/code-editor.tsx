"use client";
import { python } from "@codemirror/lang-python";
import { EditorSelection } from "@codemirror/state";
import { EditorView, keymap } from "@codemirror/view";
import { tags as t } from "@lezer/highlight";
import { createTheme } from "@uiw/codemirror-themes";
import CodeMirror from "@uiw/react-codemirror";
import { forwardRef, useImperativeHandle, useMemo, useRef } from "react";

const deskTheme = createTheme({
  theme: "dark",
  settings: {
    background: "#0b0f14",
    foreground: "#e6edf3",
    caret: "#ffb020",
    selection: "rgba(255,176,32,0.18)",
    selectionMatch: "rgba(255,176,32,0.10)",
    lineHighlight: "rgba(255,255,255,0.025)",
    gutterBackground: "#0b0f14",
    gutterForeground: "#3c4756",
    gutterActiveForeground: "#95a3b5",
    gutterBorder: "transparent",
    fontFamily: "var(--font-plex-mono), ui-monospace, monospace",
  },
  styles: [
    { tag: [t.comment, t.lineComment, t.blockComment], color: "#5f6d7e", fontStyle: "italic" },
    { tag: [t.string, t.special(t.string)], color: "#9ece6a" },
    { tag: [t.docString], color: "#7f8fa3" },
    { tag: [t.number, t.bool, t.null], color: "#e0af68" },
    { tag: [t.keyword, t.controlKeyword, t.definitionKeyword, t.moduleKeyword, t.operatorKeyword], color: "#ff9e64" },
    { tag: [t.function(t.variableName), t.function(t.definition(t.variableName))], color: "#7aa2f7" },
    { tag: [t.definition(t.variableName)], color: "#c0caf5" },
    { tag: [t.className, t.definition(t.className)], color: "#2ac3de" },
    { tag: [t.propertyName], color: "#b4f9f8" },
    { tag: [t.self], color: "#f7768e" },
    { tag: [t.operator], color: "#89ddff" },
  ],
});

export type CodeEditorHandle = { revealLine: (line: number) => void; focus: () => void };

type Props = {
  value: string;
  onChange: (v: string) => void;
  onRun?: () => void;
  onCheck?: () => void;
  readOnly?: boolean;
  height?: string;
};

export const CodeEditor = forwardRef<CodeEditorHandle, Props>(function CodeEditor(
  { value, onChange, onRun, onCheck, readOnly, height = "100%" },
  ref,
) {
  const view = useRef<EditorView | null>(null);
  const handlers = useRef({ onRun, onCheck });
  handlers.current = { onRun, onCheck };

  useImperativeHandle(ref, () => ({
    revealLine(line) {
      const v = view.current;
      if (!v) return;
      const l = v.state.doc.line(Math.min(Math.max(1, line), v.state.doc.lines));
      v.dispatch({
        selection: EditorSelection.cursor(l.from),
        effects: EditorView.scrollIntoView(l.from, { y: "start", yMargin: 40 }),
      });
      v.focus();
    },
    focus: () => view.current?.focus(),
  }));

  const extensions = useMemo(
    () => [
      python(),
      keymap.of([
        { key: "Mod-Enter", run: () => (handlers.current.onRun?.(), true) },
        { key: "Shift-Mod-Enter", run: () => (handlers.current.onCheck?.(), true) },
      ]),
      EditorView.theme({
        "&": { fontSize: "13.5px" },
        ".cm-content": { padding: "12px 0" },
        ".cm-gutters": { paddingLeft: "6px" },
        "&.cm-focused": { outline: "none" },
      }),
    ],
    [],
  );

  return (
    <CodeMirror
      value={value}
      onChange={onChange}
      height={height}
      className="h-full"
      theme={deskTheme}
      readOnly={readOnly}
      editable={!readOnly}
      extensions={extensions}
      basicSetup={{ foldGutter: false, highlightActiveLineGutter: true, tabSize: 4 }}
      onCreateEditor={(v) => (view.current = v)}
    />
  );
});
