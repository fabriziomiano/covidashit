import type { ReactNode } from 'react';
import { Link, useParams } from 'react-router-dom';
import { getVaccinesSnapshot, getVaccineChart } from '../api/client';
import { useAsync } from '../api/useAsync';
import { AgeDoseChart, ProviderPieChart, RegionCoverageChart, VaccinationTrendChart } from '../components/Charts';
import { TrendCards } from '../components/Cards';
import { EmptyState, ErrorState, LoadingState } from '../components/Status';
import type { CategoryChartPayload, DashboardConfig, PieChartPayload, TrendChartPayload } from '../types/covidash';

interface VaccinesPageProps {
  config: DashboardConfig;
}

function chartContent<T>(state: { data: T | null; error: Error | null; loading: boolean }, title: string, render: (payload: T) => ReactNode) {
  if (state.data) return render(state.data);
  if (state.error) return <ErrorState title={`${title} unavailable`} message={state.error.message} compact />;
  if (state.loading) return <LoadingState title={title} compact />;
  return <EmptyState title={title} message="No data returned by the API." compact />;
}

export function VaccinesPage({ config }: VaccinesPageProps) {
  const { area } = useParams();
  const decodedArea = area ? decodeURIComponent(area) : undefined;
  const snapshot = useAsync((signal) => getVaccinesSnapshot(decodedArea, signal), [decodedArea]);
  const regionChart = useAsync((signal) => getVaccineChart<CategoryChartPayload>('region', undefined, signal), []);
  const trendChart = useAsync((signal) => getVaccineChart<TrendChartPayload>('trend', undefined, signal), []);
  const ageChart = useAsync((signal) => getVaccineChart<CategoryChartPayload>('age', decodedArea, signal), [decodedArea]);
  const providerChart = useAsync((signal) => getVaccineChart<PieChartPayload>('provider', decodedArea, signal), [decodedArea]);

  if (snapshot.loading) return <LoadingState title="Vaccines" />;
  if (snapshot.error) return <ErrorState title="Vaccine data unavailable" message={snapshot.error.message} />;
  if (!snapshot.data) return <EmptyState title="Vaccines" message="No vaccine data returned by the API." />;

  return (
    <section className="dashboard-page">
      <div className="page-heading">
        <div>
          <p className="eyebrow">Vaccination dashboard</p>
          <h1>{snapshot.data.dashboardTitle}</h1>
          <p className="meta-line">Latest update {snapshot.data.latestUpdate} · Population {snapshot.data.population}{typeof snapshot.data.adminsPerc === 'number' ? ` · Administered ${snapshot.data.adminsPerc}%` : ''}</p>
        </div>
        <div className="coverage-cards" aria-label="Vaccination coverage">
          <article>
            <span>First Dose</span>
            <strong>{snapshot.data.percPopVax.first ?? 'n/a'}%</strong>
          </article>
          <article>
            <span>Second Dose</span>
            <strong>{snapshot.data.percPopVax.second ?? 'n/a'}%</strong>
          </article>
          <article>
            <span>Booster</span>
            <strong>{snapshot.data.percPopVax.booster ?? 'n/a'}%</strong>
          </article>
        </div>
      </div>

      <TrendCards cards={snapshot.data.trends} comparisonLabel="vs previous sample" />

      {!decodedArea ? (
        <div className="charts-grid">
          <section className="chart-panel">{chartContent(regionChart, "Admins per region", (payload) => <RegionCoverageChart payload={payload} />)}</section>
          <section className="chart-panel">{chartContent(trendChart, "Vaccination trend", (payload) => <VaccinationTrendChart payload={payload} />)}</section>
        </div>
      ) : null}

      <div className="charts-grid">
        <section className="chart-panel">{chartContent(ageChart, "Admins per age", (payload) => <AgeDoseChart payload={payload} titleSuffix={decodedArea ?? 'Italy'} />)}</section>
        <section className="chart-panel">{chartContent(providerChart, "Admins per provider", (payload) => <ProviderPieChart payload={payload} titleSuffix={decodedArea ?? 'Italy'} />)}</section>
      </div>

      <section className="area-section">
        <h2>Regional vaccines</h2>
        <div className="area-grid">{config.regions.map((region) => <Link key={region} to={`/vaccines/${encodeURIComponent(region)}`}>{region}</Link>)}</div>
      </section>
    </section>
  );
}
