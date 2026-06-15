import type { TrendCard } from '../types/covidash';
import { formatCompactNumber } from '../utils/format';

function toneClass(colour?: string) {
  if (colour?.includes('success')) return 'card-success';
  if (colour?.includes('danger')) return 'card-danger';
  if (colour?.includes('info')) return 'card-info';
  return 'card-neutral';
}

function numericValue(value: number | string | undefined) {
  if (typeof value === 'number') return value;
  const parsed = Number(String(value ?? '').replaceAll('.', '').replace(',', '.'));
  return Number.isFinite(parsed) ? parsed : null;
}

function changeLabel(card: TrendCard, comparisonLabel: string) {
  const current = numericValue(card.count);
  const previous = numericValue(card.last_week_count);
  const label = card.comparisonLabel ?? comparisonLabel;
  if (current === null || previous === null || previous === 0) return `n/a ${label}`;
  const percentage = ((current - previous) / Math.abs(previous)) * 100;
  const sign = percentage > 0 ? '+' : '';
  const rounded = Math.round(Math.abs(percentage)) * Math.sign(percentage);
  return `${sign}${rounded}% ${label}`;
}

interface CardsProps {
  cards: TrendCard[];
  comparisonLabel?: string;
}

export function TrendCards({ cards, comparisonLabel = 'vs 7d ago' }: CardsProps) {
  return (
    <div className="cards-grid">
      {cards.map((card) => (
        <article className={`metric-card ${toneClass(card.colour)}`} key={card.id}>
          <div className="metric-card__title">{card.title}</div>
          <div className="metric-card__value" title={card.countLabel ?? String(card.count ?? 'n/a')}>{formatCompactNumber(card.count ?? card.countLabel)}</div>
          <div className="metric-card__delta">{changeLabel(card, comparisonLabel)}</div>
          <div className="metric-card__meta">
            <span>{card.lastWeekDateLabel ?? card.last_week_dt ?? 'Previous'}</span>
            <span>{formatCompactNumber(card.last_week_count ?? card.lastWeekCountLabel)}</span>
          </div>
        </article>
      ))}
    </div>
  );
}
