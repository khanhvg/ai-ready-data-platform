function escapeHtml(value) {
  return String(value ?? '').replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
}
const e = escapeHtml;
const link = (path, label) => `<a href="${e(path)}">${e(label)}</a>`;
const list = (items) => `<ul>${items.map((item) => `<li>${e(item)}</li>`).join('')}</ul>`;

function home(catalog) {
  return `<p class="kicker">Đọc · hiểu · tự thực hành tại local</p><h1>Nền tảng dữ liệu sẵn sàng cho AI</h1><p class="lede">Một sản phẩm học tập chỉ đọc bằng tiếng Việt: 20 mô-đun kiến trúc, 5 góc nhìn nguồn, và 3 lab hướng dẫn thủ công. Website không chạy lệnh và không ghi nhận hoàn thành.</p><div class="stats"><span><strong>${catalog.counts.modules}</strong> mô-đun</span><span><strong>${catalog.counts.views}</strong> sơ đồ</span><span><strong>${catalog.counts.labs}</strong> lab thủ công</span></div><div class="card-grid"><article><h2>Lộ trình kiến trúc</h2>${link('/curriculum','Mở lộ trình →')}</article><article><h2>Năm góc nhìn</h2>${link('/architecture','Xem kiến trúc →')}</article><article><h2>Lab tại local</h2>${link('/labs','Đọc hướng dẫn →')}</article></div><aside class="notice"><strong>Phạm vi an toàn:</strong> không runner, không Docker, không cloud, không progress, không thao tác ghi.</aside>`;
}

function curriculum(catalog) {
  return `<p class="kicker">Lộ trình phát hành</p><h1>20 mô-đun, bốn cấp độ</h1><p class="lede">Học theo thứ tự foundation → junior → data → mid.</p><nav class="toc" aria-label="Mục lục lộ trình">${catalog.curriculum.collections.map((collection) => link(`#${collection.id}`,collection.label)).join('')}</nav>${catalog.curriculum.collections.map((collection) => `<section id="${collection.id}"><h2>${e(collection.label)}</h2><div class="module-list">${collection.modules.map((module) => `<a class="module-row" href="/curriculum/${module.id.toLowerCase()}"><span class="module-id">${module.id}</span><span><strong>${e(module.outcome)}</strong><small>${e(module.capability)}</small></span><span>→</span></a>`).join('')}</div></section>`).join('')}<aside class="notice">Bài đọc mẫu: ${link('/lessons/promotion-trust','Độ tin cậy của quyết định khuyến mãi')}.</aside>`;
}

function modulePage(module) {
  const c = module.operationsConsequence;
  return `<p class="kicker">${e(module.collectionLabel)} · Mô-đun ${module.id}</p><h1>${e(module.outcome)}</h1><p class="lede">${e(module.capability)}</p><nav class="toc" aria-label="Mục lục bài học"><a href="#context">Bối cảnh</a><a href="#decision">Quyết định</a><a href="#exercise">Bài tập tư duy</a><a href="#verify">Xác minh</a></nav><section id="context"><h2>Bối cảnh và yêu cầu</h2><p><strong>Concern:</strong> ${e(module.concern)}</p><p><strong>FR:</strong> ${e(module.requirements.functional)}</p><p><strong>NFR:</strong> ${e(module.requirements.nonFunctional)}</p></section><section id="decision"><h2>Quyết định và hệ quả</h2>${list(module.options)}<p><strong>ADR / pattern:</strong> <code>${e(module.adrOrPattern)}</code></p><p><strong>Implementation intent:</strong> ${e(module.implementationIntent)}</p><p><strong>Required views:</strong> ${e(module.requiredViews.join(', '))}</p>${list([c.operations,c.security,c.resilience,c.cost,c.governance])}</section><section id="exercise"><h2>Thought exercise có kiểm soát</h2><h3>Starter</h3><p>${e(module.starter.prompt)}</p><h3>Nhiệm vụ</h3><p>${e(module.task.instruction)}</p><h3>Controlled failure</h3><p>${e(module.controlledFailure.scenario)}</p><p class="manual-label">Chỉ suy luận trên giấy / workspace riêng · website không thực thi</p><h3>Gợi ý</h3>${list(module.hints.map(({ text }) => text))}<details><summary>Lời giải tham chiếu — mở sau khi đã dùng gợi ý</summary><p>${e(module.solution.intent)}</p></details></section><section id="verify"><h2>Checklist xác minh</h2>${list([module.verify.verifier,module.evidence.required,...module.requiredViews])}<h3>Reset an toàn</h3><p>${e(module.reset.procedure)}</p></section><section><h2>Phản tư đánh đổi</h2><p>${e(module.tradeOffReflection.reflection)}</p></section>`;
}

function architecture(catalog) {
  const a = catalog.architecture;
  return `<p class="kicker">Architecture trace</p><h1>Năm góc nhìn từ source</h1><p class="lede">Mỗi SVG được xác minh hash và có text alternative.</p><section>${a.views.map((view) => `<figure class="architecture-view"><h2>${view.id} · ${e(view.concern)}</h2><img src="${view.assetPath}" alt="Sơ đồ ${view.id}: ${e(view.concern)}" width="1200" height="800" loading="lazy"><figcaption>${e(view.concern)}. ${link(view.assetPath.replace('.svg','.txt'),'Mở text alternative')}.</figcaption><details><summary>Nội dung thay thế dạng văn bản</summary><pre><code>${e(view.text)}</code></pre></details></figure>`).join('')}</section><section><h2>11 critical flow</h2>${catalog.curriculum.criticalFlows.map((flow) => `<article><h3>${flow.id}</h3>${list(flow.steps)}</article>`).join('')}</section><section><h2>8 bridge local ↔ AWS</h2>${a.trace.bridges.map((bridge) => `<p><strong>${bridge.id}</strong>: ${e(bridge.divergence)}</p>`).join('')}</section><section><h2>Template và pattern</h2><p>${a.templates.templates.length} template · ${a.patterns.patterns.length} pattern</p>${list(a.templates.templates.map((template) => `${template.id}: ${template.purpose}`))}${list(a.patterns.patterns.map((pattern) => `${pattern.id}: ${pattern.force} → ${pattern.failure}`))}</section>`;
}

function labs(catalog) {
  return `<p class="kicker">Manual labs</p><h1>Ba lab tự thực hành tại local</h1><p class="lede">Website không kết nối terminal, không chạy lệnh và không tuyên bố hoàn thành.</p><div class="card-grid">${catalog.labs.map((lab) => `<article><h2>${e(lab.title)}</h2><p><code>${e(lab.descriptor.id)}</code></p>${link(`/labs/${lab.slug}`,'Mở hướng dẫn →')}</article>`).join('')}</div>`;
}

function labPage(lab) {
  const s = lab.sections;
  const section = (name) => `<h2>${e(name)}</h2><p class="source-text">${e(s[name] ?? '')}</p>`;
  return `<p class="manual-label">Thực hành thủ công tại local</p><h1>${e(lab.title)}</h1><p class="lede">Website chỉ trình bày hướng dẫn; không có completion state.</p><nav class="toc" aria-label="Mục lục lab"><a href="#commands">Lệnh</a><a href="#reset">Reset</a></nav>${section('Điều kiện tiên quyết')}${section('Bộ khởi đầu')}${section('Nhiệm vụ')}<section id="commands"><h2>Lệnh terminal hiện có trong repo</h2><p>Chạy thủ công từ repository root. Đây là văn bản, không phải nút thực thi.</p>${lab.commands.map((command) => `<pre class="command"><code>${e(command)}</code></pre>`).join('')}</section>${section('Lỗi có kiểm soát')}<h2>Gợi ý</h2>${['Gợi ý 1','Gợi ý 2','Gợi ý 3'].map((name) => `<details><summary>${name}</summary><p>${e(s[name])}</p></details>`).join('')}<h2>Expected checks và evidence</h2><p>${e(s['Xác minh'])}</p><p>${e(s['Evidence bất biến'])}</p><section id="reset"><h2>Reset an toàn, đúng phạm vi</h2><p>${e(s.Reset)}</p><p>Không dùng broad cleanup hoặc tự bịa lệnh reset.</p></section><h2>Solution gate</h2><details><summary>Mở lời giải có khóa</summary><p>${e(s['Lời giải có khóa'])}</p></details><h2>Phản tư trade-off</h2><p>${e(s['Phản tư đánh đổi'])}</p>`;
}

function promotion(catalog, route) {
  const lesson = catalog.promotionTrust.lesson;
  const step = lesson.narrativeSteps.find(({ id }) => id === route.stepId);
  return `<p class="kicker">Bài đọc mẫu phát hành</p><h1>${e(catalog.promotionTrust.title)}</h1><p class="lede">${e(lesson.summary)}</p><aside class="notice">Kết luận nguồn: <strong>${e(lesson.decision.status)}</strong>.</aside>${step ? `<section><h2>Bước ${step.order}: ${e(step.id)}</h2><p>Static equivalent: ${step.staticEquivalent} · reversible: ${step.reversible}.</p></section>` : `<section><h2>Câu hỏi quyết định</h2><p>${e(lesson.decision.question)}</p></section><section><h2>10 bước đọc</h2>${lesson.narrativeSteps.map((item) => link(`/lessons/promotion-trust/steps/${item.id}`,`Bước ${item.order}: ${item.id}`)).join('<br>')}</section>`}`;
}

function content(route, catalog) {
  if (route.kind === 'home') return home(catalog);
  if (route.kind === 'curriculum') return curriculum(catalog);
  if (route.kind === 'module') return modulePage(catalog.curriculum.modules.find(({ id }) => id === route.moduleId));
  if (route.kind === 'architecture') return architecture(catalog);
  if (route.kind === 'labs') return labs(catalog);
  if (route.kind === 'lab') return labPage(catalog.labs.find(({ slug }) => slug === route.labSlug));
  return promotion(catalog, route);
}

export function renderStaticDocument(route, catalog, assets = {}) {
  const scripts = (assets.scripts ?? []).map((src) => `<script type="module" src="${e(src)}"></script>`).join('');
  const styles = (assets.styles ?? []).map((href) => `<link rel="stylesheet" href="${e(href)}">`).join('');
  return `<!doctype html><html lang="vi"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><meta name="description" content="Cổng học tập nền tảng dữ liệu chỉ đọc"><title>${e(route.label)} · Data Learning</title>${styles}${scripts}</head><body><div id="root"><div class="portal-shell" data-read-only="true" data-manual-only="true" data-semantic-ready="true"><a class="skip-link" href="#main-content">Bỏ qua điều hướng</a><header class="masthead">${link('/','AI Data Learning')}<nav aria-label="Điều hướng chính">${link('/curriculum','Lộ trình')}${link('/architecture','Kiến trúc')}${link('/labs','Lab thủ công')}</nav></header><div class="page"><nav aria-label="Đường dẫn"><ol class="breadcrumbs"><li>${link('/','Trang chủ')}</li><li aria-current="page">${e(route.label)}</li></ol></nav><main id="main-content" tabindex="-1">${content(route,catalog)}</main><nav class="pager" aria-label="Bài trước và bài sau">${route.previous ? link(route.previous.path,`← ${route.previous.label}`) : ''}${route.next ? link(route.next.path,`${route.next.label} →`) : ''}</nav></div><footer><p>Stage A · đọc và học · manual-only</p><p>Không runner · không storage · không cloud</p></footer></div></div></body></html>`;
}
