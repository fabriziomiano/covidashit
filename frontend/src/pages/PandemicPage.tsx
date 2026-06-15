import { useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { getPandemicSnapshot } from '../api/client';
import { useAsync } from '../api/useAsync';
import { AreaSearch } from '../components/AreaSearch';
import { TimeSeriesChart } from '../components/Charts';
import { EmptyState, ErrorState, LoadingState } from '../components/Status';
import { TrendCards } from '../components/Cards';
import type { DashboardConfig, PandemicSeries, Scope, SeriesItem, TrendCard } from '../types/covidash';
import { useLanguage } from '../i18n';
import { formatPercent } from '../utils/format';

interface PandemicPageProps {
  config: DashboardConfig;
  scope: Scope;
}

function seriesFor(payload: PandemicSeries, group: 'daily' | 'current' | 'cum'): SeriesItem[] {
  const aliases: Record<typeof group, string[]> = {
    daily: ['daily', 'Daily', 'seriesDaily'],
    current: ['current', 'Current', 'seriesCurrent'],
    cum: ['cum', 'cumulative', 'Cumulative', 'seriesCum']
  };
  for (const key of aliases[group]) {
    const value = payload[key];
    if (Array.isArray(value)) return value as SeriesItem[];
  }
  const allSeries = Object.values(payload).filter(Array.isArray).flat() as SeriesItem[];
  return allSeries.filter((series) => {
    const id = series.id ?? series.name;
    if (group === 'daily') return id.includes('_g') || id.includes('nuovi_positivi') || id.endsWith('_ma');
    if (group === 'current') return ['totale_positivi', 'terapia_intensiva', 'totale_ospedalizzati', 'isolamento_domiciliare'].some((key) => id.includes(key));
    return ['totale_casi', 'deceduti', 'tamponi', 'dimessi_guariti'].some((key) => id.includes(key));
  });
}

function cardsFor(cards: TrendCard[], group: 'daily' | 'current' | 'cum') {
  return cards.filter((card) => card.type === group || (group === 'cum' && card.type === 'cumulative'));
}

export function PandemicPage({ config, scope }: PandemicPageProps) {
  const { t } = useLanguage();
  const { area } = useParams();
  const decodedArea = area ? decodeURIComponent(area) : undefined;
  const [activeTab, setActiveTab] = useState<'daily' | 'current' | 'cum'>('daily');
  const { data, error, loading } = useAsync((signal) => getPandemicSnapshot(scope, decodedArea, signal), [scope, decodedArea]);
  const tabs = useMemo(() => [
    { id: 'daily' as const, label: t('Daily') },
    { id: 'current' as const, label: t('Current') },
    { id: 'cum' as const, label: t('Cumulative') }
  ], [t]);

  if (loading) return <LoadingState title={t('Pandemic')} />;
  if (error) return <ErrorState title={t('Pandemic data unavailable')} message={error.message} />;
  if (!data) return <EmptyState title={t('Pandemic')} message={t('No data returned by the API.')} />;

  const activeSeries = seriesFor(data.series, activeTab);
  const activeCards = scope === 'provincial' ? data.trendCards : cardsFor(data.trendCards, activeTab);
  const chartTitle = activeTab === 'daily' ? t('Daily trend') : activeTab === 'current' ? t('Current trend') : t('Cumulative trend');

  return (
    <section className="dashboard-page">
      <div className="page-heading">
        <div>
          <p className="eyebrow">{scope === 'national' ? t('National dashboard') : scope === 'regional' ? t('Regional dashboard') : t('Provincial dashboard')}</p>
          <h1>{data.dashboardTitle}</h1>
          <p className="meta-line">{t('Latest update')} {data.latestUpdate}{data.population ? ` · ${t('Population')} ${data.population}` : ''}{data.positivityIdx && data.positivityIdx !== 'n/a' ? ` · ${t('Positivity')} ${formatPercent(data.positivityIdx)}` : ''}</p>
        </div>
        <div className="quick-links">
          <Link to="/">{t('Italy')}</Link>
          <Link to="/vaccines">{t('Vaccines')}</Link>
          {scope === 'provincial' && data.region ? <Link to={`/regions/${encodeURIComponent(data.region)}`}>{data.region}</Link> : null}
        </div>
      </div>

      {data.notes ? <aside className="notes-panel">{data.notes}</aside> : null}

      {scope !== 'provincial' ? (
        <div className="tabs" role="tablist">
          {tabs.map((tab) => <button key={tab.id} className={activeTab === tab.id ? 'active' : ''} onClick={() => setActiveTab(tab.id)}>{tab.label}</button>)}
        </div>
      ) : null}

      <TrendCards cards={activeCards.length ? activeCards : data.trendCards} />

      <div className="mobile-search" aria-label={t('Area search')}>
        <AreaSearch config={config} id="mobile-area-search-results" panel />
      </div>

      <section className="chart-panel">
        {activeSeries.length ? <TimeSeriesChart title={chartTitle} series={activeSeries} categories={data.series.dates} yAxisType={activeTab === 'cum' ? 'logarithmic' : 'linear'} showMilestones /> : <EmptyState title={t('Chart unavailable')} message={t('The API returned no series for this panel.')} />}
      </section>

      {scope === 'national' ? (
        <section className="area-section">
          <h2>{t('Regions')}</h2>
          <div className="area-grid">{config.regions.map((region) => <Link key={region} to={`/regions/${encodeURIComponent(region)}`}>{region}</Link>)}</div>
        </section>
      ) : null}

      {scope === 'regional' || scope === 'provincial' ? (
        <section className="area-section">
          <h2>{t('Provinces')}</h2>
          <div className="area-grid">{(data.regionProvinces ?? []).map((province) => <Link key={province} to={`/provinces/${encodeURIComponent(province)}`}>{province}</Link>)}</div>
        </section>
      ) : null}
    </section>
  );
}
