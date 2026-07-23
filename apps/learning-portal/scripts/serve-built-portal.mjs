import { createHash, randomUUID } from 'node:crypto';
import { createServer } from 'node:http';
import { chmod, mkdir, readFile, stat, writeFile } from 'node:fs/promises';
import { dirname, extname, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const distRoot = resolve(appRoot, 'dist');
const lifecycleControlPath = process.env.PORTAL_LIFECYCLE_CONTROL_PATH;
const fixedTestPort = process.env.PORTAL_FIXED_TEST_PORT
  ? Number.parseInt(process.env.PORTAL_FIXED_TEST_PORT, 10)
  : 0;
const semanticReady = false;

function contentType(pathname) {
  return new Map([
    ['.html', 'text/html; charset=utf-8'],
    ['.js', 'text/javascript; charset=utf-8'],
    ['.css', 'text/css; charset=utf-8'],
    ['.json', 'application/json; charset=utf-8'],
    ['.svg', 'image/svg+xml']
  ]).get(extname(pathname)) ?? 'application/octet-stream';
}

function resolveRequestPath(url) {
  const pathname = new URL(url, 'http://127.0.0.1').pathname;
  const relative = pathname === '/' ? 'index.html' : pathname.replace(/^\/+/, '');
  const candidate = resolve(distRoot, relative);
  if (candidate !== distRoot && !candidate.startsWith(`${distRoot}${sep}`)) return null;
  return candidate;
}

const publicServer = createServer(async (request, response) => {
  const host = request.headers.host;
  if (!['127.0.0.1', `127.0.0.1:${fixedTestPort}`].includes(host) && !/^127\.0\.0\.1:\d+$/.test(host ?? '')) {
    response.writeHead(400).end();
    return;
  }
  if (!['GET', 'HEAD'].includes(request.method ?? '')) {
    response.writeHead(405).end();
    return;
  }
  const target = resolveRequestPath(request.url ?? '/');
  if (!target) {
    response.writeHead(404).end();
    return;
  }
  try {
    const metadata = await stat(target);
    const finalTarget = metadata.isDirectory() ? resolve(target, 'index.html') : target;
    const bytes = await readFile(finalTarget);
    response.writeHead(200, {
      'content-type': contentType(finalTarget),
      'content-length': bytes.length,
      'content-security-policy': "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'none'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'; worker-src 'none'",
      'x-content-type-options': 'nosniff'
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
  if (request.url === '/_control/status') {
    const bytes = JSON.stringify({ state: 'running', semanticReady });
    response.writeHead(200, { 'content-type': 'application/json' }).end(bytes);
    return;
  }
  if (request.url === '/_control/stop') {
    const bytes = JSON.stringify({ state: 'stopping', semanticReady });
    response.writeHead(200, { 'content-type': 'application/json' }).end(bytes);
    publicServer.close();
    controlServer.close();
    return;
  }
  response.writeHead(404).end();
});

await new Promise((resolveListen) => publicServer.listen(fixedTestPort, '127.0.0.1', resolveListen));
await new Promise((resolveListen) => controlServer.listen(0, '127.0.0.1', resolveListen));
const publicPort = publicServer.address().port;
const controlPort = controlServer.address().port;
const instanceNonce = randomUUID();
const record = {
  schemaVersion: 'portal-scaffold-control-v1',
  instanceNonce,
  publicPort,
  controlPort,
  semanticReady,
  pid: process.pid,
  executableDigest: createHash('sha256').update(process.execPath).digest('hex')
};

if (lifecycleControlPath) {
  await mkdir(dirname(lifecycleControlPath), { recursive: true, mode: 0o700 });
  await writeFile(lifecycleControlPath, `${JSON.stringify(record)}\n`, { mode: 0o600 });
  await chmod(lifecycleControlPath, 0o600);
  setTimeout(() => {
    publicServer.close();
    controlServer.close();
  }, 12_000).unref();
} else {
  process.stdout.write(`${JSON.stringify(record)}\n`);
}
