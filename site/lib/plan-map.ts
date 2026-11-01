// Layout of the study plan as a metro map: one line per interview round, sessions as columns,
// every line ending at the superday. Coordinates are in the SVG's viewBox units.

export type LaneId = "interview" | "coding" | "ml" | "prob";

export const LANES: Record<LaneId, { label: string; color: string; y: number }> = {
  interview: { label: "Interview", color: "#f472b6", y: 78 },
  coding: { label: "Coding", color: "#60a5fa", y: 158 },
  ml: { label: "ML & stats", color: "#a78bfa", y: 238 },
  prob: { label: "Probability", color: "#ffb020", y: 318 },
};

export const MAP = { width: 1000, height: 380, left: -70, colStart: 40, colWidth: 117, sessions: 7 };
export const TERMINAL = { x: 940, y: 198 };

/** One stop per plan item. `session` 0 means "every day". `label` is the short name drawn on the map. */
export const STOPS: { key: string; lane: LaneId; x: number; session: number; label: string; below?: boolean }[] = [
  { key: "mental-math", lane: "prob", x: 62, session: 0, label: "Mental math", below: true },
  { key: "01_python_warmup", lane: "coding", x: 75, session: 1, label: "Python", below: true },
  { key: "guide", lane: "interview", x: 98, session: 1, label: "Interview guide" },
  { key: "02_numpy_pandas_basics", lane: "coding", x: 157, session: 1, label: "numpy & pandas", below: true },
  { key: "03_data_preprocessing", lane: "ml", x: 225, session: 2, label: "Data cleaning", below: true },
  { key: "04_linear_regression", lane: "ml", x: 305, session: 3, label: "Linear regression" },
  { key: "guide/cv", lane: "interview", x: 350, session: 3, label: "CV deep dive" },
  { key: "05_logistic_regression", lane: "ml", x: 420, session: 4, label: "Logistic", below: true },
  { key: "06_knn_classification", lane: "ml", x: 485, session: 4, label: "kNN" },
  { key: "07_decision_tree", lane: "ml", x: 550, session: 5, label: "Trees", below: true },
  { key: "08_probability_simulation", lane: "prob", x: 588, session: 5, label: "Simulation", below: true },
  { key: "12_probability_ev", lane: "prob", x: 683, session: 6, label: "Probability & EV", below: true },
  { key: "09_algorithms", lane: "coding", x: 768, session: 7, label: "Algorithms", below: true },
  { key: "guide/ml-stats", lane: "interview", x: 800, session: 7, label: "Rapid-fire" },
  { key: "10_mock_interview", lane: "ml", x: 832, session: 7, label: "Mock", below: true },
];
