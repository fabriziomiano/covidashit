export function ThanksPage() {
  const sources = [
    {
      name: 'PCM-DPC COVID-19',
      href: 'https://github.com/pcm-dpc/COVID-19',
      text: 'Official Italian Civil Protection pandemic datasets.'
    },
    {
      name: 'Italia Open Data Vaccini',
      href: 'https://github.com/italia/covid19-opendata-vaccini',
      text: 'Official vaccination delivery and administration datasets.'
    },
    {
      name: 'ISTAT',
      href: 'https://www.istat.it/',
      text: 'Population reference data used for coverage and per-area comparisons.'
    }
  ];

  return (
    <section className="dashboard-page narrow-page">
      <div className="page-heading">
        <div>
          <p className="eyebrow">Thanks</p>
          <h1>Thank you</h1>
          <p className="meta-line">COVIDash.it exists thanks to open data, public health datasets, and the original project contributors.</p>
        </div>
      </div>
      <p className="body-copy">COVIDash.it makes Italian COVID-19 pandemic and vaccination trends easy to inspect, compare, and share.</p>
      <section className="thanks-section">
        <h2>Data sources</h2>
        <div className="thanks-list">
          {sources.map((source) => (
            <a key={source.name} href={source.href} target="_blank" rel="noreferrer">
              <strong>{source.name}</strong>
              <span>{source.text}</span>
            </a>
          ))}
        </div>
      </section>
    </section>
  );
}
