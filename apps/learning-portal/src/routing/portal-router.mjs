import { createModuleCatalog } from "../catalog/module-catalog.mjs";

export const STEP_IDS = Object.freeze(["frame", "inspect", "run", "fail", "trace", "decide", "reset", "configure", "verify", "reflect"]);
const defaultCatalog = createModuleCatalog([{ title: "Released", description: "Released default route descriptor", lessons: [{ id: "promotion-trust", title: "Promotion trust", summary: "Released lesson", adapterId: "promotion-trust", steps: STEP_IDS.map((id) => ({ id })), model: { lesson: {}, grains: [] } }] }]);

export function publicRoutes(catalog) {
  const routes = ["/", "/module"];
  for (const lesson of catalog.modules.flatMap((module) => module.lessons)) routes.push(lesson.path, ...lesson.steps.map((step) => step.path));
  return Object.freeze(routes);
}
export const PUBLIC_ROUTES = publicRoutes(defaultCatalog);

export function resolveRoute(input, catalog = defaultCatalog) {
  if (typeof input !== "string" || input.length > 2048 || input.includes("?") || input.includes("#") || input.includes("%") || input.includes("..")) return Object.freeze({ kind: "not-found", path: "/404" });
  if (input === "/") return Object.freeze({ kind: "catalog", path: input });
  if (input === "/module") return Object.freeze({ kind: "module", path: input });
  for (const lesson of catalog.modules.flatMap((module) => module.lessons)) {
    if (input === lesson.path) return Object.freeze({ kind: "lesson", path: input, lessonId: lesson.id });
    const index = lesson.steps.findIndex((step) => step.path === input);
    if (index >= 0) return Object.freeze({ kind: "step", path: input, lessonId: lesson.id, stepId: lesson.steps[index].id, stepIndex: index });
  }
  return Object.freeze({ kind: "not-found", path: "/404" });
}
