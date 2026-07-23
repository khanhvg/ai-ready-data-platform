import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { createReleasedLearningAdapter } from '../../src/contracts/released-learning-adapter.mjs';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const repositoryRoot = resolve(appRoot, '../..');

test('PTP-RED-A-001 admits the exact 85-row release only after released validators run', () => {
  const output = execFileSync(process.execPath, ['scripts/verify-stage-a-release.mjs'], {
    cwd: appRoot,
    encoding: 'utf8'
  });
  const report = JSON.parse(output);
  assert.equal(report.releasedInputsRequired, 85);
  assert.equal(report.releasedInputsAdmitted, 85, 'PTP_RED_RELEASE_ADMISSION_ABSENT');
  assert.equal(report.semanticReady, true, 'PTP_RED_RELEASE_ADMISSION_ABSENT');
  const registry = createReleasedLearningAdapter({ repositoryRoot }).readRegistry();
  assert.deepEqual(
    registry.source.validatorsInvoked,
    ['learning-contracts-check', 'lesson-check', 'api-contracts-check'],
    'PTP_RED_RELEASE_ADMISSION_ABSENT'
  );
});

test('PTP-RED-A-002 rejects one-change drift of protected Issue #6 bytes', async () => {
  const protectedPath = resolve(
    repositoryRoot,
    'tests/fixtures/learning/promotion-trust/evidence-v1.json'
  );
  const protectedBytes = await readFile(protectedPath);
  const drifted = Buffer.from(protectedBytes);
  drifted[0] ^= 1;
  assert.throws(
    () => createReleasedLearningAdapter({ repositoryRoot, protectedByteOverrides: { [protectedPath]: drifted } }),
    /PORTAL_RELEASE_IDENTITY_MISMATCH/,
    'PTP_RED_RELEASE_ADMISSION_ABSENT'
  );
});

test('PTP-RED-A-020 rejects path, hash, version, family, field, state, and authority drift', () => {
  const mutations = [
    { path: '../outside.json' },
    { sha256: '0'.repeat(64) },
    { version: 'unit-version' },
    { family: 'unit-family' },
    { unexpectedField: true },
    { state: 'draft' },
    { authorityKind: 'test-only-structure' }
  ];
  for (const descriptorMutation of mutations) {
    assert.throws(
      () => createReleasedLearningAdapter({ repositoryRoot, descriptorMutation }),
      /PORTAL_DESCRIPTOR_AUTHORITY_FORBIDDEN/,
      'PTP_RED_PRODUCTION_REGISTRY_ABSENT'
    );
  }
});

test('adapter exposes only released read operations and no Stage A mutation authority', () => {
  const capabilities = createReleasedLearningAdapter({ repositoryRoot }).describeCapabilities();
  assert.equal(capabilities.readOnly, true);
  assert.equal(capabilities.listLessons, true, 'PTP_RED_RELEASE_ADMISSION_ABSENT');
  assert.equal(capabilities.getLesson, true, 'PTP_RED_RELEASE_ADMISSION_ABSENT');
  assert.deepEqual(capabilities.mutations, []);
  for (const forbidden of ['run', 'reset', 'verify', 'progress', 'completion', 'evidence', 'workspace', 'query']) {
    assert.equal(forbidden in capabilities, false);
  }
});
