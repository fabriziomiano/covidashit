import type {
  CategoryChartPayload,
  DashboardConfig,
  PandemicSnapshot,
  PieChartPayload,
  Scope,
  TrendChartPayload,
  VaccinesSnapshot
} from '../types/covidash';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '';

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed with ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export function getConfig() {
  return getJson<DashboardConfig>('/api/config');
}

export function getPandemicSnapshot(scope: Scope, area?: string) {
  const query = area ? `?area=${encodeURIComponent(area)}` : '';
  return getJson<PandemicSnapshot>(`/api/pandemic/${scope}${query}`);
}

export function getVaccinesSnapshot(area?: string) {
  const query = area ? `?area=${encodeURIComponent(area)}` : '';
  return getJson<VaccinesSnapshot>(`/api/vaccines${query}`);
}

export function getVaccineChart<T extends CategoryChartPayload | TrendChartPayload | PieChartPayload>(chart: string, area?: string) {
  const query = area ? `?area=${encodeURIComponent(area)}` : '';
  return getJson<T>(`/api/vax_charts/${chart}${query}`);
}
