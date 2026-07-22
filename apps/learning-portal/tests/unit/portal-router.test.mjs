import test from "node:test";
import assert from "node:assert/strict";
import { PUBLIC_ROUTES, resolveRoute } from "../../src/routing/portal-router.mjs";

test("PTP-RED-A-013 resolves the exact 13 stable public documents", () => {
  assert.equal(PUBLIC_ROUTES.length, 13, "catalog/module/lesson/step route set is absent");
  for (const path of PUBLIC_ROUTES) assert.notEqual(resolveRoute(path).kind, "not-found", `route missing: ${path}`);
});

test("unknown, traversal, encoded, query, and overlong routes fail closed", () => {
  for (const path of ["/unknown", "/../secret", "/%2e%2e/secret", "/?run=true", `/${"a".repeat(2050)}`]) {
    assert.equal(resolveRoute(path).kind, "not-found");
  }
});
