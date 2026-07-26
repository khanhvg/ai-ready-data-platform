import { findLesson } from "../catalog/module-catalog.mjs";
import { PROMOTION_TRUST_PRESENTATION } from "../contracts/released-learning-adapter.mjs";

const escape = (value) => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#39;");

function promotionTrustMarkup(view, descriptor) {
  const { lesson, grains } = descriptor.model;
  const labels = PROMOTION_TRUST_PRESENTATION.stepLabels;
  const grainCards = grains.map((grain) => `<li class="grain-card"><h3>${escape(grain.id)}</h3><p><strong>Khóa:</strong> <code>${escape(grain.keys.join(", "))}</code></p><p>${escape(grain.limitation)}</p></li>`).join("");
  const stepList = descriptor.steps.map((step, index) => `<li><a href="${step.path}"${view.stepId === step.id ? ' aria-current="step"' : ""}>${index + 1}. ${escape(step.label ?? labels[step.id] ?? step.id)}</a></li>`).join("");
  let specific = `<section aria-labelledby="question"><h2 id="question">Câu hỏi kinh doanh</h2><p lang="en">${escape(lesson.stakeholderQuestion)}</p></section><section aria-labelledby="grains"><h2 id="grains">Bốn grain độc lập</h2><ul class="grain-grid">${grainCards}</ul></section><section class="decision" aria-labelledby="decision"><h2 id="decision">Kết quả bài học được phát hành</h2><p>Lỗi có kiểm soát: <code>${escape(lesson.controlledFailure.code)}</code>. ${escape(lesson.controlledFailure.symptom)}</p><p><code>decision=${escape(lesson.decision.value)}</code></p><p><code>reason=${escape(lesson.decision.reason)}</code></p><p>Không có grain chung để chứng minh quan hệ nhân quả xuyên nguồn.</p></section><nav aria-label="Các bước bài học"><h2>Lộ trình tường thuật</h2><ol class="steps">${stepList}</ol></nav>`;
  if (view.kind === "step") {
    const step = descriptor.steps[view.stepIndex];
    const previous = view.stepIndex === 0 ? descriptor.path : descriptor.steps[view.stepIndex - 1].path;
    const next = view.stepIndex === descriptor.steps.length - 1 ? descriptor.path : descriptor.steps[view.stepIndex + 1].path;
    const boundary = PROMOTION_TRUST_PRESENTATION.boundarySteps.includes(step.id) ? `<aside class="boundary"><h2>Chỉ giải thích trong Giai đoạn A</h2><p>Không có điều khiển để chạy, đặt lại hoặc xác minh. Những hành động này chưa được thực hiện.</p></aside>` : "";
    specific = `<p class="eyebrow">Bước ${view.stepIndex + 1} / ${descriptor.steps.length}</p><h2>${escape(step.label ?? labels[step.id] ?? step.id)}</h2>${specific}${boundary}${step.id === "reflect" ? `<section><h2>Phản tư kiến trúc</h2><p lang="en">${escape(lesson.reflection)}</p></section>` : ""}<nav class="prev-next" aria-label="Điều hướng bước"><a href="${previous}">Bước trước</a><a href="${next}">Bước tiếp theo</a></nav>`;
  }
  return specific;
}

const staticAdapters = Object.freeze({ "promotion-trust": promotionTrustMarkup });

export function contentMarkup(view, catalog) {
  const descriptor = view.lessonId ? findLesson(catalog, view.lessonId) : ["lesson", "step"].includes(view.kind) ? catalog.modules.flatMap((module) => module.lessons).find((lesson) => view.path === lesson.path || view.path.startsWith(`${lesson.path}/step/`)) ?? null : null;
  if (["lesson", "step"].includes(view.kind) && !descriptor) throw new Error("CATALOG_ROUTE_DESCRIPTOR_MISSING");
  const adapter = descriptor ? staticAdapters[descriptor.adapterId] : null;
  if (descriptor && !adapter) throw new Error("CATALOG_ADAPTER_UNKNOWN");
  const breadcrumbs = [["/", "Danh mục"], ...(view.kind === "catalog" ? [] : [["/module", "Mô-đun"]]), ...(descriptor ? [[descriptor.path, descriptor.title]] : []), ...(view.kind === "step" ? [[view.path, descriptor.steps[view.stepIndex].label ?? PROMOTION_TRUST_PRESENTATION.stepLabels[view.stepId] ?? view.stepId]] : [])];
  let specific = `<h2>Một lát cắt dọc</h2><p>Khám phá câu hỏi kinh doanh, bằng chứng và quyết định có kiểm soát.</p><p><a class="primary-link" href="/module">Mở mô-đun trình bày</a></p>`;
  if (view.kind === "module") specific = `<h2>Bài học trong lát cắt</h2>${catalog.modules.flatMap((module) => module.lessons).map((lesson) => `<article class="card"><h3>${escape(lesson.title)}</h3><p>${escape(lesson.summary)}</p><p><a class="primary-link" href="${lesson.path}">Mở bài học</a></p></article>`).join("")}`;
  if (adapter) specific = adapter(view, descriptor);
  if (view.kind === "not-found") specific = `<h2>Không tìm thấy trang</h2><p>Đường dẫn không thuộc lát cắt đã phát hành.</p><p><a href="/">Về danh mục</a></p>`;
  const title = view.kind === "catalog" ? "Danh mục học tập" : view.kind === "module" ? "Mô-đun trình bày" : view.kind === "not-found" ? "Đường dẫn không hợp lệ" : descriptor.title;
  return `<a class="skip-link" href="#main-content">Bỏ qua đến nội dung chính</a><header><a class="brand" href="/">Cổng học AI-ready</a><span class="maturity">Bản học tĩnh — Giai đoạn A</span><nav aria-label="Điều hướng chính"><a href="/">Danh mục</a><a href="/module">Mô-đun</a></nav></header><nav class="breadcrumbs" aria-label="Đường dẫn"><ol>${breadcrumbs.map(([href, label], i) => `<li><a href="${href}"${i === breadcrumbs.length - 1 ? ' aria-current="page"' : ""}>${escape(label)}</a></li>`).join("")}</ol></nav><main id="main-content" data-product-scope="static-portal-slice" data-runner="unavailable" data-execution="disabled" data-reset="not-run" data-fresh-evidence="false" data-progress="disabled" data-completion="disabled"><p class="eyebrow">Lát cắt học tập tĩnh</p><h1>${escape(title)}</h1><p class="not-full">Chưa phải sản phẩm học tập đầy đủ.</p><aside class="status" aria-labelledby="availability"><h2 id="availability">Khả năng thực thi của cổng</h2><p><strong>Trình chạy không khả dụng.</strong> Không có thao tác chạy, đặt lại, bằng chứng mới, tiến độ hoặc hoàn thành.</p></aside>${specific}</main><footer><p>static-portal-stage-a · Chỉ đọc · Không ghi nhận hoàn thành</p></footer>`;
}

export function renderStaticDocument(view, catalog, assets = {}) {
  const title = view.kind === "not-found" ? "Không tìm thấy" : "Cổng học AI-ready";
  const script = assets.script ? `<script type="module" src="${escape(assets.script)}"></script>` : "";
  const style = assets.style ? `<link rel="stylesheet" href="${escape(assets.style)}">` : '<link rel="stylesheet" href="/assets/portal.css">';
  return `<!doctype html><html lang="vi"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><link rel="icon" href="data:,"><title>${title}</title>${style}</head><body><div id="root">${contentMarkup(view, catalog)}</div><div id="route-status" class="sr-only" aria-live="polite"></div>${script}</body></html>`;
}
