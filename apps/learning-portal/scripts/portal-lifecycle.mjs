import { createHash } from 'node:crypto';
import { execFileSync, spawn } from 'node:child_process';
import { chmod, lstat, mkdir, open, readFile, rm, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import http from 'node:http';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repositoryRoot = resolve(appRoot, '../..');
const artifactsRoot = resolve(repositoryRoot, '.artifacts');
const runtimeParent = resolve(artifactsRoot, 'runtime');
const runtimeRoot = resolve(repositoryRoot, '.artifacts/runtime/i5-05-stage-a');
const controlPath = resolve(runtimeRoot, 'control.json');
const startLockPath = resolve(runtimeRoot, 'start.lock');
const command = process.argv[2];
const commandId = process.argv[3];

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function canonicalize(value) {
  if (value === null || typeof value !== 'object') return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonicalize).join(',')}]`;
  return `{${Object.keys(value)
    .sort()
    .map((key) => `${JSON.stringify(key)}:${canonicalize(value[key])}`)
    .join(',')}}`;
}

async function readControl() {
  const [directoryMetadata, metadata, bytes] = await Promise.all([
    lstat(runtimeRoot),
    lstat(controlPath),
    readFile(controlPath)
  ]);
  if (
    !directoryMetadata.isDirectory() ||
    directoryMetadata.isSymbolicLink() ||
    directoryMetadata.uid !== process.getuid() ||
    (directoryMetadata.mode & 0o777) !== 0o700 ||
    !metadata.isFile() ||
    metadata.isSymbolicLink() ||
    metadata.nlink !== 1 ||
    metadata.uid !== process.getuid() ||
    (metadata.mode & 0o777) !== 0o600 ||
    bytes.length > 2 * 1024 * 1024
  ) throw new Error('PORTAL_CONTROL_RECORD_INVALID');
  const record = JSON.parse(bytes);
  if (
    record.schemaVersion !== 'portal-stage-a-control-v1' ||
    !/^[0-9a-f-]{36}$/.test(record.instanceNonce) ||
    !/^[0-9a-f]{64}$/.test(record.capability) ||
    !Number.isInteger(record.controlPort)
  ) throw new Error('PORTAL_CONTROL_RECORD_INVALID');
  return record;
}

async function ensurePrivateDirectory(path) {
  try {
    await mkdir(path, { mode: 0o700 });
  } catch (error) {
    if (error?.code !== 'EEXIST') throw error;
  }
  const metadata = await lstat(path);
  if (
    !metadata.isDirectory() ||
    metadata.isSymbolicLink() ||
    metadata.uid !== process.getuid() ||
    (metadata.mode & 0o777) !== 0o700
  ) throw new Error('PORTAL_RUNTIME_ROOT_INVALID');
}

async function assertControlAbsent() {
  try {
    await lstat(controlPath);
    throw new Error('PORTAL_ALREADY_RUNNING_OR_STALE');
  } catch (error) {
    if (error?.code !== 'ENOENT') throw error;
  }
}

function requestControl(record, pathname) {
  return new Promise((resolveRequest, reject) => {
    const request = http.request(
      {
        hostname: '127.0.0.1',
        port: record.controlPort,
        path: pathname,
        method: 'POST',
        headers: {
          'content-length': '0',
          'x-portal-instance': record.instanceNonce,
          authorization: `Bearer ${record.capability}`
        }
      },
      (response) => {
        let bytes = '';
        response.setEncoding('utf8');
        response.on('data', (chunk) => {
          bytes += chunk;
        });
        response.on('end', () =>
          resolveRequest({ status: response.statusCode, body: bytes })
        );
      }
    );
    request.on('error', reject);
    request.end();
  });
}

async function start() {
  for (const directory of [artifactsRoot, runtimeParent, runtimeRoot]) {
    await ensurePrivateDirectory(directory);
  }
  let startLock;
  try {
    startLock = await open(startLockPath, 'wx', 0o600);
    await assertControlAbsent();
    const child = spawn(process.execPath, [resolve(appRoot, 'scripts/serve-built-portal.mjs')], {
      cwd: appRoot,
      detached: true,
      stdio: 'ignore',
      env: {
        PATH: process.env.PATH ?? '/usr/bin:/bin',
        PORTAL_LIFECYCLE_CONTROL_PATH: controlPath
      }
    });
    child.unref();
    const deadline = Date.now() + 15_000;
    while (Date.now() < deadline) {
      try {
        const record = await readControl();
        process.stdout.write(
          `${JSON.stringify({
            state: 'running',
            publicPort: record.publicPort,
            semanticReady: false,
            runner: 'unavailable',
            completion: 'disabled'
          })}\n`
        );
        return;
      } catch {
        await new Promise((resolveWait) => setTimeout(resolveWait, 50));
      }
    }
    throw new Error('Portal did not become ready within the bounded window');
  } finally {
    await startLock?.close();
    if (startLock) await rm(startLockPath, { force: true });
  }
}

async function status() {
  const record = await readControl();
  const response = await requestControl(record, '/_control/status');
  if (response.status !== 200) throw new Error('PORTAL_CONTROL_AUTH_FAILED');
  const statusValue = JSON.parse(response.body);
  process.stdout.write(
    `${JSON.stringify({
      state: statusValue.state,
      publicPort: record.publicPort,
      semanticReady: false,
      runner: 'unavailable',
      stageB: 'blocked-on-issue9',
      completion: 'disabled'
    })}\n`
  );
}

async function down() {
  try {
    const record = await readControl();
    const response = await requestControl(record, '/_control/stop');
    if (response.status !== 200) throw new Error('PORTAL_CONTROL_AUTH_FAILED');
    await rm(controlPath, { force: true });
    process.stdout.write(
      `${JSON.stringify({ state: 'stopped', semanticReady: false, evidencePreserved: true })}\n`
    );
  } catch (error) {
    if (error?.code !== 'ENOENT') throw error;
    process.stdout.write(
      `${JSON.stringify({ state: 'already-stopped', semanticReady: false, evidencePreserved: true })}\n`
    );
  }
}

async function blocked(id) {
  if (!['lesson-e2e', 'local-journey-e2e'].includes(id)) {
    throw new Error('Expected one fixed blocked command ID');
  }
  const startedAt = new Date().toISOString();
  const diagnostic = Buffer.from(
    `${JSON.stringify({
      schemaVersion: 'stage-b-blocked-diagnostic-v1',
      commandId: id,
      failureCode: 'STAGE_B_DEPENDENCY_UNAVAILABLE',
      stageB: 'blocked-on-issue9',
      action: 'none'
    })}\n`
  );
  const diagnosticDirectory = resolve(appRoot, '.artifacts/stage-b-blocked');
  const diagnosticPath = resolve(diagnosticDirectory, `${id}.json`);
  await mkdir(diagnosticDirectory, { recursive: true, mode: 0o700 });
  await chmod(diagnosticDirectory, 0o700);
  await writeFile(diagnosticPath, diagnostic, { mode: 0o600 });
  await chmod(diagnosticPath, 0o600);
  const publicArgv =
    id === 'lesson-e2e'
      ? ['make', 'lesson-e2e', 'LESSON=promotion-trust']
      : ['make', 'local-journey-e2e'];
  const canonicalChildArgv = [
    'node',
    'apps/learning-portal/scripts/portal-lifecycle.mjs',
    'blocked',
    id
  ];
  const lockSha256 = sha256(await readFile(resolve(appRoot, 'package-lock.json')));
  const testedTreeSha = execFileSync('git', ['rev-parse', 'HEAD^{tree}'], {
    cwd: repositoryRoot,
    encoding: 'utf8'
  }).trim();
  const result = {
    schemaVersion: 'fitness-result-v2',
    commandId: id,
    owner: 'I5-05',
    requested: {
      subjectType: 'lesson',
      subjectId: 'promotion-trust',
      parameters: []
    },
    status: 'fail',
    failureCode: 'STAGE_B_DEPENDENCY_UNAVAILABLE',
    remediation: 'Issue #9 must publish a reviewed exact runner release before Stage B.',
    inputSha: '0972fa20dc7ec2dd30468fa700946a3e20808e43',
    testedTreeSha,
    dependencyMergeShas: ['5644f01b4c0443a81f3af0bcce80f44c847cd986'],
    contractHashes: [
      { name: 'learning-contract-set-v1', sha256: '92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638' },
      { name: 'promotion-trust-manifest-v1', sha256: '553b97ed5dc44b77564ae50b1a2211205cbd1a759f3578e5e4dfcefef99044ac' }
    ],
    fixtureHashes: [
      { name: 'promotion-trust-small-42-v1', sha256: '0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341' }
    ],
    schemaHashes: [
      { name: 'fitness-result-v2', sha256: 'd53f9b7b68b9f313bf0b9259fe5042bfb8cdbca0001570c18cd937de4971d6c6' }
    ],
    toolchain: [
      { name: 'node', version: process.versions.node },
      { name: 'npm', version: '10.9.8' }
    ],
    lockSha256,
    invocation: {
      publicArgv,
      canonicalChildArgv,
      actualChildArgvSha256: sha256(canonicalize(canonicalChildArgv)),
      cwdRole: 'repository-root'
    },
    startedAt,
    finishedAt: new Date().toISOString(),
    durationMs: 0,
    rawLocator: null,
    projectionLocator: null,
    envelopeLocator: null,
    projectionSha256: null,
    artifacts: [
      {
        locator: `apps/learning-portal/.artifacts/stage-b-blocked/${id}.json`,
        mediaType: 'application/json',
        size: diagnostic.length,
        sha256: sha256(diagnostic)
      }
    ],
    redactionClass: 'public-contract-evidence',
    retentionClass: 'review-bundle',
    rollback: { supported: true, preserveEvidence: true },
    canonicalization: 'RFC8785'
  };
  result.payloadSha256 = sha256(canonicalize(result));
  process.stderr.write(`${JSON.stringify(result)}\n`);
  process.exitCode = 2;
}

if (command === 'start') await start();
else if (command === 'status') await status();
else if (command === 'down') await down();
else if (command === 'blocked') await blocked(commandId);
else throw new Error('Expected one fixed lifecycle command');
