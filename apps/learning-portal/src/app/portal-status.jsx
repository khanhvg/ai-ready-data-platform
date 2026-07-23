export function PortalStatus({ semanticReady, message }) {
  return (
    <section aria-live="polite" className="portal-status" data-stage-b="blocked-on-issue9">
      <h2>{semanticReady ? 'Sẵn sàng' : 'Giới hạn của Stage A'}</h2>
      <p>{message}</p>
    </section>
  );
}
