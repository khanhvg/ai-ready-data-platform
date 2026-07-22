import React from "react";
import { PortalStatus } from "./portal-status.jsx";
import { ModuleNavigation } from "./module-navigation.jsx";
import { PromotionTrustLesson } from "../features/promotion-trust/promotion-trust-lesson.jsx";
import { findLesson } from "../catalog/module-catalog.mjs";

const nonClaims = { "data-product-scope": "static-portal-slice", "data-runner": "unavailable", "data-execution": "disabled", "data-reset": "not-run", "data-fresh-evidence": "false", "data-progress": "disabled", "data-completion": "disabled" };
const adapters = Object.freeze({ "promotion-trust": PromotionTrustLesson });

export function AppShell({ catalog, view }) {
  const descriptor = view.lessonId ? findLesson(catalog, view.lessonId) : null;
  if (["lesson", "step"].includes(view.kind) && !descriptor) throw new Error("CATALOG_ROUTE_DESCRIPTOR_MISSING");
  const Adapter = descriptor ? adapters[descriptor.adapterId] : null;
  if (descriptor && !Adapter) throw new Error("CATALOG_ADAPTER_UNKNOWN");
  const crumbs = [["/", "Danh mục"], ...(view.kind === "catalog" ? [] : [["/module", "Mô-đun"]]), ...(descriptor ? [[descriptor.path, descriptor.title]] : [])];
  const title = view.kind === "catalog" ? "Danh mục học tập" : view.kind === "module" ? "Mô-đun trình bày" : view.kind === "not-found" ? "Đường dẫn không hợp lệ" : descriptor.title;
  return <>
    <a className="skip-link" href="#main-content">Bỏ qua đến nội dung chính</a>
    <header><a className="brand" href="/">Cổng học AI-ready</a><span className="maturity">Bản học tĩnh — Giai đoạn A</span><nav aria-label="Điều hướng chính"><a href="/">Danh mục</a><a href="/module">Mô-đun</a></nav></header>
    <nav className="breadcrumbs" aria-label="Đường dẫn"><ol>{crumbs.map(([href, label], index) => <li key={href}><a href={href} aria-current={index === crumbs.length - 1 ? "page" : undefined}>{label}</a></li>)}</ol></nav>
    <main id="main-content" {...nonClaims}><p className="eyebrow">Lát cắt học tập tĩnh</p><h1>{title}</h1><p className="not-full">Chưa phải sản phẩm học tập đầy đủ.</p><PortalStatus />
      {view.kind === "catalog" && <><h2>Một lát cắt dọc</h2><p>Khám phá câu hỏi kinh doanh, bằng chứng và quyết định có kiểm soát.</p><p><a className="primary-link" href="/module">Mở mô-đun trình bày</a></p></>}
      {view.kind === "module" && <ModuleNavigation catalog={catalog} />}
      {Adapter && <Adapter descriptor={descriptor} view={view} />}
      {view.kind === "not-found" && <><h2>Không tìm thấy trang</h2><p>Đường dẫn không thuộc lát cắt đã phát hành.</p><p><a href="/">Về danh mục</a></p></>}
    </main>
    <footer><p>static-portal-stage-a · Chỉ đọc · Không ghi nhận hoàn thành</p></footer>
  </>;
}
