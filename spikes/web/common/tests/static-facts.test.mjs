import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const facets = Object.freeze({
  staticLogical: 'required',
  browserDecision: 'required-pending',
  manualDecision: 'required-pending',
  browserKeyboard: 'required-pending',
  namedScreenReader: 'required-pending',
  rendered200Percent: 'required-pending',
  renderedReducedMotion: 'required-pending',
  noJsManualComprehension: 'required-pending',
});

async function sources() {
  return {
    html: await readFile(new URL('../../preview/index.html', import.meta.url), 'utf8'),
    css: await readFile(new URL('../../preview/preview.css', import.meta.url), 'utf8'),
  };
}

test('WEB-A11Y-001 staticLogical uses native keyboard controls and visible focus; browser facet remains pending', async () => {
  const { html, css } = await sources();
  assert.equal(facets.staticLogical, 'required');
  assert.equal(facets.browserDecision, 'required-pending');
  assert.equal(facets.browserKeyboard, 'required-pending');
  assert.match(html, /<a[^>]+href=["']#main/);
  assert.match(html, /<(?:button|summary)\b/);
  assert.match(css, /:focus-visible/);
  assert.match(css, /outline\s*:/);
  assert.match(css, /--focus-inner\s*:\s*#fff(?:fff)?\b/i);
  assert.match(css, /--focus-outer\s*:\s*#111(?:111)?\b/i);
  assert.match(css, /:focus-visible\s*\{[^}]*outline[^}]*var\(--focus-inner\)[^}]*box-shadow[^}]*var\(--focus-outer\)/s);
});

test('WEB-A11Y-002 staticLogical has ordered landmarks, headings, tables and live status; manual AT remains pending', async () => {
  const { html } = await sources();
  assert.equal(facets.manualDecision, 'required-pending');
  assert.equal(facets.namedScreenReader, 'required-pending');
  for (const semantic of [/<header\b/, /<nav\b/, /<main\b/, /<aside\b/, /<footer\b/, /<h1\b/, /<table\b/, /role=["']status["']/]) assert.match(html, semantic);
  assert.doesNotMatch(html, /tabindex=["'](?:[1-9]\d*)["']/);
});

test('WEB-A11Y-003 staticLogical reflows rail/cards in flow with no 2D narrative scroll; rendered zoom remains pending', async () => {
  const { css } = await sources();
  assert.equal(facets.browserDecision, 'required-pending');
  assert.equal(facets.rendered200Percent, 'required-pending');
  assert.match(css, /@media\s*\([^)]*(?:max-width|max-inline-size)/);
  assert.doesNotMatch(css, /\.state-rail[^}]*position\s*:\s*(?:fixed|sticky)/s);
  assert.match(css, /overflow-wrap\s*:\s*(?:anywhere|break-word)/);
  assert.doesNotMatch(css, /(?:main|\.narrative)[^{]*\{[^}]*overflow-x\s*:\s*(?:auto|scroll)/s);
});

test('WEB-A11Y-004 staticLogical removes nonessential motion without content loss; rendered motion remains pending', async () => {
  const { css } = await sources();
  assert.equal(facets.browserDecision, 'required-pending');
  assert.equal(facets.renderedReducedMotion, 'required-pending');
  assert.match(css, /@media\s*\(prefers-reduced-motion:\s*reduce\)/);
  assert.match(css, /animation(?:-duration)?\s*:\s*(?:none|0(?:\.0+)?(?:ms|s))/);
  assert.match(css, /transition(?:-duration)?\s*:\s*(?:none|0(?:\.0+)?(?:ms|s))/);
});

test('WEB-STATIC-001 staticLogical keeps all ten acts, facts, limitations and linear navigation in HTML before JS', async () => {
  const { html } = await sources();
  assert.equal(facets.manualDecision, 'required-pending');
  assert.equal(facets.noJsManualComprehension, 'required-pending');
  assert.equal((html.match(/<section\b[^>]*data-act=["']\d+["']/g) ?? []).length, 10);
  for (const fact of ['business decision', 'simulated pipeline', 'controlled failure', 'grain', 'numerator', 'denominator', 'weighting', 'limitations', 'insufficient evidence', 'reflection']) assert.match(html, new RegExp(fact, 'i'));
  assert.match(html, /href=["']#act-\d+["'][^>]*>[^<]*(?:Previous|Trước)/i);
  assert.match(html, /href=["']#act-\d+["'][^>]*>[^<]*(?:Next|Tiếp)/i);
});

test('WEB-TRUST-001 staticLogical renders every concrete fixture fact in its independent semantic card', async () => {
  const { html } = await sources();
  for (const fact of ['Tia Hè', 'web', 'Bưu vận Bắc', 'Miền Bắc', 'không vừa', 'thời trang', 'Miền Trung', 'missing-order-status', '3']) {
    assert.match(html, new RegExp(fact, 'i'), fact);
  }
});
