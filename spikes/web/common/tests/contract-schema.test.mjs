import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const root = new URL('../', import.meta.url);
const contracts = [
  'contracts/lesson-manifest-view.schema.json',
  'contracts/mart-evidence-view.schema.json',
  'contracts/journey-state-view.schema.json',
  'contracts/lab-client-view.schema.json',
  'contracts/evidence-index-view.schema.json',
  'contracts/candidate-evidence-record.schema.json',
];
const invalidFixtures = [
  'tests/fixtures/invalid-completed-state.json',
  'tests/fixtures/invalid-cross-grain-attribution.json',
  'tests/fixtures/invalid-executable-content.json',
  'tests/fixtures/invalid-secret-canary.json',
  'tests/fixtures/invalid-stale-digest.json',
  'tests/fixtures/invalid-unknown-field.json',
];

async function json(path) {
  return JSON.parse(await readFile(new URL(path, root), 'utf8'));
}

test('WEB-CONTRACT-001 staticLogical rejects incomplete, unknown, executable, stale, secret and authority-bearing data', async () => {
  const schemas = await Promise.all(contracts.map(json));
  assert.equal(schemas.length, 6);
  for (const schema of schemas) {
    assert.equal(schema.type, 'object');
    assert.equal(schema.additionalProperties, false, `${schema.$id ?? 'schema'} must fail closed`);
    assert.ok(Array.isArray(schema.required) && schema.required.length > 0);
  }

  const lessonSchema = schemas[0];
  const martSchema = schemas[1];
  const stateSchema = schemas[2];
  assert.match(JSON.stringify(lessonSchema.required), /evidence/i);
  assert.match(JSON.stringify(lessonSchema), /hint/i);
  assert.match(JSON.stringify(martSchema.required), /grain/i);
  assert.match(JSON.stringify(martSchema.required), /weight/i);
  assert.match(JSON.stringify(martSchema.required), /limitation/i);
  assert.doesNotMatch(JSON.stringify(stateSchema), /completed/i);

  const fixtureTexts = await Promise.all(invalidFixtures.map((path) => readFile(new URL(path, root), 'utf8')));
  assert.equal(globalThis.hostileFixtureExecuted, undefined, 'inert JSON must never execute');
  assert.ok(fixtureTexts.every((value) => typeof value === 'string'));

  const validator = await import(new URL('../state/preview-state.mjs', import.meta.url));
  assert.equal(typeof validator.validatePreviewDocument, 'function');
  for (let index = 0; index < fixtureTexts.length; index += 1) {
    const parsed = JSON.parse(fixtureTexts[index]);
    const result = validator.validatePreviewDocument(parsed);
    assert.equal(result.ok, false, `${invalidFixtures[index]} must be rejected`);
    assert.ok(result.errors.some((entry) => typeof entry.path === 'string' && entry.path.startsWith('/')),
      `${invalidFixtures[index]} must report a logical JSON location`);
  }
});

test('WEB-CONTRACT-001 state-view validation shares the canonical browser state vocabulary', async () => {
  const validator = await import(new URL('../state/preview-state.mjs', import.meta.url));
  const baseline = validator.createBaselineState();
  const view = {
    attemptId: baseline.attemptId,
    fixtureKind: baseline.fixtureKind,
    fixtureDigest: baseline.fixtureDigest,
    state: baseline.state,
    currentAct: baseline.currentAct,
    committedAct: baseline.committedAct,
    hintLevel: baseline.hintLevel,
    fixtureVerifyStatus: baseline.fixtureVerifyStatus,
    evidenceReviewStatus: baseline.evidenceReviewStatus,
    resetAuditCount: baseline.resetAuditCount,
    repositoryMutation: false,
  };
  assert.equal(validator.validatePreviewDocument(view).ok, true);
  const incomplete = { ...view };
  delete incomplete.attemptId;
  delete incomplete.hintLevel;
  assert.equal(validator.validatePreviewDocument(incomplete).ok, false);
  assert.equal(validator.validatePreviewDocument({
    ...view,
    hintLevel: 'invented',
    fixtureVerifyStatus: 'verified-real',
    evidenceReviewStatus: 'complete',
    resetAuditCount: -1,
  }).ok, false);
});
