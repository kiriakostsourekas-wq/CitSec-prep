// Offline CV coach: when the AI is unavailable, match the CV against the guide's own question bank
// (00_interview_guide/cv_and_behavioral.md). Runs in the browser; nothing leaves the page.
import type { CvItem, CvPlan } from "./types";

export type OfflineSection = { kind: string; questions: string[] };
export type OfflineBank = { sections: OfflineSection[]; behavioural: string[]; askThem: string[] };

/** Built on the server from the guide's markdown, then passed to the page. */
export function buildOfflineBank(sections: { heading: string; blocks: { kind: string; md: string }[] }[]): OfflineBank {
  const text = (h: string) =>
    sections
      .filter((s) => s.heading.startsWith(h))
      .flatMap((s) => s.blocks.map((b) => b.md))
      .join("\n");
  const quoted = (md: string) =>
    [...md.matchAll(/"([^"\n]{20,}?)"/g)]
      .map((m) => m[1].replace(/\*\*|\*/g, "").trim())
      .filter((q) => q.includes("?") || /^(Tell|Walk|Describe|Explain|Give)\b/.test(q));
  const kinds = ["quant project", "ml project", "work", "competition", "personal project"];
  return {
    sections: kinds.map((kind, i) => ({ kind, questions: [...new Set(quoted(text(`${i + 1}.`)))] })),
    behavioural: text("6.")
      .split("\n")
      .filter((l) => l.startsWith("| ") && !l.startsWith("| Question"))
      .map((l) => l.split("|")[1].trim()),
    askThem: quoted(text("7.")),
  };
}

const KEYWORDS: Record<string, RegExp> = {
  "quant project": /sharpe|backtest|alpha|trading strateg|signal|portfolio|returns|factor|momentum|mean.revers|hedg|quant/i,
  "ml project": /machine learning|deep learning|neural|\bml\b|\bai\b|llm|nlp|pytorch|tensorflow|transformer|model|classif|regression|research assistant|thesis|paper/i,
  work: /intern|analyst|engineer|assistant|developer|consultant|team lead|promoted|managed|worked at|experience/i,
  competition: /olympiad|kaggle|competition|hackathon|contest|challenge|medal|ranked|finalist|prize|winner|prosperity/i,
  "personal project": /founder|co-?founded|start-?up|society|club|president|personal project|side project|built a|app\b/i,
};

const FOCUS: [RegExp, string, string][] = [
  [/sharpe|backtest|returns|portfolio|trading/i, "numpy-pandas-basics", "Your CV quotes trading results: be fluent with returns, Sharpe and drawdown in pandas."],
  [/regression|statistic|econometric/i, "linear-regression", "Regression is on your CV and is the most-asked model at Citadel."],
  [/classif|machine learning|\bml\b|model/i, "logistic-regression", "ML on your CV means questions on evaluation metrics and calibration."],
  [/probab|stochastic|olympiad|math/i, "probability-simulation", "Strong maths on the CV invites harder probability questions."],
  [/c\+\+|python|java|software|developer|algorithm/i, "algorithms", "Listed programming skills mean a live coding round."],
];

/** Pick the CV lines that best match each kind of item, and attach that section's questions. */
export function offlinePlan(cvText: string, bank: OfflineBank): CvPlan {
  const lines = cvText
    .split(/\n|•|▪|●/)
    .map((l) => l.replace(/\s+/g, " ").trim())
    .filter((l) => l.length > 25 && l.length < 300);
  const used = new Set<string>();
  const items: CvItem[] = [];
  for (const section of bank.sections) {
    const re = KEYWORDS[section.kind];
    const line = lines.find((l) => re.test(l) && !used.has(l));
    if (!line || !section.questions.length) continue;
    used.add(line);
    items.push({
      cvLine: line,
      kind: section.kind,
      risk: section.kind === "quant project" || section.kind === "ml project" ? "high" : "medium",
      why: "Matched against the guide's question bank for this kind of CV item.",
      questions: section.questions.slice(0, 6).map((q) => ({ q, lookingFor: [], followUp: "" })),
    });
  }
  const focus = FOCUS.filter(([re]) => re.test(cvText))
    .slice(0, 3)
    .map(([, module, reason]) => ({ module, reason }));
  return {
    summary:
      "The AI coach wasn't available, so these questions come from the guide's question bank, matched to lines in your CV. Rewrite each question so it names your project, then answer it out loud.",
    items,
    behavioural: bank.behavioural.map((q) => ({ q, storyHint: "" })),
    whyTarget: "",
    askThem: bank.askThem,
    focus,
  };
}

/** Strip contact details before anything is sent anywhere. */
export function redact(text: string) {
  return text
    .replace(/[\w.+-]+@[\w-]+\.[\w.-]+/g, "[email]")
    .replace(/https?:\/\/\S+|www\.\S+|(?:linkedin|github)\.com\/\S+/gi, "[link]")
    .replace(/\+?\d[\d\s().-]{7,}\d/g, (m) => (m.replace(/\D/g, "").length >= 9 ? "[phone]" : m));
}

/** Text from a PDF, read entirely in the browser with pdf.js. */
export async function pdfToText(file: File): Promise<string> {
  const pdfjs = await import("pdfjs-dist");
  pdfjs.GlobalWorkerOptions.workerSrc = `https://cdn.jsdelivr.net/npm/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;
  const doc = await pdfjs.getDocument({ data: new Uint8Array(await file.arrayBuffer()) }).promise;
  const pages: string[] = [];
  for (let i = 1; i <= Math.min(doc.numPages, 6); i++) {
    const content = await (await doc.getPage(i)).getTextContent();
    pages.push(content.items.map((it) => ("str" in it ? it.str + (it.hasEOL ? "\n" : " ") : "")).join(""));
  }
  return pages.join("\n").replace(/[ \t]+\n/g, "\n").replace(/\n{3,}/g, "\n\n").trim();
}
