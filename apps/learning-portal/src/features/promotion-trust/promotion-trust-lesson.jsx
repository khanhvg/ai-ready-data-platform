import React from "react";
import { LessonNavigation } from "../../app/lesson-navigation.jsx";

export const PROMOTION_TRUST_STEP_LABELS = Object.freeze({ frame: "Đặt câu hỏi", inspect: "Kiểm tra bằng chứng", run: "Hiểu lượt chạy", fail: "Đọc lỗi có kiểm soát", trace: "Truy vết giới hạn", decide: "Ra quyết định", reset: "Hiểu đặt lại", configure: "Cấu hình giả định", verify: "Hiểu xác minh", reflect: "Phản tư kiến trúc" });
const BOUNDARY_STEPS = new Set(["run", "reset", "configure", "verify"]);

export function PromotionTrustLesson({ descriptor, view }) {
  const { lesson, grains } = descriptor.model;
  const isStep = view.kind === "step";
  const step = isStep ? descriptor.steps[view.stepIndex] : null;
  const previous = isStep ? (view.stepIndex === 0 ? descriptor.path : descriptor.steps[view.stepIndex - 1].path) : null;
  const next = isStep ? (view.stepIndex === descriptor.steps.length - 1 ? descriptor.path : descriptor.steps[view.stepIndex + 1].path) : null;
  return <>
    {isStep && <><p className="eyebrow">Bước {view.stepIndex + 1} / {descriptor.steps.length}</p><h2>{step.label ?? PROMOTION_TRUST_STEP_LABELS[step.id]}</h2></>}
    <section aria-labelledby="question"><h2 id="question">Câu hỏi kinh doanh</h2><p lang="en">{lesson.stakeholderQuestion}</p></section>
    <section aria-labelledby="grains"><h2 id="grains">Bốn grain độc lập</h2><ul className="grain-grid">{grains.map((grain) => <li className="grain-card" key={grain.id}><h3>{grain.id}</h3><p><strong>Khóa:</strong> <code>{grain.keys.join(", ")}</code></p><p>{grain.limitation}</p></li>)}</ul></section>
    <section className="decision" aria-labelledby="decision"><h2 id="decision">Kết quả bài học được phát hành</h2><p>Lỗi có kiểm soát: <code>{lesson.controlledFailure.code}</code>. {lesson.controlledFailure.symptom}</p><p><code>decision={lesson.decision.value}</code></p><p><code>reason={lesson.decision.reason}</code></p><p>Không có grain chung để chứng minh quan hệ nhân quả xuyên nguồn.</p></section>
    <LessonNavigation current={view.stepId} descriptor={descriptor} labels={PROMOTION_TRUST_STEP_LABELS} />
    {isStep && BOUNDARY_STEPS.has(view.stepId) && <aside className="boundary"><h2>Chỉ giải thích trong Giai đoạn A</h2><p>Không có điều khiển để chạy, đặt lại hoặc xác minh. Những hành động này chưa được thực hiện.</p></aside>}
    {view.stepId === "reflect" && <section><h2>Phản tư kiến trúc</h2><p lang="en">{lesson.reflection}</p></section>}
    {isStep && <nav className="prev-next" aria-label="Điều hướng bước"><a href={previous}>Bước trước</a><a href={next}>Bước tiếp theo</a></nav>}
  </>;
}
