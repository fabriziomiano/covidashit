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

async function getJson<T>(path: string, signal?: AbortSignal): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, { signal });
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed with ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export function getConfig(signal?: AbortSignal) {
  return getJson<DashboardConfig>('/api/config', signal);
}

export function getPandemicSnapshot(scope: Scope, area?: string, signal?: AbortSignal) {
  const query = area ? `?area=${encodeURIComponent(area)}` : '';
  return getJson<PandemicSnapshot>(`/api/pandemic/${scope}${query}`, signal);
}

export function getVaccinesSnapshot(area?: string, signal?: AbortSignal) {
  const query = area ? `?area=${encodeURIComponent(area)}` : '';
  return getJson<VaccinesSnapshot>(`/api/vaccines${query}`, signal);
}

export function getVaccineChart<T extends CategoryChartPayload | TrendChartPayload | PieChartPayload>(chart: string, area?: string, signal?: AbortSignal) {
  const query = area ? `?area=${encodeURIComponent(area)}` : '';
  return getJson<T>(`/api/vax_charts/${chart}${query}`, signal);
}
