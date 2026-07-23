import { mkdir, readFile, rm } from 'node:fs/promises';
import { spawn } from 'node:child_process';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import http from 'node:http';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repositoryRoot = resolve(appRoot, '../..');
const runtimeRoot = resolve(repositoryRoot, '.artifacts/runtime/i5-05-stage-a');
const controlPath = resolve(runtimeRoot, 'scaffold-control.json');
const command = process.argv[2];

async function readControl() {
  return JSON.parse(await readFile(controlPath, 'utf8'));
}

function requestControl(record, pathname) {
  return new Promise((resolveRequest, reject) => {
    const request = http.request(
      {
        hostname: '127.0.0.1',
        port: record.controlPort,
        path: pathname,
        method: 'POST',
        headers: { 'content-length': '0' }
      },
      (response) => {
        let bytes = '';
        response.setEncoding('utf8');
        response.on('data', (chunk) => {
          bytes += chunk;
        });
        response.on('end', () => resolveRequest({ status: response.statusCode, body: bytes }));
      }
    );
    request.on('error', reject);
    request.end();
  });
}

async function start() {
  await mkdir(runtimeRoot, { recursive: true, mode: 0o700 });
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
  const deadline = Date.now() + 5_000;
  while (Date.now() < deadline) {
    try {
      const record = await readControl();
      process.stdout.write(`${JSON.stringify(record)}\n`);
      process.exitCode = record.semanticReady ? 0 : 1;
      return;
    } catch {
      await new Promise((resolveWait) => setTimeout(resolveWait, 50));
    }
  }
  throw new Error('Portal scaffold did not become ready within the bounded window');
}

async function status() {
  const record = await readControl();
  const response = await requestControl(record, '/_control/status');
  process.stdout.write(`${response.body}\n`);
  process.exitCode = record.semanticReady ? 0 : 1;
}

async function down() {
  try {
    const record = await readControl();
    const response = await requestControl(record, '/_control/stop');
    process.stdout.write(`${response.body}\n`);
    process.exitCode = record.semanticReady ? 0 : 1;
  } catch (error) {
    await rm(controlPath, { force: true });
    process.stdout.write(`${JSON.stringify({ state: 'already-stopped', semanticReady: false })}\n`);
    process.exitCode = 1;
  }
}

function blocked() {
  const result = {
    schemaVersion: 'scaffold-blocked-result',
    status: 'blocked',
    code: 'STAGE_B_DEPENDENCY_UNAVAILABLE',
    semanticReady: false
  };
  process.stderr.write(`${JSON.stringify(result)}\n`);
  process.exitCode = 2;
}

if (command === 'start') await start();
else if (command === 'status') await status();
else if (command === 'down') await down();
else if (command === 'blocked') blocked();
else throw new Error('Expected one fixed lifecycle command');
