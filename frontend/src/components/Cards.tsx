import type { TrendCard } from '../types/covidash';
import { formatCompactNumber } from '../utils/format';
import {
  Activity,
  ArrowDownLeft,
  ArrowUpRight,
  BadgePlus,
  CircleMinus,
  Cross,
  HeartPulse,
  Home,
  Hospital,
  Rocket,
  ShieldCheck,
  Smile,
  Syringe,
  TestTube2,
  type LucideIcon,
} from 'lucide-react';

const CARD_ICONS: Record<string, LucideIcon> = {
  nuovi_positivi: BadgePlus,
  ingressi_terapia_intensiva: HeartPulse,
  deceduti_g: Cross,
  tamponi_g: TestTube2,
  totale_positivi: Activity,
  terapia_intensiva: HeartPulse,
  totale_ospedalizzati: Hospital,
  isolamento_domiciliare: Home,
  totale_casi: Activity,
  deceduti: Cross,
  tamponi: TestTube2,
  dimessi_guariti: Smile,
  d1: Syringe,
  d2: ShieldCheck,
  db1: Rocket,
};

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

function cardIcon(card: TrendCard) {
  return CARD_ICONS[card.id] ?? Activity;
}

function StatusIcon({ statusIcon }: { statusIcon?: string }) {
  if (statusIcon?.includes('arrow-up')) return <ArrowUpRight aria-hidden="true" />;
  if (statusIcon?.includes('arrow-down')) return <ArrowDownLeft aria-hidden="true" />;
  return <CircleMinus aria-hidden="true" />;
}

interface CardsProps {
  cards: TrendCard[];
  comparisonLabel?: string;
}

export function TrendCards({ cards, comparisonLabel = 'vs 7d ago' }: CardsProps) {
  return (
    <div className="cards-grid">
      {cards.map((card) => {
        const Icon = cardIcon(card);
        return (
          <article className={`metric-card ${toneClass(card.colour)}`} key={card.id}>
            <div className="metric-card__head">
              <span className="metric-card__icon" title={card.title}>
                <Icon aria-hidden="true" />
              </span>
              <div className="metric-card__title">{card.title}</div>
            </div>
            <div className="metric-card__value-row">
              <div className="metric-card__value" title={card.countLabel ?? String(card.count ?? 'n/a')}>
                {formatCompactNumber(card.count ?? card.countLabel)}
              </div>
              <span className="metric-card__trend" title={changeLabel(card, comparisonLabel)}>
                <StatusIcon statusIcon={card.status_icon} />
              </span>
            </div>
            <div className="metric-card__delta">{changeLabel(card, comparisonLabel)}</div>
            <div className="metric-card__meta">
              <span>{card.lastWeekDateLabel ?? card.last_week_dt ?? 'Previous'}</span>
              <span>{formatCompactNumber(card.last_week_count ?? card.lastWeekCountLabel)}</span>
            </div>
          </article>
        );
      })}
    </div>
  );
}
