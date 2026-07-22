import http from "node:http";
import fs from "node:fs/promises";
import path from "node:path";

const root = path.resolve(import.meta.dirname, "../dist");
const mime = Object.freeze({ ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8", ".json": "application/json; charset=utf-8", ".svg": "image/svg+xml" });
const csp = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'none'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'; worker-src 'none'";
const server = http.createServer(async (request, response) => {
  const address = server.address(); const expectedHost = `127.0.0.1:${address.port}`;
  const reject = (status) => { response.writeHead(status, { "Cache-Control": "no-store" }); response.end(); };
  if (request.headers.host !== expectedHost || !["GET", "HEAD"].includes(request.method) || Number(request.headers["content-length"] ?? 0) > 0 || request.url.length > 2048 || request.url.includes("?") || request.url.includes("#") || request.url.includes("%") || request.url.includes("..")) return reject(400);
  const pathname = request.url === "/" ? "/index.html" : request.url.endsWith("/") ? `${request.url}index.html` : path.extname(request.url) ? request.url : `${request.url}/index.html`;
  const target = path.resolve(root, `.${pathname}`); if (!target.startsWith(`${root}${path.sep}`)) return reject(404);
  const headers = (targetPath, body) => ({ "Content-Type": mime[path.extname(targetPath)] ?? "application/octet-stream", "Content-Length": body.length, "Content-Security-Policy": csp, "Referrer-Policy": "no-referrer", "X-Content-Type-Options": "nosniff", "Cross-Origin-Opener-Policy": "same-origin", "Permissions-Policy": "camera=(), microphone=(), geolocation=()", "Cache-Control": "no-store" });
  try { const stat = await fs.lstat(target); if (!stat.isFile() || stat.isSymbolicLink() || stat.nlink !== 1 || stat.size > 1024 * 1024) throw new Error("not-found"); const body = await fs.readFile(target); response.writeHead(200, headers(target, body)); response.end(request.method === "HEAD" ? undefined : body); } catch { const notFound = path.join(root, "404.html"); const body = await fs.readFile(notFound); response.writeHead(200, headers(notFound, body)); response.end(request.method === "HEAD" ? undefined : body); }
});
server.listen(0, "127.0.0.1", () => console.log(`PORTAL_URL=http://127.0.0.1:${server.address().port}`));
for (const signal of ["SIGTERM", "SIGINT"]) process.on(signal, () => server.close(() => process.exit(0)));
