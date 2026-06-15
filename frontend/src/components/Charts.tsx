import { useMemo, useState } from 'react';
import type { CSSProperties } from 'react';
import {
  arc,
  extent,
  line,
  max,
  pie,
  scaleBand,
  scaleLinear,
  scaleLog,
  scaleOrdinal,
  schemeTableau10
} from 'd3';
import type { PieArcDatum } from 'd3';
import type {
  CategoryChartPayload,
  PieChartPayload,
  SeriesItem,
  TrendChartPayload
} from '../types/covidash';
import { formatCompactNumber, formatFullNumber } from '../utils/format';

const palette = scaleOrdinal<string, string>(schemeTableau10);
const doseColors = {
  first: '#4db6ac',
  second: '#45b7e8',
  booster: '#f0b45d',
  population: '#354258'
};
const pandemicMilestones = [
  { id: 'lockdown', label: 'Lockdown', date: '2020-03-22T00:00:00', color: '#f05d6a' },
  { id: 'phase2', label: 'Phase 2', date: '2020-05-04T00:00:00', color: '#f0b45d' },
  { id: 'phase3', label: 'Phase 3', date: '2020-06-15T00:00:00', color: '#40c980' },
  { id: 'critical-areas', label: 'Critical areas', date: '2020-11-06T00:00:00', color: '#f05d6a' },
  { id: 'vaccine-day', label: 'Vaccine day', date: '2020-12-27T00:00:00', color: '#45b7e8' }
];

function valueLabel(value: number) {
  return formatFullNumber(value);
}

function percentLabel(value: number) {
  return `${new Intl.NumberFormat('it-IT', { maximumFractionDigits: 1 }).format(value)}%`;
}

function dateLabel(value: string | undefined) {
  if (!value) return '';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat('it-IT', { day: '2-digit', month: 'short', year: '2-digit' }).format(date);
}

function axisDateLabel(value: string | undefined) {
  if (!value) return '';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat('it-IT', { month: 'short', year: '2-digit' }).format(date);
}

function monthDistance(first: Date, last: Date) {
  return (last.getFullYear() - first.getFullYear()) * 12 + last.getMonth() - first.getMonth();
}

function dateTickIndexes(categories: string[] | undefined, maxTicks = 12) {
  const dates = (categories ?? []).map((value) => new Date(value));
  if (!dates.length || dates.some((date) => Number.isNaN(date.getTime()))) return [];
  const first = dates[0];
  const last = dates[dates.length - 1];
  const months = Math.max(1, monthDistance(first, last));
  const step = months > 48 ? 6 : months > 24 ? 3 : months > 12 ? 2 : Math.max(1, Math.ceil(months / maxTicks));
  const ticks = [];
  const cursor = new Date(first.getFullYear(), first.getMonth(), 1);
  while (cursor <= last) {
    ticks.push(new Date(cursor));
    cursor.setMonth(cursor.getMonth() + step);
  }
  const indexes = ticks
    .map((tick) => {
      const time = tick.getTime();
      let nearest = 0;
      let distance = Number.POSITIVE_INFINITY;
      dates.forEach((date, index) => {
        const candidateDistance = Math.abs(date.getTime() - time);
        if (candidateDistance < distance) {
          nearest = index;
          distance = candidateDistance;
        }
      });
      return nearest;
    });
  const labelSet = new Set<string>();
  return Array.from(new Set([0, ...indexes, dates.length - 1]))
    .sort((a, b) => a - b)
    .filter((index) => {
      const label = axisDateLabel(categories?.[index]);
      if (labelSet.has(label)) return false;
      labelSet.add(label);
      return true;
    });
}

function milestoneIndexes(categories: string[] | undefined) {
  const dates = (categories ?? []).map((value) => new Date(value));
  if (!dates.length || dates.some((date) => Number.isNaN(date.getTime()))) return [];
  const first = dates[0].getTime();
  const last = dates[dates.length - 1].getTime();
  return pandemicMilestones.flatMap((milestone) => {
    const time = new Date(milestone.date).getTime();
    if (time < first || time > last) return [];
    let nearest = 0;
    let distance = Number.POSITIVE_INFINITY;
    dates.forEach((date, index) => {
      const candidateDistance = Math.abs(date.getTime() - time);
      if (candidateDistance < distance) {
        nearest = index;
        distance = candidateDistance;
      }
    });
    return [{ ...milestone, index: nearest }];
  });
}

function rangeForMonths(categories: string[] | undefined, months: number) {
  const dates = (categories ?? []).map((value) => new Date(value));
  if (!dates.length || dates.some((date) => Number.isNaN(date.getTime()))) return null;
  const last = dates[dates.length - 1];
  const startDate = new Date(last);
  startDate.setMonth(startDate.getMonth() - months);
  const startIndex = dates.findIndex((date) => date >= startDate);
  return { start: Math.max(0, startIndex), end: dates.length - 1 };
}

function ChartTitle({ title }: { title: string }) {
  return <h3 className="chart-title">{title}</h3>;
}

function EmptyChart({ message = 'No chart data available.' }: { message?: string }) {
  return <div className="chart-empty">{message}</div>;
}

interface TimeSeriesChartProps {
  title: string;
  series: SeriesItem[];
  categories?: string[];
  yAxisType?: 'linear' | 'logarithmic';
  showMilestones?: boolean;
  valueKind?: 'count' | 'percent';
}

export function TimeSeriesChart({
  title,
  series,
  categories,
  yAxisType = 'linear',
  showMilestones = false,
  valueKind = 'count'
}: TimeSeriesChartProps) {
  const [hoverIndex, setHoverIndex] = useState<number | null>(null);
  const fullLimit = categories?.length ? categories.length : Math.max(...series.map((item) => item.data.length));
  const [timeWindow, setTimeWindow] = useState({ start: 0, end: Math.max(0, fullLimit - 1) });
  const canDrill = fullLimit > 30;
  const displayValue = (value: number) => valueKind === 'percent' ? percentLabel(value) : valueLabel(value);
  const displayCompactValue = (value: number) => valueKind === 'percent' ? percentLabel(value) : formatCompactNumber(value);
  const effectiveWindow = useMemo(() => {
    const minSpan = Math.min(30, Math.max(1, fullLimit));
    const start = Math.max(0, Math.min(timeWindow.start, fullLimit - minSpan));
    const end = Math.min(fullLimit - 1, Math.max(start + minSpan - 1, timeWindow.end));
    return { start, end };
  }, [fullLimit, timeWindow]);

  function updateWindow(next: { start: number; end: number }) {
    const minSpan = Math.min(30, Math.max(1, fullLimit));
    const start = Math.max(0, Math.min(next.start, fullLimit - minSpan));
    const end = Math.min(fullLimit - 1, Math.max(start + minSpan - 1, next.end));
    setHoverIndex(null);
    setTimeWindow({ start, end });
  }

  function zoom(factor: number) {
    const span = effectiveWindow.end - effectiveWindow.start + 1;
    const nextSpan = Math.max(30, Math.min(fullLimit, Math.round(span * factor)));
    const center = Math.round((effectiveWindow.start + effectiveWindow.end) / 2);
    updateWindow({ start: center - Math.floor(nextSpan / 2), end: center + Math.ceil(nextSpan / 2) - 1 });
  }

  function pan(direction: -1 | 1) {
    const span = effectiveWindow.end - effectiveWindow.start + 1;
    const shift = Math.max(1, Math.round(span * 0.65));
    updateWindow({ start: effectiveWindow.start + direction * shift, end: effectiveWindow.end + direction * shift });
  }

  function setRecentMonths(months: number) {
    const next = rangeForMonths(categories, months);
    if (next) updateWindow(next);
  }

  const chart = useMemo(() => {
    const width = 960;
    const height = 360;
    const margin = { top: 18, right: 28, bottom: 42, left: 74 };
    const visibleCategories = categories?.slice(effectiveWindow.start, effectiveWindow.end + 1);
    const limit = visibleCategories?.length ? visibleCategories.length : effectiveWindow.end - effectiveWindow.start + 1;
    const chartSeries = series.map((item) => ({ ...item, data: item.data.slice(effectiveWindow.start, effectiveWindow.end + 1).map(Number) }));
    const points = chartSeries.flatMap((item) =>
      item.data.map((value, index) => ({ index, value: Number(value), name: item.name }))
    );
    const drawable = points.filter((point) => Number.isFinite(point.value));
    if (!drawable.length) return null;

    const x = scaleLinear()
      .domain(extent(drawable, (point) => point.index) as [number, number])
      .range([margin.left, width - margin.right]);
    const values = drawable.map((point) => point.value).filter((value) => yAxisType === 'linear' || value > 0);
    const yMax = max(values) ?? 1;
    const yMin = yAxisType === 'logarithmic' ? Math.max(1, Math.min(...values)) : 0;
    const y = yAxisType === 'logarithmic'
      ? scaleLog().domain([yMin, yMax]).range([height - margin.bottom, margin.top]).nice()
      : scaleLinear().domain([0, yMax]).range([height - margin.bottom, margin.top]).nice();
    const pathFor = line<number>()
      .defined((value) => Number.isFinite(value) && (yAxisType === 'linear' || value > 0))
      .x((_value, index) => x(index))
      .y((value) => y(value));
    const dynamicTickIndexes = dateTickIndexes(visibleCategories);
    const tickIndexes = dynamicTickIndexes.length
      ? dynamicTickIndexes
      : Array.from(new Set([0, Math.floor((x.domain()[1] || 0) / 2), x.domain()[1] || 0]));
    const milestones = showMilestones ? milestoneIndexes(visibleCategories) : [];
    const nearestIndex = (svgClientX: number, svgLeft: number, svgWidth: number) => {
      const viewBoxX = ((svgClientX - svgLeft) / svgWidth) * width;
      return Math.max(0, Math.min(limit - 1, Math.round(x.invert(viewBoxX))));
    };

    return { width, height, margin, x, y, pathFor, tickIndexes, chartSeries, milestones, visibleCategories, nearestIndex };
  }, [series, categories, yAxisType, showMilestones, effectiveWindow]);

  if (!chart) return <EmptyChart />;

  return (
    <div className="d3-chart">
      <div className="chart-header">
        <ChartTitle title={title} />
        {canDrill ? (
          <div className="time-controls" aria-label="Time range controls">
            <button type="button" onClick={() => pan(-1)} disabled={effectiveWindow.start === 0} title="Previous window">&#8592;</button>
            <button type="button" onClick={() => zoom(0.5)} disabled={(effectiveWindow.end - effectiveWindow.start + 1) <= 30} title="Drill down">+</button>
            <button type="button" onClick={() => zoom(2)} disabled={effectiveWindow.start === 0 && effectiveWindow.end === fullLimit - 1} title="Drill up">-</button>
            <button type="button" onClick={() => pan(1)} disabled={effectiveWindow.end >= fullLimit - 1} title="Next window">&#8594;</button>
            <button type="button" onClick={() => updateWindow({ start: 0, end: fullLimit - 1 })}>All</button>
            <button type="button" onClick={() => setRecentMonths(12)}>1Y</button>
            <button type="button" onClick={() => setRecentMonths(6)}>6M</button>
          </div>
        ) : null}
      </div>
      <svg viewBox={`0 0 ${chart.width} ${chart.height}`} role="img" aria-label={title}>
        <g>
          {chart.y.ticks(5).map((tick) => (
            <g key={tick} className="axis-tick">
              <line x1={chart.margin.left} x2={chart.width - chart.margin.right} y1={chart.y(tick)} y2={chart.y(tick)} />
              <text x={chart.margin.left - 10} y={chart.y(tick)}>{displayValue(tick)}</text>
            </g>
          ))}
          {chart.tickIndexes.map((index) => (
            <text key={index} className="x-label" x={chart.x(index)} y={chart.height - 12}>
              {axisDateLabel(chart.visibleCategories?.[index]) || String(index + 1)}
            </text>
          ))}
          {chart.milestones.map((milestone) => (
            <g key={milestone.id} className="milestone-line" style={{ '--milestone-color': milestone.color } as CSSProperties}>
              <line x1={chart.x(milestone.index)} x2={chart.x(milestone.index)} y1={chart.margin.top} y2={chart.height - chart.margin.bottom} />
              <title>{`${milestone.label} · ${dateLabel(milestone.date)}`}</title>
            </g>
          ))}
          {chart.chartSeries.map((item) => {
            const lastIndex = item.data.length - 1;
            const lastValue = item.data[lastIndex];
            return (
              <g key={item.id ?? item.name}>
                <path
                  className="series-line"
                  d={chart.pathFor(item.data) ?? undefined}
                  stroke={palette(item.name)}
                />
                {Number.isFinite(lastValue) && (yAxisType === 'linear' || lastValue > 0) ? (
                  <circle className="series-endpoint" cx={chart.x(lastIndex)} cy={chart.y(lastValue)} r="3.4" fill={palette(item.name)} />
                ) : null}
              </g>
            );
          })}
          {hoverIndex !== null ? (
            <g className="chart-hover">
              <line x1={chart.x(hoverIndex)} x2={chart.x(hoverIndex)} y1={chart.margin.top} y2={chart.height - chart.margin.bottom} />
              {chart.chartSeries.map((item) => {
                const value = item.data[hoverIndex];
                if (!Number.isFinite(value) || (yAxisType === 'logarithmic' && value <= 0)) return null;
                return <circle key={item.id ?? item.name} cx={chart.x(hoverIndex)} cy={chart.y(value)} r="4" fill={palette(item.name)} />;
              })}
            </g>
          ) : null}
          <rect
            className="chart-hitarea"
            x={chart.margin.left}
            y={chart.margin.top}
            width={chart.width - chart.margin.left - chart.margin.right}
            height={chart.height - chart.margin.top - chart.margin.bottom}
            onMouseMove={(event) => {
              const rect = event.currentTarget.ownerSVGElement?.getBoundingClientRect();
              if (rect) setHoverIndex(chart.nearestIndex(event.clientX, rect.left, rect.width));
            }}
            onMouseLeave={() => setHoverIndex(null)}
          />
        </g>
      </svg>
      {hoverIndex !== null ? (
        <div className="chart-tooltip" role="status">
          <strong>{dateLabel(chart.visibleCategories?.[hoverIndex]) || `Point ${hoverIndex + 1}`}</strong>
          {chart.chartSeries.map((item) => (
            <span key={item.id ?? item.name}>
              <i style={{ background: palette(item.name) }} />
              {item.name}
              <b>{displayValue(item.data[hoverIndex] ?? 0)}</b>
            </span>
          ))}
        </div>
      ) : null}
      <div className="chart-legend">
        {chart.chartSeries.map((item) => (
          <span key={item.id ?? item.name}>
            <i style={{ background: palette(item.name) }} />
            {item.name}
            <strong title={displayValue(item.data[item.data.length - 1] ?? 0)}>{displayCompactValue(item.data[item.data.length - 1] ?? 0)}</strong>
          </span>
        ))}
      </div>
      {chart.milestones.length ? (
        <div className="milestone-legend" aria-label="Key periods">
          <strong>Key periods</strong>
          {chart.milestones.map((milestone) => (
            <span key={milestone.id}>
              <i style={{ '--milestone-color': milestone.color } as CSSProperties} />
              {milestone.label}
              <em>{dateLabel(milestone.date)}</em>
            </span>
          ))}
        </div>
      ) : null}
    </div>
  );
}

interface BarChartProps {
  payload: CategoryChartPayload;
  titleSuffix?: string;
}

export function GroupedBarChart({ payload, titleSuffix }: BarChartProps) {
  const chart = useMemo(() => {
    const width = 900;
    const height = Math.max(360, payload.categories.length * 28 + 72);
    const margin = { top: 18, right: 34, bottom: 28, left: 168 };
    const rows = payload.categories.map((category, index) => ({
      category,
      population: payload.population.data[index] ?? 0,
      first: payload.first.data[index] ?? 0,
      second: payload.second.data[index] ?? 0,
      booster: payload.booster.data[index] ?? 0
    }));
    const xMax = max(rows, (row) => Math.max(row.population, row.first, row.second, row.booster)) ?? 1;
    const x = scaleLinear().domain([0, xMax]).range([margin.left, width - margin.right]).nice();
    const y = scaleBand()
      .domain(rows.map((row) => row.category))
      .range([margin.top, height - margin.bottom])
      .padding(0.18);
    return { width, height, margin, rows, x, y };
  }, [payload]);

  return (
    <div className="d3-chart">
      <ChartTitle title={`${payload.title}${titleSuffix ? ` | ${titleSuffix}` : ''}`} />
      <svg viewBox={`0 0 ${chart.width} ${chart.height}`} role="img" aria-label={payload.title}>
        {chart.x.ticks(4).map((tick) => (
          <g key={tick} className="axis-tick">
            <line x1={chart.x(tick)} x2={chart.x(tick)} y1={chart.margin.top} y2={chart.height - chart.margin.bottom} />
            <text x={chart.x(tick)} y={chart.height - 8}>{valueLabel(tick)}</text>
          </g>
        ))}
        {chart.rows.map((row) => {
          const yPos = chart.y(row.category) ?? 0;
          const band = chart.y.bandwidth();
          return (
            <g key={row.category}>
              <text className="bar-label" x={chart.margin.left - 10} y={yPos + band / 2}>{row.category}</text>
              <rect className="bar-population" x={chart.margin.left} y={yPos} width={chart.x(row.population) - chart.margin.left} height={band}>
                <title>{`${row.category} · Population ${valueLabel(row.population)}`}</title>
              </rect>
              <rect className="bar-first" x={chart.margin.left} y={yPos + band * 0.18} width={chart.x(row.first) - chart.margin.left} height={band * 0.2}>
                <title>{`${row.category} · First Dose ${valueLabel(row.first)}`}</title>
              </rect>
              <rect className="bar-second" x={chart.margin.left} y={yPos + band * 0.42} width={chart.x(row.second) - chart.margin.left} height={band * 0.2}>
                <title>{`${row.category} · Second Dose ${valueLabel(row.second)}`}</title>
              </rect>
              <rect className="bar-booster" x={chart.margin.left} y={yPos + band * 0.66} width={chart.x(row.booster) - chart.margin.left} height={band * 0.2}>
                <title>{`${row.category} · Booster Dose ${valueLabel(row.booster)}`}</title>
              </rect>
            </g>
          );
        })}
      </svg>
      <div className="chart-legend">
        <span><i className="legend-population" />{payload.population.name}</span>
        <span><i className="legend-first" />{payload.first.name}</span>
        <span><i className="legend-second" />{payload.second.name}</span>
        <span><i className="legend-booster" />{payload.booster.name}</span>
      </div>
    </div>
  );
}

export function RegionCoverageChart({ payload }: { payload: CategoryChartPayload }) {
  const chart = useMemo(() => {
    const width = 900;
    const height = Math.max(420, payload.categories.length * 30 + 76);
    const margin = { top: 18, right: 92, bottom: 32, left: 168 };
    const rows = payload.categories.map((category, index) => {
      const population = payload.population.data[index] || 1;
      return {
        category,
        population,
        first: (payload.first.data[index] ?? 0) / population * 100,
        second: (payload.second.data[index] ?? 0) / population * 100,
        booster: (payload.booster.data[index] ?? 0) / population * 100
      };
    }).sort((a, b) => b.second - a.second);
    const x = scaleLinear().domain([0, Math.min(105, max(rows, (row) => row.first) ?? 100)]).range([margin.left, width - margin.right]).nice();
    const y = scaleBand().domain(rows.map((row) => row.category)).range([margin.top, height - margin.bottom]).padding(0.24);
    return { width, height, margin, rows, x, y };
  }, [payload]);

  return (
    <div className="d3-chart">
      <ChartTitle title="Vaccination coverage by region" />
      <svg viewBox={`0 0 ${chart.width} ${chart.height}`} role="img" aria-label={payload.title}>
        {chart.x.ticks(5).map((tick) => (
          <g key={tick} className="axis-tick">
            <line x1={chart.x(tick)} x2={chart.x(tick)} y1={chart.margin.top} y2={chart.height - chart.margin.bottom} />
            <text x={chart.x(tick)} y={chart.height - 10}>{percentLabel(tick)}</text>
          </g>
        ))}
        {chart.rows.map((row) => {
          const yPos = chart.y(row.category) ?? 0;
          const band = chart.y.bandwidth();
          return (
            <g key={row.category}>
              <text className="bar-label" x={chart.margin.left - 10} y={yPos + band / 2}>{row.category}</text>
              <rect className="bar-track" x={chart.margin.left} y={yPos} width={chart.x(100) - chart.margin.left} height={band} />
              <rect fill={doseColors.first} x={chart.margin.left} y={yPos + band * 0.12} width={chart.x(row.first) - chart.margin.left} height={band * 0.22}>
                <title>{`${row.category} · First Dose ${percentLabel(row.first)}`}</title>
              </rect>
              <rect fill={doseColors.second} x={chart.margin.left} y={yPos + band * 0.39} width={chart.x(row.second) - chart.margin.left} height={band * 0.22}>
                <title>{`${row.category} · Second Dose ${percentLabel(row.second)}`}</title>
              </rect>
              <rect fill={doseColors.booster} x={chart.margin.left} y={yPos + band * 0.66} width={chart.x(row.booster) - chart.margin.left} height={band * 0.22}>
                <title>{`${row.category} · Booster Dose ${percentLabel(row.booster)}`}</title>
              </rect>
              <text className="value-label" x={chart.x(row.second) + 6} y={yPos + band / 2}>{percentLabel(row.second)}</text>
            </g>
          );
        })}
      </svg>
      <DoseLegend />
    </div>
  );
}

export function AgeDoseChart({ payload, titleSuffix }: { payload: CategoryChartPayload; titleSuffix?: string }) {
  const chart = useMemo(() => {
    const width = 900;
    const height = 420;
    const margin = { top: 18, right: 28, bottom: 54, left: 78 };
    const doseKeys = ['first', 'second', 'booster'] as const;
    const rows = payload.categories.map((category, index) => ({
      category,
      first: payload.first.data[index] ?? 0,
      second: payload.second.data[index] ?? 0,
      booster: payload.booster.data[index] ?? 0
    }));
    const x = scaleBand().domain(rows.map((row) => row.category)).range([margin.left, width - margin.right]).padding(0.22);
    const xDose = scaleBand().domain(doseKeys).range([0, x.bandwidth()]).padding(0.08);
    const y = scaleLinear().domain([0, max(rows, (row) => Math.max(row.first, row.second, row.booster)) ?? 1]).range([height - margin.bottom, margin.top]).nice();
    return { width, height, margin, rows, x, xDose, y, doseKeys };
  }, [payload]);

  return (
    <div className="d3-chart">
      <ChartTitle title={`${payload.title}${titleSuffix ? ` | ${titleSuffix}` : ''}`} />
      <svg viewBox={`0 0 ${chart.width} ${chart.height}`} role="img" aria-label={payload.title}>
        {chart.y.ticks(5).map((tick) => (
          <g key={tick} className="axis-tick">
            <line x1={chart.margin.left} x2={chart.width - chart.margin.right} y1={chart.y(tick)} y2={chart.y(tick)} />
            <text x={chart.margin.left - 10} y={chart.y(tick)}>{formatCompactNumber(tick)}</text>
          </g>
        ))}
        {chart.rows.map((row) => {
          const xPos = chart.x(row.category) ?? 0;
          return (
            <g key={row.category}>
              {chart.doseKeys.map((dose) => {
                const value = row[dose];
                return (
                  <rect
                    key={dose}
                    fill={doseColors[dose]}
                    x={xPos + (chart.xDose(dose) ?? 0)}
                    y={chart.y(value)}
                    width={chart.xDose.bandwidth()}
                    height={chart.height - chart.margin.bottom - chart.y(value)}
                  >
                    <title>{`${row.category} · ${dose} ${valueLabel(value)}`}</title>
                  </rect>
                );
              })}
              <text className="x-label" x={xPos + chart.x.bandwidth() / 2} y={chart.height - 18}>{row.category}</text>
            </g>
          );
        })}
      </svg>
      <DoseLegend />
    </div>
  );
}

function DoseLegend() {
  return (
    <div className="chart-legend">
      <span><i style={{ background: doseColors.first }} />First Dose</span>
      <span><i style={{ background: doseColors.second }} />Second Dose</span>
      <span><i style={{ background: doseColors.booster }} />Booster Dose</span>
    </div>
  );
}

export function VaccinationTrendChart({ payload }: { payload: TrendChartPayload }) {
  const [selected, setSelected] = useState(() => new Set(['Sicilia', 'Lombardia', 'Lazio']));
  const visibleSeries = payload.data.filter((item) => selected.has(item.name));

  function toggle(name: string) {
    setSelected((current) => {
      const next = new Set(current);
      if (next.has(name)) next.delete(name);
      else if (next.size < 5) next.add(name);
      return next;
    });
  }

  return (
    <div className="vax-trend">
      <div className="region-filter" aria-label="Trend region selector">
        {payload.data.map((item) => (
          <button key={item.name} type="button" className={selected.has(item.name) ? 'active' : ''} onClick={() => toggle(item.name)}>
            {item.name}
          </button>
        ))}
      </div>
      <TimeSeriesChart title={payload.title} series={visibleSeries.length ? visibleSeries : payload.data.slice(0, 1)} categories={payload.dates} valueKind="percent" />
    </div>
  );
}

export function ProviderPieChart({ payload, titleSuffix }: { payload: PieChartPayload; titleSuffix?: string }) {
  const chart = useMemo(() => {
    const width = 720;
    const height = 420;
    const radius = 150;
    const total = payload.data.reduce((sum, item) => sum + item[1], 0);
    const pieLayout = pie<[string, number]>()
      .sort(null)
      .value((item) => item[1]);
    const arcPath = arc<PieArcDatum<[string, number]>>()
      .innerRadius(radius * 0.58)
      .outerRadius(radius);
    const arcs = pieLayout(payload.data);
    return { width, height, radius, total, arcs, arcPath };
  }, [payload]);

  return (
    <div className="d3-chart">
      <ChartTitle title={`${payload.title}${titleSuffix ? ` | ${titleSuffix}` : ''}`} />
      <svg viewBox={`0 0 ${chart.width} ${chart.height}`} role="img" aria-label={payload.title}>
        <g transform={`translate(${chart.width / 2}, ${chart.height * 0.48})`}>
          {chart.arcs.map((item, index) => (
            <path key={item.data[0]} d={chart.arcPath(item) ?? undefined} fill={palette(item.data[0])} opacity={0.95 - index * 0.04}>
              <title>{`${item.data[0]} · ${valueLabel(item.data[1])} · ${percentLabel(item.data[1] / chart.total * 100)}`}</title>
            </path>
          ))}
          <text className="pie-total" y="-12">{formatCompactNumber(chart.total)}</text>
          <text className="pie-caption" y="12">{payload.name}</text>
        </g>
      </svg>
      <div className="chart-legend">
        {payload.data.map((item) => (
          <span key={item[0]}>
            <i style={{ background: palette(item[0]) }} />
            {item[0]}
            <strong>{percentLabel(item[1] / chart.total * 100)}</strong>
          </span>
        ))}
      </div>
    </div>
  );
}
