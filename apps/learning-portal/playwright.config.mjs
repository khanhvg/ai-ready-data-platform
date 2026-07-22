import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  timeout: 120_000,
  expect: { timeout: 10_000 },
  workers: 1,
  retries: 0,
  reporter: "line",
  use: { browserName: "chromium", channel: "chrome", locale: "vi-VN", timezoneId: "Asia/Ho_Chi_Minh", colorScheme: "light", reducedMotion: "reduce", trace: "retain-on-failure" },
  outputDir: "../../.artifacts/evidence/local-journey/playwright-output"
});
