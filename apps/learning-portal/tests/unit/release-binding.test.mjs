import test from "node:test";
import assert from "node:assert/strict";
import { loadReleasedLearning } from "../../src/contracts/released-learning-adapter.mjs";

test("PTP-RED-A-001/020 admits only the exact released binding and fixture", async () => {
  const released = await loadReleasedLearning();
  assert.equal(released.bindingId, "promotion-trust-vite-binding-v1", "released binding identity is absent");
  assert.equal(released.fixtureId, "promotion-trust-small-42-v1", "released fixture identity is absent");
  assert.equal(released.grains.length, 4, "four released grain bindings are absent");
});
