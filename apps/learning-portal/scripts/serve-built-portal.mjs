import { createHash, randomBytes, randomUUID, timingSafeEqual } from 'node:crypto';
import { createServer } from 'node:http';
import { chmod, lstat, readdir, readFile, rename, rm, stat, writeFile } from 'node:fs/promises';
import { dirname, extname, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const distRoot = resolve(appRoot, 'dist');
const lifecycleControlPath = process.env.PORTAL_LIFECYCLE_CONTROL_PATH;
const fixedTestPort = process.env.PORTAL_FIXED_TEST_PORT
  ? Number.parseInt(process.env.PORTAL_FIXED_TEST_PORT, 10)
  : 0;
const semanticReady = true;
const capability = randomBytes(32).toString('hex');
const instanceNonce = randomUUID();
const MAX_FILES = 128;
const MAX_FILE_BYTES = 1024 * 1024;
const MAX_TOTAL_BYTES = 16 * 1024 * 1024;

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function contentType(pathname) {
  return new Map([
    ['.html', 'text/html; charset=utf-8'],
    ['.js', 'text/javascript; charset=utf-8'],
    ['.css', 'text/css; charset=utf-8'],
    ['.json', 'application/json; charset=utf-8'],
    ['.svg', 'image/svg+xml']
  ]).get(extname(pathname)) ?? 'application/octet-stream';
}

async function buildInventory() {
  const rows = [];
  async function walk(directory) {
    for (const entry of await readdir(directory, { withFileTypes: true })) {
      const path = resolve(directory, entry.name);
      if (entry.isDirectory()) {
        await walk(path);
        continue;
      }
      const metadata = await stat(path, { bigint: false });
      if (
        !entry.isFile() ||
        !metadata.isFile() ||
        metadata.nlink !== 1 ||
        (metadata.mode & 0o111) !== 0 ||
        metadata.size > MAX_FILE_BYTES ||
        path.endsWith('.map')
      ) throw new Error('PORTAL_BUILD_INVENTORY_INVALID');
      const bytes = await readFile(path);
      rows.push({
        relativePath: relative(distRoot, path).split(sep).join('/'),
        path,
        content: bytes,
        bytes: bytes.length,
        sha256: sha256(bytes),
        mediaType: contentType(path)
      });
    }
  }
  await walk(distRoot);
  if (
    rows.length === 0 ||
    rows.length > MAX_FILES ||
    rows.reduce((sum, row) => sum + row.bytes, 0) > MAX_TOTAL_BYTES
  ) throw new Error('PORTAL_BUILD_INVENTORY_INVALID');
  return new Map(rows.map((row) => [row.relativePath, Object.freeze(row)]));
}

function resolveInventoryKey(rawTarget) {
  if (
    typeof rawTarget !== 'string' ||
    rawTarget.length === 0 ||
    rawTarget.length > 2048 ||
    rawTarget.includes('\\') ||
    rawTarget.includes('%') ||
    rawTarget.includes('\0') ||
    rawTarget.includes('//')
  ) return undefined;
  const queryIndex = rawTarget.indexOf('?');
  const pathname = queryIndex === -1 ? rawTarget : rawTarget.slice(0, queryIndex);
  if (pathname.split('/').some((part) => part === '.' || part === '..')) return undefined;
  const relativePath = pathname === '/' ? 'index.html' : pathname.replace(/^\/+/, '');
  return relativePath.endsWith('/') ? `${relativePath}index.html` : relativePath;
}

function authenticated(request) {
  const suppliedNonce = request.headers['x-portal-instance'];
  const authorization = request.headers.authorization;
  if (
    typeof suppliedNonce !== 'string' ||
    suppliedNonce !== instanceNonce ||
    typeof authorization !== 'string' ||
    !authorization.startsWith('Bearer ')
  ) return false;
  const supplied = Buffer.from(authorization.slice(7));
  const expected = Buffer.from(capability);
  return supplied.length === expected.length && timingSafeEqual(supplied, expected);
}

const inventory = await buildInventory();
const publicServer = createServer(async (request, response) => {
  const host = request.headers.host;
  const boundPort = publicServer.address()?.port;
  if (!Number.isInteger(boundPort) || host !== `127.0.0.1:${boundPort}`) {
    response.writeHead(400).end();
    return;
  }
  if (
    (request.headers['content-length'] !== undefined &&
      request.headers['content-length'] !== '0') ||
    request.headers['transfer-encoding'] !== undefined
  ) {
    response.writeHead(400).end();
    return;
  }
  if (!['GET', 'HEAD'].includes(request.method ?? '')) {
    response.writeHead(405).end();
    return;
  }
  const key = resolveInventoryKey(request.url ?? '/');
  if (!key) {
    response.writeHead(400).end();
    return;
  }
  const row = inventory.get(key) ?? inventory.get(`${key}/index.html`);
  if (!row) {
    response.writeHead(404).end();
    return;
  }
  try {
    const bytes = row.content;
    if (bytes.length !== row.bytes || sha256(bytes) !== row.sha256) {
      response.writeHead(409).end();
      return;
    }
    response.writeHead(200, {
      'content-type': row.mediaType,
      'content-length': bytes.length,
      'content-security-policy': "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'none'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'; worker-src 'none'",
      'x-content-type-options': 'nosniff',
      'referrer-policy': 'no-referrer',
      'cross-origin-opener-policy': 'same-origin',
      'permissions-policy': 'camera=(), microphone=(), geolocation=(), payment=(), usb=()',
      'cache-control': 'no-store'
    });
    response.end(request.method === 'HEAD' ? undefined : bytes);
  } catch {
    response.writeHead(404).end();
  }
});

const controlServer = createServer((request, response) => {
  if (request.method !== 'POST' || request.headers['content-length'] !== '0') {
    response.writeHead(400).end();
    return;
  }
  if (!authenticated(request)) {
    response.writeHead(403).end();
    return;
  }
  if (request.url === '/_control/status') {
    const bytes = JSON.stringify({ state: 'running', semanticReady, instanceNonce });
    response.writeHead(200, { 'content-type': 'application/json', 'content-length': Buffer.byteLength(bytes) }).end(bytes);
    return;
  }
  if (request.url === '/_control/stop') {
    const bytes = JSON.stringify({ state: 'stopping', semanticReady, instanceNonce });
    response
      .writeHead(200, {
        'content-type': 'application/json',
        'content-length': Buffer.byteLength(bytes)
      })
      .end(bytes, () => {
        void shutdown().catch(() => {
          process.exitCode = 1;
        });
      });
    return;
  }
  response.writeHead(404).end();
});

await new Promise((resolveListen) => publicServer.listen(fixedTestPort, '127.0.0.1', resolveListen));
await new Promise((resolveListen) => controlServer.listen(0, '127.0.0.1', resolveListen));

let shutdownPromise;
function closeServer(server) {
  return new Promise((resolveClose, reject) => {
    if (!server.listening) {
      resolveClose();
      return;
    }
    server.close((error) => {
      if (error) reject(error);
      else resolveClose();
    });
  });
}

function shutdown() {
  shutdownPromise ??= (async () => {
    await Promise.all([closeServer(publicServer), closeServer(controlServer)]);
    if (lifecycleControlPath) await rm(lifecycleControlPath, { force: true });
  })();
  return shutdownPromise;
}

const record = {
  schemaVersion: 'portal-stage-a-control-v1',
  instanceNonce,
  capability,
  publicPort: publicServer.address().port,
  controlPort: controlServer.address().port,
  semanticReady,
  executableDigest: sha256(await readFile(process.execPath))
};

if (lifecycleControlPath) {
  const controlDirectory = dirname(lifecycleControlPath);
  const directoryMetadata = await lstat(controlDirectory);
  if (
    !directoryMetadata.isDirectory() ||
    directoryMetadata.isSymbolicLink() ||
    directoryMetadata.uid !== process.getuid() ||
    (directoryMetadata.mode & 0o777) !== 0o700
  ) throw new Error('PORTAL_RUNTIME_ROOT_INVALID');
  try {
    await lstat(lifecycleControlPath);
    throw new Error('PORTAL_CONTROL_RECORD_EXISTS');
  } catch (error) {
    if (error?.code !== 'ENOENT') throw error;
  }
  const pendingPath = `${lifecycleControlPath}.${instanceNonce}.pending`;
  await writeFile(pendingPath, `${JSON.stringify(record)}\n`, { mode: 0o600, flag: 'wx' });
  await rename(pendingPath, lifecycleControlPath);
  await chmod(lifecycleControlPath, 0o600);
} else {
  process.stdout.write(`${JSON.stringify(record)}\n`);
}
