import React from "react";
import { LessonNavigation, STEP_LABELS } from "../../app/lesson-navigation.jsx";
import { STEP_IDS } from "../../routing/portal-router.mjs";

export function PromotionTrustLesson({ lesson, grains, view }) {
  const isStep = view.kind === "step";
  const boundary = isStep && ["run", "reset", "configure", "verify"].includes(view.stepId);
  const previous = isStep ? (view.stepIndex === 0 ? "/lesson/promotion-trust" : `/lesson/promotion-trust/step/${STEP_IDS[view.stepIndex - 1]}`) : null;
  const next = isStep ? (view.stepIndex === STEP_IDS.length - 1 ? "/lesson/promotion-trust" : `/lesson/promotion-trust/step/${STEP_IDS[view.stepIndex + 1]}`) : null;
  return <>
    {isStep && <><p className="eyebrow">Bước {view.stepIndex + 1} / {STEP_IDS.length}</p><h2>{STEP_LABELS[view.stepId]}</h2></>}
    <section aria-labelledby="question"><h2 id="question">Câu hỏi kinh doanh</h2><p lang="en">{lesson.stakeholderQuestion}</p></section>
    <section aria-labelledby="grains"><h2 id="grains">Bốn grain độc lập</h2><ul className="grain-grid">{grains.map((grain) => <li className="grain-card" key={grain.id}><h3>{grain.id}</h3><p><strong>Khóa:</strong> <code>{grain.keys.join(", ")}</code></p><p>{grain.limitation}</p></li>)}</ul></section>
    <section className="decision" aria-labelledby="decision"><h2 id="decision">Kết quả bài học được phát hành</h2><p>Lỗi có kiểm soát: <code>{lesson.controlledFailure.code}</code>. {lesson.controlledFailure.symptom}</p><p><code>decision={lesson.decision.value}</code></p><p><code>reason={lesson.decision.reason}</code></p><p>Không có grain chung để chứng minh quan hệ nhân quả xuyên nguồn.</p></section>
    <LessonNavigation current={view.stepId} />
    {boundary && <aside className="boundary"><h2>Chỉ giải thích trong Giai đoạn A</h2><p>Không có điều khiển để chạy, đặt lại hoặc xác minh. Những hành động này chưa được thực hiện.</p></aside>}
    {view.stepId === "reflect" && <section><h2>Phản tư kiến trúc</h2><p lang="en">{lesson.reflection}</p></section>}
    {isStep && <nav className="prev-next" aria-label="Điều hướng bước"><a href={previous}>Bước trước</a><a href={next}>Bước tiếp theo</a></nav>}
  </>;
}
