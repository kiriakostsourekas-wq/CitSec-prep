// POST /api/cv  {mode: "plan", ...} -> personalised question plan, {mode: "feedback", ...} -> feedback on one answer.
// Nothing is stored: the CV text is forwarded to the model once and dropped.
import { generatePlan, LlmError, reviewAnswer } from "@/lib/cv/llm";
import { TARGETS, type FeedbackRequest, type PlanRequest } from "@/lib/cv/types";

export const maxDuration = 60;

// Best-effort per-IP limit (per server instance). The provider's free-tier quota is the hard cap on cost: zero.
const WINDOW_MS = 60 * 60 * 1000;
const LIMITS = { plan: 6, feedback: 60 };
const hits = new Map<string, number[]>();

function allow(ip: string, mode: keyof typeof LIMITS) {
  const key = `${mode}:${ip}`;
  const now = Date.now();
  const recent = (hits.get(key) ?? []).filter((t) => now - t < WINDOW_MS);
  if (recent.length >= LIMITS[mode]) return false;
  recent.push(now);
  hits.set(key, recent);
  if (hits.size > 5000) hits.clear();
  return true;
}

const error = (status: number, message: string) => Response.json({ error: message }, { status });

export async function POST(request: Request) {
  let body: PlanRequest | FeedbackRequest;
  try {
    body = await request.json();
  } catch {
    return error(400, "Invalid request.");
  }
  if (!body || !(body.target in TARGETS)) return error(400, "Pick a target firm.");
  if (body.mode !== "plan" && body.mode !== "feedback") return error(400, "Unknown mode.");

  const ip = request.headers.get("x-forwarded-for")?.split(",")[0]?.trim() || "local";
  if (!allow(ip, body.mode)) return error(429, "You've reached this hour's limit. Try again later.");

  try {
    if (body.mode === "plan") {
      const cv = String(body.cvText ?? "").trim();
      if (cv.length < 200) return error(400, "That CV text looks too short. Paste the full CV.");
      if (cv.length > 15000) return error(400, "That's longer than a CV (over 15,000 characters). Paste just the CV.");
      return Response.json({ plan: await generatePlan(body.target, cv) });
    }
    const answer = String(body.answer ?? "").trim();
    if (answer.length < 20) return error(400, "Write a bit more: answer as you would out loud.");
    if (answer.length > 4000) return error(400, "Keep the answer under 4,000 characters (about 2 minutes spoken).");
    const lookingFor = Array.isArray(body.lookingFor) ? body.lookingFor.map(String).slice(0, 6) : [];
    const feedback = await reviewAnswer(body.target, String(body.question ?? "").slice(0, 500), lookingFor, String(body.cvLine ?? "").slice(0, 300), answer);
    return Response.json({ feedback });
  } catch (e) {
    if (e instanceof LlmError) return error(e.status, e.message);
    console.error("cv route failed", e);
    return error(500, "Something went wrong talking to the AI.");
  }
}
