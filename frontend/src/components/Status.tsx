interface StatusProps {
  title: string;
  message?: string;
}

export function LoadingState({ title, message = 'Loading dashboard data...' }: StatusProps) {
  return <div className="status-panel"><strong>{title}</strong><span>{message}</span></div>;
}

export function ErrorState({ title, message }: StatusProps) {
  return <div className="status-panel status-panel--error"><strong>{title}</strong><span>{message}</span></div>;
}

export function EmptyState({ title, message }: StatusProps) {
  return <div className="status-panel"><strong>{title}</strong><span>{message}</span></div>;
}
