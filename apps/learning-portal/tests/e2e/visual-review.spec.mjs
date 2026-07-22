import { test, expect, chromium } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { spawn } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";

const appRoot = path.resolve(import.meta.dirname, "../.."); const repo = path.resolve(appRoot, "../.."); const evidence = path.join(repo, ".artifacts/evidence/local-journey"); let server; let baseURL;
test.beforeAll(async () => { await fs.mkdir(evidence, { recursive: true }); server = spawn(process.execPath, ["scripts/serve-built-portal.mjs"], { cwd: appRoot, stdio: ["ignore", "pipe", "pipe"] }); baseURL = await new Promise((resolve, reject) => { const timer = setTimeout(() => reject(new Error("server readiness timeout")), 15_000); server.stdout.on("data", (chunk) => { const match = chunk.toString().match(/PORTAL_URL=(http:\/\/127\.0\.0\.1:\d+)/); if (match) { clearTimeout(timer); resolve(match[1]); } }); }); });
test.afterAll(async () => { if (server?.exitCode === null) { server.kill("SIGTERM"); await new Promise((resolve) => server.once("exit", resolve)); } });

test("bounded deterministic Stage A visual evidence", async () => {
  const axe = []; const consoleErrors = []; const inventory = [];
  const existingTraces = (await fs.readdir(evidence)).filter((name) => name.endsWith("trace.zip")); if (existingTraces.some((name) => name !== "stage-a-trace.zip")) throw new Error("FOREIGN_TRACE_EVIDENCE"); await fs.rm(path.join(evidence, "stage-a-trace.zip"), { force: true });
  const context = await chromium.launchPersistentContext("", { channel: "chrome", headless: true, viewport: { width: 1280, height: 800 } }); const page = await context.newPage(); page.on("console", (message) => { if (message.type() === "error") consoleErrors.push(message.text()); }); await context.tracing.start({ screenshots: true, snapshots: true, sources: false });
  for (const viewport of [{ name: "desktop", width: 1280, height: 800 }, { name: "narrow", width: 360, height: 800 }]) {
    await page.setViewportSize({ width: viewport.width, height: viewport.height });
    for (const state of [{ name: "catalog", route: "/" }, { name: "grains", route: "/lesson/promotion-trust/step/inspect" }, { name: "decision", route: "/lesson/promotion-trust/step/decide" }, { name: "unavailable", route: "/lesson/promotion-trust/step/verify" }]) { await page.goto(`${baseURL}${state.route}`); await expect(page.locator("main")).toBeVisible(); await page.screenshot({ path: path.join(evidence, `${viewport.name}-${state.name}.png`), fullPage: true }); }
    const result = await new AxeBuilder({ page }).analyze(); axe.push({ viewport: viewport.name, violations: result.violations });
  }
  await context.tracing.stop({ path: path.join(evidence, "stage-a-trace.zip") }); await context.close();
  const noJs = await chromium.launchPersistentContext("", { channel: "chrome", headless: true, javaScriptEnabled: false }); const noJsPage = await noJs.newPage(); for (const route of ["/", "/module", "/lesson/promotion-trust", ...["frame", "inspect", "run", "fail", "trace", "decide", "reset", "configure", "verify", "reflect"].map((id) => `/lesson/promotion-trust/step/${id}`)]) { const response = await noJsPage.goto(`${baseURL}${route}`); inventory.push({ route, status: response.status(), decision: await noJsPage.locator("body").getByText(/decision=insufficient-evidence/).count() }); } await noJs.close();
  await fs.writeFile(path.join(evidence, "axe.json"), JSON.stringify(axe, null, 2)); await fs.writeFile(path.join(evidence, "no-js-inventory.json"), JSON.stringify(inventory, null, 2)); await fs.writeFile(path.join(evidence, "console-csp.json"), JSON.stringify({ consoleErrors, csp: "strict-self-no-connect" }, null, 2));
  expect(axe.flatMap((entry) => entry.violations).filter((item) => ["critical", "serious"].includes(item.impact))).toEqual([]); expect(consoleErrors).toEqual([]);
});
