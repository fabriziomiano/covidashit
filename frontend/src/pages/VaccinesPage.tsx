import type { ReactNode } from 'react';
import { Link, useParams } from 'react-router-dom';
import { getVaccinesSnapshot, getVaccineChart } from '../api/client';
import { useAsync } from '../api/useAsync';
import { AreaSearch } from '../components/AreaSearch';
import { AgeDoseChart, ProviderPieChart, RegionCoverageChart, VaccinationTrendChart } from '../components/Charts';
import { TrendCards } from '../components/Cards';
import { EmptyState, ErrorState, LoadingState } from '../components/Status';
import { useLanguage } from '../i18n';
import type { CategoryChartPayload, DashboardConfig, PieChartPayload, TrendChartPayload } from '../types/covidash';

interface VaccinesPageProps {
  config: DashboardConfig;
}

function chartContent<T>(
  state: { data: T | null; error: Error | null; loading: boolean },
  title: string,
  unavailable: string,
  noDataMessage: string,
  render: (payload: T) => ReactNode,
) {
  if (state.data) return render(state.data);
  if (state.error) return <ErrorState title={`${title} ${unavailable}`} message={state.error.message} compact />;
  if (state.loading) return <LoadingState title={title} compact />;
  return <EmptyState title={title} message={noDataMessage} compact />;
}

export function VaccinesPage({ config }: VaccinesPageProps) {
  const { t } = useLanguage();
  const { area } = useParams();
  const decodedArea = area ? decodeURIComponent(area) : undefined;
  const snapshot = useAsync((signal) => getVaccinesSnapshot(decodedArea, signal), [decodedArea]);
  const regionChart = useAsync((signal) => getVaccineChart<CategoryChartPayload>('region', undefined, signal), []);
  const trendChart = useAsync((signal) => getVaccineChart<TrendChartPayload>('trend', undefined, signal), []);
  const ageChart = useAsync((signal) => getVaccineChart<CategoryChartPayload>('age', decodedArea, signal), [decodedArea]);
  const providerChart = useAsync((signal) => getVaccineChart<PieChartPayload>('provider', decodedArea, signal), [decodedArea]);

  if (snapshot.loading) return <LoadingState title={t('Vaccines')} />;
  if (snapshot.error) return <ErrorState title={t('Vaccine data unavailable')} message={snapshot.error.message} />;
  if (!snapshot.data) return <EmptyState title={t('Vaccines')} message={t('No vaccine data returned by the API.')} />;

  return (
    <section className="dashboard-page">
      <div className="page-heading">
        <div>
          <p className="eyebrow">{t('Vaccination dashboard')}</p>
          <h1>{snapshot.data.dashboardTitle}</h1>
          <p className="meta-line">{t('Latest update')} {snapshot.data.latestUpdate} · {t('Population')} {snapshot.data.population}{typeof snapshot.data.adminsPerc === 'number' ? ` · ${t('Administered')} ${snapshot.data.adminsPerc}%` : ''}</p>
        </div>
        <div className="coverage-cards" aria-label="Vaccination coverage">
          <article>
            <span>{t('First Dose')}</span>
            <strong>{snapshot.data.percPopVax.first ?? 'n/a'}%</strong>
          </article>
          <article>
            <span>{t('Second Dose')}</span>
            <strong>{snapshot.data.percPopVax.second ?? 'n/a'}%</strong>
          </article>
          <article>
            <span>{t('Booster')}</span>
            <strong>{snapshot.data.percPopVax.booster ?? 'n/a'}%</strong>
          </article>
        </div>
      </div>

      <TrendCards cards={snapshot.data.trends} comparisonLabel={t('vs previous sample')} />

      <div className="mobile-search" aria-label={t('Area search')}>
        <AreaSearch config={config} id="mobile-vaccine-search-results" panel />
      </div>

      {!decodedArea ? (
        <div className="charts-grid">
          <section className="chart-panel">{chartContent(regionChart, t('Admins per region'), t('unavailable'), t('No data returned by the API.'), (payload) => <RegionCoverageChart payload={payload} />)}</section>
          <section className="chart-panel">{chartContent(trendChart, t('Vaccination trend'), t('unavailable'), t('No data returned by the API.'), (payload) => <VaccinationTrendChart payload={payload} />)}</section>
        </div>
      ) : null}

      <div className="charts-grid">
        <section className="chart-panel">{chartContent(ageChart, t('Admins per age'), t('unavailable'), t('No data returned by the API.'), (payload) => <AgeDoseChart payload={payload} titleSuffix={decodedArea ?? 'Italy'} />)}</section>
        <section className="chart-panel">{chartContent(providerChart, t('Admins per provider'), t('unavailable'), t('No data returned by the API.'), (payload) => <ProviderPieChart payload={payload} titleSuffix={decodedArea ?? 'Italy'} />)}</section>
      </div>

      <section className="area-section">
        <h2>{t('Regional vaccines')}</h2>
        <div className="area-grid">{config.regions.map((region) => <Link key={region} to={`/vaccines/${encodeURIComponent(region)}`}>{region}</Link>)}</div>
      </section>
    </section>
  );
}
