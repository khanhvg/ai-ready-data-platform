import { defineConfig } from '@playwright/test';

const port = 4175;

export default defineConfig({
  testDir: './tests/e2e',
  workers: 1,
  retries: 0,
  timeout: 60_000,
  expect: { timeout: 5_000 },
  reporter: [['line']],
  outputDir: '.artifacts/playwright',
  webServer: {
    command: 'node scripts/serve-built-portal.mjs',
    url: `http://127.0.0.1:${port}/`,
    reuseExistingServer: false,
    timeout: 15_000,
    env: {
      PORTAL_FIXED_TEST_PORT: String(port)
    }
  },
  use: {
    baseURL: `http://127.0.0.1:${port}`,
    actionTimeout: 5_000,
    navigationTimeout: 15_000,
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
    video: 'off',
    browserName: 'chromium',
    channel: 'chrome'
  },
  projects: [
    {
      name: 'chrome-desktop',
      use: { viewport: { width: 1280, height: 800 } }
    },
    {
      name: 'chrome-narrow',
      use: { viewport: { width: 360, height: 800 } }
    }
  ]
});
