import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { createReleasedLearningAdapter } from '../../src/contracts/released-learning-adapter.mjs';
import { createReleasedModuleProvider } from '../../src/catalog/released-module-provider.mjs';
import { deriveModuleCatalog } from '../../src/catalog/module-catalog.mjs';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const repositoryRoot = resolve(appRoot, '../..');
const lesson = JSON.parse(
  await readFile(resolve(repositoryRoot, 'learning/lessons/promotion-trust/lesson-v1.json'), 'utf8')
);

test('PTP-RED-A-010 derives the released catalog, module, lesson, and ten-step journey', () => {
  const registry = createReleasedModuleProvider(
    createReleasedLearningAdapter({ repositoryRoot })
  ).readRegistry();
  const catalog = deriveModuleCatalog(registry);
  assert.equal(catalog.semanticReady, true, 'PTP_RED_CATALOG_SEMANTICS_ABSENT');
  assert.equal(catalog.modules.length, 1, 'PTP_RED_CATALOG_SEMANTICS_ABSENT');
  assert.equal(catalog.modules[0].lessons[0].id, lesson.id, 'PTP_RED_CATALOG_SEMANTICS_ABSENT');
  assert.deepEqual(
    catalog.modules[0].lessons[0].narrativeSteps.map(({ id }) => id),
    ['frame', 'inspect', 'run', 'fail', 'trace', 'decide', 'reset', 'configure', 'verify', 'reflect'],
    'PTP_RED_CATALOG_SEMANTICS_ABSENT'
  );
});

test('PTP-RED-A-011 preserves the released decision without cross-grain attribution', () => {
  const registry = createReleasedLearningAdapter({ repositoryRoot }).readRegistry();
  const catalog = deriveModuleCatalog(registry);
  const releasedLesson = catalog.modules.flatMap(({ lessons }) => lessons).find(({ id }) => id === lesson.id);
  assert.equal(
    releasedLesson?.decision?.status,
    'insufficient-evidence/no-common-grain',
    'PTP_RED_CATALOG_SEMANTICS_ABSENT'
  );
  assert.deepEqual(
    releasedLesson?.sourceGrains?.map(({ id }) => id),
    ['promotion', 'fulfillment', 'returns', 'dq'],
    'PTP_RED_CATALOG_SEMANTICS_ABSENT'
  );
});

test('pure catalog derivation accepts branded test-only structure without granting production authority', () => {
  const structuralRegistry = Object.freeze({
    authorityKind: 'test-only-structure',
    descriptors: Object.freeze([
      Object.freeze({
        id: 'unit-module',
        title: 'Unit module',
        lessons: Object.freeze([{ id: 'unit-lesson', narrativeSteps: [{ id: 'unit-step' }] }])
      })
    ])
  });
  const catalog = deriveModuleCatalog(structuralRegistry);
  assert.equal(catalog.modules[0].id, 'unit-module');
  assert.equal(catalog.authorityKind, 'test-only-structure');
  assert.equal(Object.isFrozen(catalog), true);
  assert.equal(catalog.semanticReady, false);
});

test('PTP-RED-A-015 distinguishes unavailable runner state from a controlled lesson failure', () => {
  const capabilities = createReleasedLearningAdapter({ repositoryRoot }).describeCapabilities();
  assert.equal(capabilities.runner?.state, 'unavailable', 'PTP_RED_CATALOG_SEMANTICS_ABSENT');
  assert.equal(capabilities.runner?.controlledFailure, false, 'PTP_RED_CATALOG_SEMANTICS_ABSENT');
  assert.equal(capabilities.completion, false, 'PTP_RED_CATALOG_SEMANTICS_ABSENT');
});
