import { FormEvent, KeyboardEvent, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import type { DashboardConfig } from '../types/covidash';
import { useLanguage } from '../i18n';

interface AreaSearchProps {
  config: DashboardConfig;
  id: string;
  panel?: boolean;
}

export function AreaSearch({ config, id, panel = false }: AreaSearchProps) {
  const navigate = useNavigate();
  const { t } = useLanguage();
  const [search, setSearch] = useState('');
  const [open, setOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(0);
  const areas = useMemo(
    () => [
      ...config.regions.map((name) => ({ name, type: 'Region' as const, path: `/regions/${encodeURIComponent(name)}` })),
      ...config.provinces.map((name) => ({ name, type: 'Province' as const, path: `/provinces/${encodeURIComponent(name)}` }))
    ],
    [config]
  );
  const matches = useMemo(() => {
    const query = search.trim().toLocaleLowerCase('it-IT');
    const filtered = query
      ? areas.filter((area) => area.name.toLocaleLowerCase('it-IT').includes(query))
      : areas.filter((area) => area.type === 'Region');
    return filtered.slice(0, 8);
  }, [areas, search]);

  function goTo(path: string) {
    navigate(path);
    setSearch('');
    setOpen(false);
    setActiveIndex(0);
  }

  function submitSearch(event: FormEvent) {
    event.preventDefault();
    const selected = matches[activeIndex] ?? matches[0];
    if (selected) goTo(selected.path);
  }

  function handleKeys(event: KeyboardEvent<HTMLInputElement>) {
    if (event.key === 'ArrowDown') {
      event.preventDefault();
      setOpen(true);
      setActiveIndex((index) => Math.min(index + 1, matches.length - 1));
    }
    if (event.key === 'ArrowUp') {
      event.preventDefault();
      setActiveIndex((index) => Math.max(index - 1, 0));
    }
    if (event.key === 'Escape') {
      setOpen(false);
      setActiveIndex(0);
    }
    if (event.key === 'Enter') {
      event.preventDefault();
      const selected = matches[activeIndex] ?? matches[0];
      if (selected) goTo(selected.path);
    }
  }

  return (
    <form className={`area-search${panel ? ' area-search--panel' : ''}`} onSubmit={submitSearch}>
      {panel ? (
        <div className="area-search__intro">
          <strong>{t('Find regional or provincial dashboards')}</strong>
          <span>{t('Use the search after the first metrics when you need to jump to a specific area.')}</span>
        </div>
      ) : null}
      <input
        value={search}
        onChange={(event) => { setSearch(event.target.value); setOpen(true); setActiveIndex(0); }}
        onFocus={() => setOpen(true)}
        onKeyDown={handleKeys}
        placeholder={t('Search area')}
        aria-label={t('Search region or province')}
        aria-expanded={open}
        aria-controls={id}
        autoComplete="off"
      />
      <button type="submit">{t('Go')}</button>
      {open ? (
        <div className="area-results" id={id}>
          {matches.length ? matches.map((area, index) => (
            <button
              type="button"
              key={`${area.type}-${area.name}`}
              className={index === activeIndex ? 'active' : ''}
              onMouseDown={(event) => event.preventDefault()}
              onClick={() => goTo(area.path)}
            >
              <span>{area.name}</span>
              <em>{t(area.type)}</em>
            </button>
          )) : <p>{t('No area found')}</p>}
        </div>
      ) : null}
    </form>
  );
}
