import React from "react";

export function ModuleNavigation({ catalog }) {
  return <section aria-labelledby="module-lessons"><h2 id="module-lessons">Bài học trong lát cắt</h2>{catalog.modules.map((module) => <article className="card" key={module.title}><h3>{module.lessons[0].title}</h3><p>{module.lessons[0].summary}</p><p><a className="primary-link" href="/lesson/promotion-trust">Mở bài học</a></p></article>)}</section>;
}
