import { test, expect, chromium } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { spawn } from "node:child_process";
import path from "node:path";

const appRoot = path.resolve(import.meta.dirname, "../.."); let server; let baseURL;
test.beforeAll(async () => { server = spawn(process.execPath, ["scripts/serve-built-portal.mjs"], { cwd: appRoot, stdio: ["ignore", "pipe", "pipe"] }); baseURL = await new Promise((resolve, reject) => { const timer = setTimeout(() => reject(new Error("server readiness timeout")), 15_000); server.stdout.on("data", (chunk) => { const match = chunk.toString().match(/PORTAL_URL=(http:\/\/127\.0\.0\.1:\d+)/); if (match) { clearTimeout(timer); resolve(match[1]); } }); server.once("exit", (code) => reject(new Error(`server exited ${code}`))); }); });
test.afterAll(async () => { if (server && server.exitCode === null) { server.kill("SIGTERM"); await new Promise((resolve) => server.once("exit", resolve)); } });

test("Stage A catalog to step journey is honest, accessible, responsive, and static", async () => {
  const requests = []; const errors = [];
  for (const viewport of [{ width: 1280, height: 800 }, { width: 360, height: 800 }]) {
    const context = await chromium.launchPersistentContext("", { channel: "chrome", headless: true, viewport, locale: "vi-VN", timezoneId: "Asia/Ho_Chi_Minh", reducedMotion: "reduce" }); const page = await context.newPage();
    page.on("request", (request) => { if (!request.url().startsWith(baseURL)) requests.push(request.url()); }); page.on("console", (message) => { if (message.type() === "error") errors.push(message.text()); }); page.on("pageerror", (error) => errors.push(error.message));
    await page.goto(baseURL); await expect(page.getByRole("heading", { level: 1 })).toHaveText("Danh mục học tập");
    await page.getByRole("link", { name: "Mở mô-đun trình bày" }).click(); await expect(page).toHaveURL(`${baseURL}/module`);
    await page.getByRole("link", { name: "Mở bài học" }).click(); await expect(page).toHaveURL(`${baseURL}/lesson/promotion-trust`);
    for (const id of ["frame", "inspect", "run", "fail", "trace", "decide", "reset", "configure", "verify", "reflect"]) { await page.goto(`${baseURL}/lesson/promotion-trust/step/${id}`); await expect(page.locator("main")).toHaveAttribute("data-runner", "unavailable"); await expect(page.locator("main")).toHaveAttribute("data-completion", "disabled"); await expect(page.locator("main")).toContainText("decision=insufficient-evidence"); await expect(page.locator("main")).toContainText("reason=no-common-grain"); }
    await page.goBack(); await page.goForward(); await page.reload(); await expect(page.locator("main")).toHaveAttribute("data-fresh-evidence", "false");
    await page.keyboard.press("Tab"); await expect(page.locator(":focus")).toBeVisible();
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth); expect(overflow).toBeLessThanOrEqual(0);
    const results = await new AxeBuilder({ page }).analyze(); expect(results.violations.filter((item) => ["critical", "serious"].includes(item.impact))).toEqual([]);
    await page.goto(`${baseURL}/unknown`); await expect(page).toHaveTitle(/Không tìm thấy/); await context.close();
  }
  expect(requests).toEqual([]); expect(errors.filter((message) => !message.startsWith("Failed to load resource: the server responded with a status of 404"))).toEqual([]);
  const noJs = await chromium.launchPersistentContext("", { channel: "chrome", headless: true, javaScriptEnabled: false, viewport: { width: 360, height: 800 } }); const page = await noJs.newPage();
  await page.goto(`${baseURL}/lesson/promotion-trust/step/decide`); await expect(page.locator("main")).toContainText("decision=insufficient-evidence"); await expect(page.getByRole("link", { name: /Bước tiếp theo/ })).toBeVisible(); await noJs.close();
});
