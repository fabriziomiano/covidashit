export type Scope = 'national' | 'regional' | 'provincial';

export interface TrendCard {
  id: string;
  title: string;
  type: 'daily' | 'current' | 'cum' | 'vax' | string;
  icon?: string;
  colour?: string;
  status_icon?: string;
  count?: number;
  countLabel?: string;
  last_week_count?: number;
  lastWeekCountLabel?: string;
  last_week_dt?: string;
  lastWeekDateLabel?: string;
  comparisonLabel?: string;
  percentage?: string;
  percentage_difference?: string;
}

export interface SeriesItem {
  id?: string;
  name: string;
  data: number[];
  visible?: boolean;
  type?: string;
}

export interface PandemicSeries {
  daily?: SeriesItem[];
  current?: SeriesItem[];
  cum?: SeriesItem[];
  cumulative?: SeriesItem[];
  dates?: string[];
  [key: string]: unknown;
}

export interface DashboardConfig {
  version: string;
  pageTitle: string;
  regions: string[];
  provinces: string[];
  italyMap: Record<string, string[]>;
  varsConfig: Record<string, { title: string; type: string; desc?: string; icon?: string }>;
}

export interface PandemicSnapshot {
  scope: Scope;
  area?: string | null;
  dashboardTitle: string;
  pageTitle: string;
  trendCards: TrendCard[];
  series: PandemicSeries;
  breakdown: Record<string, Array<{ area: string; count: number | string; url?: string }>>;
  notes?: string;
  latestUpdate: string;
  positivityIdx?: string | number;
  population?: string | null;
  region?: string | null;
  regionProvinces?: string[];
}

export interface VaccinesSnapshot {
  scope: 'vaccines';
  area?: string | null;
  dashboardTitle: string;
  pageTitle: string;
  latestUpdate: string;
  adminsPerc: number | string;
  percPopVax: { first: number | null; second: number | null; booster: number | null };
  trends: TrendCard[];
  population: string;
}

export interface CategoryChartPayload {
  title: string;
  yAxisTitle?: string;
  categories: string[];
  first: { name: string; data: number[] };
  second: { name: string; data: number[] };
  booster: { name: string; data: number[] };
  population: { name: string; data: number[] };
}

export interface TrendChartPayload {
  title: string;
  yAxisTitle: string;
  dates: string[];
  data: SeriesItem[];
}

export interface PieChartPayload {
  title: string;
  name: string;
  data: Array<[string, number]>;
}
