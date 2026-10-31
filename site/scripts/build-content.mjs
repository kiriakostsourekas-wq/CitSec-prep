// Turns the prep kit (the repo one level up) into data for the website.
// The repo stays the single source of truth: edit a README / hints.md / exercise and rebuild.
//
//   node scripts/build-content.mjs
//
// Writes content/generated/content.json and copies the files Python needs into public/kit/.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SITE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const REPO = path.resolve(SITE, "..");
const OUT_JSON = path.join(SITE, "content/generated/content.json");
const KIT = path.join(SITE, "public/kit");

const read = (rel) => fs.readFileSync(path.join(REPO, rel), "utf8");
const exists = (rel) => fs.existsSync(path.join(REPO, rel));

// Hand-written framing for each module; everything else is parsed from the repo.
const MODULE_META = {
  "01_python_warmup": { blurb: "Loops, dicts, sorting, a class and csv, all in plain Python with no libraries.", tags: ["python"] },
  "02_numpy_pandas_basics": { blurb: "Arrays, axis and broadcasting; DataFrames, groupby, pivot, rolling; Sharpe and drawdown.", tags: ["numpy", "pandas"] },
  "03_data_preprocessing": { blurb: "Messy customer data to a clean feature matrix, without leaking the test set.", tags: ["pandas", "ml"] },
  "04_linear_regression": { blurb: "OLS three ways, ridge, standard errors, and the famous duplicate-data question.", tags: ["ml", "stats"], star: true },
  "05_logistic_regression": { blurb: "Sigmoid, log-loss, gradient descent, precision/recall, ROC-AUC, odds ratios.", tags: ["ml", "stats"] },
  "06_knn_classification": { blurb: "kNN from scratch, feature scaling, k-fold CV by hand, bonus Naive Bayes.", tags: ["ml"] },
  "07_decision_tree": { blurb: "Gini and entropy, best split, a recursive tree, and overfitting versus depth.", tags: ["ml"] },
  "08_probability_simulation": { blurb: "Exact answers versus Monte Carlo, plus 12 interview probability questions.", tags: ["probability"] },
  "09_algorithms": { blurb: "Moving average, two-sum, DP, heaps, and a bonus limit order book.", tags: ["coding"] },
  "10_mock_interview": { blurb: "A timed 60-minute end-to-end ML case with the interviewer's script.", tags: ["mock"], star: true },
};

// The study plan from the root README (Citadel track).
const SESSIONS = [
  { n: 1, hours: 3, items: [["guide", "format, how to answer, profile"], ["01_python_warmup"], ["02_numpy_pandas_basics", "part A (numpy)"]] },
  { n: 2, hours: 3, items: [["02_numpy_pandas_basics", "parts B–D (pandas)"], ["03_data_preprocessing"]] },
  { n: 3, hours: 3, items: [["04_linear_regression", "+ its follow-ups"], ["guide/cv", "first pass of the CV deep dive"]] },
  { n: 4, hours: 3, items: [["05_logistic_regression"], ["06_knn_classification", "A–C"]] },
  { n: 5, hours: 3.5, items: [["07_decision_tree"], ["08_probability_simulation"]] },
  { n: 6, hours: 3, items: [["09_algorithms", "A–C"], ["10_mock_interview", "timed"], ["guide/ml-stats", "rapid-fire ML/stats"]] },
];
const FAST_TRACK = [
  ["guide", "Interview guide + CV file"], ["04_linear_regression"], ["05_logistic_regression"],
  ["07_decision_tree", "A–C"], ["09_algorithms", "A1–A3"], ["08_probability_simulation", "README questions"],
  ["04_linear_regression", "follow-ups in 04 / 05 / 07"],
];

const slugOf = (folder) => folder.replace(/^\d+_/, "").replace(/_/g, "-");

// ---------------------------------------------------------------- markdown helpers
/** Rewrite `04_linear_regression/...` style references into site links. */
function linkify(md) {
  return md
    .replace(/`((?:0[1-9]|10)_[a-z_]+)(\/[^`]*)?`/g, (m, folder) => (MODULE_META[folder] ? `[${m}](/modules/${slugOf(folder)})` : m))
    .replace(/`(?:00\/|00_interview_guide\/)?cv_and_behavioral\.md`/g, (m) => `[${m}](/guide/cv)`)
    .replace(/`(?:00\/|00_interview_guide\/)?ml_stats_questions\.md`/g, (m) => `[${m}](/guide/ml-stats)`)
    .replace(/`00_interview_guide\/README\.md`/g, (m) => `[${m}](/guide)`);
}

/** Split markdown into plain blocks and folded <details> blocks (the kit's "answer hidden" convention). */
function splitFolds(md) {
  const parts = [];
  const re = /<details>\s*<summary>([\s\S]*?)<\/summary>([\s\S]*?)<\/details>/g;
  let last = 0;
  for (const m of md.matchAll(re)) {
    const before = md.slice(last, m.index).trim();
    if (before) parts.push({ kind: "md", md: before });
    parts.push({ kind: "fold", summary: m[1].trim(), md: m[2].trim() });
    last = m.index + m[0].length;
  }
  const rest = md.slice(last).trim();
  if (rest) parts.push({ kind: "md", md: rest });
  return parts;
}

/** "## Heading" sections of a markdown file; text before the first one becomes the intro. */
function sections(md, level = 2) {
  const marker = "#".repeat(level) + " ";
  const lines = md.split("\n");
  const out = [];
  let cur = { heading: "", lines: [] };
  for (const line of lines) {
    if (line.startsWith(marker)) {
      out.push(cur);
      cur = { heading: line.slice(marker.length).trim(), lines: [] };
    } else cur.lines.push(line);
  }
  out.push(cur);
  return out
    .map((s) => ({ heading: s.heading, blocks: splitFolds(linkify(s.lines.join("\n"))) }))
    .filter((s) => s.heading || s.blocks.length);
}

const stripTitle = (md) => md.replace(/^# .*\n/, "");
// The local working copy may cross-link the separate Jane Street track; the site is Citadel only.
const citadelOnly = (md) => md.split("\n").filter((l) => !/jane street|jane_street/i.test(l)).join("\n");

// ---------------------------------------------------------------- python helpers
function pyFunctions(src) {
  const lines = src.split("\n");
  const fns = {};
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(/^(?:def|class) (\w+)\s*[(:]/);
    if (!m) continue;
    let start = i;
    while (start > 0 && lines[start - 1].startsWith("@")) start--;
    let end = i + 1;
    while (end < lines.length && (lines[end].trim() === "" || /^\s/.test(lines[end]))) end++;
    while (end > i + 1 && lines[end - 1].trim() === "") end--;
    const body = lines.slice(start, end).join("\n");
    const doc = body.match(/^\s+(?:"""|''')([\s\S]*?)(?:"""|''')/m);
    fns[m[1]] = { source: body, doc: doc ? dedent(doc[1]) : "" };
  }
  return fns;
}

function dedent(text) {
  const lines = text.replace(/^\n+|\s+$/g, "").split("\n");
  const indents = lines.slice(1).filter((l) => l.trim()).map((l) => l.match(/^ */)[0].length);
  const cut = indents.length ? Math.min(...indents) : 0;
  return [lines[0].trim(), ...lines.slice(1).map((l) => l.slice(cut))].join("\n");
}

function parseTasks(checkSrc) {
  const re = /@checks\.task\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"((?:[^"\\]|\\.)*)"\s*\)/g;
  return [...checkSrc.matchAll(re)].map((m) => ({ id: m[1], func: m[2], title: m[3].replace(/\\"/g, '"') }));
}

function parseParts(exerciseSrc) {
  const parts = {};
  for (const m of exerciseSrc.matchAll(/^# PART ([A-Z])\s*[-:·]\s*(.+)$/gm)) parts[m[1]] = sentenceCase(m[2]);
  // 10_mock_interview: "# ------ Stage 1 (10 min): explore + clean ------"
  for (const m of exerciseSrc.matchAll(/^# -+ Stage (\d+) \(([^)]*)\): (.+?) -+$/gm)) parts[`S${m[1]}`] = `${sentenceCase(m[3])} · ${m[2]}`;
  return parts;
}

const KEEP_CAPS = new Set(["OLS", "CV", "ML", "SE", "AUC", "ROC"]);
const CAPS_FIX = { KNN: "kNN", GAUSSIAN: "Gaussian", NAIVE: "Naive", BAYES: "Bayes" };
function sentenceCase(text) {
  const t = text.trim().replace(/\s+/g, " ")
    .replace(/\b[A-Z][A-Z]+\b/g, (w) => CAPS_FIX[w] ?? (KEEP_CAPS.has(w) ? w : w.toLowerCase()));
  return t.charAt(0).toUpperCase() + t.slice(1);
}

function parseHints(hintsMd, tasks) {
  const hints = {};
  for (const sec of hintsMd.split(/^### /m).slice(1)) {
    const [heading, ...rest] = sec.split("\n");
    const ids = new Set(heading.match(/\b[A-Z]\d\b/g) ?? []);
    for (const t of tasks) if (heading.includes("`" + t.func + "`")) ids.add(t.id);
    const folds = splitFolds(rest.join("\n")).filter((b) => b.kind === "fold").map((b) => linkify(b.md));
    const note = splitFolds(rest.join("\n")).filter((b) => b.kind === "md").map((b) => b.md).join("\n\n");
    for (const id of ids) {
      hints[id] ??= { hints: [], note: "" };
      hints[id].hints.push(...folds);
      if (note) hints[id].note = note;
    }
  }
  return hints;
}

/** Data files a module reads, including ones that live in another folder (01 reuses 02's CSV). */
function dataFiles(folder, sources) {
  const files = new Set();
  if (exists(`${folder}/data`)) for (const f of fs.readdirSync(path.join(REPO, folder, "data"))) files.add(`${folder}/data/${f}`);
  for (const src of sources)
    for (const m of src.matchAll(/"((?:0[1-9]|10)_[a-z_]+)"\s*\/\s*"data"\s*\/\s*"([\w.-]+)"/g)) files.add(`${m[1]}/data/${m[2]}`);
  return [...files].sort();
}

function copyToKit(rel) {
  const dst = path.join(KIT, rel);
  fs.mkdirSync(path.dirname(dst), { recursive: true });
  fs.copyFileSync(path.join(REPO, rel), dst);
}

// ---------------------------------------------------------------- build
function buildModule(folder) {
  const readme = read(`${folder}/README.md`);
  const titleLine = readme.match(/^# (\d+)\s*·\s*(.+?)(?:\s*\((?:≈\s*)?([^)]*)\))?\s*$/m);
  const template = exists(`tools/templates/${folder}_exercise.py`) ? read(`tools/templates/${folder}_exercise.py`) : read(`${folder}/exercise.py`);
  const check = read(`${folder}/check.py`);
  const solution = read(`${folder}/solution.py`);
  const tasks = parseTasks(check);
  const exFns = pyFunctions(template);
  const solFns = pyFunctions(solution);
  const hints = parseHints(read(`${folder}/hints.md`), tasks);
  const parts = parseParts(template);
  const data = dataFiles(folder, [template, check, solution]);

  for (const rel of [`${folder}/check.py`, `${folder}/solution.py`, ...data]) copyToKit(rel);

  const secs = sections(stripTitle(readme));
  const isFollowUps = (h) => /follow-up|questions to practise|wrap-up/i.test(h);
  return {
    folder,
    slug: slugOf(folder),
    number: folder.slice(0, 2),
    title: titleLine ? titleLine[2].trim() : folder,
    time: titleLine?.[3]?.replace(/^≈\s*/, "") ?? "",
    ...MODULE_META[folder],
    notes: secs.filter((s) => !isFollowUps(s.heading)),
    followUps: secs.filter((s) => isFollowUps(s.heading)),
    parts,
    tasks: tasks.map((t) => ({
      ...t,
      part: /^[A-D]\d/.test(t.id) ? t.id[0] : t.id,
      doc: exFns[t.func]?.doc ?? "",
      solution: solFns[t.func]?.source ?? "",
      hints: hints[t.id]?.hints ?? [],
      hintNote: hints[t.id]?.note ?? "",
    })),
    starter: template,
    files: [`tools/checker.py`, `${folder}/check.py`, ...data],
    solutionFile: `${folder}/solution.py`,
  };
}

function buildDoc(rel, { title, slug } = {}) {
  const md = citadelOnly(read(rel));
  return { slug, title: title ?? md.match(/^# (.+)$/m)?.[1] ?? rel, sections: sections(stripTitle(md)) };
}

fs.rmSync(KIT, { recursive: true, force: true });
copyToKit("tools/checker.py");

const folders = fs.readdirSync(REPO).filter((d) => MODULE_META[d]).sort();
const modules = folders.map(buildModule);
const content = {
  modules,
  guide: {
    main: buildDoc("00_interview_guide/README.md", { slug: "", title: "What to expect in the final round" }),
    cv: buildDoc("00_interview_guide/cv_and_behavioral.md", { slug: "cv" }),
    mlStats: buildDoc("00_interview_guide/ml_stats_questions.md", { slug: "ml-stats" }),
  },
  cheatsheets: fs.readdirSync(path.join(REPO, "cheatsheets")).filter((f) => f.endsWith(".md")).sort()
    .map((f) => buildDoc(`cheatsheets/${f}`, { slug: f.replace(/(_cheatsheet)?\.md$/, "").replace(/_/g, "-") })),
  plan: {
    sessions: SESSIONS,
    fastTrack: FAST_TRACK,
  },
};

fs.mkdirSync(path.dirname(OUT_JSON), { recursive: true });
fs.writeFileSync(OUT_JSON, JSON.stringify(content));
const nTasks = modules.reduce((n, m) => n + m.tasks.length, 0);
const missingHints = modules.flatMap((m) => m.tasks.filter((t) => !t.hints.length).map((t) => `${m.number}:${t.id}`));
const missingSol = modules.flatMap((m) => m.tasks.filter((t) => !t.solution).map((t) => `${m.number}:${t.id}`));
console.log(`content: ${modules.length} modules, ${nTasks} tasks, ${content.cheatsheets.length} cheatsheets`);
if (missingHints.length) console.log(`  tasks without hints: ${missingHints.join(" ")}`);
if (missingSol.length) console.log(`  tasks without a solution function: ${missingSol.join(" ")}`);
