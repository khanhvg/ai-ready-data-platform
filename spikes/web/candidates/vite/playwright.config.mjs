import { defineConfig } from '@playwright/test';

const baseURL = process.env.BASE_URL;
if (!baseURL || baseURL !== 'http://127.0.0.1:4175') {
  throw new Error('BASE_URL must be the owned same-origin host http://127.0.0.1:4175');
}

export default defineConfig({
  testDir: './tests',
  workers: 1,
  retries: 0,
  timeout: 60_000,
  expect: { timeout: 5_000 },
  reporter: [['json']],
  use: {
    baseURL,
    actionTimeout: 5_000,
    navigationTimeout: 15_000,
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
    video: 'off',
  },
  projects: [
    {
      name: 'chromium-desktop',
      grep: /@(journey|desktop-only)/,
      use: { browserName: 'chromium', channel: 'chrome', viewport: { width: 1280, height: 800 } },
    },
    {
      name: 'chromium-narrow',
      grep: /@journey/,
      use: { browserName: 'chromium', channel: 'chrome', viewport: { width: 360, height: 800 } },
    },
  ],
});
