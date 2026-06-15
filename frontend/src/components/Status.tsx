import { useLanguage } from '../i18n';

interface StatusProps {
  title: string;
  message?: string;
  compact?: boolean;
}

export function LoadingState({ title, message = 'Loading dashboard data...', compact = false }: StatusProps) {
  const { t } = useLanguage();
  return (
    <div className={`status-panel${compact ? ' status-panel--compact' : ''}`} role="status" aria-live="polite">
      <span className="spinner" aria-hidden="true" />
      <strong>{t(title)}</strong>
      <span>{t(message)}</span>
    </div>
  );
}

export function ErrorState({ title, message, compact = false }: StatusProps) {
  const { t } = useLanguage();
  return <div className={`status-panel status-panel--error${compact ? ' status-panel--compact' : ''}`}><strong>{t(title)}</strong><span>{message ? t(message) : undefined}</span></div>;
}

export function EmptyState({ title, message = 'No data returned by the API.', compact = false }: StatusProps) {
  const { t } = useLanguage();
  return <div className={`status-panel${compact ? ' status-panel--compact' : ''}`}><strong>{t(title)}</strong><span>{t(message)}</span></div>;
}
