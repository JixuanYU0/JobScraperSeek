import { useState, useEffect } from 'react';
import './App.css';
import JobsList from './components/JobsList';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(null);

  // Fetch jobs on mount and every 5 minutes
  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 5 * 60 * 1000); // Auto-refresh every 5 minutes
    return () => clearInterval(interval);
  }, []);

  const fetchJobs = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/api/v1/jobs/latest?limit=100`);
      if (!response.ok) throw new Error('Failed to fetch jobs');
      const data = await response.json();
      setJobs(data);
      setLastUpdate(new Date());
      setError(null);
    } catch (err) {
      console.error('Error fetching jobs:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatLastUpdate = () => {
    if (!lastUpdate) return '';
    const now = new Date();
    const diff = Math.floor((now - lastUpdate) / 1000); // seconds

    if (diff < 60) return 'just now';
    if (diff < 3600) return `${Math.floor(diff / 60)} minutes ago`;
    return lastUpdate.toLocaleTimeString();
  };

  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <h1>Job Listings Dashboard</h1>
          <p className="subtitle">Latest opportunities from Seek.com.au</p>
        </div>
      </header>

      <main className="container">
        {/* Stats Bar */}
        <section className="stats-bar">
          <div className="stat">
            <div className="stat-value">{jobs.length}</div>
            <div className="stat-label">Total Jobs</div>
          </div>
          <div className="stat">
            <div className="stat-value">
              {jobs.filter(j => {
                const posted = new Date(j.scraped_at);
                const dayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
                return posted > dayAgo;
              }).length}
            </div>
            <div className="stat-label">Last 24 Hours</div>
          </div>
          <div className="stat">
            <div className="stat-value">
              {[...new Set(jobs.map(j => j.company))].length}
            </div>
            <div className="stat-label">Companies</div>
          </div>
          <div className="stat">
            <div className="stat-value auto-refresh">
              {loading ? '⟳' : '✓'}
            </div>
            <div className="stat-label">
              Updated {formatLastUpdate()}
            </div>
          </div>
        </section>

        {error && (
          <div className="alert alert-error">
            <strong>Connection Error:</strong> {error}
            <button onClick={fetchJobs} className="btn btn-small">Retry</button>
          </div>
        )}

        {/* Jobs List */}
        <section className="section">
          {loading && jobs.length === 0 ? (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Loading jobs...</p>
            </div>
          ) : (
            <JobsList jobs={jobs} onRefresh={fetchJobs} />
          )}
        </section>
      </main>

      <footer className="footer">
        <div className="container">
          <p>
            Jobs automatically updated daily via scheduled scraping |{' '}
            <button onClick={fetchJobs} className="link-button">
              Refresh Now
            </button>
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
