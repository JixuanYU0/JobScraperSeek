#!/usr/bin/env python3
"""Test configuration and URL building without running the full scraper."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from src.utils import Config

    print("=" * 60)
    print("Configuration Test")
    print("=" * 60)

    # Load config
    config = Config()
    print("✓ Config loaded successfully\n")

    # Test URL building
    base_url = config.get("scraper.base_url")
    classification_slug = config.get("scraper.classification_slug")
    date_range = config.get("scraper.date_range")
    subclassification_ids = config.get("scraper.subclassification_ids")

    print(f"Base URL: {base_url}")
    print(f"Classification: {classification_slug}")
    print(f"Date Range: {date_range} days")
    print(f"Subclassification IDs: {subclassification_ids}\n")

    # Build URL
    from urllib.parse import quote

    url = f"{base_url}/{classification_slug}"
    params = []

    if date_range and date_range > 0:
        params.append(f"daterange={date_range}")

    if subclassification_ids:
        encoded_ids = quote(subclassification_ids, safe='')
        params.append(f"subclassification={encoded_ids}")

    if params:
        url = f"{url}?{'&'.join(params)}"

    print("Generated URL:")
    print(url)
    print()

    # Test filters
    excluded_companies = config.get("scraper.excluded_companies", [])
    excluded_subcategories = config.get("scraper.excluded_subcategories", [])

    print(f"✓ {len(excluded_companies)} recruitment agencies will be filtered")
    print(f"✓ {len(excluded_subcategories)} subcategories will be filtered as backup")

    if subclassification_ids:
        num_subcats = len(subclassification_ids.split(','))
        print(f"✓ {num_subcats} subcategories filtered at source (Seek server)")

    print("\n" + "=" * 60)
    print("Configuration Test: PASSED ✓")
    print("=" * 60)

except ImportError as e:
    print(f"❌ Error: {e}")
    print("\nPlease install dependencies first:")
    print("  pip install pyyaml")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
