import test from "node:test";
import assert from "node:assert/strict";
import { renderStaticDocument } from "../../src/render/static-document.mjs";
import { provideReleasedModules } from "../../src/catalog/released-module-provider.mjs";
import { createModuleCatalog } from "../../src/catalog/module-catalog.mjs";

test("PTP-RED-A-014/021 static output carries facts, navigation, and non-claims", async () => {
  const catalog = createModuleCatalog(await provideReleasedModules());
  const html = renderStaticDocument({ kind: "lesson", path: "/lesson/promotion-trust" }, catalog);
  for (const fact of ["insufficient-evidence", "no-common-grain", "data-runner=\"unavailable\"", "Chưa phải sản phẩm học tập đầy đủ", "Bỏ qua đến nội dung chính"]) {
    assert.match(html, new RegExp(fact), `static renderer lacks ${fact}`);
  }
  assert.doesNotMatch(html, /<button|dangerouslySetInnerHTML|data-progress=\"enabled\"/);
});

test("SA-R11 static rendering selects the requested descriptor instead of modules[0]", () => {
  const model = { grains: [], lesson: { title: "Synthetic selected", summary: "Selected", stakeholderQuestion: "Synthetic question", controlledFailure: { code: "SYNTHETIC", symptom: "Synthetic" }, decision: { value: "insufficient-evidence", reason: "no-common-grain" }, reflection: "Synthetic reflection" } };
  const catalog = createModuleCatalog([
    { title: "First", description: "First", lessons: [{ id: "first-safe", title: "Wrong first lesson", summary: "Wrong", adapterId: "promotion-trust", steps: [{ id: "only", label: "Only" }], model }] },
    { title: "Second", description: "Second", lessons: [{ id: "synthetic-safe", title: "Synthetic selected", summary: "Selected", adapterId: "promotion-trust", steps: [{ id: "open", label: "Open" }, { id: "close", label: "Close" }], model }] },
  ]);
  const html = renderStaticDocument({ kind: "lesson", path: "/lesson/synthetic-safe", lessonId: "synthetic-safe" }, catalog);
  assert.match(html, /Synthetic selected/);
  assert.match(html, /\/lesson\/synthetic-safe\/step\/open/);
  assert.doesNotMatch(html, /Wrong first lesson/);
});
