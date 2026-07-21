import assert from 'node:assert/strict';
import test from 'node:test';

test('WEB-STATE-002 staticLogical reset is deterministic, idempotent and separately audit-counted', async () => {
  const { createBaselineState, reducePreviewState, resettableDigest } = await import(new URL('../state/preview-state.mjs', import.meta.url));
  const baseline = createBaselineState();
  const changed = reducePreviewState(baseline, { type: 'next-explicit' });
  const once = reducePreviewState(changed, { type: 'reset-explicit' });
  const twice = reducePreviewState(once, { type: 'reset-explicit' });
  assert.equal(resettableDigest(once), resettableDigest(baseline));
  assert.equal(resettableDigest(twice), resettableDigest(baseline));
  assert.equal(once.resetAuditCount, changed.resetAuditCount + 1);
  assert.equal(twice.resetAuditCount, once.resetAuditCount + 1);
  assert.equal(once.historyMode, 'replace');
  assert.equal(twice.historyMode, 'replace');
  assert.equal(once.repositoryMutation, false);
  assert.equal(twice.repositoryMutation, false);
});
