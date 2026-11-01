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

## CV coach (`/cv`, `app/api/cv/route.ts`)
The PDF is read in the browser with pdf.js, and contact details are removed before anything is sent. The text goes once to an
OpenAI-compatible chat API. Nothing is stored server-side. If the AI isn't configured, is over quota or is down, the page
falls back to matching the CV against the question bank in `00_interview_guide/cv_and_behavioral.md`.

| Variable | Required | Default |
|---|---|---|
| `GROQ_API_KEY` (or `LLM_API_KEY`) | yes, for AI mode | — |
| `LLM_MODEL` | no | `openai/gpt-oss-120b` |
| `LLM_BASE_URL` | no (set it to switch provider, e.g. `https://api.x.ai/v1`) | `https://api.groq.com/openai/v1` |

For local testing, put the variables in `site/.env.local`. That file is gitignored.
