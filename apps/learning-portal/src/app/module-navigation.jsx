export function ModuleNavigation({ currentPath, navigation, onNavigate }) {
  return (
    <nav aria-label="Điều hướng cổng học tập" className="module-navigation">
      {navigation.map((item) => (
        <a aria-current={item.path === currentPath ? 'page' : undefined} href={item.path} key={item.path} onClick={onNavigate}>
          {item.label}
        </a>
      ))}
    </nav>
  );
}
