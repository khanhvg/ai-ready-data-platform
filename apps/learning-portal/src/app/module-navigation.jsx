import React from "react";

export function ModuleNavigation({ catalog }) {
  return <section aria-labelledby="module-lessons"><h2 id="module-lessons">Bài học trong lát cắt</h2>{catalog.modules.flatMap((module) => module.lessons.map((lesson) => <article className="card" key={lesson.id}><h3>{lesson.title}</h3><p>{lesson.summary}</p><p><a className="primary-link" href={lesson.path}>Mở bài học</a></p></article>))}</section>;
}
