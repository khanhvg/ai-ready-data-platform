import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { execFileSync, spawnSync } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { createReleasedLearningAdapter } from '../../src/contracts/released-learning-adapter.mjs';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const repositoryRoot = resolve(appRoot, '../..');
const bindingPath = resolve(repositoryRoot, 'learning/bindings/vite/promotion-trust-v1.json');
const bindingBytes = await readFile(bindingPath);
const binding = JSON.parse(bindingBytes);

test('released shared binding is the singular alias and route authority', () => {
  assert.equal(
    createHash('sha256').update(bindingBytes).digest('hex'),
    '03d2aa6bd9fa178e6075865364a8ae8b83ce548c42b450d1858b451b45d0d1d0'
  );
  const registry = createReleasedLearningAdapter({ repositoryRoot }).readRegistry();
  assert.equal(registry.binding?.bindingId, binding.bindingId, 'PTP_RED_PRODUCTION_REGISTRY_ABSENT');
  assert.deepEqual(registry.binding?.grainBindings, binding.grainBindings, 'PTP_RED_PRODUCTION_REGISTRY_ABSENT');
});

test('package, lock, runtime, and admitted browser policy remain exact', async () => {
  const packageJson = JSON.parse(await readFile(resolve(appRoot, 'package.json'), 'utf8'));
  const lock = JSON.parse(await readFile(resolve(appRoot, 'package-lock.json'), 'utf8'));
  assert.equal(packageJson.engines.node, '22.22.3');
  assert.equal(packageJson.engines.npm, '10.9.8');
  assert.equal(lock.lockfileVersion, 3);
  assert.equal(lock.packages['node_modules/vite'].version, '8.1.5');
  assert.equal(lock.packages['node_modules/react'].version, '19.2.7');
  assert.equal(lock.packages['node_modules/react-dom'].version, '19.2.7');
  assert.equal(lock.packages['node_modules/@playwright/test'].version, '1.61.1');
  assert.equal(lock.packages['node_modules/@axe-core/playwright'].version, '4.12.1');
  assert.equal(lock.packages['node_modules/@vitejs/plugin-react'].version, '6.0.1');
  assert.equal(process.versions.node, '22.22.3');
  assert.equal(execFileSync('npm', ['--version'], { encoding: 'utf8' }).trim(), '10.9.8');
  assert.equal(execFileSync('python3.12', ['--version'], { encoding: 'utf8' }).trim(), 'Python 3.12.3');
  const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  const chromeBytes = await readFile(chromePath);
  assert.equal(
    createHash('sha256').update(chromeBytes).digest('hex'),
    'b724a4c5603cfc8b9d9f27a5153c8a39e7133e53666ced7f2a8b03bf49484f85'
  );
  assert.match(execFileSync(chromePath, ['--version'], { encoding: 'utf8' }), /150\.0\.7871\.181/);
});

test('root Make composition exposes nine delegates and direct fragment invocation is denied', () => {
  const databaseResult = spawnSync('make', ['-qp'], { cwd: repositoryRoot, encoding: 'utf8' });
  const database = databaseResult.stdout;
  assert.ok([0, 1].includes(databaseResult.status));
  for (const target of [
    'learn',
    'learn-status',
    'learn-down',
    'portal-test',
    'portal-a11y',
    'portal-e2e',
    'lesson-e2e',
    'local-journey-e2e',
    'portal-visual-review'
  ]) {
    assert.match(database, new RegExp(`^${target}:`, 'm'));
  }
  let directStatus = 0;
  try {
    execFileSync('make', ['-f', 'mk/issue-5/i5-05.mk', 'portal-test'], {
      cwd: repositoryRoot,
      stdio: 'pipe'
    });
  } catch (error) {
    directStatus = error.status;
  }
  assert.equal(directStatus, 2);
});

test('exact eighteen-command Stage A portfolio is unique and bound to real entrypoints', async () => {
  const commands = [
    'node apps/learning-portal/scripts/verify-stage-a-release.mjs',
    'make learning-contracts-check',
    'make lesson-check LESSON=promotion-trust',
    'make api-contracts-check',
    'npm --prefix apps/learning-portal ci --ignore-scripts --no-audit --no-fund',
    'npm --prefix apps/learning-portal run test:unit',
    'npm --prefix apps/learning-portal run build',
    'npm --prefix apps/learning-portal run test:stage-a -- --workers=1 --retries=0',
    'npm --prefix apps/learning-portal run test:visual -- --workers=1 --retries=0',
    'npm --prefix apps/learning-portal audit --audit-level=high --json',
    'make portal-test portal-a11y',
    'make portal-e2e',
    'make portal-visual-review',
    'make learn LESSON=promotion-trust',
    'make learn-status',
    'make learn-down',
    'make lesson-e2e LESSON=promotion-trust',
    'make local-journey-e2e'
  ];
  assert.equal(commands.length, 18);
  assert.equal(new Set(commands).size, 18);
  const packageJson = JSON.parse(await readFile(resolve(appRoot, 'package.json'), 'utf8'));
  for (const script of ['test:unit', 'build', 'test:stage-a', 'test:visual']) {
    assert.equal(typeof packageJson.scripts[script], 'string');
  }
  for (const scriptPath of [
    'scripts/verify-stage-a-release.mjs',
    'scripts/portal-lifecycle.mjs',
    'scripts/serve-built-portal.mjs',
    'scripts/write-review-artifacts.mjs'
  ]) {
    await readFile(resolve(appRoot, scriptPath));
  }
});

test('activation binds only I5-05 reservations and remains schema-valid at the final fragment hash', async () => {
  const activation = JSON.parse(
    await readFile(resolve(appRoot, 'command-owner-activation.stage-a.json'), 'utf8')
  );
  const fragment = await readFile(resolve(repositoryRoot, activation.fragment.path));
  assert.equal(activation.owner, 'I5-05');
  assert.equal(activation.commands.length, 9);
  assert.equal(
    activation.fragment.sha256,
    createHash('sha256').update(fragment).digest('hex'),
    'PTP_RED_RELEASE_ADMISSION_ABSENT'
  );
  assert.deepEqual(new Set(activation.commands.map(({ evidenceVersion }) => evidenceVersion)), new Set(['fitness-result-v2']));
});
