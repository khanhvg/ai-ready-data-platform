import { StrictMode, useCallback, useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { AppShell } from './app/app-shell.jsx';
import { createReleasedLearningAdapter } from './contracts/released-learning-adapter.mjs';
import { createReleasedModuleProvider } from './catalog/released-module-provider.mjs';
import { deriveModuleCatalog } from './catalog/module-catalog.mjs';
import { derivePortalRoutes, resolvePortalRoute } from './routing/portal-router.mjs';
import { createSafeViewModel } from './contracts/safe-view-model.mjs';
import './styles.css';

const adapter = createReleasedLearningAdapter();
const registry = createReleasedModuleProvider(adapter).readRegistry();
const catalog = deriveModuleCatalog(registry);
const routes = derivePortalRoutes(catalog);
function PortalApplication() {
  const [pathname, setPathname] = useState(window.location.pathname);
  const route = resolvePortalRoute(pathname, routes) ?? routes[0];
  const viewModel = useMemo(() => createSafeViewModel(route, catalog), [route]);
  const onNavigate = useCallback((event) => {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const url = new URL(event.currentTarget.href);
    if (url.origin !== window.location.origin) return;
    const nextRoute = resolvePortalRoute(url.pathname, routes);
    if (!nextRoute) return;
    event.preventDefault();
    window.history.pushState(null, '', nextRoute.path);
    setPathname(nextRoute.path);
    window.requestAnimationFrame(() => document.getElementById('lesson-content')?.focus());
  }, []);
  useEffect(() => {
    const onPopState = () => setPathname(window.location.pathname);
    window.addEventListener('popstate', onPopState);
    return () => window.removeEventListener('popstate', onPopState);
  }, []);
  return <AppShell viewModel={viewModel} onNavigate={onNavigate} />;
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <PortalApplication />
  </StrictMode>
);
