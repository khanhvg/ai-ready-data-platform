import React from "react";
import { createRoot } from "react-dom/client";
import { AppShell } from "./app/app-shell.jsx";
import { resolveRoute } from "./routing/portal-router.mjs";
import { createModuleCatalog } from "./catalog/module-catalog.mjs";
import "./styles.css";

const catalog = createModuleCatalog(globalThis.__PORTAL_CATALOG__?.modules);
const bindings = catalog.modules.flatMap((module) => module.lessons.map((lesson) => lesson.model.bindingId));
if (bindings.length !== 1 || bindings[0] !== "promotion-trust-vite-binding-v1") throw new Error("PORTAL_CATALOG_RELEASE_MISMATCH");
createRoot(document.getElementById("root")).render(<AppShell catalog={catalog} view={resolveRoute(location.pathname, catalog)} />);
createRoot(document.getElementById("route-status")).render(<span>Điều hướng chỉ đọc đã sẵn sàng.</span>);
