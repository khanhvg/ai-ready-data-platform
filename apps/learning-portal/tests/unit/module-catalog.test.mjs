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
