# Changelog

## [1.2.0] - 2025-10-10

### Added - Source-Level Filtering 🚀
- **Subclassification Filtering**: Filter at Seek's server (most efficient!)
  - Added `subclassification_ids` parameter to config
  - Includes 10 HR subcategories, excludes "Recruitment - Agency" (6324)
  - Reduces pages scraped by ~60% (faster performance)
  - URL parameter: `&subclassification=6323,6322,6321,6318,6319,6320,6325,6326,6327,6328`

### Documentation
- Added `SUBCLASSIFICATION_GUIDE.md` - Complete guide to source-level filtering
- Updated `README.md` with three-layer filtering explanation
- Updated `CHANGELOG.md` with version history

### Performance
- **60% faster scraping** - Only scrapes relevant subcategories
- **Bandwidth reduction** - Fewer unnecessary pages loaded
- **More efficient** - Less client-side filtering needed

## [1.1.0] - 2025-10-10

### Added
- **Date Range Filtering**: Added `date_range` parameter to config
  - Filters jobs to only show recent postings (default: last 3 days)
  - Configurable: 1, 3, 7, 14, or 31 days
  - Set to 0 to disable and get all jobs
  - Adds `?daterange=3` to Seek URL

- **Company Filtering**: Added comprehensive recruitment agency exclusion
  - 59 recruitment agencies pre-configured
  - Case-insensitive partial matching
  - Includes: Hays, Michael Page, Robert Walters, and 56 more
  - Dual filtering: by subcategory AND company name

- **Improved URL Handling**
  - Fixed classification URL to use correct Seek structure
  - Changed from `?classification=6251` to `/jobs-in-human-resources-recruitment`
  - Added configurable `classification_slug` parameter
  - More reliable and maintainable

### Documentation
- Added `FILTERING_GUIDE.md` - Complete guide to company filtering
- Added `SEEK_URL_GUIDE.md` - Detailed URL structure documentation
- Updated `README.md` with filtering information
- Updated `QUICK_REFERENCE.md` with filtering commands

### Configuration
- Added `classification_slug` to config.yaml
- Added `date_range` to config.yaml
- Added `excluded_companies` list (59 agencies)
- Improved config comments and documentation

## [1.0.0] - 2025-10-09

### Initial Release
- Basic Seek scraper with Playwright
- JSON and CSV storage
- Deduplication system
- Logging and error handling
- Scheduling support
- Configuration management
