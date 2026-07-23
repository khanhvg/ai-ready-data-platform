import assert from 'node:assert/strict';
import test from 'node:test';
import { loadPortalCatalog } from '../../src/sources/portal-source-loader.mjs';
import { renderStaticDocument } from '../../src/render/static-document.mjs';
import { derivePortalRoutes } from '../../src/routing/portal-router.mjs';

const catalog=loadPortalCatalog(); const routes=derivePortalRoutes(catalog);
test('every route renders Vietnamese core content and read-only markers without JavaScript',()=>{
  for(const route of routes){const html=renderStaticDocument(route,catalog);assert.match(html,/lang="vi"/);assert.match(html,/data-read-only="true"/);assert.match(html,/data-manual-only="true"/);assert.doesNotMatch(html,/<form\b|<button\b/i);}
});
test('module, architecture, lab, and promotion content retain released facts',()=>{
  const module=renderStaticDocument(routes.find(({path})=>path==='/curriculum/f01'),catalog); assert.match(module,/Concern/);assert.match(module,/Functional requirement|<strong>FR/);assert.match(module,/Controlled failure/);assert.match(module,/Checklist/);
  const architecture=renderStaticDocument(routes.find(({path})=>path==='/architecture'),catalog); assert.equal((architecture.match(/<figure/g)||[]).length,5);assert.match(architecture,/11 critical flow/);assert.match(architecture,/8 bridge/);
  const lab=renderStaticDocument(routes.find(({path})=>path==='/labs/deterministic-ingest'),catalog);assert.match(lab,/Thực hành thủ công tại local/);assert.match(lab,/<pre class="command"><code>make seed SCALE=small SEED=42/);assert.match(lab,/Solution gate/);
  assert.match(renderStaticDocument(routes.find(({path})=>path==='/lessons/promotion-trust'),catalog),/insufficient-evidence\/no-common-grain/);
});
