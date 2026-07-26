import test from "node:test";
import assert from "node:assert/strict";
import { loadReleasedLearning } from "../../src/contracts/released-learning-adapter.mjs";

test("PTP-RED-A-011 maps the canonical controlled decision without attribution", async () => {
  const released = await loadReleasedLearning();
  assert.equal(released.lesson?.decision.value, "insufficient-evidence", "canonical decision is absent");
  assert.equal(released.lesson?.decision.reason, "no-common-grain", "canonical reason is absent");
  assert.equal(released.lesson?.limitations.length, 2, "released limitations are absent");
  assert.equal("records" in released, false, "raw records must never enter the portal model");
});
