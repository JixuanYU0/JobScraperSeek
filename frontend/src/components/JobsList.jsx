import { useState } from 'react';
import JobCard from './JobCard';

function JobsList({ jobs, onRefresh }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterLocation, setFilterLocation] = useState('');
  const [filterCompany, setFilterCompany] = useState('');

  // Extract unique locations and companies for filters
  const uniqueLocations = [...new Set(jobs.map(job => job.location))].sort();
  const uniqueCompanies = [...new Set(jobs.map(job => job.company))].sort();

  // Filter jobs
  const filteredJobs = jobs.filter(job => {
    const matchesSearch = job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         job.company.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesLocation = !filterLocation || job.location === filterLocation;
    const matchesCompany = !filterCompany || job.company === filterCompany;

    return matchesSearch && matchesLocation && matchesCompany;
  });

  const handleExport = () => {
    // Export to CSV
    const headers = ['Title', 'Company', 'Location', 'Salary', 'Job Type', 'URL', 'Scraped At'];
    const rows = filteredJobs.map(job => [
      job.title,
      job.company,
      job.location,
      job.salary || 'N/A',
      job.job_type || 'N/A',
      job.url,
      new Date(job.scraped_at).toLocaleString()
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `seek-jobs-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="jobs-list">
      <div className="jobs-controls">
        <div className="search-filters">
          <input
            type="text"
            placeholder="Search jobs or companies..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />

          <select
            value={filterLocation}
            onChange={(e) => setFilterLocation(e.target.value)}
            className="filter-select"
          >
            <option value="">All Locations</option>
            {uniqueLocations.map(loc => (
              <option key={loc} value={loc}>{loc}</option>
            ))}
          </select>

          <select
            value={filterCompany}
            onChange={(e) => setFilterCompany(e.target.value)}
            className="filter-select"
          >
            <option value="">All Companies</option>
            {uniqueCompanies.map(company => (
              <option key={company} value={company}>{company}</option>
            ))}
          </select>
        </div>

        <div className="action-buttons">
          <button onClick={onRefresh} className="btn btn-secondary">
            Refresh
          </button>
          <button onClick={handleExport} className="btn btn-secondary">
            Export CSV
          </button>
        </div>
      </div>

      <div className="results-info">
        Showing {filteredJobs.length} of {jobs.length} jobs
      </div>

      {filteredJobs.length === 0 ? (
        <div className="empty-state">
          <p>No jobs found. Try adjusting your filters or start a new scrape.</p>
        </div>
      ) : (
        <div className="jobs-grid">
          {filteredJobs.map(job => (
            <JobCard key={job.job_id} job={job} />
          ))}
        </div>
      )}
    </div>
  );
}

export default JobsList;
