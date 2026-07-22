import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const NOTICE = 'SYNTHETIC LEARN-PREVIEW — UNSCORED — CANNOT COMPLETE';

test('WEB-PREVIEW-001 staticLogical keeps the exact permanent notice on all authority surfaces', async () => {
  const html = await readFile(new URL('../../preview/index.html', import.meta.url), 'utf8');
  for (const surface of ['entry', 'state-rail', 'verify-evidence', 'export-template']) {
    assert.match(html, new RegExp(`data-notice-surface=["']${surface}["'][^>]*>[\\s\\S]{0,500}${NOTICE}`), surface);
  }
  const state = await import(new URL('../state/preview-state.mjs', import.meta.url));
  const exported = state.exportEvidence(state.createBaselineState());
  assert.equal(exported.notice, NOTICE);
  assert.equal(JSON.stringify(exported).includes('completed'), false);
});
