import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

test('WEB-E2E-001 staticLogical journey is deterministic, reversible and non-completing; browser decision remains pending', async () => {
  const vectors = JSON.parse(await readFile(new URL('../state/preview-state-vectors.json', import.meta.url), 'utf8'));
  const model = await import(new URL('../state/preview-state.mjs', import.meta.url));
  assert.equal(vectors.staticLogical, 'required');
  assert.equal(vectors.browserDecision, 'required-pending');
  assert.equal(vectors.manualDecision, 'required-pending');
  assert.deepEqual(vectors.journey.map(({ action }) => action), [
    'frame-explicit',
    'controlled-failure-explicit',
    'diagnose-explicit',
    'alternative-explicit',
    'reset-explicit',
    'verify-fixture-explicit',
    'review-evidence-explicit',
    'reflection-open-explicit',
  ]);
  let state = model.createBaselineState();
  for (const vector of vectors.journey) {
    state = model.reducePreviewState(state, { type: vector.action });
    assert.equal(state.state, vector.expectedState, vector.action);
    assert.equal(state.committedAct, vector.expectedCommittedAct, vector.action);
  }
  assert.equal(state.fixtureVerifyStatus, 'verified-synthetic-only');
  assert.equal(state.evidenceReviewStatus, 'reviewed-synthetic-only');
  assert.equal(state.conclusion, 'insufficient evidence');
  assert.equal(JSON.stringify(state).includes('completed'), false);
});
