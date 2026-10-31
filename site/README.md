# Superday Prep: the website

The Citadel track of this repo as an interactive website. It's built with Next.js, and Python runs in the browser via [Pyodide](https://pyodide.org).

The site has **no content of its own**. `scripts/build-content.mjs` reads the repo one level up (the module READMEs,
`hints.md`, `tools/templates/*_exercise.py`, `check.py`, `solution.py`, the datasets, the interview guide and the cheatsheets). It
writes `content/generated/content.json` and copies the files Python needs into `public/kit/`. Edit the kit and rebuild.

## How the coding works
- `public/runtime/py-worker.mjs` loads Pyodide with numpy, pandas and scikit-learn in a Web Worker.
- `public/runtime/runner.py` runs `exercise.py` as `__main__` (**Run**) or the folder's unchanged `check.py` (**Check**), and
  returns one PASS / FAIL / TODO / ERROR result per task.
- Code and progress are stored in `localStorage` only.

## Develop
```bash
npm install
npm run dev        # regenerates content first, then http://localhost:3000
```

## Deploy on Vercel
- Import the GitHub repo and set **Root Directory** to `site`.
- Keep "Include files outside the root directory in the Build Step" enabled. The content step reads `../`.
