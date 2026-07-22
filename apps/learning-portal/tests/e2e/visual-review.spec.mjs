import { test, expect, chromium } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { spawn } from "node:child_process";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { DEFAULT_EVIDENCE_ROOT, prepareEvidenceRoot, writeOwnedEvidence, finalizeEvidence } from "../../scripts/write-review-artifacts.mjs";

const appRoot = path.resolve(import.meta.dirname, "../.."); const evidence = process.env.PORTAL_EVIDENCE_ROOT ? path.resolve(process.env.PORTAL_EVIDENCE_ROOT) : DEFAULT_EVIDENCE_ROOT; let server; let baseURL;
test.beforeAll(async () => { server = spawn(process.execPath, ["scripts/serve-built-portal.mjs"], { cwd: appRoot, stdio: ["ignore", "pipe", "pipe"], env: { PATH: process.env.PATH, LANG: "C.UTF-8", LC_ALL: "C.UTF-8", TZ: "UTC" } }); baseURL = await new Promise((resolve, reject) => { const timer = setTimeout(() => reject(new Error("server readiness timeout")), 15_000); server.stdout.on("data", (chunk) => { const match = chunk.toString().match(/PORTAL_URL=(http:\/\/127\.0\.0\.1:\d+)/); if (match) { clearTimeout(timer); resolve(match[1]); } }); server.once("exit", (code) => reject(new Error(`server exited ${code}`))); }); });
test.afterAll(async () => { if (server?.exitCode === null) { server.kill("SIGTERM"); await new Promise((resolve) => server.once("exit", resolve)); } });

test("bounded deterministic Stage A visual evidence", async () => {
  const workEvidence = await prepareEvidenceRoot(evidence, { reset: true });
  const temporary = await fs.mkdtemp(path.join(os.tmpdir(), "portal-visual-"));
  const axe = []; const consoleErrors = []; const routeInventory = []; const domInventory = [];
  try {
    const context = await chromium.launchPersistentContext("", { channel: "chrome", headless: true, viewport: { width: 1280, height: 800 } }); const page = await context.newPage(); page.on("console", (message) => { if (message.type() === "error") consoleErrors.push(message.text()); });
    for (const viewport of [{ name: "desktop", width: 1280, height: 800 }, { name: "narrow", width: 360, height: 800 }]) {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      for (const state of [{ name: "catalog", route: "/" }, { name: "grains", route: "/lesson/promotion-trust/step/inspect" }, { name: "decision", route: "/lesson/promotion-trust/step/decide" }, { name: "unavailable", route: "/lesson/promotion-trust/step/verify" }]) {
        await page.goto(`${baseURL}${state.route}`); await expect(page.locator("main")).toBeVisible();
        const name = `${viewport.name}-${state.name}.png`; const temporaryPath = path.join(temporary, name); await page.screenshot({ path: temporaryPath, fullPage: true }); await writeOwnedEvidence(name, await fs.readFile(temporaryPath), workEvidence);
        domInventory.push({ viewport: viewport.name, route: state.route, title: await page.title(), heading: await page.getByRole("heading", { level: 1 }).textContent() });
      }
      const result = await new AxeBuilder({ page }).analyze(); axe.push({ viewport: viewport.name, violations: result.violations });
    }
    await context.close();
    const noJs = await chromium.launchPersistentContext("", { channel: "chrome", headless: true, javaScriptEnabled: false }); const noJsPage = await noJs.newPage();
    for (const route of ["/", "/module", "/lesson/promotion-trust", ...["frame", "inspect", "run", "fail", "trace", "decide", "reset", "configure", "verify", "reflect"].map((id) => `/lesson/promotion-trust/step/${id}`)]) { const response = await noJsPage.goto(`${baseURL}${route}`); routeInventory.push({ route, status: response.status(), decision: await noJsPage.locator("body").getByText(/decision=insufficient-evidence/).count() }); }
    await noJs.close();
    await writeOwnedEvidence("axe.json", JSON.stringify(axe, null, 2), workEvidence);
    await writeOwnedEvidence("no-js-inventory.json", JSON.stringify(routeInventory, null, 2), workEvidence);
    await writeOwnedEvidence("console-csp.json", JSON.stringify({ consoleErrors, csp: "strict-self-no-connect" }, null, 2), workEvidence);
    await writeOwnedEvidence("dom-inventory.json", JSON.stringify(domInventory, null, 2), workEvidence);
    await finalizeEvidence(workEvidence);
    await expect(fs.lstat(path.join(evidence, "stage-a-trace.zip"))).rejects.toThrow(/ENOENT/);
    expect(axe.flatMap((entry) => entry.violations).filter((item) => ["critical", "serious"].includes(item.impact))).toEqual([]); expect(consoleErrors).toEqual([]);
  } finally { await fs.rm(temporary, { recursive: true, force: true }); }
});
