import { createHash } from 'node:crypto';
import { existsSync, readFileSync, realpathSync } from 'node:fs';
import { basename, dirname, delimiter, resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const ROOT = realpathSync(resolve(dirname(fileURLToPath(import.meta.url)), '../../../..'));
const HARNESS = resolve(ROOT, 'spikes/web/harness');
const FULL_SHA = /^[0-9a-f]{40}$/;
const AUTHORIZED_INPUT = '0c73f4712c8ac7902042735ff1da96ef1e5285a3';
const REGISTRY_HASHES = {
  'authority.json': 'c35c4ef5228ef3af9d21f0ad273022723d86b771e44ddf20ec6d78e2326bee0f',
  'toolchain.json': 'da4ac9ddf640c49018403359a5eed4b97a7e20739da6883e9adac1d6a52fb086',
  'candidate-modes.json': '2957c84624ef16d0ebb037ea3fde66d20a0d2dae6d0d049b1e9c4bb7a8ce3181',
  'test-ids.json': 'b1aec72463e4b7219c574a5e6025f68be5e064adab312e35b1a8fe6f9e60b706',
  'score-anchors.json': '56a15b9babf3e354d5df8279929df0c12e61c2e2e58bc90a8364038b424c9a75',
  'stage-status.json': 'a8cbee86a97bec80c539daf32dea7232593eb9dc0b1531a80d7da7af927fbb03',
};

const EXPECTED_WEB_IDS = [
  'WEB-CONTRACT-001', 'WEB-CONTRACT-002', 'WEB-CONTRACT-003',
  'WEB-PREVIEW-001', 'WEB-PREVIEW-002', 'WEB-STATE-001', 'WEB-STATE-002',
  'WEB-FAIL-001', 'WEB-TRUST-001', 'WEB-TRUST-002', 'WEB-A11Y-001',
  'WEB-A11Y-002', 'WEB-A11Y-003', 'WEB-A11Y-004', 'WEB-STATIC-001',
  'WEB-NOSCROLL-001', 'WEB-API-001', 'WEB-E2E-001', 'WEB-NONCOPY-001',
];

const EXPECTED_MODES = {
  astro: 'static-react-island',
  next: 'standalone-app-router',
  vite: 'static-mpa-progressive-react',
};

const EXPECTED_PACKAGES = {
  astro: '7.1.3', next: '16.2.10', vite: '8.1.5', react: '19.2.7',
  'react-dom': '19.2.7', playwright: '1.61.1',
};

const EXPECTED_SCORES = {
  'authoring-content-schema-mdx': 20,
  'accessibility-static-reduced-motion': 20,
  'lab-state-evidence-typed-api': 20,
  'startup-rss-client-js': 15,
  'unit-e2e-visual-evidence': 10,
  'hosted-ecs-evolution-rollback': 10,
  'maintenance-dependency-supply-chain': 5,
};

export const AUTHORIZED_MAKE_TARGETS = [
  'i5-02-authority-check', 'i5-02-protected-hash-check',
  'i5-02-toolchain-check', 'i5-02-changed-path-check',
  'i5-02-security-check', 'i5-02-credential-check', 'i5-02-non-copy-check',
  'web-common-test', 'learn-preview', 'learn-preview-status',
  'learn-preview-reset-check', 'learn-preview-down',
];

const EXPECTED_STAGES = {
  gate0: 'authorized', gateA: 'authorized-after-gate0', candidates: 'deferred',
  barrierB: 'closed', gateC: 'blocked', gateD: 'blocked', fullIssue: 'incomplete',
};

function sameValues(actual, expected) {
  return Array.isArray(actual)
    && actual.length === expected.length
    && actual.every((value, index) => value === expected[index]);
}

function exactObject(actual, expected) {
  return actual && Object.keys(actual).length === Object.keys(expected).length
    && Object.entries(expected).every(([key, value]) => actual[key] === value);
}

function add(failures, id, condition, reason) {
  if (!condition) failures.push({ id, reason });
}

export function validateAuthoritySnapshot({ implementationInput, snapshot }) {
  const failures = [];
  const input = snapshot?.input ?? {};
  add(failures, 'G0-AUTH-001',
    FULL_SHA.test(implementationInput ?? '')
      && implementationInput === input.supplied
      && input.supplied === input.authorized
      && FULL_SHA.test(input.head ?? '')
      && input.inputIsAncestorOfHead === true,
    'implementation input must be the authorized full SHA and an ancestor of HEAD');

  const remote = snapshot?.remote ?? {};
  add(failures, 'G0-REMOTE-001',
    remote.fetched === true
      && remote.branch === 'feature/issue-5-02-web-spike'
      && FULL_SHA.test(remote.tracking ?? '')
      && remote.tracking === remote.live
      && (remote.live === input.authorized || remote.live === input.head),
    'tracking and freshly observed live branch must be known, equal, and authoritative');

  const ancestry = snapshot?.ancestry ?? {};
  add(failures, 'G0-ANCESTRY-001',
    Array.isArray(ancestry.required)
      && ancestry.required.length === 6
      && new Set(ancestry.required).size === 6
      && ancestry.required.every((sha) => ancestry.present?.includes(sha)),
    'every immutable ancestor must be present exactly once in the authority registry');

  const protectedState = snapshot?.protected ?? {};
  add(failures, 'G0-PROTECTED-001',
    protectedState.hashes?.Makefile === '6b75a7a1f8e516e8967d317edb9de35378c02eddd645d2731dcf5cfc9bf52f54'
      && protectedState.hashes?.['.gitignore'] === 'aa93e47707e95286126f47b3d70fe7fc6c047b49c861184533e38b3c5a971316'
      && protectedState.hashes?.['release-manifest.json'] === 'f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539'
      && protectedState.discoveryTree === 'ed45ef287be3c0830466ae4a6b60a6bf22b1eb70'
      && Array.isArray(protectedState.forbiddenPresent)
      && protectedState.forbiddenPresent.length === 0,
    'protected hashes, discovery tree, and required absences must match the audit');

  const paths = snapshot?.paths ?? {};
  add(failures, 'G0-PATH-001',
    Array.isArray(paths.changed) && Array.isArray(paths.allowed)
      && paths.changed.every((path) => paths.allowed.includes(path)),
    'all committed, staged, unstaged, and untracked paths must be audit-allowed');

  const toolchain = snapshot?.toolchain ?? {};
  add(failures, 'G0-TOOLCHAIN-001',
    toolchain.actual?.node === '22.22.3'
      && toolchain.actual?.npm === '10.9.8'
      && toolchain.frozen?.node === '22.22.3'
      && toolchain.frozen?.npm === '10.9.8'
      && toolchain.frozen?.lockfileVersion === 3
      && exactObject(toolchain.frozen?.packages, EXPECTED_PACKAGES)
      && Object.values(toolchain.frozen?.packages ?? {}).every((version) => /^\d+\.\d+\.\d+$/.test(version)),
    'current Node and the exact frozen npm/package policy must match without ranges');

  const registries = snapshot?.registries ?? {};
  const registryValid = registries.authority?.schema === 'i5-02-authority-v1'
    && exactObject(registries.modes, EXPECTED_MODES)
    && sameValues(registries.testIds, EXPECTED_WEB_IDS)
    && new Set(registries.testIds ?? []).size === EXPECTED_WEB_IDS.length;
  add(failures, 'G0-REGISTRY-001',
    registryValid,
    'authority, candidate-mode, and canonical 19 WEB-ID registries must be exact');

  const score = snapshot?.scoreAnchors ?? {};
  const categories = score.categories ?? {};
  const scoreValid = score.frozenBeforeCandidateWork === true
    && score.editedAfterFreeze === false
    && Object.keys(categories).length === 7
    && Object.entries(EXPECTED_SCORES).every(([name, weight]) => {
      const category = categories[name];
      return category?.weight === weight
        && Object.keys(category.levels ?? {}).length === 6
        && Array.from({ length: 6 }, (_, level) => String(level)).every((level) =>
          Array.isArray(category.levels[level]?.predicates)
            && category.levels[level].predicates.length > 0
            && category.levels[level].predicates.every((predicate) =>
              typeof predicate === 'string' && predicate.trim().length > 0));
    });
  add(failures, 'G0-ANCHOR-001', scoreValid,
    'seven pre-observation weighted categories must each define fixed levels 0 through 5');

  const stages = snapshot?.stages ?? {};
  add(failures, 'G0-STAGE-001',
    Object.entries(EXPECTED_STAGES).every(([key, value]) => stages[key] === value)
      && stages.issueComplete !== true && stages.decisionGrade !== true,
    'only Gate 0/A may be authorized; later stages and full issue must remain closed');

  const deferred = snapshot?.deferred ?? {};
  add(failures, 'G0-DEFERRED-001',
    Array.isArray(deferred.presentPaths) && deferred.presentPaths.length === 0
      && sameValues(deferred.makeTargets, AUTHORIZED_MAKE_TARGETS),
    'candidate/later paths must be absent and the Make surface must contain exactly twelve targets');

  return { ok: failures.length === 0, failures };
}

function json(name) {
  return JSON.parse(readFileSync(resolve(HARNESS, name), 'utf8'));
}

function git(args) {
  return execFileSync('git', args, { cwd: ROOT, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).trim();
}

function sha256(path) {
  return createHash('sha256').update(readFileSync(resolve(ROOT, path))).digest('hex');
}

function changedPaths(input) {
  const paths = new Set();
  for (const args of [
    ['diff', '--name-only', `${input}...HEAD`],
    ['diff', '--name-only'],
    ['diff', '--cached', '--name-only'],
  ]) {
    for (const path of git(args).split('\n').filter(Boolean)) paths.add(path);
  }
  const status = git(['status', '--porcelain=v1', '--untracked-files=all']);
  for (const line of status.split('\n').filter(Boolean)) {
    const raw = line.slice(3);
    const path = raw.includes(' -> ') ? raw.split(' -> ').at(-1) : raw;
    paths.add(path.replace(/^"|"$/g, ''));
  }
  return [...paths].sort();
}

function makeTargets() {
  const source = readFileSync(resolve(ROOT, 'mk/issue-5/i5-02.mk'), 'utf8');
  if (/^\s*(?:-?include|sinclude)\b/m.test(source)
      || /^\s*[^#\n:]*%[^\n:]*:/m.test(source)
      || /\$\((?:eval|call|wildcard|MAKE)\b/.test(source)
      || /^\s*(?!\$\(error\b)[^#\n:]*\$\([^\n:]+\)[^\n:]*:/m.test(source)
      || /^\s*(?:gmake|make|\+gmake|\+make)\b/m.test(source)
      || /^\s*[A-Za-z_][A-Za-z0-9_]*\s*[:?+]?=\s*g?make\b/m.test(source)) {
    throw new Error('G0-DEFERRED-001: Make includes, patterns, recursion, or computed dispatch are forbidden');
  }
  return [...source.matchAll(/^([a-zA-Z0-9][a-zA-Z0-9-]*):(?:\s|$)/gm)].map((match) => match[1]);
}

function installedNpmVersion() {
  const executable = (process.env.PATH ?? '').split(delimiter)
    .map((directory) => resolve(directory, 'npm'))
    .find((path) => existsSync(path));
  if (!executable) throw new Error('G0-TOOLCHAIN-001: npm executable is not present on PATH');
  let directory = dirname(realpathSync(executable));
  for (;;) {
    const manifest = resolve(directory, 'package.json');
    if (existsSync(manifest)) {
      const parsed = JSON.parse(readFileSync(manifest, 'utf8'));
      if (parsed.name === 'npm' && typeof parsed.version === 'string') return parsed.version;
    }
    const parent = dirname(directory);
    if (parent === directory) break;
    directory = parent;
  }
  throw new Error('G0-TOOLCHAIN-001: cannot independently read installed npm metadata');
}

function validateWorktreeAuthority(expectedBranch) {
  const records = git(['worktree', 'list', '--porcelain']).split(/\n\n+/).map((record) =>
    Object.fromEntries(record.split('\n').filter(Boolean).map((line) => {
      const separator = line.indexOf(' ');
      return separator === -1 ? [line, true] : [line.slice(0, separator), line.slice(separator + 1)];
    })));
  const primary = records[0]?.worktree ? realpathSync(records[0].worktree) : '';
  const branchRef = `refs/heads/${expectedBranch}`;
  const matches = records.filter((record) => record.branch === branchRef);
  if (basename(ROOT) !== 'ai-ready-data-platform-issue-5-02-web-spike'
      || dirname(primary) !== dirname(ROOT)
      || matches.length !== 1
      || realpathSync(matches[0].worktree) !== ROOT) {
    throw new Error('G0-AUTH-001: exact product worktree path/branch pairing is not unique');
  }
}

function buildSnapshot(implementationInput) {
  for (const [name, digest] of Object.entries(REGISTRY_HASHES)) {
    const actual = createHash('sha256').update(readFileSync(resolve(HARNESS, name))).digest('hex');
    if (actual !== digest) throw new Error(`G0-REGISTRY-001: frozen registry digest mismatch: ${name}`);
  }
  const authority = json('authority.json');
  const toolchain = json('toolchain.json');
  const modes = json('candidate-modes.json');
  const testIds = json('test-ids.json');
  const scoreAnchors = json('score-anchors.json');
  const stages = json('stage-status.json');
  if (toolchain.schema !== 'i5-02-toolchain-v1'
      || toolchain.npmInvocationAllowedDuringGate0A !== false
      || modes.schema !== 'i5-02-candidate-modes-v1' || modes.activation !== 'deferred'
      || testIds.schema !== 'i5-02-test-ids-v1'
      || scoreAnchors.schema !== 'i5-02-score-anchors-v1'
      || stages.schema !== 'i5-02-stage-status-v1') {
    throw new Error('G0-REGISTRY-001: malformed registry schema or activation policy');
  }
  validateWorktreeAuthority(authority.branch);
  const head = git(['rev-parse', 'HEAD']);
  const branch = git(['branch', '--show-current']);
  const tracking = git(['rev-parse', '@{upstream}']);
  const liveLine = git(['ls-remote', '--heads', 'origin', `refs/heads/${authority.branch}`]);
  const live = liveLine.split(/\s+/)[0] ?? '';
  const presentAncestors = authority.requiredAncestors.filter((sha) => {
    try { git(['merge-base', '--is-ancestor', sha, head]); return true; } catch { return false; }
  });
  const forbidden = [
    ...authority.requiredAbsent,
    'spikes/web/candidates',
    'spikes/web/harness/fixture-handoff.json',
    'spikes/web/evidence/retention-index.json',
    'docs/decisions/0005-web-stack.md',
    'docs/decisions/evidence/adr-0005-web-stack-scorecard.md',
    'docs/decisions/evidence/adr-0005-web-stack-scorecard.json',
  ].filter((path) => existsSync(resolve(ROOT, path)));
  const changed = changedPaths(implementationInput);
  const retained = changed.filter((path) => path.startsWith(authority.allowedRetainedPrefix)
    && /^spikes\/web\/evidence\/retained\/gate-a\/[a-zA-Z0-9][a-zA-Z0-9._-]*\/.+/.test(path));
  const transient = changed.filter((path) =>
    /^\.artifacts\/runtime\/i5-02\/learn-preview\/[1-9][0-9]{0,4}\.json$/.test(path)
      || /^\.artifacts\/evidence\/web-spike\/[a-zA-Z0-9][a-zA-Z0-9._-]*\/(?:gate-(?:0|a)|recovery-rerun)\/.+/.test(path));

  let inputIsAncestorOfHead = false;
  try { git(['merge-base', '--is-ancestor', implementationInput, head]); inputIsAncestorOfHead = true; } catch {}

  return {
    input: { supplied: implementationInput, authorized: authority.implementationInputSha, head, inputIsAncestorOfHead },
    remote: { tracking, live, fetched: Boolean(liveLine), branch },
    ancestry: { required: authority.requiredAncestors, present: presentAncestors },
    protected: {
      hashes: Object.fromEntries(Object.keys(authority.protectedHashes).map((path) => [path, sha256(path)])),
      discoveryTree: git(['rev-parse', `HEAD:${authority.discoveryPath}`]),
      forbiddenPresent: forbidden,
    },
    paths: { changed, allowed: [...authority.allowedTrackedPaths, ...retained, ...transient] },
    toolchain: {
      actual: { node: process.versions.node, npm: installedNpmVersion() },
      frozen: { node: toolchain.node, npm: toolchain.npm, lockfileVersion: toolchain.lockfileVersion, packages: toolchain.packages },
    },
    registries: { authority, modes: modes.modes, testIds: testIds.ids },
    scoreAnchors,
    stages,
    deferred: { presentPaths: forbidden.filter((path) => path.startsWith('spikes/web/candidates') || path.includes('fixture-handoff') || path.includes('adr-0005') || path.endsWith('0005-web-stack.md') || path.includes('retention-index')), makeTargets: makeTargets() },
  };
}

function implementationFiles({ includeInvalidFixtures = false } = {}) {
  const authority = json('authority.json');
  const retained = changedPaths(AUTHORIZED_INPUT).filter((path) =>
    path.startsWith(authority.allowedRetainedPrefix)
      && /^spikes\/web\/evidence\/retained\/gate-a\/[a-zA-Z0-9][a-zA-Z0-9._-]*\/.+/.test(path));
  return [...new Set([...authority.allowedTrackedPaths, ...retained])]
    .filter((path) => existsSync(resolve(ROOT, path)))
    .filter((path) => includeInvalidFixtures || !path.includes('/tests/fixtures/'));
}

export function scanCredentialSources(entries) {
  const failures = [];
  const canaryPath = 'spikes/web/common/tests/fixtures/invalid-secret-canary.json';
  const allowedBearer = ['Bearer', 'TEST_SECRET_CANARY_DO_NOT_ACCEPT'].join(' ');
  const allowedPrivatePath = ['', 'Users', 'example', 'private', 'evidence.json'].join('/');
  const credential = /-----BEGIN [A-Z ]*PRIVATE KEY-----|\bAKIA[0-9A-Z]{16}\b|\bASIA[0-9A-Z]{16}\b|\bgh[pousr]_[A-Za-z0-9_]{20,}\b|\bBearer\s+[A-Za-z0-9._~+\/-]{12,}|\b(?:password|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*["'][^"'\n]{8,}["']|https?:\/\/[^\s/:@]+:[^\s/@]+@|(?:^|["'\s])\/Users\/[A-Za-z0-9._-]+\//i;
  for (const entry of entries) {
    let source = entry.source;
    if (entry.path === canaryPath) {
      const bearerCount = source.split(allowedBearer).length - 1;
      const pathCount = source.split(allowedPrivatePath).length - 1;
      if (bearerCount !== 1 || pathCount !== 1) {
        failures.push({ id: 'WEB-API-001', reason: `invalid credential canary policy in ${entry.path}` });
        continue;
      }
      source = source.replace(allowedBearer, '').replace(allowedPrivatePath, '');
    }
    if (credential.test(source)) {
      failures.push({ id: 'WEB-API-001', reason: `credential-like value in ${entry.path}` });
    }
  }
  return failures;
}

function selectorFailures(check) {
  if (!['security', 'credential', 'non-copy'].includes(check)) return [];
  const failures = [];
  const files = implementationFiles();
  if (check === 'security') {
    const required = ['spikes/web/preview/index.html', 'spikes/web/preview/preview.css', 'spikes/web/preview/preview.mjs'];
    if (!required.every((path) => existsSync(resolve(ROOT, path)))) {
      return [{ id: 'WEB-API-001', reason: 'Gate A preview assets are absent; security scan fails closed' }];
    }
    const executable = files.filter((path) => /\.(?:html|mjs|css)$/.test(path)
      && !path.includes('/tests/') && !path.endsWith('/authority-check.mjs'));
    const forbidden = /https?:\/\/|(?:import\s*\(|from\s+|src\s*=\s*|href\s*=\s*)["']\/\/[A-Za-z0-9]|\b0\.0\.0\.0\b|\[::\]|serviceWorker|sourceMappingURL|\beval\s*\(|new\s+Function\b|XMLHttpRequest|WebSocket|EventSource|sendBeacon|Access-Control-Allow-Origin|\bdata:(?:text\/javascript|application\/javascript)|\b(?:POST|PUT|PATCH|DELETE)\s+\/(?:api|mutation)\b/i;
    for (const path of executable) {
      const source = readFileSync(resolve(ROOT, path), 'utf8');
      const fetchCalls = source.match(/\bfetch\s*\(/g) ?? [];
      const exactLoopbackReadinessProbe = path === 'spikes/web/harness/scripts/preview-control.mjs'
        && fetchCalls.length === 1
        && source.includes("fetch(`${LOOPBACK_SCHEME}://${HOST}:${port}/__i5_02_ready`, {\n      redirect: 'error',\n      signal: AbortSignal.timeout(800),\n    })");
      if (forbidden.test(source) || (fetchCalls.length > 0 && !exactLoopbackReadinessProbe)) {
        failures.push({ id: 'WEB-API-001', reason: `forbidden runtime/network capability in ${path}` });
      }
    }
  }
  if (check === 'credential') {
    const credentialEntries = implementationFiles({ includeInvalidFixtures: true })
      .map((path) => ({ path, source: readFileSync(resolve(ROOT, path), 'utf8') }));
    failures.push(...scanCredentialSources(credentialEntries));
  }
  if (check === 'non-copy') {
    const inventory = resolve(ROOT, 'spikes/web/non-copy-inventory.md');
    const preview = resolve(ROOT, 'spikes/web/preview/index.html');
    if (!existsSync(inventory) || !existsSync(preview)) {
      failures.push({ id: 'WEB-NONCOPY-001', reason: 'non-copy inventory or preview is absent; scan fails closed' });
    } else {
      const statement = readFileSync(inventory, 'utf8');
      if (!/(original|project-owned|project owned)/i.test(statement)) {
        failures.push({ id: 'WEB-NONCOPY-001', reason: 'non-copy inventory lacks an original-work declaration' });
      }
      try {
        execFileSync(process.execPath, ['--test', 'spikes/web/common/tests/non-copy.test.mjs'], {
          cwd: ROOT, stdio: ['ignore', 'ignore', 'pipe'],
        });
      } catch {
        failures.push({ id: 'WEB-NONCOPY-001', reason: 'canonical non-copy source comparison failed' });
      }
    }
  }
  return failures;
}

const SELECTORS = new Set([
  'authority', 'protected-hash', 'toolchain', 'changed-path', 'security',
  'credential', 'non-copy',
]);

function parseCli(argv) {
  let implementationInput;
  let check = 'authority';
  for (let index = 0; index < argv.length; index += 2) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (!value || (flag !== '--implementation-input' && flag !== '--check')) {
      throw new Error('usage: authority-check.mjs --implementation-input <sha> [--check <selector>]');
    }
    if (flag === '--implementation-input') implementationInput = value;
    if (flag === '--check') check = value;
  }
  if (!implementationInput || !SELECTORS.has(check)) throw new Error('missing input or unknown exact check selector');
  return { implementationInput, check };
}

async function main() {
  let parsed;
  try {
    parsed = parseCli(process.argv.slice(2));
    if (parsed.implementationInput !== AUTHORIZED_INPUT) {
      process.stdout.write(`${JSON.stringify({
        schema: 'fitness-result-v1', issue: 7, gate: 'gate-0', check: parsed.check,
        resultStatus: 'fail', decisionGrade: false, issueComplete: false,
        opensBarrierB: false,
        failures: [{ id: 'G0-AUTH-001', reason: 'implementation input is not the exact audited SHA' }],
      }, null, 2)}\n`);
      process.exitCode = 1;
      return;
    }
    const result = validateAuthoritySnapshot({
      implementationInput: parsed.implementationInput,
      snapshot: buildSnapshot(parsed.implementationInput),
    });
    result.failures.push(...selectorFailures(parsed.check));
    result.ok = result.failures.length === 0;
    const output = {
      schema: 'fitness-result-v1', issue: 7, gate: 'gate-0', check: parsed.check,
      resultStatus: result.ok ? 'pass' : 'fail', decisionGrade: false,
      issueComplete: false, opensBarrierB: false, failures: result.failures,
    };
    process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
    if (!result.ok) process.exitCode = 1;
  } catch (error) {
    process.stderr.write(`authority check failed closed: ${error.message}\n`);
    process.exitCode = 1;
  }
}

if (process.argv[1] && realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) await main();
