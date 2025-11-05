"""Test script for the Seek Job Scraper API."""

import requests
import time
import json
from typing import Optional


class APITester:
    """Test client for the API."""

    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1"
        self.headers = {}
        if api_key:
            self.headers["X-API-Key"] = api_key

    def print_response(self, response: requests.Response, test_name: str):
        """Pretty print API response."""
        print(f"\n{'='*60}")
        print(f"TEST: {test_name}")
        print(f"{'='*60}")
        print(f"Status Code: {response.status_code}")
        print(f"Response:")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
        print(f"{'='*60}\n")

    def test_health(self):
        """Test health check endpoint."""
        response = requests.get(f"{self.api_url}/health")
        self.print_response(response, "Health Check")
        return response.status_code == 200

    def test_trigger_scrape(self, headless: bool = True, max_pages: int = 1) -> Optional[str]:
        """Test scraping trigger endpoint."""
        payload = {
            "headless": headless,
            "max_pages": max_pages
        }
        response = requests.post(
            f"{self.api_url}/scrape",
            json=payload,
            headers=self.headers
        )
        self.print_response(response, "Trigger Scraping Job")

        if response.status_code == 202:
            return response.json()["job_id"]
        return None

    def test_scrape_status(self, job_id: str):
        """Test scrape status endpoint."""
        response = requests.get(
            f"{self.api_url}/scrape/{job_id}",
            headers=self.headers
        )
        self.print_response(response, f"Check Status for Job {job_id}")
        return response.json()

    def test_list_scrape_jobs(self):
        """Test list scrape jobs endpoint."""
        response = requests.get(
            f"{self.api_url}/scrape",
            headers=self.headers
        )
        self.print_response(response, "List All Scrape Jobs")
        return response.status_code == 200

    def test_get_jobs(self, page: int = 1, page_size: int = 10):
        """Test get jobs endpoint."""
        response = requests.get(
            f"{self.api_url}/jobs?page={page}&page_size={page_size}",
            headers=self.headers
        )
        self.print_response(response, f"Get Jobs (Page {page})")
        return response.status_code == 200

    def test_get_latest_jobs(self, limit: int = 5):
        """Test get latest jobs endpoint."""
        response = requests.get(
            f"{self.api_url}/jobs/latest?limit={limit}",
            headers=self.headers
        )
        self.print_response(response, f"Get Latest {limit} Jobs")
        return response.status_code == 200

    def test_register_webhook(self, webhook_url: str):
        """Test webhook registration."""
        payload = {
            "webhook_url": webhook_url,
            "events": ["scrape.completed"],
            "description": "Test webhook"
        }
        response = requests.post(
            f"{self.api_url}/webhooks",
            json=payload,
            headers=self.headers
        )
        self.print_response(response, "Register Webhook")

        if response.status_code == 201:
            return response.json()["webhook_id"]
        return None

    def test_list_webhooks(self):
        """Test list webhooks endpoint."""
        response = requests.get(
            f"{self.api_url}/webhooks",
            headers=self.headers
        )
        self.print_response(response, "List Webhooks")
        return response.status_code == 200

    def test_delete_webhook(self, webhook_id: str):
        """Test delete webhook endpoint."""
        response = requests.delete(
            f"{self.api_url}/webhooks/{webhook_id}",
            headers=self.headers
        )
        self.print_response(response, f"Delete Webhook {webhook_id}")
        return response.status_code == 204

    def poll_until_complete(self, job_id: str, max_wait: int = 300, interval: int = 5):
        """Poll job status until completion or timeout."""
        print(f"\nPolling job {job_id} until completion...")
        start_time = time.time()

        while time.time() - start_time < max_wait:
            status_data = self.test_scrape_status(job_id)
            status = status_data.get("status")

            if status == "completed":
                print(f"✅ Job completed successfully!")
                print(f"   Jobs found: {status_data.get('jobs_found', 0)}")
                print(f"   New jobs: {status_data.get('jobs_new', 0)}")
                return True
            elif status == "failed":
                print(f"❌ Job failed: {status_data.get('error')}")
                return False

            print(f"⏳ Job status: {status}... waiting {interval}s")
            time.sleep(interval)

        print(f"⏱️ Timeout waiting for job completion")
        return False


def run_comprehensive_test():
    """Run comprehensive API test suite."""
    print("""
╔══════════════════════════════════════════════════════════╗
║         Seek Job Scraper API - Test Suite               ║
╚══════════════════════════════════════════════════════════╝
    """)

    # Initialize tester
    tester = APITester(base_url="http://localhost:8000")

    # Test 1: Health Check
    print("\n📋 Test 1: Health Check")
    if not tester.test_health():
        print("❌ Health check failed! Is the server running?")
        return

    # Test 2: Trigger Scraping (with only 1 page for fast testing)
    print("\n📋 Test 2: Trigger Scraping Job")
    job_id = tester.test_trigger_scrape(headless=True, max_pages=1)

    if not job_id:
        print("❌ Failed to trigger scraping job")
        return

    # Test 3: Check Job Status
    print("\n📋 Test 3: Check Job Status")
    tester.test_scrape_status(job_id)

    # Test 4: List All Scrape Jobs
    print("\n📋 Test 4: List All Scrape Jobs")
    tester.test_list_scrape_jobs()

    # Test 5: Wait for completion (optional - commented out for quick tests)
    # print("\n📋 Test 5: Wait for Job Completion")
    # tester.poll_until_complete(job_id, max_wait=120, interval=5)

    # Test 6: Get Latest Jobs
    print("\n📋 Test 6: Get Latest Jobs")
    tester.test_get_latest_jobs(limit=5)

    # Test 7: Get Jobs with Pagination
    print("\n📋 Test 7: Get Jobs with Pagination")
    tester.test_get_jobs(page=1, page_size=10)

    # Test 8: Webhook Registration
    print("\n📋 Test 8: Register Webhook")
    webhook_id = tester.test_register_webhook("https://webhook.site/test-webhook")

    # Test 9: List Webhooks
    print("\n📋 Test 9: List Webhooks")
    tester.test_list_webhooks()

    # Test 10: Delete Webhook
    if webhook_id:
        print("\n📋 Test 10: Delete Webhook")
        tester.test_delete_webhook(webhook_id)

    print("""
╔══════════════════════════════════════════════════════════╗
║              Test Suite Completed!                       ║
╚══════════════════════════════════════════════════════════╝

Next Steps:
1. Check http://localhost:8000/api/docs for interactive API documentation
2. Wait for your scraping job to complete and check results
3. Integrate with n8n using the webhook URL
    """)


def run_quick_scrape_test():
    """Quick test: trigger scrape and wait for results."""
    print("""
╔══════════════════════════════════════════════════════════╗
║         Quick Scrape Test (Single Page)                 ║
╚══════════════════════════════════════════════════════════╝
    """)

    tester = APITester()

    # Health check
    print("1. Checking API health...")
    if not tester.test_health():
        print("❌ API is not healthy!")
        return

    # Trigger scrape
    print("\n2. Triggering scrape (1 page only)...")
    job_id = tester.test_trigger_scrape(headless=True, max_pages=1)

    if not job_id:
        print("❌ Failed to start scrape!")
        return

    # Wait for completion
    print(f"\n3. Waiting for scrape to complete...")
    success = tester.poll_until_complete(job_id, max_wait=120, interval=5)

    if success:
        # Get results
        print("\n4. Fetching results...")
        tester.test_get_latest_jobs(limit=10)
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed or timed out")


if __name__ == "__main__":
    import sys

    print("""
Seek Job Scraper API Test Script
================================

Choose test mode:
1. Comprehensive Test (all endpoints, fast)
2. Quick Scrape Test (trigger and wait for results)
3. Exit

Note: Make sure the API server is running on http://localhost:8000
    """)

    choice = input("Enter choice (1-3): ").strip()

    if choice == "1":
        run_comprehensive_test()
    elif choice == "2":
        run_quick_scrape_test()
    elif choice == "3":
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid choice. Please run again and choose 1, 2, or 3.")
