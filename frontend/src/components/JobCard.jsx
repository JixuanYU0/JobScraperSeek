function JobCard({ job }) {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="job-card">
      <div className="job-card-header">
        <h3 className="job-title">
          <a href={job.job_url} target="_blank" rel="noopener noreferrer">
            {job.title}
          </a>
        </h3>
        <span className="job-time">{formatDate(job.scraped_at)}</span>
      </div>

      <div className="job-company">
        <strong>{job.company}</strong>
      </div>

      <div className="job-details">
        <span className="job-detail-item">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
            <path d="M8 0a6 6 0 0 0-6 6c0 3.3 6 10 6 10s6-6.7 6-10a6 6 0 0 0-6-6zm0 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4z"/>
          </svg>
          {job.location}
        </span>

        {job.salary && (
          <span className="job-detail-item">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
              <path d="M8 0C3.6 0 0 3.6 0 8s3.6 8 8 8 8-3.6 8-8-3.6-8-8-8zm1 12H7V7h2v5zm0-6H7V4h2v2z"/>
            </svg>
            {job.salary}
          </span>
        )}

        {job.job_type && (
          <span className="job-detail-item">
            <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
              <path d="M14 4h-2V3c0-.55-.45-1-1-1H5c-.55 0-1 .45-1 1v1H2c-1.1 0-2 .9-2 2v7c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zM5 3h6v1H5V3z"/>
            </svg>
            {job.job_type}
          </span>
        )}
      </div>

      {job.description && (
        <div className="job-description">
          {job.description.substring(0, 150)}
          {job.description.length > 150 ? '...' : ''}
        </div>
      )}

      <div className="job-card-footer">
        <a
          href={job.job_url}
          target="_blank"
          rel="noopener noreferrer"
          className="btn btn-small btn-primary"
        >
          View on Seek
        </a>
      </div>
    </div>
  );
}

export default JobCard;
