// Question generators ported from 11_mental_math/drill.py (same topics, ranges and tolerance).

export type Question = { text: string; answer: number; topic: Topic };
type Gen = () => [string, number];

const randint = (a: number, b: number) => a + Math.floor(Math.random() * (b - a + 1));
const choice = <T,>(xs: T[]) => xs[Math.floor(Math.random() * xs.length)];
const round = (x: number, d: number) => Math.round(x * 10 ** d) / 10 ** d;
const uniform = (a: number, b: number) => a + Math.random() * (b - a);

const GENERATORS = {
  mul: (() => {
    const k = Math.random();
    const [a, b] = k < 0.4 ? [randint(12, 99), randint(3, 9)] : k < 0.8 ? [randint(11, 49), randint(11, 29)] : [randint(101, 999), randint(2, 9)];
    return [`${a} × ${b}`, a * b];
  }) as Gen,
  div: (() => {
    if (Math.random() < 0.6) {
      const b = randint(3, 19), c = randint(3, 60);
      return [`${b * c} ÷ ${b}`, c];
    }
    const b = choice([4, 8, 5, 20, 25, 40]);
    const a = randint(1, 4 * b);
    return [`${a} ÷ ${b}`, a / b];
  }) as Gen,
  add: (() => {
    let a = round(uniform(10, 99), 1), b = round(uniform(10, 99), 1);
    if (Math.random() < 0.5) return [`${a} + ${b}`, round(a + b, 1)];
    [a, b] = [Math.max(a, b), Math.min(a, b)];
    return [`${a} − ${b}`, round(a - b, 1)];
  }) as Gen,
  pct: (() => {
    const p = choice([5, 10, 12.5, 15, 20, 25, 30, 40, 60, 75, 2.5, 120]);
    const n = choice([40, 80, 120, 160, 240, 320, 360, 480, 640, 800, 1200]);
    return [`${p}% of ${n}`, (p * n) / 100];
  }) as Gen,
  frac: (() => {
    const d = choice([3, 6, 7, 8, 9, 11, 12, 16]);
    const k = randint(1, d - 1);
    return [`${k}/${d} as a decimal (3 d.p.)`, round(k / d, 3)];
  }) as Gen,
  sq: (() => {
    const n = choice([...Array.from({ length: 22 }, (_, i) => 11 + i), 45, 55, 65, 75, 85, 95]);
    return [`${n}²`, n * n];
  }) as Gen,
  ev: (() => {
    const k = Math.random();
    if (k < 0.33) {
      const p = choice([0.1, 0.2, 0.25, 0.4, 0.6, 0.75]);
      const a = randint(1, 20) * 5, b = randint(0, 10) * 2;
      return [`EV: ${p} chance of ${a}, else ${b}`, round(p * a + (1 - p) * b, 2)];
    }
    if (k < 0.66) {
      const n = randint(2, 6);
      return [`expected sum of ${n} dice`, 3.5 * n];
    }
    const s = choice([4, 6, 8, 10, 12, 20]);
    return [`expected value of one fair d${s} (1..${s})`, (s + 1) / 2];
  }) as Gen,
};

export type Topic = keyof typeof GENERATORS;
export const TOPICS: { id: Topic; label: string }[] = [
  { id: "mul", label: "Multiply" },
  { id: "div", label: "Divide" },
  { id: "add", label: "Decimals ±" },
  { id: "pct", label: "Percent" },
  { id: "frac", label: "Fractions" },
  { id: "sq", label: "Squares" },
  { id: "ev", label: "Expected value" },
];

export function nextQuestion(topics: Topic[]): Question {
  const topic = choice(topics);
  const [text, answer] = GENERATORS[topic]();
  return { text, answer, topic };
}

/** Same rule as drill.py: exact for integers, ±0.005 for decimals. */
export function isCorrect(raw: string, truth: number) {
  const s = raw.replace(/,/g, "").trim();
  if (!s) return false;
  const x = Number(s);
  if (Number.isNaN(x)) return false;
  return Math.abs(x - truth) <= (Number.isInteger(truth) ? 1e-9 : 0.005 + 1e-9);
}

export const fmt = (x: number) => String(Number(x.toFixed(6)));
