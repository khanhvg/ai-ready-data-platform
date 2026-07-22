import http from "node:http";
import net from "node:net";
import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";

process.umask(0o077);
const appRoot = path.resolve(import.meta.dirname, "..");
const root = path.join(appRoot, "dist");
const inventoryPath = path.join(root, ".portal-build-inventory.json");
const forbiddenEnvironment = /^(?:AWS_|AZURE_|GOOGLE_|GCP_|CLOUD_|HTTP_PROXY$|HTTPS_PROXY$|ALL_PROXY$|NO_PROXY$|NODE_OPTIONS$|NODE_PATH$|VITE_|NPM_CONFIG_(?:PROXY|HTTPS_PROXY)$|DOCKER_|ORB_|TF_|TERRAFORM_)/i;
for (const name of Object.keys(process.env)) if (forbiddenEnvironment.test(name)) throw new Error(`ENVIRONMENT_UNSAFE:${name}`);
const sha256 = (bytes) => crypto.createHash("sha256").update(bytes).digest("hex");
const readPinned = async (file, limit) => {
  const before = await fs.lstat(file); if (!before.isFile() || before.isSymbolicLink() || before.nlink !== 1 || before.uid !== process.getuid() || before.size > limit) throw new Error(`BUILD_FILE_UNSAFE:${file}`);
  const handle = await fs.open(file, fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW);
  try { const opened = await handle.stat(); if (opened.dev !== before.dev || opened.ino !== before.ino || opened.nlink !== 1 || !opened.isFile()) throw new Error(`BUILD_FILE_INODE_MISMATCH:${file}`); const bytes = await handle.readFile(); return { bytes, stat: opened }; } finally { await handle.close(); }
};
const inventoryRead = await readPinned(inventoryPath, 1024 * 1024);
const inventory = JSON.parse(inventoryRead.bytes.toString("utf8"));
const packageBytes = (await readPinned(path.join(appRoot, "package.json"), 1024 * 1024)).bytes;
const lockBytes = (await readPinned(path.join(appRoot, "package-lock.json"), 4 * 1024 * 1024)).bytes;
const nodeBytes = (await readPinned(process.execPath, 128 * 1024 * 1024)).bytes;
const npmBytes = (await readPinned(path.resolve(path.dirname(process.execPath), "../lib/node_modules/npm/bin/npm-cli.js"), 1024 * 1024)).bytes;
const packageValue = JSON.parse(packageBytes.toString("utf8"));
if (inventory.schemaVersion !== "portal-build-inventory-v1" || inventory.production !== true || inventory.node !== process.versions.node || inventory.node !== packageValue.engines?.node || inventory.npm !== packageValue.engines?.npm || inventory.nodeBinarySha256 !== sha256(nodeBytes) || inventory.npmCliSha256 !== sha256(npmBytes) || inventory.packageJsonSha256 !== sha256(packageBytes) || inventory.lockSha256 !== sha256(lockBytes)) throw new Error("BUILD_RUNTIME_IDENTITY_MISMATCH");
const actualPaths = [];
async function walk(directory) { const stat = await fs.lstat(directory); if (!stat.isDirectory() || stat.isSymbolicLink() || stat.uid !== process.getuid()) throw new Error("BUILD_DIRECTORY_UNSAFE"); for (const item of await fs.readdir(directory, { withFileTypes: true })) { const absolute = path.join(directory, item.name); if (absolute === inventoryPath) continue; if (item.isSymbolicLink()) throw new Error("BUILD_DIRECTORY_UNSAFE"); if (item.isDirectory()) await walk(absolute); else if (item.isFile()) actualPaths.push(path.relative(root, absolute).split(path.sep).join("/")); else throw new Error("BUILD_DIRECTORY_UNSAFE"); } }
await walk(root);
const expectedPaths = inventory.files?.map((row) => row.path).sort();
if (!Array.isArray(expectedPaths) || new Set(expectedPaths).size !== expectedPaths.length || JSON.stringify(actualPaths.sort()) !== JSON.stringify(expectedPaths)) throw new Error("BUILD_INVENTORY_NOT_CLOSED");
const mime = Object.freeze({ ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8", ".json": "application/json; charset=utf-8", ".svg": "image/svg+xml" });
const bodies = new Map();
for (const row of inventory.files) {
  if (!row || typeof row.path !== "string" || !Array.isArray(row.urls) || !/^[A-Za-z0-9._/-]+$/.test(row.path) || row.path.includes("..")) throw new Error("BUILD_INVENTORY_INVALID");
  const pinned = await readPinned(path.join(root, row.path), 1024 * 1024);
  if (pinned.bytes.length !== row.bytes || sha256(pinned.bytes) !== row.sha256) throw new Error(`BUILD_FILE_HASH_MISMATCH:${row.path}`);
  for (const url of row.urls) { if (bodies.has(url)) throw new Error("BUILD_URL_DUPLICATE"); bodies.set(url, Object.freeze({ body: pinned.bytes, type: mime[path.extname(row.path)] ?? "application/octet-stream" })); }
}
if (!bodies.has("/__not_found__")) throw new Error("BUILD_NOT_FOUND_MISSING");
const csp = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'none'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'; worker-src 'none'";
const baseHeaders = Object.freeze({ "Content-Security-Policy": csp, "Referrer-Policy": "no-referrer", "X-Content-Type-Options": "nosniff", "Cross-Origin-Opener-Policy": "same-origin", "Permissions-Policy": "camera=(), microphone=(), geolocation=()", "Cache-Control": "no-store" });
const headers = (entry) => ({ ...baseHeaders, "Content-Type": entry?.type ?? "text/plain; charset=utf-8", "Content-Length": entry?.body.length ?? 0 });
const validPath = (value) => typeof value === "string" && value.length <= 2048 && /^\/[A-Za-z0-9._/-]*$/.test(value) && !value.includes("//") && !value.includes("..") && !value.includes("%") && !value.includes("?") && !value.includes("#");
const server = http.createServer((request, response) => {
  const address = server.address();
  const reject = (status) => { response.writeHead(status, headers(null)); response.end(); };
  if (request.headers.host !== `127.0.0.1:${address.port}`) return reject(400);
  if (!['GET', 'HEAD'].includes(request.method)) return reject(405);
  if (request.headers["transfer-encoding"] !== undefined || request.headers.expect !== undefined) return reject(400);
  const lengths = request.headersDistinct["content-length"] ?? [];
  if (lengths.length > 1 || (lengths.length === 1 && lengths[0] !== "0")) return reject(400);
  if (!validPath(request.url)) return reject(400);
  const entry = bodies.get(request.url) ?? bodies.get("/__not_found__");
  const status = bodies.has(request.url) ? 200 : 404;
  response.writeHead(status, headers(entry));
  response.end(request.method === "HEAD" ? undefined : entry.body);
});
server.on("clientError", (_error, socket) => { socket.end(`HTTP/1.1 400 Bad Request\r\n${Object.entries(headers(null)).map(([key, value]) => `${key}: ${value}`).join("\r\n")}\r\nConnection: close\r\n\r\n`); });

const args = Object.fromEntries(process.argv.slice(2).reduce((rows, value, index, values) => value.startsWith("--") ? [...rows, [value.slice(2), values[index + 1]]] : rows, []));
let control;
if (args["control-socket"] || args["authority-file"] || args.challenge || args["run-id"]) {
  if (!args["control-socket"] || !args["authority-file"] || !/^[0-9a-f]{64}$/.test(args.challenge ?? "") || !/^[0-9a-f]{32}$/.test(args["run-id"] ?? "")) throw new Error("CONTROL_ARGUMENT_INVALID");
  const controlPath = path.resolve(args["control-socket"]); const authorityPath = path.resolve(args["authority-file"]); const parent = await fs.lstat(path.dirname(controlPath)); const authorityParent = await fs.lstat(path.dirname(authorityPath));
  if (!parent.isDirectory() || parent.isSymbolicLink() || parent.uid !== process.getuid() || (parent.mode & 0o777) !== 0o700 || path.basename(controlPath) !== "control.sock") throw new Error("CONTROL_SOCKET_FOREIGN");
  if (!authorityParent.isDirectory() || authorityParent.isSymbolicLink() || authorityParent.uid !== process.getuid() || (authorityParent.mode & 0o777) !== 0o700 || path.basename(authorityPath) !== "child-authority.json") throw new Error("CHILD_AUTHENTICATION_FAILED");
  const { publicKey, privateKey } = crypto.generateKeyPairSync("ed25519"); const publicBytes = publicKey.export({ format: "der", type: "spki" });
  const authorityHandle = await fs.open(authorityPath, "wx", 0o400); try { await authorityHandle.writeFile(JSON.stringify({ schemaVersion: "portal-child-authority-v1", runId: args["run-id"], publicKey: publicBytes.toString("base64") })); } finally { await authorityHandle.close(); }
  const signedResponse = (payload) => ({ ...payload, signature: crypto.sign(null, Buffer.from(JSON.stringify(payload)), privateKey).toString("base64") });
  control = net.createServer((socket) => { let raw = ""; socket.setEncoding("utf8"); socket.on("data", (chunk) => { raw += chunk; if (raw.length > 1024) socket.destroy(); }); socket.on("end", () => { let value; try { value = JSON.parse(raw); } catch { socket.end('{"ok":false,"code":"CONTROL_PROTOCOL_INVALID"}\n'); return; } const supplied = Buffer.from(String(value.challenge ?? "")); const expected = Buffer.from(args.challenge); const authenticated = supplied.length === expected.length && crypto.timingSafeEqual(supplied, expected); if (value.version !== "portal-control-v2" || value.runId !== args["run-id"] || !authenticated || !/^[0-9a-f]{64}$/.test(value.requestNonce ?? "") || !["status", "shutdown"].includes(value.action) || Object.keys(value).sort().join(",") !== "action,challenge,requestNonce,runId,version") { socket.end('{"ok":false,"code":"CONTROL_CHALLENGE_STALE"}\n'); return; } if (value.action === "status") { socket.end(JSON.stringify(signedResponse({ action: "status", ok: true, requestNonce: value.requestNonce, runId: args["run-id"], status: "running", url: `http://127.0.0.1:${server.address().port}` })) + "\n"); return; } socket.end(JSON.stringify(signedResponse({ action: "shutdown", ok: true, requestNonce: value.requestNonce, runId: args["run-id"], status: "shutting-down" })) + "\n", () => server.close(() => control.close(async () => { await fs.rm(controlPath, { force: true }); process.exit(0); }))); }); });
  control.listen(controlPath);
}
server.listen(0, "127.0.0.1", () => console.log(`PORTAL_URL=http://127.0.0.1:${server.address().port}`));
for (const signal of ["SIGTERM", "SIGINT"]) process.on(signal, () => server.close(() => control ? control.close(() => process.exit(0)) : process.exit(0)));
