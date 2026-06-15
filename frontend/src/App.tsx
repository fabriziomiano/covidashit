import { Navigate, Route, Routes } from 'react-router-dom';
import { getConfig } from './api/client';
import { useAsync } from './api/useAsync';
import { Layout } from './components/Layout';
import { ErrorState, LoadingState } from './components/Status';
import { PandemicPage } from './pages/PandemicPage';
import { ThanksPage } from './pages/ThanksPage';
import { VaccinesPage } from './pages/VaccinesPage';

export default function App() {
  const { data: config, error, loading } = useAsync(getConfig, []);

  if (loading) return <LoadingState title="COVIDash.it" message="Loading application configuration..." />;
  if (error || !config) return <ErrorState title="Configuration unavailable" message={error?.message ?? 'Unable to load /api/config'} />;

  return (
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
  );
}
