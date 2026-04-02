# Real Estate Price Analyzer

A production-style data pipeline that turns messy real estate listing pages into normalized, comparable, and time-aware pricing intelligence.

## Problem Statement

Real estate pricing data is fragmented across listing websites, inconsistent in format, and difficult to compare quickly. Raw listing price alone is not enough to make meaningful decisions because value depends on location, size, property type, and data quality.

This project solves that by collecting listing data from source websites, validating and cleaning it, storing raw and curated layers separately, and generating reproducible analytics such as median price by area, price per square foot or meter, expensive versus affordable locations, and pricing trends over time.

At its core, this is not a scraping script. It is a reliable ingestion and analytics system.

## Project Goals

The system is designed to:

* collect real estate listings from one or more websites
* preserve raw source data for traceability
* clean and standardize inconsistent fields
* enforce schema validation and data contracts
* compute pricing metrics that are actually comparable
* support multiple runs without corrupting historical data
* generate reproducible reports and exports
* provide a foundation for trend analysis and lightweight valuation modeling

## Why This Project Matters

Real estate data becomes useful only after normalization.

A listing priced at £400,000 could be cheap or expensive depending on:

* its size
* its location
* its property type
* whether the data is even valid

This project converts unstructured listing data into structured pricing intelligence that buyers, renters, analysts, and portfolio teams can use.

## Features

### MVP

* single-site scraper
* extraction of:

  * title
  * location
  * price
  * property type
  * bedrooms
  * bathrooms
  * area / square footage
  * listing URL
* raw and cleaned data layers
* data cleaning and normalization pipeline
* duplicate detection by listing URL
* average and median price by location
* average and median price per square foot / meter
* most expensive and cheapest areas
* CSV export for processed outputs
* configurable request headers and delays
* structured logging for scrape and cleaning runs

## Tech Stack

### Core

* **Python**
* **requests + BeautifulSoup** for static site scraping
* **Selenium** only when JavaScript rendering is required
* **Pandas** for cleaning, aggregation, reshaping, and analytics
* **Pydantic** for schema validation on scraped records
* **SQLAlchemy** for persistence and repository abstractions
* **SQLite / PostgreSQL** for local and production-friendly storage
* **Matplotlib / Plotly** for visual reporting
* **pytest** for parser, cleaning, and analysis tests
* **Docker** for reproducible local execution
* **Prefect** as an optional orchestration layer for scheduled runs

### Why These Choices

* `requests` and `BeautifulSoup` keep the scraping layer lightweight and fast.
* `Selenium` is deliberately optional to avoid unnecessary browser overhead.
* `Pandas` is the backbone of reproducible data cleaning and descriptive analytics.
* `Pydantic` makes input quality explicit and prevents malformed records from silently entering downstream logic.
* `SQLAlchemy` supports future transition from CSV-backed workflows to a proper database layer with minimal architectural change.
* `Docker` ensures reproducibility across machines and environments.

---

## System Architecture

Architecture follows a layered pipeline design:

```text
Source Website
      |
      v
Scraper (requests / BeautifulSoup / Selenium)
      |
      v
Raw Data Storage
      |
      v
Cleaning & Normalization Pipeline
      |
      v
Pandas Analysis Engine
      |
      +------> CSV / Reports
      |
      +------> Visualizations


## Data Layers

The project uses separate data layers to preserve lineage and support reproducibility.

### Raw Layer

Stores unmodified scraped records.

Examples:

* `data/raw/raw_listings.csv`
* `raw_listings` database table

Purpose:

* preserves source fidelity
* supports debugging when parsing or cleaning rules change
* enables reprocessing without rescraping

### Cleaned Layer

Stores normalized, validated records ready for analysis.

Examples:

* `data/processed/cleaned_listings.csv`
* `cleaned_listings` database table

Purpose:

* standardizes units and currencies
* resolves missing or malformed values where possible
* removes or flags invalid and duplicate records

### Analytics Layer

Stores computed outputs for reporting.

Examples:

* `data/processed/analysis_output.csv`
* `reports/figures/*.png`

Purpose:

* publish metrics by location and property type
* generate visual summaries
* support downstream dashboards or presentations

---

## End-to-End Data Flow

1. **Scrape listing pages**

   * fetch listing index pages
   * paginate through results
   * extract listing cards and detail pages where required

2. **Validate raw records**

   * map HTML to raw schema
   * capture missing or malformed fields
   * log page-level extraction issues

3. **Persist raw data**

   * append raw records with scrape timestamp and source metadata
   * preserve each run for traceability

4. **Clean and normalize**

   * parse currencies and numeric values
   * standardize area units
   * normalize location strings
   * standardize property type categories
   * validate URLs and remove duplicates

5. **Generate analytical features**

   * `price_numeric`
   * `area_numeric`
   * `price_per_area`
   * run timestamp
   * source site
   * deduplication indicators
   * quality flags

6. **Run analytics**

   * compute descriptive statistics
   * aggregate by location
   * aggregate by property type
   * detect outliers
   * rank cheapest and most expensive areas
   * optionally fit baseline regression models

7. **Export results**

   * save CSV outputs
   * generate charts into `reports/figures`
   * produce reproducible run artifacts

---

## Key Metrics and Calculations

This project emphasizes normalized and trustworthy metrics instead of naive averages.

### 1. Price per Area

Core normalization metric:

[
price_per_area = \frac{price}{area}
]

Why it matters:

* raw price is misleading without size
* supports fair comparisons across different properties
* enables location and property-type benchmarking

Reported outputs:

* mean
* median
* distribution
* grouped by location
* grouped by property type

### 2. Location-Based Aggregations

Grouped by location:

* listing count
* average price
* median price
* average price per area
* median price per area

Median is preferred for ranking because it is more robust to luxury outliers.

### 3. Outlier Detection

Used to identify:

* unrealistically large or small areas
* extreme price per area values
* suspicious scraped records

Methods:

* IQR-based filtering
* z-score based checks where appropriate

Senior signal:

> We do not trust raw data. We validate it before drawing conclusions.

### 4. Distribution Analysis

Used to understand spread rather than just central tendency:

* histogram of price per area
* boxplots by location
* variance analysis by area or property type

Example insight:

* a location may have a high median but also high spread, suggesting unstable pricing

### 5. Cheapest vs Most Expensive Areas

Rank locations by:

* median price per area

This avoids misleading conclusions caused by a few extreme listings.

### 6. Property Type Segmentation

Compare:

* apartments vs houses vs studios
* average price
* median price
* average price per area
* median price per area

Example insight:

* apartments may have higher pricing density even when total prices are lower

### 7. Time-Based Trends

If historical runs are stored, the project supports:

* price over time
* price per area over time
* location trend tracking
* market movement monitoring across scrape runs

This is a strong signal that the system supports longitudinal analysis, not just one-off snapshots.

### 8. Data Quality Metrics

Track and report:

* missing value rate by field
* records dropped during cleaning
* duplicate rate
* invalid area rate
* invalid price rate

Example:

* 12 percent of records had invalid area values and were excluded from price-per-area calculations

### 9. Deduplication

Primary strategy:

* deduplicate by canonical listing URL

Optional stronger strategy:

* hash title + location + price + area when URL quality is poor

Outputs:

* records before deduplication
* records after deduplication
* duplicate rate by run

### 10. Weighted Metrics

Used to avoid distortion from small properties:

[
weighted\ average\ price_per_area = \frac{\sum price}{\sum area}
]

This is often more representative than a simple arithmetic average.

---

## Regression Layer

Regression is not the core of the project, but it adds a valuable senior-level modeling component.

### Purpose

Use regression as:

* a baseline valuation model
* a driver analysis tool
* a pricing anomaly detector

### Recommended Targets

#### Descriptive Analytics Target

* `price_per_area`

Useful for comparing normalized pricing across locations and property types.

#### Modeling Target

* `log(price)`

Useful because real estate prices are often skewed and log transformation improves stability.

### Example Features

Numeric features:

* area
* bedrooms
* bathrooms

Categorical features:

* location
* property type

Optional enriched features:

* listing date
* furnished status
* parking
* new build vs resale
* floor number
* distance to city center

### Model Outputs

* coefficients
* intercept
* R²
* MAE
* RMSE
* residuals
* most overvalued listings
* most undervalued listings

### Example Interpretation

A regression result might support statements like:

* each additional square meter is associated with an increase in price, holding other variables constant
* city-center properties remain more expensive even after controlling for size and property type
* apartments have higher price density than houses after normalization

### Important Limitations

* regression shows association, not causation
* missing features can bias coefficient estimates
* nonlinear market behavior may reduce fit quality
* poor scraped data can make the model unreliable

This is why cleaning, validation, and outlier handling come before modeling.

---

## Design Decisions

### 1. Separate Raw and Clean Layers

Raw data is never overwritten by cleaned data.

Why:

* supports debugging
* preserves lineage
* allows reprocessing with improved cleaning rules

### 2. Idempotent Ingestion

Each run should be safe to execute repeatedly.

Why:

* pipelines often run on schedules
* duplicate data corruption is a common real-world failure mode
* historical tracking requires controlled inserts rather than blind overwrite behavior

### 3. Schema Validation at the Boundary

Pydantic schemas validate records as early as possible.

Why:

* reduces downstream surprises
* makes contract violations explicit
* improves parser maintainability

### 4. Repository Abstraction

Persistence is handled via repository classes.

Why:

* isolates storage logic
* enables CSV-first and DB-backed modes
* simplifies testing

### 5. Modular Pipelines

Scrape, clean, and analysis phases are separated.

Why:

* easier extension
* easier retries
* clearer ownership of failures

### 6. Median Over Mean for Rankings

Median is preferred for location affordability comparisons.

Why:

* real estate data is heavily skewed
* luxury outliers distort mean-based rankings

---

## Trade-Offs

### Chosen Simplifications

* start with a single-site scraper before generalizing to multiple sites
* use CSV outputs for transparency before making the database mandatory
* use linear regression as a baseline model instead of jumping to complex ensembles
* keep Selenium optional to reduce runtime and operational complexity

### Why These Trade-Offs Are Reasonable

The project optimizes for strong engineering fundamentals first:

* reliable ingestion
* clean data contracts
* correct normalization
* reproducible outputs

This is more valuable than adding premature modeling complexity on top of weak data foundations.

---

## Error Handling and Logging

### Error Handling

The system explicitly handles:

* missing HTML fields
* malformed HTML structures
* layout changes in source pages
* blocked requests
* request timeouts
* invalid numeric parsing
* duplicate URLs
* broken pagination
* missing area or price values
* invalid or unsupported units

### Logging

The pipeline logs:

* scrape start time
* scrape end time
* source URL
* pages scraped
* records extracted
* records dropped during cleaning
* duplicates removed
* errors per page
* output file paths
* run identifiers

### Suggested Flags

```bash
python -m real_estate_analyzer.cli scrape --base-url "<listing-url>" --max-pages 10
python -m real_estate_analyzer.cli clean --input data/raw/raw_listings.csv --output data/processed/cleaned_listings.csv
python -m real_estate_analyzer.cli analyze --input data/processed/cleaned_listings.csv --output data/processed/analysis_output.csv
```

If you later add a REST API, document endpoints such as:

* `POST /scrape`
* `POST /clean`
* `POST /analyze`
* `GET /reports/latest`

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd real-estate-price-analyzer
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file if needed:

```env
BASE_URL=https://example-listings-site.com
REQUEST_TIMEOUT=20
REQUEST_DELAY_SECONDS=2
USER_AGENT=Mozilla/5.0 ...
DATABASE_URL=sqlite:///data/app.db
```

### 5. Run the Pipeline

```bash
python -m real_estate_analyzer.cli run-all
```

---

## Docker Setup

### Build

```bash
docker build -t real-estate-price-analyzer .
```

### Run

```bash
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/reports:/app/reports \
  real-estate-price-analyzer
```

### Why Docker

Docker ensures:

* reproducible execution
* consistent dependencies
* easier onboarding
* cleaner CI integration

---

## Output Artifacts

After a successful run, expected outputs include:

* `data/raw/raw_listings.csv`
* `data/processed/cleaned_listings.csv`
* `data/processed/analysis_output.csv`
* `reports/figures/price_per_area_histogram.png`
* `reports/figures/location_boxplot.png`

---

## Testing

### Run Tests

```bash
pytest
```

### Test Coverage Should Include

* HTML parser correctness
* price parsing and numeric normalization
* unit conversion logic
* schema validation
* deduplication logic
* cleaning rules
* aggregation correctness
* regression pipeline sanity checks
* repository behavior

### Example Test Categories

* `tests/unit/test_price_parsers.py`
* `tests/unit/test_html_parsers.py`
* `tests/unit/test_clean_service.py`
* `tests/integration/test_scrape_pipeline.py`
* `tests/integration/test_analysis_pipeline.py`

---

## Scaling Strategy

If this system were taken toward production, the next steps would be:

### Scraping

* rotate user agents and backoff strategies
* add retry logic with circuit-breaker style controls
* split per-site logic into adapter modules
* move toward queue-based scraping for scale

### Storage

* replace flat file outputs as the system of record with PostgreSQL
* partition historical data by scrape date or source
* add audit metadata for each run

### Orchestration

* schedule jobs with Prefect
* add run metadata, retry policies, and failure notifications
* track SLA-style metrics for pipeline health

### Analytics

* expose outputs through dashboards
* support area-level geospatial enrichment
* add anomaly detection and forecasting
* compare markets across multiple sources

### Quality

* add data quality checks and thresholds
* fail runs if required-field completeness drops below threshold
* alert on sudden parser failure rates or layout breakages

---

## Future Improvements

* multi-site adapter framework
* automated scheduled scraping
* dashboard UI
* postcode or coordinate enrichment
* geospatial clustering
* baseline and advanced price forecasting
* anomaly detection for suspicious listings
* confidence intervals for area-level metrics
* richer property attributes such as parking, furnishing, and floor number
* cloud deployment with scheduled workflows and centralized logging

---

## Example Insights This Project Can Produce

* Downtown has the highest median price per square foot, but also the highest pricing variance.
* Smaller apartments show higher price density than larger houses.
* Outliers inflated the average listing price by a meaningful margin before cleaning.
* After normalization by area, some “premium” locations are less expensive than raw price rankings suggest.
* Historical trend tracking shows whether pricing changes are broad-based or isolated to certain areas.

---

## What Interviewers Should Notice

This project is intentionally built to demonstrate engineering maturity, not just scraping ability.

It shows:

* strong data modeling decisions
* careful handling of messy real-world data
* robust normalization logic
* idempotent and reproducible pipeline design
* business-relevant analytical interpretation

> The core challenge was not scraping pages. It was designing a reliable pipeline that transforms inconsistent listing data into normalized, comparable pricing metrics with strong data quality guarantees.



