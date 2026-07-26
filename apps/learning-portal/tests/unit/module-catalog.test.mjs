import test from "node:test";
import assert from "node:assert/strict";
import { provideReleasedModules } from "../../src/catalog/released-module-provider.mjs";
import { createModuleCatalog } from "../../src/catalog/module-catalog.mjs";

test("PTP-RED-A-010 exposes one honest reusable vertical slice", async () => {
  const catalog = createModuleCatalog(await provideReleasedModules());
  assert.equal(catalog.modules.length, 1, "released vertical slice is absent");
  assert.equal(catalog.modules[0].lessons[0].id, "promotion-trust");
  assert.equal(catalog.modules[0].id, undefined, "presentation module must not invent an identifier");
});

test("SA-R11 rejects duplicate released descriptors", () => {
  assert.throws(() => createModuleCatalog([{ lessons: [{ id: "promotion-trust" }] }, { lessons: [{ id: "promotion-trust" }] }]), /DUPLICATE_RELEASED_LESSON/);
});

const syntheticModule = () => ({
  title: "Synthetic module",
  description: "Test-only descriptor",
  lessons: [{
    id: "synthetic-safe",
    title: "Synthetic safe lesson",
    summary: "Exercises the generic content seam.",
    adapterId: "promotion-trust",
    steps: [
      { id: "open", label: "Open" },
      { id: "close", label: "Close" },
    ],
    model: { lesson: { title: "Synthetic safe lesson" }, grains: [] },
  }],
});

test("SA-R11 derives a second safe descriptor without promotion-specific routing data", () => {
  const first = { title: "First", description: "First module", lessons: [{ id: "first-safe", title: "First", summary: "First", adapterId: "promotion-trust", steps: [{ id: "only", label: "Only" }], model: { lesson: {}, grains: [] } }] };
  const catalog = createModuleCatalog([first, syntheticModule()]);
  assert.equal(catalog.modules[1].lessons[0].path, "/lesson/synthetic-safe");
  assert.deepEqual(catalog.modules[1].lessons[0].steps.map((step) => step.path), ["/lesson/synthetic-safe/step/open", "/lesson/synthetic-safe/step/close"]);
});

test("SA-R11 rejects unknown, duplicate, and unsafe descriptor fields with stable errors", () => {
  const cases = [
    [null, /CATALOG_DESCRIPTOR_INVALID/],
    [{ title: "Bad", description: "Bad", extra: true, lessons: [] }, /CATALOG_DESCRIPTOR_UNKNOWN_FIELD/],
    [{ title: "Bad", description: "Bad", lessons: [{ ...syntheticModule().lessons[0], id: "../unsafe" }] }, /CATALOG_ID_UNSAFE/],
    [{ title: "Bad", description: "Bad", lessons: [{ ...syntheticModule().lessons[0], adapterId: "unknown-adapter" }] }, /CATALOG_ADAPTER_UNKNOWN/],
    [{ title: "Bad", description: "Bad", lessons: [{ ...syntheticModule().lessons[0], steps: [{ id: "same", label: "A" }, { id: "same", label: "B" }] }] }, /DUPLICATE_RELEASED_STEP/],
  ];
  for (const [descriptor, pattern] of cases) assert.throws(() => createModuleCatalog([descriptor]), pattern);
});
