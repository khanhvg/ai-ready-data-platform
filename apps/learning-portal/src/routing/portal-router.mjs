export const STEP_IDS = Object.freeze(["frame", "inspect", "run", "fail", "trace", "decide", "reset", "configure", "verify", "reflect"]);
export const PUBLIC_ROUTES = Object.freeze(["/", "/module", "/lesson/promotion-trust", ...STEP_IDS.map((id) => `/lesson/promotion-trust/step/${id}`)]);

export function resolveRoute(input) {
  if (typeof input !== "string" || input.length > 2048 || input.includes("?") || input.includes("#") || input.includes("%") || input.includes("..")) return Object.freeze({ kind: "not-found", path: "/404" });
  if (input === "/") return Object.freeze({ kind: "catalog", path: input });
  if (input === "/module") return Object.freeze({ kind: "module", path: input });
  if (input === "/lesson/promotion-trust") return Object.freeze({ kind: "lesson", path: input, lessonId: "promotion-trust" });
  const match = input.match(/^\/lesson\/promotion-trust\/step\/([a-z-]+)$/);
  if (match && STEP_IDS.includes(match[1])) return Object.freeze({ kind: "step", path: input, lessonId: "promotion-trust", stepId: match[1], stepIndex: STEP_IDS.indexOf(match[1]) });
  return Object.freeze({ kind: "not-found", path: "/404" });
}
