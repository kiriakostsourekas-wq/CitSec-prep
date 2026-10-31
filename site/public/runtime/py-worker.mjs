// Python (Pyodide) in a Web Worker, so long-running code never freezes the page.
// Messages in:  {id, type: "init"} | {id, type: "mount", files: [path]} | {id, type: "write", path, content}
//               {id, type: "script", folder, filename} | {id, type: "checks", folder, which, wanted}
// Messages out: {type: "status", status, detail} | {type: "stdout", id, text} | {id, ok, result | error}
const PYODIDE = "https://cdn.jsdelivr.net/pyodide/v314.0.7/full/";
const PACKAGES = ["numpy", "pandas", "scikit-learn"];

let pyodide = null;
let runner = null;
let currentId = null;
const mounted = new Set();

const status = (status, detail = "") => postMessage({ type: "status", status, detail });

async function init() {
  if (runner) return;
  status("loading", "Starting Python…");
  const { loadPyodide } = await import(/* webpackIgnore: true */ PYODIDE + "pyodide.mjs");
  pyodide = await loadPyodide({ indexURL: PYODIDE });
  status("loading", "Loading numpy, pandas, scikit-learn…");
  await pyodide.loadPackage(PACKAGES, { messageCallback: () => {} });
  status("loading", "Warming up…");
  await pyodide.runPythonAsync("import numpy, pandas, sklearn.linear_model");  // first import is the slow part
  const stream = (text) => postMessage({ type: "stdout", id: currentId, text });
  pyodide.setStdout({ batched: stream });
  pyodide.setStderr({ batched: stream });
  pyodide.FS.writeFile("/runner.py", await (await fetch("/runtime/runner.py")).text());
  pyodide.runPython("import sys; sys.path.insert(0, '/')");
  runner = pyodide.pyimport("runner");
  status("ready");
}

function writeFile(path, content) {
  const full = "/prep/" + path;
  pyodide.FS.mkdirTree(full.slice(0, full.lastIndexOf("/")));
  pyodide.FS.writeFile(full, content);
}

async function mount(files) {
  await Promise.all(files.filter((f) => !mounted.has(f)).map(async (f) => {
    const res = await fetch("/kit/" + f);
    if (!res.ok) throw new Error(`could not fetch ${f}`);
    writeFile(f, new Uint8Array(await res.arrayBuffer()));
    mounted.add(f);
  }));
}

async function loadImports(folder, filename) {
  // matplotlib etc. are only downloaded if the code actually imports them
  const code = pyodide.FS.readFile(`/prep/${folder}/${filename}`, { encoding: "utf8" });
  await pyodide.loadPackagesFromImports(code, { messageCallback: () => {} });
}

const handlers = {
  init: () => init(),
  mount: async ({ files }) => { await init(); await mount(files); },
  write: async ({ path, content }) => { await init(); writeFile(path, content); },
  script: async ({ folder, filename }) => {
    await loadImports(folder, filename);
    return JSON.parse(runner.run_script(folder, filename));
  },
  checks: async ({ folder, which, wanted }) => {
    await loadImports(folder, `${which}.py`);
    return JSON.parse(runner.run_checks(folder, which, pyodide.toPy(wanted ?? [])));
  },
};

// one job at a time, in arrival order
let queue = Promise.resolve();
onmessage = ({ data }) => {
  queue = queue.then(async () => {
    currentId = data.id;
    try {
      const result = await handlers[data.type](data);
      postMessage({ id: data.id, ok: true, result });
    } catch (err) {
      if (!runner) status("error", String(err?.message ?? err));
      postMessage({ id: data.id, ok: false, error: String(err?.message ?? err) });
    }
  });
};
