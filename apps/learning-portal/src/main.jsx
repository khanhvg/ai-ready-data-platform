import { StrictMode, useCallback, useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import catalog from 'virtual:portal-catalog';
import { AppShell } from './app/app-shell.jsx';
import { derivePortalRoutes, resolvePortalRoute } from './routing/portal-router.mjs';
import './styles.css';

const routes = derivePortalRoutes(catalog);

function PortalApplication() {
  const [pathname, setPathname] = useState(window.location.pathname);
  const route = resolvePortalRoute(pathname, routes) ?? routes[0];
  const navigate = useCallback((event) => {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const url = new URL(event.currentTarget.href);
    const next = url.origin === location.origin && resolvePortalRoute(url.pathname, routes);
    if (!next) return;
    event.preventDefault();
    history.pushState(null, '', next.path);
    setPathname(next.path);
    requestAnimationFrame(() => document.querySelector('main')?.focus());
  }, []);
  useEffect(() => {
    const pop = () => setPathname(location.pathname);
    addEventListener('popstate', pop);
    return () => removeEventListener('popstate', pop);
  }, []);
  return <AppShell catalog={catalog} route={route} onNavigate={navigate} />;
}

createRoot(document.getElementById('root')).render(<StrictMode><PortalApplication /></StrictMode>);
