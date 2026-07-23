import { createSafeViewModel } from '../contracts/safe-view-model.mjs';

function escapeText(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

export function renderStaticDocument(route, catalog, assets = { scripts: [], styles: [] }) {
  const model = createSafeViewModel(route, catalog);
  const navigation = model.navigation
    .map(
      (item) =>
        `<a href="${escapeText(item.path)}"${
          item.path === model.routePath ? ' aria-current="page"' : ''
        }>${escapeText(item.label)}</a>`
    )
    .join('');
  const scripts = (assets.scripts ?? [])
    .map((source) => `<script type="module" src="${escapeText(source)}"></script>`)
    .join('');
  const styles = (assets.styles ?? [])
    .map((source) => `<link rel="stylesheet" href="${escapeText(source)}">`)
    .join('');
  const factAttributes = model.factIds
    .map((factId) => `<span class="visually-hidden" data-fact-id="${escapeText(factId)}"></span>`)
    .join('');
  const grains = model.sourceGrains
    .map(
      (grain) => `<article class="grain-card" data-fact-id="grain-${escapeText(grain.id)}">
<h4>${escapeText(grain.displayId)}</h4><p>Khóa: ${escapeText(grain.keys.join(' · '))}</p>
<p>Không được nối suy diễn với ba grain còn lại.</p></article>`
    )
    .join('');
  const limitations = (model.lesson?.limitations ?? [])
    .map(
      ({ id, statement }) =>
        `<li data-fact-id="limitation-${escapeText(id)}"><strong>${escapeText(id)}</strong>: ${escapeText(statement)}</li>`
    )
    .join('');
  const hints = (model.lesson?.hints ?? [])
    .map(
      ({ order, id }) =>
        `<li>${escapeText(order)}. ${escapeText(id)} — chỉ hướng dẫn, không hoàn thành bài.</li>`
    )
    .join('');
  const step = model.step
    ? `<section class="selected-step"><p class="section-label">Đang xem</p><h3>Bước ${escapeText(model.step.order)}: ${escapeText(model.step.id)}</h3><p>Bước tường thuật có bản tương đương tĩnh; không có thao tác chạy, đặt lại hay xác minh.</p></section>`
    : '';
  const stepNavigation = model.navigation
    .filter(({ path }) => path.includes('/steps/'))
    .map(({ label }) => `<li><span>${escapeText(label)}</span></li>`)
    .join('');
  return `<!doctype html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%23154f3d'/%3E%3Cpath d='M8 9h16v3H8zm0 6h12v3H8zm0 6h9v3H8z' fill='white'/%3E%3C/svg%3E">
<title>${escapeText(model.heading)}</title>
${styles}
</head>
<body>
<div id="root">
<div class="portal-shell" data-review-inventory="closed" data-s3-coverage="14" data-semantic-ready="${String(model.semanticReady)}">
<header class="masthead"><div><p class="eyebrow">${escapeText(model.eyebrow)}</p><h1>${escapeText(model.heading)}</h1></div><p class="maturity">Một lát cắt trình bày · chưa phải khóa học đầy đủ</p></header>
<nav class="module-navigation" aria-label="Điều hướng cổng học tập">${navigation}</nav>
<div class="portal-grid">
<aside class="lesson-navigation" aria-label="Mười bước tường thuật đã phát hành"><p class="section-label">10 bước · chỉ đọc</p><ol>${stepNavigation}</ol></aside>
<main id="lesson-content" tabindex="-1">
<section aria-live="polite" class="portal-status"><h2>Giới hạn của Stage A</h2><p>${escapeText(model.message)}</p></section>
<article class="lesson-card">
<header><p class="section-label">Bài học đại diện</p><h2>${escapeText(model.lesson?.titleVi ?? model.lesson?.title)}</h2><p class="lede">${escapeText(model.lesson?.summaryVi ?? model.lesson?.summary)}</p></header>
${step}
<section><p class="section-label">Kết luận được phát hành</p><h3>${escapeText(model.lesson?.decision?.question)}</h3><p class="decision" data-fact-id="decision-${escapeText(model.lesson?.decision?.status)}">${escapeText(model.lesson?.decision?.status)}</p><p>Giữ bốn grain độc lập; không có grain chung để quy kết quan hệ nhân quả.</p></section>
<section><p class="section-label">Bốn grain độc lập</p><h3>Phạm vi bằng chứng</h3><div class="grain-grid">${grains}</div></section>
<section><p class="section-label">Giới hạn</p><h3>Điều bằng chứng không chứng minh</h3><ul>${limitations}</ul></section>
<section><p class="section-label">Gợi ý theo thứ tự</p><h3>Quan sát trước khi kết luận</h3><ol>${hints}</ol></section>
<section class="reflection"><p class="section-label">Phản tư về đánh đổi</p><h3>${escapeText(model.lesson?.reflection?.prompt)}</h3><p>Thêm một grain chỉ hợp lệ khi được phát hành qua hợp đồng đã duyệt; Stage A không tự tạo grain chung.</p></section>
${factAttributes}
</article>
</main>
</div>
</div>
</div>
${scripts}
</body>
</html>
`;
}
