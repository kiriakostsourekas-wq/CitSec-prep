"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, useSyncExternalStore } from "react";
import { LANES, type LaneId, MAP, TERMINAL } from "@/lib/plan-map";
import { type Progress, taskKey, useProgress } from "@/lib/progress";

export type MapStop = {
  key: string;
  lane: LaneId;
  x: number;
  session: number;
  label: string;
  below?: boolean;
  title: string;
  href: string;
  time: string;
  note: string;
  folder?: string;
  taskIds?: string[];
};

type Status = { done: number; total: number; complete: boolean; started: boolean };

function statusOf(p: Progress, s: MapStop): Status {
  if (s.folder && s.taskIds?.length) {
    const done = s.taskIds.filter((id) => p.tasks[taskKey(s.folder!, id)] === "PASS").length;
    return { done, total: s.taskIds.length, complete: done === s.taskIds.length, started: done > 0 };
  }
  const v = p.visited?.[s.key] ? 1 : 0;
  return { done: v, total: 1, complete: v === 1, started: v === 1 };
}

const BG = "#07090c";
const TAIL_X = 880;
const viewW = MAP.width - MAP.left;
const pct = (x: number, y: number) => ({ left: `${((x - MAP.left) / viewW) * 100}%`, top: `${(y / MAP.height) * 100}%` });
const tail = (x: number, y: number) =>
  `M ${x} ${y} L ${TAIL_X} ${y} C ${TAIL_X + 36} ${y} ${TERMINAL.x - 40} ${TERMINAL.y} ${TERMINAL.x - 18} ${TERMINAL.y}`;
const reducedMotion = () => typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const noop = () => () => {};

/** The study plan as a live metro map: one line per interview round, lit up as you make progress. */
export function PlanMap({ stops, sessions }: { stops: MapStop[]; sessions: { n: number; hours: number }[] }) {
  const p = useProgress();
  const router = useRouter();
  const [hover, setHover] = useState<string | null>(null);
  const motion = !useSyncExternalStore(noop, reducedMotion, () => true);

  const status = Object.fromEntries(stops.map((s) => [s.key, statusOf(p, s)]));
  const ordered = [...stops].filter((s) => s.session > 0).sort((a, b) => a.session - b.session || a.x - b.x);
  const next = ordered.find((s) => !status[s.key].complete) ?? null;
  const doneCount = stops.filter((s) => status[s.key].complete).length;
  const hovered = stops.find((s) => s.key === hover);

  const lanes = (Object.keys(LANES) as LaneId[]).map((id) => ({
    id,
    ...LANES[id],
    stops: stops.filter((s) => s.lane === id).sort((a, b) => a.x - b.x),
  }));

  const nextPrev = next ? lanes.find((l) => l.id === next.lane)!.stops.filter((s) => s.x < next.x).at(-1) : undefined;

  return (
    <div>
      {/* ------------------------------------------------ wide screens: the map */}
      <div className="relative hidden lg:block">
        <svg viewBox={`${MAP.left} 0 ${viewW} ${MAP.height}`} className="h-auto w-full select-none" role="img" aria-label="Study plan map">
          {sessions.map((s, i) => {
            const x0 = MAP.colStart + i * MAP.colWidth;
            const current = next?.session === s.n;
            return (
              <g key={s.n}>
                <rect
                  x={x0}
                  y={30}
                  width={MAP.colWidth}
                  height={MAP.height - 40}
                  rx={10}
                  fill={current ? "rgba(255,176,32,0.045)" : i % 2 ? "rgba(255,255,255,0.014)" : "transparent"}
                />
                <text x={x0 + MAP.colWidth / 2} y={20} textAnchor="middle" fontSize={12} className="tabular-nums">
                  <tspan fontWeight={500} fill={current ? "#ffb020" : "#95a3b5"}>
                    Session {s.n}
                  </tspan>
                  <tspan dx={6} fill="#5f6d7e">
                    {s.hours} h
                  </tspan>
                </text>
              </g>
            );
          })}

          {lanes.map((l) => {
            const first = l.stops[0];
            if (!first) return null;
            const segs = l.stops.map((s, i) => {
              const to = l.stops[i + 1];
              return { from: s, d: to ? `M ${s.x} ${l.y} L ${to.x} ${l.y}` : tail(s.x, l.y) };
            });
            return (
              <g key={l.id}>
                <text x={first.x - 22} y={l.y + 4} textAnchor="end" fontSize={12} fontWeight={500} fill={l.color}>
                  {l.label}
                </text>
                <path d={`M ${first.x} ${l.y} ` + tail(l.stops.at(-1)!.x, l.y).slice(1)} fill="none" stroke={l.color} strokeOpacity={0.16} strokeWidth={6} strokeLinecap="round" />
                {segs.map((seg, i) => {
                  // A finished station lights the track towards the next one, as far as that station's own progress.
                  if (!status[seg.from.key].complete) return null;
                  const to = l.stops[i + 1];
                  const toSt = to && status[to.key];
                  const frac = !to ? 1 : toSt.complete ? 1 : Math.max(0.15, toSt.done / toSt.total);
                  const len = to ? to.x - seg.from.x : 1;
                  return (
                    <path
                      key={i}
                      d={seg.d}
                      fill="none"
                      stroke={l.color}
                      strokeWidth={6}
                      strokeLinecap="round"
                      strokeDasharray={to ? `${frac * len} ${len}` : undefined}
                      className="transition-[stroke-dasharray] duration-700"
                    />
                  );
                })}
              </g>
            );
          })}

          {motion && next && nextPrev && (
            <circle r={3.5} fill="#fff">
              <animateMotion dur="2.4s" repeatCount="indefinite" path={`M ${nextPrev.x} ${LANES[next.lane].y} L ${next.x - 10} ${LANES[next.lane].y}`} />
            </circle>
          )}

          {/* the terminal */}
          <g>
            <circle cx={TERMINAL.x} cy={TERMINAL.y} r={17} fill={BG} stroke="#e6edf3" strokeWidth={3} />
            <circle cx={TERMINAL.x} cy={TERMINAL.y} r={7} fill={doneCount === stops.length ? "#ffb020" : "#e6edf3"} />
            <text x={TERMINAL.x} y={TERMINAL.y + 42} textAnchor="middle" fontSize={17} fontWeight={600} fill="#e6edf3" className="serif">
              Superday
            </text>
            <text x={TERMINAL.x} y={TERMINAL.y + 59} textAnchor="middle" fontSize={12} fill="#5f6d7e" className="tabular-nums">
              {doneCount} of {stops.length} stops
            </text>
          </g>

          {stops.map((s) => {
            const { color, y } = LANES[s.lane];
            const st = status[s.key];
            const isNext = next?.key === s.key;
            const ring = 2 * Math.PI * 13;
            const lit = st.complete || st.started || isNext;
            const open = () => router.push(s.href);
            return (
              <g
                key={s.key}
                role="link"
                tabIndex={0}
                aria-label={`${s.title}: ${st.complete ? "done" : `${st.done} of ${st.total}`}`}
                onClick={open}
                onKeyDown={(e) => e.key === "Enter" && open()}
                onMouseEnter={() => setHover(s.key)}
                onMouseLeave={() => setHover(null)}
                onFocus={() => setHover(s.key)}
                onBlur={() => setHover(null)}
                className="cursor-pointer outline-none"
              >
                <circle cx={s.x} cy={y} r={18} fill="transparent" />
                {isNext && <circle cx={s.x} cy={y} r={9} fill="none" stroke={color} strokeWidth={2} className="map-pulse" />}
                {st.started && !st.complete && (
                  <circle
                    cx={s.x}
                    cy={y}
                    r={13}
                    fill="none"
                    stroke={color}
                    strokeWidth={2.5}
                    strokeLinecap="round"
                    strokeDasharray={`${(st.done / st.total) * ring} ${ring}`}
                    transform={`rotate(-90 ${s.x} ${y})`}
                  />
                )}
                <circle
                  cx={s.x}
                  cy={y}
                  r={hover === s.key ? 9.5 : 8}
                  fill={st.complete ? color : BG}
                  stroke={color}
                  strokeWidth={3}
                  opacity={lit ? 1 : 0.6}
                  className="transition-all duration-200"
                />
                {st.complete && (
                  <path d={`M ${s.x - 3.5} ${y} L ${s.x - 1} ${y + 2.5} L ${s.x + 3.5} ${y - 2.5}`} fill="none" stroke={BG} strokeWidth={2} strokeLinecap="round" />
                )}
                <text
                  x={s.x}
                  y={s.below ? y + 31 : y - 21}
                  textAnchor="middle"
                  fontSize={12.5}
                  fontWeight={isNext ? 600 : 400}
                  fill={lit || hover === s.key ? "#e6edf3" : "#95a3b5"}
                >
                  {s.label}
                </text>
              </g>
            );
          })}
        </svg>

        {hovered && <StopCard stop={hovered} status={status[hovered.key]} isNext={next?.key === hovered.key} />}
      </div>

      {/* ------------------------------------------------ narrow screens: the same line, vertical */}
      <ol className="lg:hidden">
        {[...sessions.map((s) => ({ n: s.n, title: `Session ${s.n}`, hours: `${s.hours} h` })), { n: 0, title: "Every day", hours: "8 min" }].map((sec) => {
          const own = stops.filter((s) => s.session === sec.n).sort((a, b) => a.x - b.x);
          return (
            <li key={sec.n}>
              <div className={`flex items-baseline justify-between pb-2 pt-5 text-[13px] font-medium tabular-nums ${next?.session === sec.n ? "text-accent" : "text-muted"}`}>
                <span>{sec.title}</span>
                <span>{sec.hours}</span>
              </div>
              <ul>
                {own.map((s) => {
                  const st = status[s.key];
                  const { color } = LANES[s.lane];
                  const isNext = next?.key === s.key;
                  return (
                    <li key={s.key} className="relative pl-9">
                      <span className="absolute bottom-0 left-[11px] top-0 w-[3px] rounded-full" style={{ background: color, opacity: st.complete ? 1 : 0.18 }} />
                      <span
                        className={`absolute left-[4px] top-[14px] grid size-[17px] place-items-center rounded-full border-[3px] text-[9px] font-bold ${isNext ? "map-pulse-css" : ""}`}
                        style={{ borderColor: color, background: st.complete ? color : BG, color: BG }}
                      >
                        {st.complete ? "✓" : ""}
                      </span>
                      <Link href={s.href} className="block py-2.5">
                        <span className={`block ${st.complete || isNext ? "text-text" : "text-muted"} ${isNext ? "font-medium" : ""}`}>{s.title}</span>
                        <span className="block text-xs text-dim">
                          {[LANES[s.lane].label, s.note, s.folder ? `${st.done} of ${st.total} tasks` : ""].filter(Boolean).join(", ")}
                        </span>
                      </Link>
                    </li>
                  );
                })}
              </ul>
            </li>
          );
        })}
      </ol>

      {/* ------------------------------------------------ next stop */}
      <div className="mt-6 flex flex-wrap items-center gap-x-6 gap-y-3 rounded-xl border border-line bg-raised px-5 py-4">
        {next ? (
          <>
            <span className="size-2.5 shrink-0 rounded-full" style={{ background: LANES[next.lane].color }} />
            <div className="min-w-0 flex-1">
              <div className="text-xs text-dim">
                Next stop, {next.session ? `session ${next.session}` : "every day"}
              </div>
              <div className="mt-0.5 font-serif text-lg font-semibold text-text">
                {next.title}
                {next.note && <span className="text-sm text-dim"> {next.note}</span>}
              </div>
            </div>
            <Link href={next.href} className="rounded-md bg-accent px-4 py-2 text-sm font-semibold text-accent-ink hover:brightness-110">
              {status[next.key].started ? "Continue" : "Start"}
            </Link>
          </>
        ) : (
          <div className="text-text">Every stop is done. Redo the mock interview once more, then get some sleep.</div>
        )}
      </div>
    </div>
  );
}

function StopCard({ stop, status, isNext }: { stop: MapStop; status: Status; isNext: boolean }) {
  const { color, label } = LANES[stop.lane];
  const pos = pct(stop.x, LANES[stop.lane].y);
  return (
    <div
      className="pointer-events-none absolute z-10 w-64 rounded-xl border border-line-strong bg-panel/95 p-4 shadow-2xl backdrop-blur"
      style={{ ...pos, transform: `translate(-50%, ${stop.lane === "interview" || stop.lane === "coding" ? "34px" : "calc(-100% - 34px)"})` }}
    >
      <div className="flex items-center gap-2 text-xs" style={{ color }}>
        <span className="size-2 rounded-full" style={{ background: color }} />
        {label}, {stop.session ? `session ${stop.session}` : "every day"}
        {isNext && <span className="ml-auto text-accent">Next stop</span>}
      </div>
      <div className="mt-2 font-serif text-[17px] font-semibold text-text">{stop.title}</div>
      {stop.note && <div className="mt-0.5 text-sm text-muted">{stop.note}</div>}
      <div className="mt-3 flex items-center gap-3">
        <div className="h-1 flex-1 overflow-hidden rounded-full bg-line">
          <div className="h-full rounded-full" style={{ width: `${(status.done / status.total) * 100}%`, background: color }} />
        </div>
        <span className="text-xs tabular-nums text-dim">
          {stop.folder ? `${status.done} of ${status.total} tasks` : status.complete ? "Done" : "Not opened yet"}
        </span>
      </div>
      {stop.time && <div className="mt-2 text-xs text-dim">About {stop.time}</div>}
    </div>
  );
}
