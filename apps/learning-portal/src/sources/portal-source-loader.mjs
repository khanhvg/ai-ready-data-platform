import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const repositoryRoot = resolve(dirname(fileURLToPath(import.meta.url)), '../../../..');
const LEVELS = Object.freeze([
  ['foundation', 'Nền tảng'],
  ['junior', 'Junior'],
  ['data', 'Dữ liệu'],
  ['mid', 'Mid-level']
]);

const AUTHORITIES = Object.freeze({
  'learning/curriculum/architecture-curriculum-v1.json': 'd7221b143c999d4531d1ee9a1435cafc5fca427eb47b608efa366945b0277a2c',
  'learning/curriculum/modules/foundation-v1.json': 'c3760218a59e3b56fe29e95ee867b679303e990cbd66697f9239dc27f92ab687',
  'learning/curriculum/modules/junior-v1.json': '91a9b8087b385c82dbd34f25e76f58d4158abc741fc068712171278801a15c8a',
  'learning/curriculum/modules/data-v1.json': 'ac77ac4b03f9ed028489d2b06a12e709703084bb7b9294f1d17c8538e70735d3',
  'learning/curriculum/modules/mid-v1.json': '962d4fa85233ce0fc9fb034168177ce844929abad62c678cd5a2cf57b2c21b2a',
  'learning/curriculum/traces/architecture-trace-v1.json': '579acab852cc7fc764be4cdecd1bbf1c68781e8f8fcea65f517675ca6deed449',
  'learning/curriculum/templates/architecture-templates-v1.json': 'bb71273cc4b8d2f077bc8e2f176c8271b96d7a112c16712482f05d8c50e4bcaf',
  'learning/curriculum/patterns/system-design-patterns-v1.json': '98d7088dc609bb657dc4bf3f2e995968eab5ef7e9d9399ad27af038290635104',
  'learning/curriculum/release-binding-i5-06-stage-a-v1.json': 'cc40ecc8ac48d0d4e95b881974bc1e43d38759a11cefb19beded40a3e838a7d7',
  'architecture/expansions/i5-06/rendered/render-manifest.json': '869fba2547246c4a1933042f442908f7e3c795c6b6c9f9e1a021a8ab1872cef6',
  'learning/labs/data-platform/deterministic-ingest/lab-v1.json': 'be9874e825a17f527514c14ebf2184493ec868c73aab705dcb668008166b0785',
  'learning/labs/data-platform/deterministic-ingest/content.vi.md': 'd9a1542ab87f4735447bd73480fe3eb3e4ac490e9c1d0e0979d4e2d88bb33752',
  'learning/labs/data-platform/model-quality/lab-v1.json': '0b7a4301eba9b4f14008eac469a1a1f2e31b6a02c9579890b0be3d0e2326581f',
  'learning/labs/data-platform/model-quality/content.vi.md': '887685b8fffb17b43084a6aa396bc91dbad4e2635fe1aa12d359fed81451ff4f',
  'learning/labs/data-platform/weighted-metrics/lab-v1.json': '06ad138dc9de782b537d6db6ae4b8a0197a39e2940e59450011959e172c454e8',
  'learning/labs/data-platform/weighted-metrics/content.vi.md': '3a0c5bb6262e21b40d2cce51398d118e16188c2e13042bce4fc433821b713fd2'
  ,'learning/lessons/promotion-trust/lesson-v1.json': '758c6fb1ad75b283c313536d61bee61655bba6d27a2e685825ca20a28c838675'
  ,'learning/labs/promotion-trust/lab-v1.json': '89ece51f41a17821d3266d2ba1fb7680cb70b07c2e9c5566d473aac9978d42d8'
  ,'learning/manifests/promotion-trust-v1.json': '553b97ed5dc44b77564ae50b1a2211205cbd1a759f3578e5e4dfcefef99044ac'
  ,'learning/bindings/vite/promotion-trust-v1.json': '03d2aa6bd9fa178e6075865364a8ae8b83ce548c42b450d1858b451b45d0d1d0'
  ,'learning/contracts/learning-contract-set-v1.json': '92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638'
});

const LABS = Object.freeze([
  ['deterministic-ingest', 'Ingest xác định và grain', ['make seed SCALE=small SEED=42', 'make load', 'make health']],
  ['model-quality', 'Lớp mô hình và chất lượng', ['make dbt']],
  ['weighted-metrics', 'Metric có trọng số', ['make bi']]
]);

function sha256(bytes) {
  return createHash('sha256').update(bytes).digest('hex');
}

function readAuthority(path) {
  const bytes = readFileSync(resolve(repositoryRoot, path));
  if (sha256(bytes) !== AUTHORITIES[path]) throw new Error(`PORTAL_SOURCE_HASH_MISMATCH:${path}`);
  return bytes;
}

function readJson(path) {
  return JSON.parse(readAuthority(path));
}

function sections(markdown) {
  const result = {};
  let key = 'Giới thiệu';
  for (const line of markdown.split('\n')) {
    const heading = /^## (.+)$/.exec(line);
    if (heading) {
      key = heading[1].trim();
      result[key] = [];
    } else if (result[key]) result[key].push(line);
  }
  return Object.fromEntries(Object.entries(result).map(([name, lines]) => [name, lines.join('\n').trim()]));
}

function assertExact(condition, code) {
  if (!condition) throw new Error(`PORTAL_SOURCE_BINDING_INVALID:${code}`);
}

export function loadPortalCatalog() {
  const curriculum = readJson('learning/curriculum/architecture-curriculum-v1.json');
  const collections = LEVELS.map(([id, label]) => ({
    id,
    label,
    ...readJson(`learning/curriculum/modules/${id}-v1.json`)
  }));
  const trace = readJson('learning/curriculum/traces/architecture-trace-v1.json');
  const templates = readJson('learning/curriculum/templates/architecture-templates-v1.json');
  const patterns = readJson('learning/curriculum/patterns/system-design-patterns-v1.json');
  const release = readJson('learning/curriculum/release-binding-i5-06-stage-a-v1.json');
  const renderManifest = readJson('architecture/expansions/i5-06/rendered/render-manifest.json');
  const rootMakefile = readFileSync(resolve(repositoryRoot, 'Makefile'), 'utf8');
  for (const target of ['seed', 'load', 'health', 'dbt', 'bi']) {
    assertExact(new RegExp(`^${target}:`, 'm').test(rootMakefile), `MAKE_TARGET_${target}`);
  }
  const modules = collections.flatMap((collection) =>
    collection.modules.map((module) => ({ ...module, collectionId: collection.id, collectionLabel: collection.label }))
  );
  const expectedIds = ['F01','F02','F03','F04','J01','J02','J03','J04','J05','J06','D01','D02','D03','D04','D05','D06','M01','M02','M03','M04'];
  assertExact(curriculum.schemaVersion === 'i5-06-architecture-curriculum-v1', 'CURRICULUM_VERSION');
  assertExact(release.schemaVersion === 'i5-06-architecture-release-binding-v1', 'RELEASE_VERSION');
  assertExact(collections.every(({ schemaVersion }) => schemaVersion === 'i5-06-architecture-module-collection-v1'), 'MODULE_VERSION');
  assertExact(JSON.stringify(modules.map(({ id }) => id)) === JSON.stringify(expectedIds), 'MODULE_IDS');
  assertExact(curriculum.modules.length === 20 && modules.length === 20, 'MODULE_COUNT');
  assertExact(modules.every((module, index) => module.learningSignature === curriculum.modules[index].learningSignature), 'MODULE_SIGNATURE');
  const moduleFields = ['adrOrPattern','capability','concern','controlledFailure','evidence','hints','implementationIntent','operationsConsequence','options','outcome','requiredViews','requirements','reset','solution','starter','task','tradeOffReflection','verify'];
  assertExact(modules.every((module) => moduleFields.every((field) => Object.hasOwn(module, field))), 'MODULE_REQUIRED_FIELDS');
  assertExact(curriculum.criticalFlows.length === 11 && trace.criticalFlows.length === 11, 'FLOW_COUNT');
  assertExact(trace.bridges.length === 8 && new Set(trace.topology.bridgeIds).size === 8, 'BRIDGE_COUNT');
  assertExact(curriculum.views.length === 5 && renderManifest.views.length === 5, 'VIEW_COUNT');
  assertExact(templates.templates.length === 12 && patterns.patterns.length === 2, 'REGISTRY_COUNT');

  const views = curriculum.views.map((view, index) => {
    const rendered = renderManifest.views[index];
    assertExact(rendered.viewId === view.id, `VIEW_ID_${view.id}`);
    const base = `architecture/expansions/i5-06/rendered/${view.id}`;
    const svg = readFileSync(resolve(repositoryRoot, `${base}.svg`));
    const text = readFileSync(resolve(repositoryRoot, `${base}.txt`));
    assertExact(sha256(svg) === rendered.svgSha256 && sha256(text) === rendered.textSha256, `VIEW_HASH_${view.id}`);
    assertExact(!/<(?:script|foreignObject)\b|\son[a-z]+\s*=|(?:href|src)\s*=\s*["'](?:https?:|\/\/)/i.test(svg.toString('utf8')), `VIEW_ACTIVE_CONTENT_${view.id}`);
    return { ...view, ...rendered, assetPath: `/architecture/${view.id}.svg`, text: text.toString('utf8').trim() };
  });

  const labs = LABS.map(([slug, title, commands]) => {
    const descriptorPath = `learning/labs/data-platform/${slug}/lab-v1.json`;
    const contentPath = `learning/labs/data-platform/${slug}/content.vi.md`;
    const descriptor = readJson(descriptorPath);
    const markdown = readAuthority(contentPath).toString('utf8');
    assertExact(descriptor.schemaVersion === 'lab-v1' && descriptor.id === `data-platform-${slug}-v1`, `LAB_${slug}`);
    assertExact(descriptor.commands.every(({ id }) => id.startsWith('candidate.')), `LAB_COMMAND_BOUNDARY_${slug}`);
    return { slug, title, descriptor, markdown, sections: sections(markdown), commands, descriptorPath, contentPath };
  });

  const promotionLesson = readJson('learning/lessons/promotion-trust/lesson-v1.json');
  const promotionLab = readJson('learning/labs/promotion-trust/lab-v1.json');
  const promotionManifest = readJson('learning/manifests/promotion-trust-v1.json');
  const promotionBinding = readJson('learning/bindings/vite/promotion-trust-v1.json');
  const contractSet = readJson('learning/contracts/learning-contract-set-v1.json');
  assertExact(promotionLesson.schemaVersion === 'lesson-v1' && promotionLesson.id === 'promotion-trust', 'PROMOTION_LESSON');
  assertExact(promotionLab.schemaVersion === 'lab-v1' && promotionLab.lessonId === promotionLesson.id, 'PROMOTION_LAB');
  assertExact(promotionManifest.schemaVersion === 'promotion-trust-learning-manifest-v1' && promotionManifest.lesson.sha256 === AUTHORITIES['learning/lessons/promotion-trust/lesson-v1.json'] && promotionManifest.lab.sha256 === AUTHORITIES['learning/labs/promotion-trust/lab-v1.json'], 'PROMOTION_MANIFEST');
  assertExact(promotionBinding.schemaVersion === 'promotion-trust-vite-binding-v1' && promotionBinding.stageA.contractSet.sha256 === AUTHORITIES['learning/contracts/learning-contract-set-v1.json'] && promotionBinding.stageA.promotionManifest.sha256 === AUTHORITIES['learning/manifests/promotion-trust-v1.json'], 'PROMOTION_BINDING');
  assertExact(contractSet.schemaVersion === 'learning-contract-set-v1' && contractSet.contracts.some(({ path, contentSha256 }) => path === 'learning/lessons/promotion-trust/lesson-v1.json' && contentSha256 === AUTHORITIES[path]), 'PROMOTION_CONTRACT_SET');
  return Object.freeze({
    schemaVersion: 'portal-read-only-catalog-v1',
    locale: 'vi',
    sourceHashes: AUTHORITIES,
    curriculum: { ...curriculum, collections, modules },
    architecture: { trace, templates, patterns, views },
    labs,
    promotionTrust: { path: '/lessons/promotion-trust', title: 'Độ tin cậy của quyết định khuyến mãi', lesson: promotionLesson },
    counts: { modules: 20, flows: 11, bridges: 8, views: 5, templates: 12, patterns: 2, labs: 3 },
    manualOnly: true
  });
}

export { AUTHORITIES, repositoryRoot };
