import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { chmod, lstat, mkdir, mkdtemp, open, readFile, readdir, rm } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createReleasedLearningAdapter } from '../src/contracts/released-learning-adapter.mjs';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repositoryRoot = resolve(appRoot, '../..');
const cookInputSha = '0972fa20dc7ec2dd30468fa700946a3e20808e43';
const releasedIntegrationSha = '5644f01b4c0443a81f3af0bcce80f44c847cd986';
const releasedIntegrationTree = 'a38594d420fe7df2b30265a8a72bb5fad1698012';
const expectedNode = '22.22.3';
const expectedNpm = '10.9.8';
const expectedChrome = '150.0.7871.181';
const expectedChromeSha256 = 'b724a4c5603cfc8b9d9f27a5153c8a39e7133e53666ced7f2a8b03bf49484f85';
const expectedPythonFreezeSha256 =
  'cdb87ed71e0996f90041371cc25138afa02d78b134cbdc4afe9c25baa6649bba';
const expectedRuntimeMarker = Object.freeze({
  inputSha: 'abcaa2de7247d99c642fcad1535c24870f08c79f',
  lockSha256: 'f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2',
  planSha256: '5ab9e91b888ab9fdfc20a59497fd7796f24d0ea19cc66ed794a9ad095fcac3fa',
  schemaVersion: 'learning-runtime-admission-v1',
  toolSha256: '6a8aaa88c4d38b85c8a889779be900d1d99d95f7bbca3977a03a3a4f2642808d'
});
const releasedInputPaths = Object.freeze([
  'docs/decisions/0005-web-stack.md',
  'docs/decisions/evidence/adr-0005-web-stack-scorecard.json',
  'spikes/web/harness/simple-vite-v3.json',
  'spikes/web/harness/toolchain.json',
  'spikes/web/candidates/vite/package.json',
  'spikes/web/candidates/vite/package-lock.json',
  'spikes/web/candidates/vite/playwright.config.mjs',
  'spikes/web/candidates/vite/vite.config.mjs',
  'spikes/web/candidates/vite/index.html',
  'spikes/web/candidates/vite/src/fixture.mjs',
  'spikes/web/candidates/vite/src/lesson-contract.mjs',
  'spikes/web/candidates/vite/src/main.jsx',
  'spikes/web/candidates/vite/src/styles.css',
  'spikes/web/candidates/vite/tests/foundation.test.mjs',
  'spikes/web/candidates/vite/tests/promotion-trust-contract.test.mjs',
  'spikes/web/candidates/vite/tests/simple-vite-smoke.spec.mjs',
  'contracts/openapi/learning-platform-openapi-profile-v1.schema.json',
  'contracts/openapi/learning-platform-problem-details-v1.schema.json',
  'contracts/openapi/learning-platform-v1.yaml',
  'learning/contracts/command-owner-activation-i5-03-v1.json',
  'learning/contracts/completion-reconciliation-v1.json',
  'learning/contracts/completion-reconciliation-v1.schema.json',
  'learning/contracts/fitness-result-v2.schema.json',
  'learning/contracts/lab-v1.schema.json',
  'learning/contracts/learning-contract-set-v1.json',
  'learning/contracts/learning-contract-set-v1.schema.json',
  'learning/contracts/learning-contract-version-registry-v1.json',
  'learning/contracts/learning-contract-version-registry-v1.schema.json',
  'learning/contracts/learning-evidence-v1.schema.json',
  'learning/contracts/lesson-v1.schema.json',
  'learning/contracts/operation-matrix-v1.json',
  'learning/contracts/operation-matrix-v1.schema.json',
  'learning/contracts/progress-v1.schema.json',
  'learning/contracts/promotion-trust-learning-manifest-v1.schema.json',
  'learning/contracts/canonicalization-v1.json',
  'learning/contracts/command-owner-activation-v1.schema.json',
  'learning/contracts/evidence-envelope-v1.schema.json',
  'learning/contracts/fitness-result-v1.schema.json',
  'learning/contracts/golden-evidence-v1.schema.json',
  'learning/contracts/make-input-contract-v1.json',
  'learning/contracts/promotion-trust-evidence-v1.schema.json',
  'learning/contracts/promotion-trust-fixture-manifest-v1.schema.json',
  'learning/contracts/promotion-trust-fixture-manifest-v2.schema.json',
  'learning/contracts/promotion-trust-portable-run-attestation-v1.schema.json',
  'learning/contracts/promotion-trust-v1.schema.json',
  'learning/contracts/retail-golden-v1.schema.json',
  'learning/contracts/schema-version-registry.json',
  'learning/labs/promotion-trust/lab-v1.json',
  'learning/lessons/promotion-trust/lesson-v1.json',
  'learning/manifests/promotion-trust-v1.json',
  'scripts/learning_contracts/__init__.py',
  'scripts/learning_contracts/canonical.py',
  'scripts/learning_contracts/check.py',
  'scripts/learning_contracts/completion.py',
  'scripts/learning_contracts/evidence.py',
  'scripts/learning_contracts/fitness.py',
  'scripts/learning_contracts/guidance.py',
  'scripts/learning_contracts/openapi.py',
  'scripts/learning_contracts/references.py',
  'scripts/learning_contracts/registry.py',
  'scripts/learning_contracts/runtime.py',
  'scripts/learning_contracts/schema.py',
  'scripts/learning_contracts/state.py',
  'Makefile',
  'learning/contracts/command-owner-registry-v1.json',
  'mk/issue-5/i5-03.mk',
  'contracts/data/retail-golden-v1.json',
  'contracts/data/promotion-trust-v1.yaml',
  'tests/fixtures/learning/promotion-trust/evidence-v1.json',
  'tests/fixtures/learning/promotion-trust/manifest.json',
  'release-manifest.json',
  'requirements/golden-py312-macos-arm64.lock',
  'plans/260721-008-version-learning-contracts/phase-05-stage-a-compatibility-release-and-staged-handoff.md',
  'learning/bindings/vite/promotion-trust-v1.json',
  'learning/contracts/promotion-trust-vite-binding-v1.schema.json',
  'scripts/learning_contracts/vite_binding.py',
  'tests/contracts/learning/test_vite_consumer_binding.py',
  'tests/fixtures/learning/bindings/vite/invalid/absolute-path.json',
  'tests/fixtures/learning/bindings/vite/invalid/completion-authority-override.json',
  'tests/fixtures/learning/bindings/vite/invalid/contract-key-drift.json',
  'tests/fixtures/learning/bindings/vite/invalid/dependency-hash-drift.json',
  'tests/fixtures/learning/bindings/vite/invalid/duplicate-target-key.json',
  'tests/fixtures/learning/bindings/vite/invalid/fixture-key-drift.json',
  'tests/fixtures/learning/bindings/vite/invalid/grain-id-drift.json',
  'tests/fixtures/learning/bindings/vite/invalid/raw-record-leak.json'
]);

function git(...args) {
  return execFileSync('git', args, { cwd: repositoryRoot });
}

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function assertCondition(condition, code) {
  if (!condition) throw new Error(code);
}

async function ensureReleasedPythonRuntime() {
  const artifactsRoot = resolve(repositoryRoot, '.artifacts');
  const workspacesRoot = resolve(artifactsRoot, 'workspaces');
  const runtimeRoot = resolve(repositoryRoot, '.artifacts/workspaces/golden');
  for (const directory of [artifactsRoot, workspacesRoot, runtimeRoot]) {
    try {
      await mkdir(directory, { mode: 0o700 });
    } catch (error) {
      if (error?.code !== 'EEXIST') throw error;
    }
    const metadata = await lstat(directory);
    assertCondition(
      metadata.isDirectory() &&
        !metadata.isSymbolicLink() &&
        metadata.uid === process.getuid() &&
        (metadata.mode & 0o777) === 0o700,
      'PORTAL_RUNTIME_IDENTITY_MISMATCH'
    );
  }
  const admissionLockPath = resolve(runtimeRoot, '.portal-stage-a-admission.lock');
  let admissionLock;
  const admissionDeadline = Date.now() + 120_000;
  while (!admissionLock && Date.now() < admissionDeadline) {
    try {
      admissionLock = await open(admissionLockPath, 'wx', 0o600);
    } catch (error) {
      if (error?.code !== 'EEXIST') throw error;
      await new Promise((resolveWait) => setTimeout(resolveWait, 50));
    }
  }
  assertCondition(Boolean(admissionLock), 'PORTAL_RUNTIME_ADMISSION_LOCKED');
  try {
  const measureEnvironment = (interpreter) => {
    execFileSync(interpreter, ['-m', 'pip', 'check'], {
      cwd: repositoryRoot,
      stdio: 'pipe',
      timeout: 120_000
    });
    const freezeLines = execFileSync(interpreter, ['-m', 'pip', 'freeze', '--all'], {
      cwd: repositoryRoot,
      encoding: 'utf8',
      timeout: 120_000
    })
      .trim()
      .split('\n')
      .filter(Boolean)
      .sort();
    return sha256(`${freezeLines.join('\n')}\n`);
  };
  for (const name of await readdir(runtimeRoot)) {
    try {
      const candidate = resolve(runtimeRoot, name);
      const markerPath = resolve(candidate, 'runtime-admission.json');
      const [candidateMetadata, markerMetadata] = await Promise.all([
        lstat(candidate),
        lstat(markerPath)
      ]);
      assertCondition(
        candidateMetadata.isDirectory() &&
          !candidateMetadata.isSymbolicLink() &&
          candidateMetadata.uid === process.getuid() &&
          (candidateMetadata.mode & 0o777) === 0o700 &&
          markerMetadata.isFile() &&
          !markerMetadata.isSymbolicLink() &&
          markerMetadata.nlink === 1 &&
          markerMetadata.uid === process.getuid() &&
          markerMetadata.size <= 2 * 1024 * 1024,
        'PORTAL_RUNTIME_IDENTITY_MISMATCH'
      );
      const marker = JSON.parse(await readFile(markerPath, 'utf8'));
      const interpreter = resolve(candidate, 'venv/bin/python');
      const interpreterBytes = await readFile(interpreter);
      const markerIdentityMatches =
        Object.entries(expectedRuntimeMarker).every(([key, value]) => marker[key] === value) &&
        Object.keys(marker).sort().join('\n') ===
          [...Object.keys(expectedRuntimeMarker), 'interpreterSha256'].sort().join('\n');
      const freezeSha256 = measureEnvironment(interpreter);
      if (
        markerIdentityMatches &&
        sha256(interpreterBytes) === marker.interpreterSha256 &&
        freezeSha256 === expectedPythonFreezeSha256
      ) {
        return {
          runtimeRoot,
          interpreterSha256: marker.interpreterSha256,
          freezeSha256
        };
      }
    } catch {
      // Only a complete hash-bound admission marker is reusable.
    }
  }
  const candidate = await mkdtemp(resolve(runtimeRoot, 'portal-stage-a-'));
  await chmod(candidate, 0o700);
  const interpreter = resolve(candidate, 'venv/bin/python');
  execFileSync('python3.12', ['-m', 'venv', resolve(candidate, 'venv')], {
    cwd: repositoryRoot,
    stdio: 'pipe',
    timeout: 120_000
  });
  execFileSync(
    interpreter,
    [
      '-m',
      'pip',
      'install',
      '--require-hashes',
      '--only-binary=:all:',
      '--no-cache-dir',
      '--index-url',
      'https://pypi.org/simple',
      '-r',
      resolve(repositoryRoot, 'requirements/golden-py312-macos-arm64.lock')
    ],
    {
      cwd: repositoryRoot,
      stdio: 'pipe',
      timeout: 300_000,
      env: { PATH: process.env.PATH ?? '/usr/bin:/bin', LANG: 'C.UTF-8', LC_ALL: 'C.UTF-8' }
    }
  );
  const freezeSha256 = measureEnvironment(interpreter);
  assertCondition(freezeSha256 === expectedPythonFreezeSha256, 'PORTAL_RUNTIME_IDENTITY_MISMATCH');
  const interpreterSha256 = sha256(await readFile(interpreter));
  execFileSync(
    'make',
    [
      'learning-runtime-admit',
      `LEARNING_RUNTIME_ROOT=${runtimeRoot}`,
      `LEARNING_RUNTIME_CANDIDATE=${candidate}`,
      `LEARNING_RUNTIME_INTERPRETER_SHA256=${interpreterSha256}`
    ],
    { cwd: repositoryRoot, stdio: 'pipe', timeout: 120_000 }
  );
  const marker = JSON.parse(
    await readFile(resolve(candidate, 'runtime-admission.json'), 'utf8')
  );
  assertCondition(
    Object.entries(expectedRuntimeMarker).every(([key, value]) => marker[key] === value) &&
      marker.interpreterSha256 === interpreterSha256,
    'PORTAL_RUNTIME_IDENTITY_MISMATCH'
  );
  assertCondition(
    measureEnvironment(interpreter) === expectedPythonFreezeSha256,
    'PORTAL_RUNTIME_IDENTITY_MISMATCH'
  );
  return { runtimeRoot, interpreterSha256, freezeSha256 };
  } finally {
    await admissionLock.close();
    await rm(admissionLockPath, { force: true });
  }
}

const sourceHead = git('rev-parse', 'HEAD').toString('utf8').trim();
const sourceTree = git('rev-parse', 'HEAD^{tree}').toString('utf8').trim();
git('merge-base', '--is-ancestor', cookInputSha, sourceHead);
assertCondition(
  git('rev-parse', `${releasedIntegrationSha}^{tree}`).toString('utf8').trim() ===
    releasedIntegrationTree,
  'PORTAL_RELEASE_IDENTITY_MISMATCH'
);
assertCondition(
  releasedInputPaths.length === 85 && new Set(releasedInputPaths).size === 85,
  'PORTAL_RELEASE_IDENTITY_MISMATCH'
);

const releasedRows = [];
for (const path of releasedInputPaths) {
  const workingBytes = await readFile(resolve(repositoryRoot, path));
  const releasedBytes = git('show', `${releasedIntegrationSha}:${path}`);
  assertCondition(workingBytes.equals(releasedBytes), 'PORTAL_RELEASE_IDENTITY_MISMATCH');
  releasedRows.push({
    path,
    bytes: workingBytes.length,
    sha256: sha256(workingBytes)
  });
}

const packageLock = JSON.parse(await readFile(resolve(appRoot, 'package-lock.json'), 'utf8'));
const releasedLock = JSON.parse(
  await readFile(resolve(repositoryRoot, 'spikes/web/candidates/vite/package-lock.json'), 'utf8')
);
const dependencyGraph = (lock) =>
  Object.fromEntries(Object.entries(lock.packages).filter(([path]) => path !== ''));
assertCondition(
  JSON.stringify(dependencyGraph(packageLock)) === JSON.stringify(dependencyGraph(releasedLock)),
  'PORTAL_LOCK_GRAPH_MISMATCH'
);
assertCondition(packageLock.lockfileVersion === 3, 'PORTAL_LOCK_GRAPH_MISMATCH');
assertCondition(process.versions.node === expectedNode, 'PORTAL_RUNTIME_IDENTITY_MISMATCH');
assertCondition(
  execFileSync('npm', ['--version'], { encoding: 'utf8' }).trim() === expectedNpm,
  'PORTAL_RUNTIME_IDENTITY_MISMATCH'
);
assertCondition(
  execFileSync('python3.12', ['--version'], { encoding: 'utf8' }).trim() === 'Python 3.12.3',
  'PORTAL_RUNTIME_IDENTITY_MISMATCH'
);

const pythonRuntime = await ensureReleasedPythonRuntime();
for (const [target, ...argumentsForTarget] of [
  ['learning-contracts-check'],
  ['lesson-check', 'LESSON=promotion-trust'],
  ['api-contracts-check']
]) {
  execFileSync(
    'make',
    [
      target,
      ...argumentsForTarget,
      `LEARNING_RUNTIME_ROOT=${pythonRuntime.runtimeRoot}`,
      `LEARNING_RUNTIME_INTERPRETER_SHA256=${pythonRuntime.interpreterSha256}`
    ],
    {
    cwd: repositoryRoot,
    stdio: 'pipe',
    env: {
      PATH: process.env.PATH ?? '/usr/bin:/bin',
      LANG: 'C.UTF-8',
      LC_ALL: 'C.UTF-8'
    },
      timeout: 120_000
    }
  );
}

const registry = createReleasedLearningAdapter({ repositoryRoot }).readRegistry();
assertCondition(
  registry.source.releasedInputCount === releasedInputPaths.length,
  'PORTAL_RELEASE_IDENTITY_MISMATCH'
);
const release = {
  inputSha: cookInputSha,
  releasedIntegrationSha,
  releasedIntegrationTree,
  sourceHead,
  sourceTree,
  inputIsAncestor: true,
  node: process.versions.node,
  lockSha256: sha256(await readFile(resolve(appRoot, 'package-lock.json'))),
  expectedNode,
  expectedNpm,
  expectedChrome,
  expectedChromeSha256,
  pythonRuntimeRoot: '.artifacts/workspaces/golden',
  pythonInterpreterSha256: pythonRuntime.interpreterSha256,
  pythonFreezeSha256: pythonRuntime.freezeSha256,
  releasedInputsAdmitted: releasedRows.length,
  releasedInputsRequired: releasedInputPaths.length,
  releasedInputAggregateSha256: sha256(
    `${releasedRows.map((row) => `${row.path}\t${row.bytes}\t${row.sha256}`).join('\n')}\n`
  ),
  validatorsInvoked: registry.source.validatorsInvoked,
  identityReady: true,
  semanticReady: true
};
process.stdout.write(`${JSON.stringify(release)}\n`);

if (process.argv[2] === '--build') {
  const distRoot = resolve(appRoot, 'dist');
  assertCondition(dirname(distRoot) === appRoot, 'PORTAL_BUILD_ROOT_INVALID');
  const validateDistRoot = async (required) => {
    const metadata = await lstat(distRoot).catch((error) => {
      if (!required && error?.code === 'ENOENT') return undefined;
      throw error;
    });
    if (!metadata) return;
    assertCondition(
      metadata.isDirectory() &&
        !metadata.isSymbolicLink() &&
        metadata.uid === process.getuid(),
      'PORTAL_BUILD_ROOT_INVALID'
    );
  };
  await validateDistRoot(false);
  const buildLockPath = resolve(pythonRuntime.runtimeRoot, '.portal-stage-a-build.lock');
  let buildLock;
  const buildDeadline = Date.now() + 120_000;
  while (!buildLock && Date.now() < buildDeadline) {
    try {
      buildLock = await open(buildLockPath, 'wx', 0o600);
    } catch (error) {
      if (error?.code !== 'EEXIST') throw error;
      await new Promise((resolveWait) => setTimeout(resolveWait, 50));
    }
  }
  assertCondition(Boolean(buildLock), 'PORTAL_BUILD_LOCKED');
  try {
    execFileSync(resolve(appRoot, 'node_modules/.bin/vite'), ['build'], {
      cwd: appRoot,
      stdio: 'inherit',
      timeout: 120_000,
      env: { PATH: process.env.PATH ?? '/usr/bin:/bin' }
    });
    execFileSync(process.execPath, [resolve(appRoot, 'scripts/generate-static-routes.mjs')], {
      cwd: appRoot,
      stdio: 'inherit',
      timeout: 120_000,
      env: { PATH: process.env.PATH ?? '/usr/bin:/bin' }
    });
    await validateDistRoot(true);
  } finally {
    await buildLock.close();
    await rm(buildLockPath, { force: true });
  }
} else if (process.argv.length > 2) {
  throw new Error('PORTAL_VERIFY_ARGUMENT_INVALID');
}
