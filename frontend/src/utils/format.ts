export function formatFullNumber(value: number) {
  return new Intl.NumberFormat('it-IT', { maximumFractionDigits: 0 }).format(Math.round(value));
}

export function formatCompactNumber(value: number | string | undefined | null) {
  const numeric = typeof value === 'number' ? value : Number(String(value ?? '').replaceAll('.', ''));
  if (!Number.isFinite(numeric)) return value?.toString() ?? 'n/a';
  const absolute = Math.abs(numeric);
  if (absolute >= 1_000_000) return `${new Intl.NumberFormat('it-IT', { maximumFractionDigits: 1 }).format(numeric / 1_000_000)}M`;
  if (absolute >= 1_000) return `${new Intl.NumberFormat('it-IT', { maximumFractionDigits: 1 }).format(numeric / 1_000)}K`;
  return formatFullNumber(numeric);
}

export function formatPercent(value: number | string | undefined | null) {
  if (value === undefined || value === null || value === 'n/a') return '';
  return String(value).endsWith('%') ? String(value) : `${value}%`;
}
