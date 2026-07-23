import { PortalStatus } from './portal-status.jsx';
import { LessonNavigation } from './lesson-navigation.jsx';
import { ModuleNavigation } from './module-navigation.jsx';
import { PromotionTrustLesson } from '../features/promotion-trust/promotion-trust-lesson.jsx';

export function AppShell({ viewModel, onNavigate }) {
  return (
    <div className="portal-shell" data-review-inventory="closed" data-s3-coverage="14" data-semantic-ready={String(viewModel.semanticReady)}>
      <header className="masthead">
        <div><p className="eyebrow">{viewModel.eyebrow}</p><h1>{viewModel.heading}</h1></div>
        <p className="maturity">Một lát cắt trình bày · chưa phải khóa học đầy đủ</p>
      </header>
      <ModuleNavigation currentPath={viewModel.routePath} navigation={viewModel.navigation} onNavigate={onNavigate} />
      <div className="portal-grid">
        <LessonNavigation currentPath={viewModel.routePath} navigation={viewModel.navigation} onNavigate={onNavigate} />
        <main id="lesson-content" tabIndex="-1">
          <PortalStatus semanticReady={viewModel.semanticReady} message={viewModel.message} />
          <PromotionTrustLesson viewModel={viewModel} />
        </main>
      </div>
    </div>
  );
}
