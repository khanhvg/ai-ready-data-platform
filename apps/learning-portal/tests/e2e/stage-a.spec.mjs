import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

async function expectAxeClean(page) {
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations.filter(({ impact }) => ['critical', 'serious'].includes(impact))).toEqual([]);
}

test('home → curriculum → module → architecture → manual lab journey', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading',{name:'Nền tảng dữ liệu sẵn sàng cho AI'})).toBeVisible();
  await expectAxeClean(page);
  await page.getByRole('link',{name:'Mở lộ trình →'}).click();
  await expect(page).toHaveURL(/\/curriculum$/);
  await expectAxeClean(page);
  await page.locator('.module-list a[href="/curriculum/f01"]').click();
  await expect(page.getByRole('heading',{level:1})).toContainText('Nhận diện bên liên quan');
  await expectAxeClean(page);
  await page.getByRole('link',{name:'Kiến trúc'}).click();
  await expect(page.locator('figure.architecture-view')).toHaveCount(5);
  await expectAxeClean(page);
  await page.getByRole('link',{name:'Lab thủ công',exact:true}).click();
  await page.locator('.card-grid a[href="/labs/deterministic-ingest"]').click();
  await expect(page.getByText('Thực hành thủ công tại local',{exact:true})).toBeVisible();
  await expect(page.locator('pre code')).toContainText(['make seed SCALE=small SEED=42','make load','make health']);
  await expectAxeClean(page);
});

test('all 20 modules and three labs are discoverable and direct links reload',async({page})=>{
  await page.goto('/curriculum');
  await expect(page.locator('.module-list a[href^="/curriculum/"]')).toHaveCount(20);
  for(const id of ['f01','f02','f03','f04','j01','j02','j03','j04','j05','j06','d01','d02','d03','d04','d05','d06','m01','m02','m03','m04']) expect((await page.request.get(`/curriculum/${id}`)).status()).toBe(200);
  await page.goto('/labs'); await expect(page.locator('.card-grid a[href^="/labs/"]')).toHaveCount(3);
  for(const slug of ['deterministic-ingest','model-quality','weighted-metrics']) expect((await page.request.get(`/labs/${slug}`)).status()).toBe(200);
  await page.goto('/curriculum/m04'); await page.reload(); await expect(page.getByText('M04',{exact:false}).first()).toBeVisible();
  await page.goto('/labs/weighted-metrics'); await page.reload(); await expect(page.getByText('Thực hành thủ công tại local',{exact:true})).toBeVisible();
  expect((await page.request.get('/not-a-released-route')).status()).toBe(404);
});

test('history, keyboard focus, narrow overflow, reduced motion, and axe pass',async({page})=>{
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/');
  const link=page.locator('a[href="/curriculum"]').first(); await link.focus(); await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/\/curriculum$/); await expect(page.locator('main')).toBeFocused();
  await page.locator('.module-list a[href="/curriculum/f01"]').click(); await page.goBack(); await expect(page).toHaveURL(/\/curriculum$/); await page.goForward(); await expect(page).toHaveURL(/\/curriculum\/f01$/);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  await expectAxeClean(page);
  expect(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior)).toBe('auto');
  await expect(page.locator('html')).toHaveAttribute('lang','vi');
});

test('read-only boundary has no actionable controls, storage, cookies, or external requests',async({page})=>{
  const external=[]; page.on('request',(request)=>{if(!request.url().startsWith('http://127.0.0.1:4175/'))external.push(request.url())});
  await page.goto('/labs/model-quality');
  expect(await page.locator('form, button, input, textarea, select, [contenteditable="true"]').count()).toBe(0);
  await expect(page.locator('[data-read-only="true"][data-manual-only="true"]')).toHaveCount(1);
  expect(await page.context().cookies()).toEqual([]);
  expect(await page.evaluate(()=>({local:localStorage.length,session:sessionStorage.length,worker:Boolean(navigator.serviceWorker?.controller)}))).toEqual({local:0,session:0,worker:false});
  expect(external).toEqual([]);
});

test('no-JavaScript parity contains core module, architecture, and command content',async({browser})=>{
  const context=await browser.newContext({javaScriptEnabled:false,viewport:{width:360,height:800}}); const page=await context.newPage();
  try{
    expect((await page.goto('http://127.0.0.1:4175/curriculum/f01'))?.status()).toBe(200); await expect(page.getByText('Controlled failure',{exact:true})).toBeVisible();
    expect((await page.goto('http://127.0.0.1:4175/architecture'))?.status()).toBe(200); await expect(page.locator('figure')).toHaveCount(5);
    expect((await page.goto('http://127.0.0.1:4175/labs/deterministic-ingest'))?.status()).toBe(200); await expect(page.getByText('Thực hành thủ công tại local',{exact:true})).toBeVisible(); await expect(page.locator('pre code')).toContainText(['make seed SCALE=small SEED=42','make load','make health']);
    expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  }finally{await context.close()}
});
