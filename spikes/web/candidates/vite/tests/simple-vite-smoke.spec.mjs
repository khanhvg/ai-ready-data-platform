import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

const exact = {
  title: 'Can this promotion headline be trusted?',
  notice: 'TRACKED REAL FIXTURE — UNSCORED — CANNOT COMPLETE',
  baseline: 'Exploration is reversible and unverified.',
  failure: 'Controlled failure: no common grain; no answer, attribution, completion, or score saved.',
  reset: 'Reset: baseline restored; no answer, attribution, completion, or score persisted.',
  reflection: 'Reflection: What additional common-grain evidence would be needed before making a causal claim?',
  noJsReset: 'Without JavaScript, reset is unavailable; all facts remain in their baseline state.',
  grains: [
    ['grain-promotion', 'promo_name × channel', 'Promotion aggregates cannot identify fulfillment, returns, or data-quality causes.'],
    ['grain-fulfillment', 'carrier × region_name', 'No shared key permits attribution to a promotion.'],
    ['grain-returns', 'reason × category_name × region_name', 'No shared key permits attribution to a promotion.'],
    ['grain-data-quality', 'scenario', 'Scenario evidence is independent and does not establish a cause.'],
  ],
};

const checkpointIds = ['lesson-entry', 'lesson-status', ...exact.grains.flatMap(([id]) => [id, `${id}-limitation`]), 'lesson-conclusion', 'lesson-reason', 'no-js-reset-limitation', 'reflection-prompt'];

async function assertNoOverflow(page) {
  const facts = await page.evaluate(ids => ({
    viewport: innerWidth,
    document: [document.documentElement.scrollWidth, document.documentElement.clientWidth],
    body: [document.body.scrollWidth, document.body.clientWidth],
    rects: ids.map(id => {
      const element = document.querySelector(`[data-testid="${id}"]`);
      if (!element) return { id, missing: true };
      const { left, right } = element.getBoundingClientRect();
      return { id, left, right };
    }),
  }), checkpointIds);
  expect(facts.document[0]).toBeLessThanOrEqual(facts.document[1]);
  expect(facts.body[0]).toBeLessThanOrEqual(facts.body[1]);
  for (const rect of facts.rects.filter(({ missing }) => !missing)) {
    expect(rect.left, rect.id).toBeGreaterThanOrEqual(0);
    expect(rect.right, rect.id).toBeLessThanOrEqual(facts.viewport);
  }
  return facts;
}

async function focusByKeyboard(page, testId, reverse = false) {
  for (let index = 0; index < 40; index += 1) {
    await page.keyboard.press(reverse ? 'Shift+Tab' : 'Tab');
    if (await page.locator(`[data-testid="${testId}"]`).evaluate(element => element === document.activeElement).catch(() => false)) break;
  }
  const facts = await page.locator(`[data-testid="${testId}"]`).evaluate(element => {
    const style = getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    const width = Number.parseFloat(style.outlineWidth);
    const offset = Number.parseFloat(style.outlineOffset);
    const x = rect.left + rect.width / 2;
    const y = rect.top + rect.height / 2;
    return {
      active: element === document.activeElement,
      outlineStyle: style.outlineStyle,
      outlineWidth: width,
      outlineOffset: offset,
      inside: rect.left - width - offset >= 0 && rect.right + width + offset <= innerWidth && rect.top - width - offset >= 0 && rect.bottom + width + offset <= innerHeight,
      ownsHit: element.contains(document.elementFromPoint(x, y)),
    };
  });
  expect(facts).toMatchObject({ active: true, outlineStyle: 'solid', inside: true, ownsHit: true });
  expect(facts.outlineWidth).toBeGreaterThanOrEqual(2);
  expect(facts.outlineOffset).toBeGreaterThanOrEqual(2);
  return { testId, ...facts };
}

async function completeJourney(page) {
  const requests = [];
  const facts = { checkpoints: [], focus: [], overflow: [] };
  page.on('request', request => requests.push(request.url()));
  await page.goto('/');
  await expect(page.locator('html')).toHaveAttribute('lang', 'vi');
  await expect(page.getByTestId('lesson-entry')).toContainText(exact.title);
  await expect(page.getByText(exact.notice, { exact: true })).toBeVisible();
  await expect(page.getByTestId('lesson-status')).toHaveText(exact.baseline);
  facts.checkpoints.push({ id: 'entry', status: exact.baseline });
  facts.overflow.push({ checkpoint: 'entry', ...await assertNoOverflow(page) });

  facts.focus.push(await focusByKeyboard(page, 'run-bounded-probe'));
  await page.keyboard.press('Enter');
  await expect(page.getByTestId('run-bounded-probe')).toBeFocused();
  await expect(page.getByTestId('lesson-status')).toHaveText(exact.failure);
  facts.checkpoints.push({ id: 'controlled-failure', status: exact.failure });
  facts.overflow.push({ checkpoint: 'controlled-failure', ...await assertNoOverflow(page) });

  for (const [id, grain, limitation] of exact.grains) {
    await expect(page.getByTestId(id)).toHaveText(grain);
    await expect(page.getByTestId(`${id}-limitation`)).toHaveText(limitation);
    facts.checkpoints.push({ id, grain, limitation });
    facts.overflow.push({ checkpoint: id, ...await assertNoOverflow(page) });
  }
  await expect(page.getByTestId('lesson-conclusion')).toHaveText('insufficient-evidence');
  await expect(page.getByTestId('lesson-reason')).toHaveText('no-common-grain');
  await expect(page.locator('[data-testid="relationship"], [data-testid="attribution"]')).toHaveCount(0);
  facts.checkpoints.push({ id: 'conclusion', value: 'insufficient-evidence', reason: 'no-common-grain', relationships: 0, attribution: 0 });

  facts.focus.push(await focusByKeyboard(page, 'reset-lesson'));
  await page.keyboard.press('Space');
  await expect(page.getByTestId('reset-lesson')).toBeFocused();
  await expect(page.getByTestId('lesson-status')).toHaveText(exact.reset);
  const persistence = await page.evaluate(async () => ({
    cookie: document.cookie,
    localStorage: localStorage.length,
    sessionStorage: sessionStorage.length,
    caches: 'caches' in globalThis ? (await caches.keys()).length : 0,
    indexedDb: indexedDB.databases ? (await indexedDB.databases()).length : 0,
    serviceWorkers: 'serviceWorker' in navigator ? (await navigator.serviceWorker.getRegistrations()).length : 0,
  }));
  expect(persistence).toEqual({ cookie: '', localStorage: 0, sessionStorage: 0, caches: 0, indexedDb: 0, serviceWorkers: 0 });
  facts.checkpoints.push({ id: 'reset', status: exact.reset, persistence });
  await expect(page.getByTestId('reflection-prompt')).toHaveText(exact.reflection);
  await expect(page.locator('[data-testid*="complete"], [data-testid*="score"]')).toHaveCount(0);
  facts.checkpoints.push({ id: 'reflection', text: exact.reflection, completionControls: 0, scoreControls: 0 });
  facts.overflow.push({ checkpoint: 'reflection', ...await assertNoOverflow(page) });
  const requestOrigins = [...new Set(requests.map(url => new URL(url).origin))].sort();
  expect(requestOrigins).toEqual(['http://127.0.0.1:4175']);
  return { ...facts, requestOrigins };
}

test('@journey V3-03 V3-04 representative promotion-trust journey', async ({ page }, testInfo) => {
  const facts = await completeJourney(page);
  await testInfo.attach('v3-03-v3-04-journey-facts.json', {
    body: Buffer.from(JSON.stringify({ project: testInfo.project.name, viewport: testInfo.project.use.viewport, ...facts }, null, 2)),
    contentType: 'application/json',
  });
});

test('@desktop-only V3-05 one whole-page axe scan', async ({ page }, testInfo) => {
  await completeJourney(page);
  const axeResult = await new AxeBuilder({ page }).analyze();
  await testInfo.attach('v3-05-axe-complete.json', { body: Buffer.from(JSON.stringify(axeResult, null, 2)), contentType: 'application/json' });
  const blocking = axeResult.violations.filter(({ impact }) => impact === 'critical' || impact === 'serious');
  expect(blocking).toEqual([]);
});

test('@desktop-only V3-06 real JavaScript-disabled response and DOM fallback', async ({ browser }, testInfo) => {
  const context = await browser.newContext({ javaScriptEnabled: false, baseURL: 'http://127.0.0.1:4175' });
  try {
    const page = await context.newPage();
    const response = await page.goto('/');
    expect(response).not.toBeNull();
    const bytes = await response.body();
    const text = bytes.toString('utf8');
    const csp = response.headers()['content-security-policy'];
    expect(csp).toBe("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'");
    const ordered = ['lesson-entry', ...exact.grains.flatMap(([id]) => [id, `${id}-limitation`]), 'lesson-conclusion', 'lesson-reason', 'no-js-reset-limitation', 'reflection-prompt'];
    let offset = -1;
    for (const id of ordered) {
      const next = text.indexOf(`data-testid="${id}"`);
      expect(next, `${id} must be in response bytes and source order`).toBeGreaterThan(offset);
      offset = next;
    }
    for (const token of [exact.title, exact.notice, exact.baseline, ...exact.grains.flatMap(([, grain, limitation]) => [grain, limitation]), 'insufficient-evidence', 'no-common-grain', exact.noJsReset, exact.reflection]) {
      expect(text).toContain(token);
    }
    const inventory = [];
    for (const id of ordered) {
      const locator = page.getByTestId(id);
      await expect(locator).toBeVisible();
      inventory.push({ id, text: await locator.innerText() });
    }
    await expect(page.getByTestId('run-bounded-probe')).toHaveCount(0);
    await expect(page.getByTestId('reset-lesson')).toHaveCount(0);
    await testInfo.attach('v3-06-response.html', { body: bytes, contentType: 'text/html; charset=utf-8' });
    await testInfo.attach('v3-06-no-js-inventory.json', { body: Buffer.from(JSON.stringify({ responseBytes: bytes.length, csp, inventory }, null, 2)), contentType: 'application/json' });
  } finally {
    await context.close();
  }
});
