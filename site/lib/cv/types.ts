// Shapes shared by the CV coach page and /api/cv.

export const TARGETS = {
  citadel: "Citadel (hedge fund), quantitative research",
  securities: "Citadel Securities (market maker), quantitative research and trading",
} as const;
export type Target = keyof typeof TARGETS;

export type CvQuestion = { q: string; lookingFor: string[]; followUp: string };
export type CvItem = { cvLine: string; kind: string; risk: "high" | "medium" | "low"; why: string; questions: CvQuestion[] };
export type CvPlan = {
  summary: string;
  items: CvItem[];
  behavioural: { q: string; storyHint: string }[];
  whyTarget: string;
  askThem: string[];
  focus: { module: string; reason: string }[];
};

/** "ai" = generated from this CV by the model; "offline" = keyword match against the guide's question bank. */
export type SavedPlan = { plan: CvPlan; mode: "ai" | "offline"; target: Target; createdAt: string };

export type Feedback = { score: number; verdict: "strong" | "solid" | "weak"; good: string[]; missing: string[]; followUp: string; tip: string };

export type PlanRequest = { mode: "plan"; target: Target; cvText: string };
export type FeedbackRequest = { mode: "feedback"; target: Target; question: string; lookingFor: string[]; cvLine: string; answer: string };
