import { execFileSync } from 'node:child_process';
import { readFile, stat } from 'node:fs/promises';
import { expect, test } from '@playwright/test';

test('@desktop visual states write bounded review evidence without approval claims', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('[data-semantic-ready="false"]')).toBeVisible();
  await page.screenshot({ path: '.artifacts/playwright/desktop-neutral.png', fullPage: true });
  const output = execFileSync(process.execPath, ['scripts/write-review-artifacts.mjs'], {
    cwd: process.cwd(),
    encoding: 'utf8'
  });
  const locator = JSON.parse(output);
  const review = JSON.parse(await readFile(locator.path, 'utf8'));
  expect(review.independentlyReviewed).toBe(false);
  expect(review.humanApproved).toBe(false);
  expect(review.schemaVersion, 'PTP_RED_EVIDENCE_CLOSURE_ABSENT').toBe(
    'stage-a-current-generation-v1'
  );
  expect((await stat(locator.path)).size).toBeLessThanOrEqual(2 * 1024 * 1024);
});

test('@narrow visual review captures ten stable lesson states and one bounded trace contract', async ({
  page
}) => {
  await page.goto('/');
  await expect(page.locator('[data-semantic-ready="false"]')).toBeVisible();
  await page.screenshot({ path: '.artifacts/playwright/narrow-neutral.png', fullPage: true });
  await expect(page.locator('[data-review-inventory="closed"]'), 'PTP_RED_EVIDENCE_CLOSURE_ABSENT').toHaveCount(1);
});
