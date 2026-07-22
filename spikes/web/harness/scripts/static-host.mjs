import { createServer } from 'node:http';
import { createHash } from 'node:crypto';
import { constants } from 'node:fs';
import { lstat, open, readFile, realpath } from 'node:fs/promises';
import { dirname, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { canonicalJson, FIXTURE_DIGEST } from '../../common/state/preview-state.mjs';

export const HOST = '127.0.0.1';
export const CSP = "default-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'; script-src 'self'; style-src 'self'; img-src 'self'; font-src 'none'; connect-src 'none'; object-src 'none'; worker-src 'none'; manifest-src 'none'";

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const PREVIEW_ROOT = resolve(SCRIPT_DIR, '../../preview');
const FIXTURE_PATH = resolve(SCRIPT_DIR, '../../common/fixtures/synthetic-promotion-trust-v1.json');
const AUDITED_INPUT_SHA = '0c73f4712c8ac7902042735ff1da96ef1e5285a3';
const SECURE_OPEN_FLAGS = constants.O_RDONLY | constants.O_NOFOLLOW;
const ROUTES = new Map([
  ['/', ['index.html', 'text/html; charset=utf-8']],
  ['/index.html', ['index.html', 'text/html; charset=utf-8']],
  ['/preview.css', ['preview.css', 'text/css; charset=utf-8']],
  ['/preview.mjs', ['preview.mjs', 'text/javascript; charset=utf-8']],
]);

export function validateRequestTarget(method, target) {
  if (method !== 'GET') return { ok: false, code: 'METHOD_REJECTED' };
  if (typeof target !== 'string' || (!ROUTES.has(target) && target !== '/__i5_02_ready')) {
    return { ok: false, code: 'ROUTE_REJECTED' };
  }
  return { ok: true };
}

export function validateResolvedAsset({ realRoot, resolvedPath, isSymlink }) {
  if (isSymlink) return { ok: false, code: 'SYMLINK_REJECTED' };
  const child = relative(realRoot, resolvedPath);
  if (child === '' || child === '..' || child.startsWith(`..${sep}`) || resolve(realRoot, child) !== resolvedPath) {
    return { ok: false, code: 'PATH_REJECTED' };
  }
  return { ok: true };
}

export function createReadinessPayload({ lesson, fixtureDigest, runId, implementationInput }) {
  return {
    ready: true,
    lesson,
    fixtureDigest,
    runId,
    implementationInput,
  };
}

export function validateHostAuthority({ lesson, fixtureDigest, runId, implementationInput }) {
  if (lesson !== 'promotion-trust') return { ok: false, code: 'LESSON_REJECTED' };
  if (fixtureDigest !== FIXTURE_DIGEST) return { ok: false, code: 'FIXTURE_DIGEST_MISMATCH' };
  if (implementationInput !== AUDITED_INPUT_SHA) return { ok: false, code: 'IMPLEMENTATION_INPUT_REJECTED' };
  if (typeof runId !== 'string' || !/^gate-a-[a-z0-9-]+$/.test(runId)) return { ok: false, code: 'RUN_ID_REJECTED' };
  return { ok: true };
}

function validateFixtureBytes(bytes) {
  try {
    const fixture = JSON.parse(bytes.toString('utf8'));
    const { fixtureDigest: declared, ...payload } = fixture;
    const actual = `sha256:${createHash('sha256').update(canonicalJson(payload)).digest('hex')}`;
    return declared === FIXTURE_DIGEST && actual === FIXTURE_DIGEST;
  } catch {
    return false;
  }
}

export function validateReadinessPayload(payload, expected) {
  const fields = ['lesson', 'fixtureDigest', 'runId', 'implementationInput'];
  const mismatches = fields.filter((field) => payload?.[field] !== expected?.[field]);
  if (payload?.ready !== true) mismatches.unshift('ready');
  return mismatches.length === 0
    ? { ok: true }
    : { ok: false, code: 'READINESS_MISMATCH', mismatches };
}

function send(response, status, contentType, body) {
  response.writeHead(status, {
    'Content-Type': contentType,
    'Content-Security-Policy': CSP,
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'no-referrer',
  });
  response.end(body);
}

export async function readVerifiedAsset(route, {
  lstatAsset = lstat,
  realpathAsset = realpath,
  openAsset = open,
} = {}) {
  const realRoot = await realpath(PREVIEW_ROOT);
  const entry = ROUTES.get(route);
  if (!entry) return { ok: false, code: 'ROUTE_REJECTED' };
  const [asset, contentType] = entry;
  const assetPath = resolve(realRoot, asset);
  try {
    const info = await lstatAsset(assetPath);
    if (info.isSymbolicLink()) return { ok: false, code: 'SYMLINK_REJECTED' };
    if (!info.isFile()) return { ok: false, code: 'ASSET_REJECTED' };
    const resolvedPath = await realpathAsset(assetPath);
    const pathCheck = validateResolvedAsset({ realRoot, resolvedPath, isSymlink: false });
    if (!pathCheck.ok) return pathCheck;
    const handle = await openAsset(resolvedPath, SECURE_OPEN_FLAGS);
    try {
      const opened = await handle.stat();
      if (!opened.isFile()) return { ok: false, code: 'ASSET_REJECTED' };
      return { ok: true, contentType, bytes: await handle.readFile() };
    } finally {
      await handle.close();
    }
  } catch (error) {
    if (error?.code === 'ELOOP') return { ok: false, code: 'SYMLINK_REJECTED' };
    return { ok: false, code: 'ASSET_MISSING' };
  }
}

export async function createStaticHost(options) {
  const authority = validateHostAuthority(options);
  if (!authority.ok) throw new Error(authority.code);
  if (!validateFixtureBytes(await readFile(FIXTURE_PATH))) throw new Error('FIXTURE_DIGEST_MISMATCH');
  const readiness = createReadinessPayload(options);
  return createServer(async (request, response) => {
    const target = validateRequestTarget(request.method, request.url);
    if (!target.ok) {
      send(response, target.code === 'METHOD_REJECTED' ? 405 : 404, 'text/plain; charset=utf-8', target.code);
      return;
    }
    if (request.url === '/__i5_02_ready') {
      send(response, 200, 'application/json; charset=utf-8', JSON.stringify(readiness));
      return;
    }
    try {
      const asset = await readVerifiedAsset(request.url);
      if (!asset.ok) {
        send(response, 404, 'text/plain; charset=utf-8', asset.code);
        return;
      }
      send(response, 200, asset.contentType, asset.bytes);
    } catch {
      send(response, 404, 'text/plain; charset=utf-8', 'ASSET_MISSING');
    }
  });
}

function parseArgs(values) {
  const result = {};
  for (let index = 0; index < values.length; index += 2) {
    const name = values[index];
    if (!name?.startsWith('--') || values[index + 1] === undefined) throw new Error('INVALID_ARGUMENTS');
    result[name.slice(2)] = values[index + 1];
  }
  return result;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const port = Number(args.port);
  if (!Number.isInteger(port) || port < 1 || port > 65535) throw new Error('INVALID_PORT');
  const authority = validateHostAuthority({
    lesson: args.lesson,
    fixtureDigest: args['fixture-digest'],
    runId: args['run-id'],
    implementationInput: args['implementation-input'],
  });
  if (!authority.ok) throw new Error(authority.code);
  const server = await createStaticHost({
    lesson: args.lesson,
    fixtureDigest: args['fixture-digest'],
    runId: args['run-id'],
    implementationInput: args['implementation-input'],
  });
  server.on('error', (error) => {
    process.stderr.write(`${error.code === 'EADDRINUSE' ? 'PORT_OCCUPIED' : 'HOST_ERROR'}\n`);
    process.exitCode = 1;
  });
  server.listen(port, HOST);
  const close = () => server.close(() => process.exit(0));
  process.on('SIGINT', close);
  process.on('SIGTERM', close);
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  });
}
