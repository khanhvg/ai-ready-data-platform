import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

test('WEB-FAIL-001 staticLogical gives controlled, environmental and unexpected failures distinct behavior', async () => {
  const taxonomy = JSON.parse(await readFile(new URL('../contracts/failure-codes.json', import.meta.url), 'utf8'));
  const controlled = taxonomy.failures.find(({ code }) => code === 'PROMOTION_HEADLINE_INSUFFICIENT');
  const environmentCodes = ['FIXTURE_UNAVAILABLE', 'FIXTURE_DIGEST_MISMATCH', 'STATIC_ASSET_UNAVAILABLE'];
  const environmental = taxonomy.failures.filter(({ code }) => environmentCodes.includes(code));
  const unexpected = taxonomy.failures.find(({ code }) => code === 'PREVIEW_UNEXPECTED');
  assert.ok(controlled && unexpected);
  assert.equal(environmental.length, 3);
  assert.equal(controlled.class, 'controlled-analytical');
  assert.equal(controlled.progression, 'diagnosis-only');
  assert.ok(environmental.every((failure) => failure.class === 'environmental' && failure.progression === 'stopped'));
  assert.equal(unexpected.class, 'unexpected-product');
  assert.equal(unexpected.progression, 'stopped');
  for (const failure of [controlled, ...environmental, unexpected]) {
    for (const field of ['copy', 'recovery', 'evidence', 'cue']) assert.match(failure[field], /\S/, `${failure.code}.${field}`);
  }
  assert.equal(new Set([controlled, environmental[0], unexpected].map(({ copy }) => copy)).size, 3);
  assert.equal(new Set([controlled, environmental[0], unexpected].map(({ recovery }) => recovery)).size, 3);
});
