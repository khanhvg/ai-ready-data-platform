import { PortalStatus } from './portal-status.jsx';

export function AppShell({ viewModel }) {
  return (
    <main className="portal-shell" data-semantic-ready={String(viewModel.semanticReady)}>
      <header>
        <p className="eyebrow">Stage A</p>
        <h1>{viewModel.heading}</h1>
      </header>
      <PortalStatus semanticReady={viewModel.semanticReady} message={viewModel.message} />
      <nav aria-label="Điều hướng cổng học tập">
        {viewModel.navigation.map((item) => (
          <a href={item.path} key={item.path}>
            {item.label}
          </a>
        ))}
      </nav>
    </main>
  );
}
