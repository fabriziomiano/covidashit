import { useParams } from 'react-router-dom';
import { getVaccinesSnapshot, getVaccineChart } from '../api/client';
import { useAsync } from '../api/useAsync';
import { AgeDoseChart, ProviderPieChart, RegionCoverageChart, VaccinationTrendChart } from '../components/Charts';
import { TrendCards } from '../components/Cards';
import { EmptyState, ErrorState, LoadingState } from '../components/Status';
import type { CategoryChartPayload, DashboardConfig, PieChartPayload, TrendChartPayload } from '../types/covidash';

interface VaccinesPageProps {
  config: DashboardConfig;
}

export function VaccinesPage({ config }: VaccinesPageProps) {
  const { area } = useParams();
  const decodedArea = area ? decodeURIComponent(area) : undefined;
  const snapshot = useAsync(() => getVaccinesSnapshot(decodedArea), [decodedArea]);
  const regionChart = useAsync(() => getVaccineChart<CategoryChartPayload>('region'), []);
  const trendChart = useAsync(() => getVaccineChart<TrendChartPayload>('trend'), []);
  const ageChart = useAsync(() => getVaccineChart<CategoryChartPayload>('age', decodedArea), [decodedArea]);
  const providerChart = useAsync(() => getVaccineChart<PieChartPayload>('provider', decodedArea), [decodedArea]);

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
          <section className="chart-panel">{regionChart.data ? <RegionCoverageChart payload={regionChart.data} /> : <LoadingState title="Admins per region" />}</section>
          <section className="chart-panel">{trendChart.data ? <VaccinationTrendChart payload={trendChart.data} /> : <LoadingState title="Vaccination trend" />}</section>
        </div>
      ) : null}

      <div className="charts-grid">
        <section className="chart-panel">{ageChart.data ? <AgeDoseChart payload={ageChart.data} titleSuffix={decodedArea ?? 'Italy'} /> : <LoadingState title="Admins per age" />}</section>
        <section className="chart-panel">{providerChart.data ? <ProviderPieChart payload={providerChart.data} titleSuffix={decodedArea ?? 'Italy'} /> : <LoadingState title="Admins per provider" />}</section>
      </div>

      <section className="area-section">
        <h2>Regional vaccines</h2>
        <div className="area-grid">{config.regions.map((region) => <a key={region} href={`/vaccines/${encodeURIComponent(region)}`}>{region}</a>)}</div>
      </section>
    </section>
  );
}
