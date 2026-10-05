# CV deep dive & behavioural questions

At final rounds **every line of your CV is fair game**, and the most impressive lines get the hardest questions.
Below are the questions to expect for each *type* of CV item a strong undergraduate (1st–3rd year) usually has, plus what a
strong answer must contain. Skip the sections that don't apply to you. **Write your own answers in the "Your notes" boxes**
(edit this file) and say them out loud at least twice. Keep each story to about 2 minutes.

Structure for stories, **STAR**: *Situation* (1 sentence), *Task* (your responsibility), *Action* (what **you** did, in detail, using "I" not "we"), *Result* (numbers, what you learned).

General rules:
- If it's on your CV, you must be able to explain it **two levels deeper** than what's written.
- Know your own numbers exactly (accuracy, Sharpe, dataset size, team size, ranking) and how they were computed.
- Point out the limitations of your own work before the interviewer does. Self-criticism is a strong signal in research roles.
- Never claim more ownership than you had. "We built…, and my part was…" is fine.

---

## 1. A quant / trading research project (backtest, signal, strategy with a Sharpe ratio)
If your CV shows a strategy result (e.g. "Sharpe of X on N stocks"), a quant interviewer will spend most of the time here.
They want to know whether you understand the **pitfalls of backtesting**, not just the headline number.

Expect:
1. "Walk me through the project in 2 minutes. What was **your** contribution specifically?"
2. "How exactly is the Sharpe computed?" Daily or monthly returns? Annualized how (√252)? Over which period? In-sample or **out-of-sample**? Gross or **net of transaction costs**?
3. "What's the benchmark?" Buy-and-hold over the same period? Is the strategy long-short (market-neutral) or long-only? What's its **beta**?
   Does the alpha survive after controlling for known factors (market, size, value, momentum)?
4. "Your universe is *today's* index members (e.g. S&P 500)?" Then it has **survivorship bias**: companies that were removed (often after doing badly) are missing.
   Point-in-time constituents fix it.
5. "Any **look-ahead**?" Signals must only use data available at the time: `shift(1)`, fundamentals by their *release* date, no future-based normalization.
   **If you used an LLM or any pre-trained model:** could it have seen the test period in its training data (knowledge leakage)? How did you rule it out?
6. "How many signals / parameter settings did you try before reporting this one?" → **multiple testing / data snooping**. Was there a held-out period you touched only once?
7. "If there are regimes or clusters: how are they defined, and is the label computed without future information?"
8. "What's the turnover? Capacity? What happens to the Sharpe at 10 bps of cost per trade?"
9. "What would you do with 3 more months?"
10. "What's the weakest part of this work?" (Have an honest answer ready.)

**Useful formula to have ready:** with i.i.d. returns, the standard error of an annualized Sharpe estimated from Y years of **daily** data is
≈ √((1 + SR²/(2·252))/Y) ≈ 1/√Y (Lo, 2002). Example: SR = 2 over 3 years gives SE ≈ 0.58, so the 95% CI is roughly [0.9, 3.1].
That interval is wide, and it ignores multiple testing, which makes things worse. Being able to say this about your own number is impressive.

> **Your notes:**
> - My contribution:
> - Sharpe computation (frequency, period, in/out-of-sample, costs):
> - Universe (survivorship?), look-ahead checks:
> - Number of trials / how I avoided overfitting:
> - Weakest point & next step:

## 2. An ML / AI project, research assistantship, or lab work
Expect: "What was the problem and why did it matter?", "What was the baseline and how much did you beat it by?",
"How did you split the data? Any leakage?", "Why that model and not a simpler one?", "What did you try that didn't work?",
"How did you evaluate?" (metrics, held-out sets, for LLM work: benchmarks, contamination checks, pass@k).
If you worked on LLMs (fine-tuning, RL, data labelling or evaluation): be ready to explain in plain words what training stage you
touched (pre-training / SFT / RLHF or RL with verifiable rewards / evaluation) and what you would measure to know it worked.

> **Your notes:**

## 3. Work experience / internship / part-time job (especially with responsibility)
Expect behavioural questions:
- "What was the hardest part of the job? What did you own end-to-end?"
- "If you were promoted or led people: how? How did you keep quality high across the team?" (rubrics, spot-checks, calibration, metrics)
- "Tell me about a conflict with a colleague / a time you had to give hard feedback."
- "Tell me about a mistake you made at work and how you handled it."
- Link it to the role: reviewing others' work carefully, catching subtle errors, and communicating clearly are daily tasks in research and trading.

> **Your notes (one STAR story on ownership/leadership, one on conflict or failure):**

## 4. Competitions: math/physics olympiads, programming contests, Kaggle, trading competitions
- "How do you approach a problem you've never seen?" (special cases, invariants, work backwards, simplify, know when to switch approaches)
- "Tell me about a time you were stuck for a long time. What did you do?"
- "Tell me about a result that disappointed you. How did you react?" (resilience; be gracious, not defensive)
- **Trading competitions** (e.g. university trading challenges): "What were the cases? What was your strategy in the market-making / algorithmic case?
  How did you manage risk? What went wrong during the competition, and how did you adapt?" Trading interviewers *love* this. Have one concrete episode:
  a position, a decision under uncertainty, and the result.
- **Kaggle-type contests:** "What was your validation strategy? Did the public leaderboard mislead you?" (overfitting to the leaderboard is a classic.)

> **Your notes:**

## 5. Personal projects, start-ups, clubs
- "Why did you start it? Where is it now? What did you learn?" If it's paused or stopped, say so plainly and focus on the lessons
  (talking to users, building with a team, prioritization, what you'd do differently).
- For code projects: "What was the hardest bug? What would you refactor?" Be ready to share your screen and walk through the code.

> **Your notes:**

---

## 6. Standard behavioural questions (prepare 1 story each; the same story can serve several questions)
| Question | Which story will you use? |
|---|---|
| Why Citadel / Citadel Securities? (be specific: research culture, the people, the speed of feedback from markets, what you read about the firm) | |
| Why quant / trading rather than software engineering, pure AI research, or academia? | |
| Tell me about yourself (90 seconds: background → what you study → 1–2 highlights → why this role) | |
| Your biggest failure | |
| A time you worked in a team that wasn't working well | |
| A time you changed your mind because of data | |
| Something you taught yourself recently | |
| Where do you see yourself in 5 years? | |

## 7. Questions to ask your interviewers (have 2–3 per interview)
- "What does a typical week look like for an intern/new joiner on your team?"
- "How do researchers decide when an idea is dead vs worth more time?"
- "How is the balance between modelling and data engineering in your day-to-day?"
- "What distinguishes the interns who get return offers?"
- "What's something you changed your mind about since joining?"
