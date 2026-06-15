import { FormEvent, KeyboardEvent, useMemo, useState } from 'react';
import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom';
import type { DashboardConfig } from '../types/covidash';

interface LayoutProps {
  config: DashboardConfig;
}

export function Layout({ config }: LayoutProps) {
  const navigate = useNavigate();
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
    <div className="app-shell">
      <header className="topbar">
        <Link className="brand" to="/">
          <img src="/static/img/covidash_32.png" alt="" onError={(event) => { event.currentTarget.style.display = 'none'; }} />
          <span>COVIDash.it</span>
        </Link>
        <nav className="main-nav" aria-label="Primary">
          <NavLink to="/">Pandemic</NavLink>
          <NavLink to="/vaccines">Vax</NavLink>
        </nav>
        <form className="area-search" onSubmit={submitSearch}>
          <input
            value={search}
            onChange={(event) => { setSearch(event.target.value); setOpen(true); setActiveIndex(0); }}
            onFocus={() => setOpen(true)}
            onKeyDown={handleKeys}
            placeholder="Search area"
            aria-label="Search region or province"
            aria-expanded={open}
            aria-controls="area-search-results"
            autoComplete="off"
          />
          <button type="submit">Go</button>
          {open ? (
            <div className="area-results" id="area-search-results">
              {matches.length ? matches.map((area, index) => (
                <button
                  type="button"
                  key={`${area.type}-${area.name}`}
                  className={index === activeIndex ? 'active' : ''}
                  onMouseDown={(event) => event.preventDefault()}
                  onClick={() => goTo(area.path)}
                >
                  <span>{area.name}</span>
                  <em>{area.type}</em>
                </button>
              )) : <p>No area found</p>}
            </div>
          ) : null}
        </form>
      </header>
      <main>
        <Outlet />
      </main>
      <footer className="footer">
        <span>
          COVIDash.it &middot; Re-Made with ❤ in Catania by{' '}
          <a href="https://github.com/FabrizioMiano" target="_blank" rel="noreferrer">FabrizioMiano</a>{' '}
          with the help of Code
        </span>
        <span>Version {config.version}</span>
        <Link to="/thanks">Acknowledgements</Link>
      </footer>
    </div>
  );
}
