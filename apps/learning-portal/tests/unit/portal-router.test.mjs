import test from "node:test";
import assert from "node:assert/strict";
import { PUBLIC_ROUTES, resolveRoute } from "../../src/routing/portal-router.mjs";
import { createModuleCatalog } from "../../src/catalog/module-catalog.mjs";

test("PTP-RED-A-013 resolves the exact 13 stable public documents", () => {
  assert.equal(PUBLIC_ROUTES.length, 13, "catalog/module/lesson/step route set is absent");
  for (const path of PUBLIC_ROUTES) assert.notEqual(resolveRoute(path).kind, "not-found", `route missing: ${path}`);
});

test("unknown, traversal, encoded, query, and overlong routes fail closed", () => {
  for (const path of ["/unknown", "/../secret", "/%2e%2e/secret", "/?run=true", `/${"a".repeat(2050)}`]) {
    assert.equal(resolveRoute(path).kind, "not-found");
  }
});

test("SA-R11 router derives lesson and ordered step dispatch from the validated catalog", () => {
  const catalog = createModuleCatalog([{ title: "Synthetic", description: "Test-only", lessons: [{ id: "synthetic-safe", title: "Synthetic", summary: "Safe", adapterId: "promotion-trust", steps: [{ id: "open", label: "Open" }, { id: "close", label: "Close" }], model: { lesson: {}, grains: [] } }] }]);
  assert.equal(resolveRoute("/lesson/synthetic-safe", catalog).lessonId, "synthetic-safe");
  assert.deepEqual(resolveRoute("/lesson/synthetic-safe/step/close", catalog), { kind: "step", path: "/lesson/synthetic-safe/step/close", lessonId: "synthetic-safe", stepId: "close", stepIndex: 1 });
  assert.equal(resolveRoute("/lesson/promotion-trust", catalog).kind, "not-found");
});
