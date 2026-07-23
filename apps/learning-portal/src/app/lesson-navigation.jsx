export function LessonNavigation({ currentPath, navigation, onNavigate }) {
  const steps = navigation.filter((item) => item.path.includes('/steps/'));
  return (
    <aside className="lesson-navigation" aria-label="Mười bước tường thuật đã phát hành">
      <p className="section-label">10 bước · chỉ đọc</p>
      <ol>
        {steps.map((item) => (
          <li aria-current={item.path === currentPath ? 'step' : undefined} key={item.path}>
            <span>{item.label}</span>
          </li>
        ))}
      </ol>
    </aside>
  );
}
