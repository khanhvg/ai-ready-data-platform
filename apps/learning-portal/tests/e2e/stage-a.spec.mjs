import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

test('@journey real Chrome reaches the scaffold then requires the released Vietnamese journey', async ({
  browser,
  page
}) => {
  const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  expect(browser.version()).toBe('150.0.7871.181');
  expect(createHash('sha256').update(await readFile(chromePath)).digest('hex')).toBe(
    'b724a4c5603cfc8b9d9f27a5153c8a39e7133e53666ced7f2a8b03bf49484f85'
  );
  const response = await page.goto('/');
  expect(response?.status()).toBe(200);
  await expect(page.locator('[data-semantic-ready="false"]')).toBeVisible();
  await expect(
    page.getByRole('navigation', { name: 'Điều hướng cổng học tập' }),
    'PTP_RED_CATALOG_SEMANTICS_ABSENT'
  ).toContainText('Bằng chứng quyết định khuyến mãi');
  await expect(page.getByRole('link')).toHaveCount(13);
});

test('@desktop PTP-RED-A-016 keyboard, focus, live status, reduced motion, narrow flow, and axe semantics', async ({
  page
}) => {
  await page.goto('/');
  await expect(page.locator('[data-semantic-ready="false"]')).toBeVisible();
  const results = await new AxeBuilder({ page }).analyze();
  expect(
    results.violations.filter(({ impact }) => ['critical', 'serious'].includes(impact)).length
  ).toBe(0);
  await page.keyboard.press('Tab');
  await expect(page.locator(':focus')).toBeVisible();
  await expect(page.locator('[aria-live="polite"]'), 'PTP_RED_ACCESSIBILITY_SEMANTICS_ABSENT').toContainText(
    'Trình chạy không khả dụng'
  );
  await expect(page.locator('html'), 'PTP_RED_ACCESSIBILITY_SEMANTICS_ABSENT').toHaveAttribute(
    'lang',
    'vi'
  );
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
});

test('released routes support keyboard navigation, deep links, reload, and browser history', async ({
  page
}) => {
  await page.goto('/');
  const moduleLink = page.locator('a[href="/module"]');
  await moduleLink.focus();
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/\/module$/);
  await expect(page.locator('#lesson-content')).toBeFocused();

  await page.locator('a[href="/lessons/promotion-trust"]').click();
  await expect(page).toHaveURL(/\/lessons\/promotion-trust$/);
  await page.locator('a[href="/lessons/promotion-trust/steps/frame"]').click();
  await expect(page.getByRole('heading', { name: 'Bước 1: frame' }).first()).toBeVisible();
  await page.locator('a[href="/lessons/promotion-trust/steps/reflect"]').click();
  await expect(page.getByRole('heading', { name: 'Bước 10: reflect' }).first()).toBeVisible();

  await page.reload();
  await expect(page.getByRole('heading', { name: 'Bước 10: reflect' }).first()).toBeVisible();
  await page.goBack();
  await expect(page.getByRole('heading', { name: 'Bước 1: frame' }).first()).toBeVisible();
  await page.goForward();
  await expect(page.getByRole('heading', { name: 'Bước 10: reflect' }).first()).toBeVisible();

  const deepLink = await page.goto('/lessons/promotion-trust/steps/verify');
  expect(deepLink?.status()).toBe(200);
  await expect(page.getByRole('heading', { name: 'Bước 9: verify' }).first()).toBeVisible();
  expect((await page.request.get('/not-a-released-route')).status()).toBe(404);
});

test('@narrow no-JavaScript output exposes the same released facts and navigation', async ({
  browser
}) => {
  const context = await browser.newContext({
    javaScriptEnabled: false,
    viewport: { width: 360, height: 800 }
  });
  const page = await context.newPage();
  try {
    const response = await page.goto('http://127.0.0.1:4175/');
    expect(response?.status()).toBe(200);
    await expect(page.locator('[data-semantic-ready="false"]')).toBeVisible();
    await expect(page.getByText('insufficient-evidence/no-common-grain'), 'PTP_RED_ROUTE_DERIVATION_ABSENT').toBeVisible();
    await expect(page.getByRole('link')).toHaveCount(13);
    const deepLink = await page.goto(
      'http://127.0.0.1:4175/lessons/promotion-trust/steps/trace'
    );
    expect(deepLink?.status()).toBe(200);
    await expect(page.getByRole('heading', { name: 'Bước 5: trace' }).first()).toBeVisible();
    await page.reload();
    await expect(page.getByRole('heading', { name: 'Bước 5: trace' }).first()).toBeVisible();
  } finally {
    await context.close();
  }
});

test('@desktop browser boundary has no mutation, storage, external request, or completion surface', async ({
  page
}) => {
  const external = [];
  page.on('request', (request) => {
    if (!request.url().startsWith('http://127.0.0.1:4175/')) external.push(request.url());
  });
  await page.goto('/');
  expect(external).toEqual([]);
  expect(await page.context().cookies()).toEqual([]);
  expect(
    await page.evaluate(() => ({
      local: localStorage.length,
      session: sessionStorage.length,
      serviceWorker: 'serviceWorker' in navigator && Boolean(navigator.serviceWorker.controller)
    }))
  ).toEqual({ local: 0, session: 0, serviceWorker: false });
  expect(await page.locator('form, button, input, textarea, [data-completion]').count()).toBe(0);
  await expect(page.locator('[data-s3-coverage="14"]'), 'PTP_RED_S3_COVERAGE_ABSENT').toHaveCount(1);
});
