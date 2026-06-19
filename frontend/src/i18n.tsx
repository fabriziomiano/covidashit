import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';

export type Locale = 'en' | 'it';

// Current React translations are adapted from the previous Poedit/Babel Italian catalog.
const MESSAGES: Record<Locale, Record<string, string>> = {
  en: {},
  it: {
    'COVIDash.it | Italian COVID-19 Dashboard': 'COVIDash.it | Dashboard COVID-19 Italia',
    'Explore Italian COVID-19 pandemic trends across national, regional, and provincial dashboards.': 'Esplora l\'andamento della pandemia COVID-19 in Italia su dashboard nazionali, regionali e provinciali.',
    'Explore Italian COVID-19 pandemic and vaccination data from open public datasets.': 'Esplora dati italiani su pandemia e vaccinazioni da dataset pubblici open data.',
    'Italy Vaccination Dashboard | COVIDash.it': 'Dashboard Vaccini Italia | COVIDash.it',
    'Explore Italian COVID-19 vaccination data, dose trends, and regional comparisons.': 'Esplora dati vaccinali COVID-19 in Italia, andamento delle dosi e confronti regionali.',
    'Acknowledgements | COVIDash.it': 'Ringraziamenti | COVIDash.it',
    Thanks: 'Grazie',
    'Thank you': 'Grazie',
    'Data sources': 'Fonti dati',
    'COVIDash.it acknowledgements for the open data sources and contributors behind the dashboard.': 'Ringraziamenti COVIDash.it per fonti open data e contributori alla dashboard.',
    Vax: 'Vaccini',
    Vaccines: 'Vaccini',
    'Search area': 'Cerca area',
    'Search region or province': 'Cerca regione o provincia',
    Go: 'Vai',
    Region: 'Regione',
    Province: 'Provincia',
    'No area found': 'Nessuna area trovata',
    Acknowledgements: 'Ringraziamenti',
    Version: 'Versione',
    'Loading application configuration...': 'Caricamento configurazione applicazione...',
    'Configuration unavailable': 'Configurazione non disponibile',
    'Unable to load /api/config': 'Impossibile caricare /api/config',
    'Loading dashboard data...': 'Caricamento dati dashboard...',
    'National dashboard': 'Dashboard nazionale',
    'Regional dashboard': 'Dashboard regionale',
    'Provincial dashboard': 'Dashboard provinciale',
    'Latest update': 'Ultimo aggiornamento',
    Population: 'Popolazione',
    Positivity: 'Indice positivita',
    Italy: 'Italia',
    Daily: 'Giornaliero',
    Current: 'Corrente',
    Cumulative: 'Cumulato',
    Pandemic: 'Pandemia',
    'Pandemic data unavailable': 'Dati pandemia non disponibili',
    'No data returned by the API.': 'Nessun dato restituito dall\'API.',
    'Daily trend': 'Andamento giornaliero',
    'Current trend': 'Andamento corrente',
    'Cumulative trend': 'Andamento cumulato',
    'Chart unavailable': 'Grafico non disponibile',
    'The API returned no series for this panel.': 'L\'API non ha restituito serie per questo pannello.',
    Regions: 'Regioni',
    Provinces: 'Province',
    'Vaccination dashboard': 'Dashboard vaccini',
    'Vaccine data unavailable': 'Dati vaccinali non disponibili',
    'No vaccine data returned by the API.': 'Nessun dato vaccinale restituito dall\'API.',
    Administered: 'Somministrate',
    'First Dose': 'Prima dose',
    'Second Dose': 'Seconda dose',
    Booster: 'Booster',
    'vs previous sample': 'vs campione precedente',
    'vs 7d ago': 'vs 7gg fa',
    Previous: 'Precedente',
    'Admins per region': 'Somministrazioni per regione',
    'Vaccination trend': 'Andamento vaccinazioni',
    'Admins per age': 'Somministrazioni per eta',
    'Admins per provider': 'Somministrazioni per fornitore',
    unavailable: 'non disponibile',
    'Regional vaccines': 'Vaccini regionali',
    'Page not found': 'Pagina non trovata',
    'Choose a dashboard from the navigation.': 'Scegli una dashboard dalla navigazione.',
    'COVIDash.it exists thanks to open data, public health datasets, and the original project contributors.': 'COVIDash.it esiste grazie a open data, dataset pubblici sanitari e contributori del progetto originale.',
    'COVIDash.it makes Italian COVID-19 pandemic and vaccination trends easy to inspect, compare, and share.': 'COVIDash.it rende i dati italiani su pandemia e vaccinazioni facili da consultare, confrontare e condividere.',
    'Official Italian Civil Protection pandemic datasets.': 'Dataset ufficiali della Protezione Civile italiana.',
    'Official vaccination delivery and administration datasets.': 'Dataset ufficiali su consegne e somministrazioni vaccinali.',
    'Population reference data used for coverage and per-area comparisons.': 'Dati popolazione usati per copertura vaccinale e confronti territoriali.',
    'Official Italian vaccination open data.': 'Open data ufficiali italiani sulle vaccinazioni.',
    'Population data used for vaccine coverage calculations.': 'Dati popolazione usati per calcolare la copertura vaccinale.',
    'Read the acknowledgements': 'Apri i ringraziamenti',
    'Area search': 'Cerca area',
    'Find regional or provincial dashboards': 'Trova dashboard regionali o provinciali',
    'Use the search after the first metrics when you need to jump to a specific area.': 'Usa la ricerca dopo i primi indicatori quando vuoi saltare a un\'area specifica.',
    'Historical COVID-19 archive': 'Archivio storico COVID-19',
    'Data is preserved for inspection and is no longer a live public-health feed.': 'I dati sono conservati per consultazione e non sono piu un flusso sanitario in tempo reale.',
    Explore: 'Esplora',
    Track: 'Monitora',
    'COVID-19 vaccination data and dose trends': 'dati vaccinali COVID-19 e andamento delle dosi',
    'COVID-19 cases, testing, hospitalizations, and trend indicators': 'casi COVID-19, tamponi, ricoveri e indicatori di andamento',
    'COVID-19 provincial trend data and daily indicators': 'dati provinciali COVID-19 e indicatori giornalieri',
    'n/a': 'n/d',
  },
};

interface LanguageContextValue {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  t: (message: string) => string;
}

const LanguageContext = createContext<LanguageContextValue | null>(null);

function initialLocale(): Locale {
  const params = new URLSearchParams(window.location.search);
  const requested = params.get('lang')?.toLowerCase();
  if (requested === 'en' || requested === 'it') return requested;
  const stored = window.localStorage.getItem('covidash-locale');
  if (stored === 'en' || stored === 'it') return stored;
  return window.navigator.language.toLowerCase().startsWith('it') ? 'it' : 'en';
}

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>(() => initialLocale());

  const setLocale = (nextLocale: Locale) => {
    setLocaleState(nextLocale);
    window.localStorage.setItem('covidash-locale', nextLocale);
  };

  useEffect(() => {
    document.documentElement.lang = locale;
  }, [locale]);

  const value = useMemo(() => ({
    locale,
    setLocale,
    t: (message: string) => MESSAGES[locale][message] ?? message,
  }), [locale]);

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) throw new Error('useLanguage must be used inside LanguageProvider');
  return context;
}

export function translateText(message: string, locale: Locale) {
  return MESSAGES[locale][message] ?? message;
}
