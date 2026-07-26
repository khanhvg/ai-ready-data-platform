import React from "react";

export function LessonNavigation({ current, descriptor, labels }) {
  return <nav aria-label="Các bước bài học"><h2>Lộ trình tường thuật</h2><ol className="steps">{descriptor.steps.map((step, index) => <li key={step.id}><a href={step.path} aria-current={current === step.id ? "step" : undefined}>{index + 1}. {step.label ?? labels[step.id] ?? step.id}</a></li>)}</ol></nav>;
}
