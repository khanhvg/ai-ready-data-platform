export function PortalStatus({ semanticReady, message }) {
  return (
    <section aria-live="polite" className="portal-status">
      <h2>{semanticReady ? 'Sẵn sàng' : 'Chưa sẵn sàng'}</h2>
      <p>{message}</p>
    </section>
  );
}
