import { createHash } from 'node:crypto';
import { execFileSync, spawn } from 'node:child_process';
import { mkdtemp, readFile, readdir, rm } from 'node:fs/promises';
import http from 'node:http';
import os from 'node:os';
import { dirname, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadPortalCatalog } from '../src/sources/portal-source-loader.mjs';
import { derivePortalRoutes } from '../src/routing/portal-router.mjs';

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const distRoot = resolve(appRoot, 'dist');
const catalog = loadPortalCatalog();
const routes = derivePortalRoutes(catalog);
const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');
const assert = (condition, code) => { if (!condition) throw new Error(code); };

async function inventory() {
  const rows = [];
  async function walk(directory) {
    for (const entry of await readdir(directory, { withFileTypes: true })) {
      const path = resolve(directory, entry.name);
      if (entry.isDirectory()) await walk(path);
      else {
        const bytes = await readFile(path);
        rows.push([relative(distRoot, path).split(sep).join('/'), bytes.length, sha256(bytes)]);
      }
    }
  }
  await walk(distRoot);
  return rows.sort(([left], [right]) => left.localeCompare(right));
}

function build() {
  execFileSync(resolve(appRoot, 'node_modules/.bin/vite'), ['build'], { cwd: appRoot, stdio: 'pipe', env: { PATH: process.env.PATH ?? '/usr/bin:/bin' } });
  execFileSync(process.execPath, ['scripts/generate-static-routes.mjs'], { cwd: appRoot, stdio: 'pipe', env: { PATH: process.env.PATH ?? '/usr/bin:/bin' } });
}

function request(record, options = {}) {
  return new Promise((resolveRequest, reject) => {
    const body = options.body ?? '';
    const request = http.request({
      host: '127.0.0.1', port: options.control ? record.controlPort : record.publicPort,
      path: options.path ?? '/', method: options.method ?? 'GET',
      headers: options.control ? { 'content-length': '0', 'x-portal-instance': record.instanceNonce, authorization: `Bearer ${record.capability}` } : {
        host: options.host ?? `127.0.0.1:${record.publicPort}`, 'content-length': String(Buffer.byteLength(body)), ...(options.headers ?? {})
      }
    }, (response) => { let data=''; response.setEncoding('utf8'); response.on('data',(chunk)=>data+=chunk); response.on('end',()=>resolveRequest({ status:response.statusCode, body:data, headers:response.headers })); });
    request.on('error', reject); request.end(body);
  });
}

async function waitForRecord(path) {
  const deadline = Date.now() + 5_000;
  while (Date.now() < deadline) { try { return JSON.parse(await readFile(path,'utf8')); } catch { await new Promise((done)=>setTimeout(done,25)); } }
  throw new Error('PORTAL_SERVER_START_TIMEOUT');
}

assert(process.argv.length <= 3 && [undefined, '--build'].includes(process.argv[2]), 'PORTAL_VERIFY_ARGUMENT_INVALID');
assert(routes.length === 38 && catalog.counts.modules === 20 && catalog.counts.labs === 3 && catalog.counts.views === 5, 'PORTAL_CATALOG_COUNT_MISMATCH');
assert(catalog.counts.flows === 11 && catalog.counts.bridges === 8 && catalog.manualOnly === true, 'PORTAL_SOURCE_AUTHORITY_MISMATCH');

build();
const first = await inventory();
build();
const second = await inventory();
assert(JSON.stringify(first) === JSON.stringify(second), 'PORTAL_BUILD_NONDETERMINISTIC');
assert(first.filter(([path]) => path.endsWith('.html')).length === routes.length, 'PORTAL_STATIC_ROUTE_COUNT_MISMATCH');
assert(first.every(([path]) => !path.endsWith('.map')), 'PORTAL_SOURCE_MAP_FORBIDDEN');
for (const route of routes) {
  const path = route.path === '/' ? 'index.html' : `${route.path.slice(1)}/index.html`;
  const html = await readFile(resolve(distRoot, path), 'utf8');
  assert(html.includes('data-read-only="true"') && html.includes('data-manual-only="true"'), 'PORTAL_NO_JS_PARITY_MISSING');
}
const textFiles = first.filter(([path]) => /\.(?:html|js|css|json|txt|svg)$/.test(path));
const combined = (await Promise.all(textFiles.map(([path]) => readFile(resolve(distRoot,path),'utf8')))).join('\n');
for (const forbidden of [
  /<form\b/i, /<button\b/i, /localStorage/, /sessionStorage/, /indexedDB/, /serviceWorker/,
  /XMLHttpRequest/, /WebSocket/, /BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY/, /AWS_SECRET_ACCESS_KEY/,
  /OPENAI_API_KEY/, /ANTHROPIC_API_KEY/, /\/Users\//, /apps\/lab-runner/, /runner\/operations/
]) assert(!forbidden.test(combined), `PORTAL_READ_ONLY_SCAN_FAILED:${forbidden}`);
const applicationSource = `${await readFile(resolve(appRoot,'src/main.jsx'),'utf8')}\n${await readFile(resolve(appRoot,'src/app/app-shell.jsx'),'utf8')}`;
for (const forbidden of [/fetch\s*\(/,/XMLHttpRequest/,/WebSocket/,/sendBeacon\s*\(/]) assert(!forbidden.test(applicationSource), `PORTAL_NETWORK_SOURCE_FAILED:${forbidden}`);
for (const command of ['make seed SCALE=small SEED=42','make load','make health','make dbt','make bi']) assert(combined.includes(command), 'PORTAL_MANUAL_COMMAND_MISSING');

const temporaryRoot = await mkdtemp(resolve(os.tmpdir(), 'portal-release-'));
const controlPath = resolve(temporaryRoot, 'control.json');
const child = spawn(process.execPath, ['scripts/serve-built-portal.mjs'], { cwd: appRoot, stdio:'ignore', env:{ PATH:process.env.PATH ?? '/usr/bin:/bin', PORTAL_LIFECYCLE_CONTROL_PATH:controlPath } });
const record = await waitForRecord(controlPath);
try {
  assert((await request(record)).status === 200, 'PORTAL_SERVER_HOME_FAILED');
  assert((await request(record,{path:'/curriculum/f01'})).status === 200, 'PORTAL_SERVER_DEEP_LINK_FAILED');
  assert((await request(record,{path:'/labs/weighted-metrics'})).status === 200, 'PORTAL_SERVER_LAB_LINK_FAILED');
  assert((await request(record,{path:'/unknown'})).status === 404, 'PORTAL_SERVER_404_FAILED');
  assert((await request(record,{path:'/%2e%2e/index.html'})).status === 400, 'PORTAL_SERVER_TRAVERSAL_FAILED');
  assert((await request(record,{method:'POST'})).status === 405, 'PORTAL_SERVER_METHOD_FAILED');
  assert((await request(record,{body:'x'})).status === 400, 'PORTAL_SERVER_BODY_FAILED');
  assert((await request(record,{host:'example.invalid'})).status === 400, 'PORTAL_SERVER_HOST_FAILED');
  const head = await request(record,{method:'HEAD'}); assert(head.status === 200 && head.body === '', 'PORTAL_SERVER_HEAD_FAILED');
  const response = await request(record); assert(/connect-src 'none'/.test(response.headers['content-security-policy']), 'PORTAL_CSP_FAILED');
  assert((await request(record,{control:true,path:'/_control/stop',method:'POST'})).status === 200, 'PORTAL_CLEANUP_FAILED');
} finally {
  if (child.exitCode === null) child.kill('SIGTERM');
  await new Promise((done)=>{ if(child.exitCode!==null) done(); else { child.once('exit',done); setTimeout(done,1000).unref(); } });
  await rm(temporaryRoot,{recursive:true,force:true});
}

process.stdout.write(`${JSON.stringify({ schemaVersion:'portal-read-only-release-v1', routes:routes.length, ...catalog.counts, sourceAuthorities:Object.keys(catalog.sourceHashes).length, deterministicBuild:true, manualOnly:true, securityReadOnly:true, cleanup:true })}\n`);
