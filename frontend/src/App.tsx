import { useEffect } from 'react';
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import { getConfig } from './api/client';
import { useAsync } from './api/useAsync';
import { Layout } from './components/Layout';
import { ErrorState, LoadingState } from './components/Status';
import { PandemicPage } from './pages/PandemicPage';
import { ThanksPage } from './pages/ThanksPage';
import { VaccinesPage } from './pages/VaccinesPage';

const SITE_URL = 'https://covidash.it';

function setMeta(selector: string, attribute: 'content' | 'href', value: string) {
  const element = document.head.querySelector(selector);
  if (element) element.setAttribute(attribute, value);
}

function routeSeo(pathname: string) {
  const normalized = pathname.replace(/\/$/, '') || '/';
  const segments = normalized.split('/').filter(Boolean).map((segment) => decodeURIComponent(segment));
  if (normalized === '/') {
    return {
      title: 'COVIDash.it | Italian COVID-19 Dashboard',
      description: 'Explore Italian COVID-19 pandemic trends across national, regional, and provincial dashboards.',
    };
  }
  if (segments[0] === 'vaccines') {
    const area = segments[1];
    return {
      title: area ? `${area} Vaccination Dashboard | COVIDash.it` : 'Italy Vaccination Dashboard | COVIDash.it',
      description: area
        ? `Explore COVID-19 vaccination data and dose trends for ${area}.`
        : 'Explore Italian COVID-19 vaccination data, dose trends, and regional comparisons.',
    };
  }
  if (segments[0] === 'regions' && segments[1]) {
    return {
      title: `${segments[1]} COVID-19 Dashboard | COVIDash.it`,
      description: `Track COVID-19 cases, testing, hospitalizations, and trend indicators for ${segments[1]}.`,
    };
  }
  if (segments[0] === 'provinces' && segments[1]) {
    return {
      title: `${segments[1]} COVID-19 Dashboard | COVIDash.it`,
      description: `Track COVID-19 provincial trend data and daily indicators for ${segments[1]}.`,
    };
  }
  if (segments[0] === 'thanks') {
    return {
      title: 'Acknowledgements | COVIDash.it',
      description: 'COVIDash.it acknowledgements for the open data sources and contributors behind the dashboard.',
    };
  }
  return {
    title: 'COVIDash.it | Italian COVID-19 Dashboard',
    description: 'Explore Italian COVID-19 pandemic and vaccination data from open public datasets.',
  };
}

function Seo() {
  const location = useLocation();

  useEffect(() => {
    const seo = routeSeo(location.pathname);
    const canonical = `${SITE_URL}${location.pathname}`;
    document.title = seo.title;
    setMeta('meta[name="description"]', 'content', seo.description);
    setMeta('meta[property="og:title"]', 'content', seo.title);
    setMeta('meta[property="og:description"]', 'content', seo.description);
    setMeta('meta[property="og:url"]', 'content', canonical);
    setMeta('meta[name="twitter:title"]', 'content', seo.title);
    setMeta('meta[name="twitter:description"]', 'content', seo.description);
    setMeta('link[rel="canonical"]', 'href', canonical);
  }, [location.pathname]);

  return null;
}

export default function App() {
  const { data: config, error, loading } = useAsync(getConfig, []);

  if (loading) return <LoadingState title="COVIDash.it" message="Loading application configuration..." />;
  if (error || !config) return <ErrorState title="Configuration unavailable" message={error?.message ?? 'Unable to load /api/config'} />;

  return (
    <>
      <Seo />
      <Routes>
        <Route element={<Layout config={config} />}>
        <Route index element={<PandemicPage config={config} scope="national" />} />
        <Route path="regions/:area" element={<PandemicPage config={config} scope="regional" />} />
        <Route path="provinces/:area" element={<PandemicPage config={config} scope="provincial" />} />
        <Route path="vaccines" element={<VaccinesPage config={config} />} />
        <Route path="vaccines/:area" element={<VaccinesPage config={config} />} />
        <Route path="thanks" element={<ThanksPage />} />
        <Route path="national" element={<Navigate to="/" replace />} />
        <Route path="*" element={<ErrorState title="Page not found" message="Choose a dashboard from the navigation." />} />
        </Route>
      </Routes>
    </>
  );
}
