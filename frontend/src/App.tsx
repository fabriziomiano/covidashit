import { useEffect } from 'react';
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import { getConfig } from './api/client';
import { LanguageProvider, translateText, useLanguage } from './i18n';
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

function routeSeo(pathname: string, locale: 'en' | 'it') {
  const normalized = pathname.replace(/\/$/, '') || '/';
  const segments = normalized.split('/').filter(Boolean).map((segment) => decodeURIComponent(segment));
  const translate = (message: string) => translateText(message, locale);
  if (normalized === '/') {
    return {
      title: translate('COVIDash.it | Italian COVID-19 Dashboard'),
      description: translate('Explore Italian COVID-19 pandemic trends across national, regional, and provincial dashboards.'),
    };
  }
  if (segments[0] === 'vaccines') {
    const area = segments[1];
    return {
      title: area ? `${area} ${translate('Vaccines')} | COVIDash.it` : translate('Italy Vaccination Dashboard | COVIDash.it'),
      description: area
        ? `${translate('Explore')} ${translate('COVID-19 vaccination data and dose trends')} ${locale === 'it' ? 'per' : 'for'} ${area}.`
        : translate('Explore Italian COVID-19 vaccination data, dose trends, and regional comparisons.'),
    };
  }
  if (segments[0] === 'regions' && segments[1]) {
    return {
      title: `${segments[1]} COVID-19 | COVIDash.it`,
      description: `${translate('Track')} ${translate('COVID-19 cases, testing, hospitalizations, and trend indicators')} ${locale === 'it' ? 'per' : 'for'} ${segments[1]}.`,
    };
  }
  if (segments[0] === 'provinces' && segments[1]) {
    return {
      title: `${segments[1]} COVID-19 | COVIDash.it`,
      description: `${translate('Track')} ${translate('COVID-19 provincial trend data and daily indicators')} ${locale === 'it' ? 'per' : 'for'} ${segments[1]}.`,
    };
  }
  if (segments[0] === 'thanks') {
    return {
      title: translate('Acknowledgements | COVIDash.it'),
      description: translate('COVIDash.it acknowledgements for the open data sources and contributors behind the dashboard.'),
    };
  }
  return {
    title: translate('COVIDash.it | Italian COVID-19 Dashboard'),
    description: translate('Explore Italian COVID-19 pandemic and vaccination data from open public datasets.'),
  };
}

function Seo() {
  const location = useLocation();
  const { locale } = useLanguage();

  useEffect(() => {
    const seo = routeSeo(location.pathname, locale);
    const canonical = `${SITE_URL}${location.pathname}`;
    document.title = seo.title;
    setMeta('meta[name="description"]', 'content', seo.description);
    setMeta('meta[property="og:title"]', 'content', seo.title);
    setMeta('meta[property="og:description"]', 'content', seo.description);
    setMeta('meta[property="og:url"]', 'content', canonical);
    setMeta('meta[name="twitter:title"]', 'content', seo.title);
    setMeta('meta[name="twitter:description"]', 'content', seo.description);
    setMeta('link[rel="canonical"]', 'href', canonical);
  }, [locale, location.pathname]);

  return null;
}

function AppRoutes() {
  const { data: config, error, loading } = useAsync(getConfig, []);

  const { t } = useLanguage();

  if (loading) return <LoadingState title="COVIDash.it" message={t('Loading application configuration...')} />;
  if (error || !config) return <ErrorState title={t('Configuration unavailable')} message={error?.message ?? t('Unable to load /api/config')} />;

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
          <Route path="*" element={<ErrorState title={t('Page not found')} message={t('Choose a dashboard from the navigation.')} />} />
        </Route>
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <LanguageProvider>
      <AppRoutes />
    </LanguageProvider>
  );
}
