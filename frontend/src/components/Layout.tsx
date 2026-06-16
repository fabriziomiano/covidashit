import { Link, NavLink, Outlet } from 'react-router-dom';
import { AreaSearch } from './AreaSearch';
import type { DashboardConfig } from '../types/covidash';
import { useLanguage } from '../i18n';

interface LayoutProps {
  config: DashboardConfig;
}

export function Layout({ config }: LayoutProps) {
  const { locale, setLocale, t } = useLanguage();

  return (
    <div className="app-shell">
      <header className="topbar">
        <Link className="brand" to="/">
          <img src="/static/img/covidash_32.png" alt="" onError={(event) => { event.currentTarget.style.display = 'none'; }} />
          <span>COVIDash.it</span>
        </Link>
        <nav className="main-nav" aria-label="Primary">
          <NavLink to="/">{t('Pandemic')}</NavLink>
          <NavLink to="/vaccines">{t('Vax')}</NavLink>
        </nav>
        <div className="top-actions">
          <div className="language-toggle" aria-label="Language">
            <button type="button" className={locale === 'it' ? 'active' : ''} onClick={() => setLocale('it')}>IT</button>
            <button type="button" className={locale === 'en' ? 'active' : ''} onClick={() => setLocale('en')}>EN</button>
          </div>
          <div className="desktop-search">
            <AreaSearch config={config} id="area-search-results" />
          </div>
        </div>
      </header>
      <main>
        <Outlet context={{ config }} />
      </main>
      <footer className="footer">
        <span>
          COVIDash.it &middot; Re-Made with ❤ in Catania by{' '}
          <a href="https://github.com/FabrizioMiano" target="_blank" rel="noreferrer">FabrizioMiano</a>{' '}
          with the help of Codex &middot; <Link to="/thanks">Acknowledgements</Link>
        </span>
      </footer>
    </div>
  );
}
