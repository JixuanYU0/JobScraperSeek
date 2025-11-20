#!/usr/bin/env python3
"""
Backfill job_type field for all existing jobs in jobs.json
Uses the same inference logic as the scraper.
"""

import json
from typing import Optional


def infer_job_type(description: str, salary: Optional[str] = None) -> str:
    """Infer job type from description and salary text.

    Args:
        description: Job description text
        salary: Salary text (optional)

    Returns:
        Inferred job type
    """
    if not description:
        return "Full-time"  # Default

    # Combine description and salary for analysis
    text = description.lower()
    if salary:
        text += " " + salary.lower()

    # Check for contract/temp keywords first (highest priority)
    contract_keywords = ['contract', 'contractor', 'temp', 'temporary', 'fixed term', 'fixed-term']
    if any(keyword in text for keyword in contract_keywords):
        return "Contract/Temp"

    # Check for casual keywords
    casual_keywords = ['casual', 'vacation', 'on call', 'on-call', 'relief', 'fill-in']
    if any(keyword in text for keyword in casual_keywords):
        return "Casual"

    # Check for part-time keywords
    part_time_keywords = ['part time', 'part-time', 'p/t', 'pt ', 'parttime']
    if any(keyword in text for keyword in part_time_keywords):
        return "Part-time"

    # Check for full-time keywords
    full_time_keywords = ['full time', 'full-time', 'f/t', 'ft ', 'fulltime', 'permanent', 'ongoing']
    if any(keyword in text for keyword in full_time_keywords):
        return "Full-time"

    # Default to Full-time if no specific type is mentioned (most common)
    return "Full-time"


def main():
    """Backfill job_type for all jobs."""
    print("Loading jobs.json...")
    with open('data/jobs.json', 'r') as f:
        jobs = json.load(f)

    print(f"Total jobs: {len(jobs)}")

    # Count jobs without job_type
    missing_count = sum(1 for job in jobs if not job.get('job_type'))
    print(f"Jobs missing job_type: {missing_count}")

    # Backfill job_type
    updated_count = 0
    for job in jobs:
        if not job.get('job_type'):
            description = job.get('description', '')
            salary = job.get('salary')
            job['job_type'] = infer_job_type(description, salary)
            updated_count += 1

    print(f"Updated {updated_count} jobs with inferred job_type")

    # Show distribution
    type_counts = {}
    for job in jobs:
        jt = job.get('job_type', 'Unknown')
        type_counts[jt] = type_counts.get(jt, 0) + 1

    print("\nJob type distribution:")
    for jt in sorted(type_counts.keys()):
        print(f"  {jt}: {type_counts[jt]}")

    # Save back to file
    print("\nSaving updated jobs.json...")
    with open('data/jobs.json', 'w') as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

    print("✅ Backfill complete!")


if __name__ == '__main__':
    main()
