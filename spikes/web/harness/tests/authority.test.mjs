import assert from 'node:assert/strict';
import test from 'node:test';
import { pathToFileURL } from 'node:url';

const INPUT_SHA = '0c73f4712c8ac7902042735ff1da96ef1e5285a3';
const IMMUTABLE_ANCESTORS = [
  'e8ca5f3ee9e8976a4b92915fd7d7dc687609f7a9',
  '0890c4abab46f81d110be6cbd6de3560e631a735',
  'a39251d45a56124322b9143ad16b926b2656073b',
  'f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c',
  'e440c5855732d5d8f5d634e3cc1359c010cc5ed3',
  '0486642528b9a6ba8e96cee18d6eda76c3b5deb9',
];
const CHECKER_URL = pathToFileURL(
  new URL('../scripts/authority-check.mjs', import.meta.url).pathname,
).href;

const WEB_IDS = [
  'WEB-CONTRACT-001', 'WEB-CONTRACT-002', 'WEB-CONTRACT-003',
  'WEB-PREVIEW-001', 'WEB-PREVIEW-002',
  'WEB-STATE-001', 'WEB-STATE-002', 'WEB-FAIL-001',
  'WEB-TRUST-001', 'WEB-TRUST-002',
  'WEB-A11Y-001', 'WEB-A11Y-002', 'WEB-A11Y-003', 'WEB-A11Y-004',
  'WEB-STATIC-001', 'WEB-NOSCROLL-001', 'WEB-API-001',
  'WEB-E2E-001', 'WEB-NONCOPY-001',
];

const MAKE_TARGETS = [
  'i5-02-authority-check',
  'i5-02-protected-hash-check',
  'i5-02-toolchain-check',
  'i5-02-changed-path-check',
  'i5-02-security-check',
  'i5-02-credential-check',
  'i5-02-non-copy-check',
  'web-common-test',
  'learn-preview',
  'learn-preview-status',
  'learn-preview-reset-check',
  'learn-preview-down',
];

const SCORE_CATEGORIES = [
  ['authoring-content-schema-mdx', 20],
  ['accessibility-static-reduced-motion', 20],
  ['lab-state-evidence-typed-api', 20],
  ['startup-rss-client-js', 15],
  ['unit-e2e-visual-evidence', 10],
  ['hosted-ecs-evolution-rollback', 10],
  ['maintenance-dependency-supply-chain', 5],
];

function anchors() {
  return Object.fromEntries(SCORE_CATEGORIES.map(([name, weight]) => [name, {
    weight,
    levels: Object.fromEntries(Array.from({ length: 6 }, (_, level) => [
      String(level),
      { predicates: [`fixed-${name}-${level}`] },
    ])),
  }]));
}

function validSnapshot() {
  return {
    input: {
      supplied: INPUT_SHA,
      authorized: INPUT_SHA,
      head: INPUT_SHA,
      inputIsAncestorOfHead: true,
    },
    remote: {
      tracking: INPUT_SHA,
      live: INPUT_SHA,
      fetched: true,
      branch: 'feature/issue-5-02-web-spike',
    },
    ancestry: {
      required: [...IMMUTABLE_ANCESTORS],
      present: [...IMMUTABLE_ANCESTORS],
    },
    protected: {
      hashes: {
        Makefile: '6b75a7a1f8e516e8967d317edb9de35378c02eddd645d2731dcf5cfc9bf52f54',
        '.gitignore': 'aa93e47707e95286126f47b3d70fe7fc6c047b49c861184533e38b3c5a971316',
        'release-manifest.json': 'f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539',
      },
      discoveryTree: 'ed45ef287be3c0830466ae4a6b60a6bf22b1eb70',
      forbiddenPresent: [],
    },
    paths: {
      changed: ['spikes/web/harness/tests/authority.test.mjs'],
      allowed: ['spikes/web/harness/tests/authority.test.mjs'],
    },
    toolchain: {
      actual: { node: '22.22.3', npm: '10.9.8' },
      frozen: {
        node: '22.22.3', npm: '10.9.8', lockfileVersion: 3,
        packages: {
          astro: '7.1.3', next: '16.2.10', vite: '8.1.5',
          react: '19.2.7', 'react-dom': '19.2.7', playwright: '1.61.1',
        },
      },
    },
    registries: {
      authority: { schema: 'i5-02-authority-v1' },
      modes: {
        astro: 'static-react-island',
        next: 'standalone-app-router',
        vite: 'static-mpa-progressive-react',
      },
      testIds: [...WEB_IDS],
    },
    scoreAnchors: {
      frozenBeforeCandidateWork: true,
      editedAfterFreeze: false,
      categories: anchors(),
    },
    stages: {
      gate0: 'authorized',
      gateA: 'authorized-after-gate0',
      candidates: 'deferred',
      barrierB: 'closed',
      gateC: 'blocked',
      gateD: 'blocked',
      fullIssue: 'incomplete',
    },
    deferred: {
      presentPaths: [],
      makeTargets: MAKE_TARGETS,
    },
  };
}

async function loadChecker(testId) {
  try {
    return await import(CHECKER_URL);
  } catch (error) {
    if (error?.code === 'ERR_MODULE_NOT_FOUND') {
      assert.fail(`${testId}: intentional RED — authority checker/registries are absent`);
    }
    throw error;
  }
}

async function assertSingleFailure(testId, mutate) {
  const { validateAuthoritySnapshot } = await loadChecker(testId);
  assert.equal(typeof validateAuthoritySnapshot, 'function',
    `${testId}: checker must export dependency-free validateAuthoritySnapshot`);

  const snapshot = validSnapshot();
  mutate(snapshot);
  const result = await validateAuthoritySnapshot({
    implementationInput: INPUT_SHA,
    snapshot,
  });

  assert.equal(result?.ok, false, `${testId}: invalid fixture must fail closed`);
  assert.deepEqual(result.failures?.map(({ id }) => id), [testId],
    `${testId}: fixture must fail for its intended control only`);
  assert.match(result.failures[0].reason, /\S/,
    `${testId}: failure must include a useful reason`);
}

test('G0-AUTH-001 rejects a missing or wrong implementation input SHA', async () => {
  await assertSingleFailure('G0-AUTH-001', (snapshot) => {
    snapshot.input.supplied = 'not-a-full-authorized-sha';
  });
});

test('G0-REMOTE-001 rejects unfetched, unknown, or divergent tracking/live state', async () => {
  await assertSingleFailure('G0-REMOTE-001', (snapshot) => {
    snapshot.remote.live = '1111111111111111111111111111111111111111';
  });
});

test('G0-ANCESTRY-001 rejects a missing immutable ancestor', async () => {
  await assertSingleFailure('G0-ANCESTRY-001', (snapshot) => {
    snapshot.ancestry.present.pop();
  });
});

test('G0-PROTECTED-001 rejects protected hash, absence, or discovery-tree drift', async () => {
  await assertSingleFailure('G0-PROTECTED-001', (snapshot) => {
    snapshot.protected.hashes.Makefile = '0'.repeat(64);
  });
});

test('G0-PATH-001 rejects a changed path outside the exact allow-list', async () => {
  await assertSingleFailure('G0-PATH-001', (snapshot) => {
    snapshot.paths.changed.push('Makefile');
  });
});

test('G0-TOOLCHAIN-001 rejects version drift and non-exact frozen policy', async () => {
  await assertSingleFailure('G0-TOOLCHAIN-001', (snapshot) => {
    snapshot.toolchain.frozen.packages.react = '^19.2.7';
  });
});

test('G0-REGISTRY-001 rejects malformed authority/mode/WEB-ID registries', async () => {
  await assertSingleFailure('G0-REGISTRY-001', (snapshot) => {
    snapshot.registries.testIds.push('WEB-CONTRACT-001');
  });
});

test('G0-ANCHOR-001 rejects incomplete or post-observation score anchors', async () => {
  await assertSingleFailure('G0-ANCHOR-001', (snapshot) => {
    delete snapshot.scoreAnchors.categories['authoring-content-schema-mdx'].levels['5'];
  });
});

test('G0-STAGE-001 rejects false stage or full-issue readiness', async () => {
  await assertSingleFailure('G0-STAGE-001', (snapshot) => {
    snapshot.stages.fullIssue = 'complete';
  });
});

test('G0-DEFERRED-001 rejects candidate/later paths or Make targets', async () => {
  await assertSingleFailure('G0-DEFERRED-001', (snapshot) => {
    snapshot.deferred.presentPaths.push('spikes/web/candidates/astro/package.json');
  });
});
