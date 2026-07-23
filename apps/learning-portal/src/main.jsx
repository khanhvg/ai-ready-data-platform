import { StrictMode } from 'react';
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
const route = resolvePortalRoute(window.location.pathname, routes);
const viewModel = createSafeViewModel(route, catalog);

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AppShell viewModel={viewModel} />
  </StrictMode>
);
