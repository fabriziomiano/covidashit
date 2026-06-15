interface StatusProps {
  title: string;
  message?: string;
  compact?: boolean;
}

export function LoadingState({ title, message = 'Loading dashboard data...', compact = false }: StatusProps) {
  return (
    <div className={`status-panel${compact ? ' status-panel--compact' : ''}`} role="status" aria-live="polite">
      <span className="spinner" aria-hidden="true" />
      <strong>{title}</strong>
      <span>{message}</span>
    </div>
  );
}

export function ErrorState({ title, message, compact = false }: StatusProps) {
  return <div className={`status-panel status-panel--error${compact ? ' status-panel--compact' : ''}`}><strong>{title}</strong><span>{message}</span></div>;
}

export function EmptyState({ title, message, compact = false }: StatusProps) {
  return <div className={`status-panel${compact ? ' status-panel--compact' : ''}`}><strong>{title}</strong><span>{message}</span></div>;
}
