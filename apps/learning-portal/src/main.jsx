import React from "react";
import { createRoot } from "react-dom/client";
import { AppShell } from "./app/app-shell.jsx";
import { resolveRoute } from "./routing/portal-router.mjs";
import "./styles.css";

const catalog = globalThis.__PORTAL_CATALOG__;
if (catalog?.modules?.[0]?.model?.bindingId !== "promotion-trust-vite-binding-v1") throw new Error("PORTAL_CATALOG_RELEASE_MISMATCH");
createRoot(document.getElementById("root")).render(<AppShell catalog={catalog} view={resolveRoute(location.pathname)} />);
createRoot(document.getElementById("route-status")).render(<span>Điều hướng chỉ đọc đã sẵn sàng.</span>);
