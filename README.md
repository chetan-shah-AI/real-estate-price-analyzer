# Pricing Analyzer – Real Estate Data Intelligence Platform

# What is this project

A data-driven pricing intelligence system that analyzes real estate listings across multiple UK cities using scraped property data. The project focuses on exploratory data analysis (EDA), price normalization (price per area), and cross-city comparisons to uncover actionable insights for property valuation and investment decisions.

The system ingests cleaned datasets (e.g., Rightmove data), computes derived metrics like price per area, and provides analytical insights across cities and property types.

# 0. Problem Statement

Real estate pricing is highly inconsistent and difficult to benchmark due to:

Variability in property attributes (area, bedrooms, type)
Missing or incomplete data (e.g., area missing for many listings)
Lack of normalized metrics (price alone is insufficient)
Difficulty comparing properties across cities

This leads to poor decision-making for buyers, investors, and analysts.

# 1. Project Goals

The system is designed to:

- Build a data pipeline for real estate datasets
- Perform EDA across multiple cities
- Normalize pricing using price per area
- Enable cross-city and cross-property-type comparisons
- Identify pricing trends, anomalies, and insights
- Provide a foundation for future predictive modeling

# 2. Real Life Business Cases where this project would help and why

1. Real Estate Investment Firms
Identify undervalued properties using price-per-area benchmarks
Compare cities to allocate capital efficiently

2. Property Buyers
Understand fair pricing across regions
Avoid overpaying for properties

3. Real Estate Platforms (e.g., marketplaces)
Improve listing recommendations
Provide pricing insights to users

4. Banks / Mortgage Providers
Risk assessment using property valuation benchmarks

5. Urban Planning & Policy
Analyze housing affordability across cities

# 3. Feature → File Mapping with Evidence from the Code

 - 1. Data ingestion (CSV loading) → EDA.ipynb

Code in the file

import pandas as pd 

df_birmingham = pd.read_csv("CLEANED_DATA/rightmove/rm_properties_birmingham.csv")
df_birmingham

What this shows
The notebook reads a cleaned property dataset from disk into a pandas DataFrame. That is the entry point for the analysis pipeline.

Why we need it
Without this step, the notebook has no structured data to inspect, transform, aggregate, or visualize.

- 2. Data exploration (summary, stats) → EDA.ipynb

Code in the file

df_birmingham.info()
df_birmingham.describe()

What this shows
info() gives column names, data types, and non-null counts. describe() gives summary statistics such as count, mean, standard deviation, min, max, and quartiles.

Why we need it
This is how you verify schema quality early, understand the shape of the data, and identify issues before doing business analysis or modeling.

 - 3. Data quality checks → EDA.ipynb

Code evidence in the file

And the notebook output shows missingness percentages such as:

title 0.000000
location 0.000000
price 0.900901
bedrooms 7.507508
bathrooms 7.807808

What this shows
The notebook explicitly measures data quality and field completeness rather than assuming the source is clean.


- 4. Feature engineering (price_per_area) → EDA.ipynb

Code in the file

df_birmingham["price_per_area"] = df_birmingham["price"] / df_birmingham["area"]

What this shows
The notebook creates a normalized metric from raw listing price and property area.

Why we need it
Raw price alone is not comparable across differently sized properties. price_per_area is the core business metric that makes cross-property and cross-city comparison meaningful.

- 5. Multi-city aggregation → EDA.ipynb

Code in the file

df_all_cities_groupby_city_mean = df_all_cities.groupby("city")["price_per_area"].mean().reset_index().rename(columns={"price_per_area": "mean_price_per_area"}).sort_values(by="mean_price_per_area", ascending=False)

df_all_cities_groupby_city_median = df_all_cities.groupby("city")["price_per_area"].median().reset_index().rename(columns={"price_per_area": "median_price_per_area"}).sort_values(by="median_price_per_area", ascending=False)

There is also grouping by property type:

df_all_cities_groupby_property_mean = df_all_cities.groupby("property_type")["price_per_area"].mean().reset_index().rename(columns={"price_per_area": "median_price_per_area"}).sort_values(by="median_price_per_area", ascending=False)

What this shows
The notebook combines all cities into a shared dataset and then computes aggregate metrics by both city and property type.

Why we need it
This is what turns city-level files into market-level intelligence. It enables benchmarking, regional analysis, and business comparisons across segments.

 - 6. Visualization (bar plots, comparisons) → EDA.ipynb

Code in the file

df_all_cities_groupby_city_median.plot(x="city", y="median_price_per_area", kind="bar", figsize=(12, 6), title="Median Price per Area by City")
df_all_cities_groupby_property_mean.plot(x="property_type", y="median_price_per_area", kind="bar", figsize=(12, 6), title=f"Average Price per Area by Property Type")

And the notebook saves chart outputs:

plt.savefig("reports/median_price_per_area_by_city.png")
plt.savefig(f"reports/median_price_per_area_by_property_type_{city}.png")

What this shows
The project does not stop at tables. It renders comparison visuals for stakeholder-friendly analysis.

Why we need it
Visualizations accelerate decision-making by making trends, rankings, and outliers easy to interpret.

- 7. Linear regression modeling → EDA.ipynb
I can verify that the notebook implements a linear regression pipeline setup, including feature preparation, encoding, and data validation. The following code is present:

from sklearn.linear_model import LinearRegression
X = df_all_cities[["area", "bedrooms", "bathrooms", "property_type"]]
X = pd.get_dummies(X, columns=["property_type"], drop_first=True)

y = df_all_cities["price"]
y.isnull().sum()
X.isnull().sum()

This confirms that:

A regression model is intended (via LinearRegression)
Input features (X) and target (y) are clearly defined
Categorical variables are encoded using one-hot encoding
The dataset is validated to ensure no missing values before modeling

What this means
The notebook successfully implements a model-ready regression pipeline, including:

Multi-city dataset creation
Missing value handling (mean/median imputation)
Feature engineering and selection
Categorical encoding for ML compatibility
Validation of clean training data

This represents the complete data preparation phase for regression modeling.

What is not clearly shown

I have not done

model.fit(X, y)
train_test_split(...)
model.predict(...)

or evaluation metrics such as RMSE or R².


 - 8. Reporting output directory → /reports/

Code in the file

import os
os.mkdir("reports")
plt.savefig("reports/median_price_per_area_by_city.png")
df_all_cities_groupby_city_mean.to_csv("reports/mean_price_per_area_by_city.csv", index=False)
df_all_cities_groupby_city_median.to_csv("reports/median_price_per_area_by_city.csv", index=False)

What this shows
The notebook creates a dedicated reporting folder and persists both graphics and tabular outputs to it.

Why we need it
This separates generated artifacts from source code and makes the analysis reproducible and shareable.


# 4. Tech Stack

- Python
- requests + BeautifulSoup for static site scraping
- Selenium only when JavaScript rendering is required
- Pandas for cleaning, aggregation, reshaping, and analytics
- NumPy for numerical operations and feature transformations
- scikit-learn for regression modeling and preprocessing
- Pydantic for schema validation on scraped records

Why These Choices

- requests and BeautifulSoup keep the scraping layer lightweight and fast.
- Selenium is deliberately optional to avoid unnecessary browser overhead.
- Pandas serves as the backbone for:
Data cleaning
Feature engineering
Aggregation and analysis
- NumPy supports efficient numerical operations required for modeling.
- scikit-learn enables:
Linear regression modeling
Feature preprocessing (e.g., encoding categorical variables)
Easy extension to more advanced models (Random Forest, Gradient Boosting)
- Pydantic enforces strong data contracts and prevents malformed scraped data from entering the pipeline.

---

# 5.System Architecture

Raw Scraped Data → Cleaned CSV → EDA → Insights / Reports 

- Scraping layer gathers raw data
- Cleaning layer ensures data quality
- EDA layer extracts meaning and prepares features
- Reporting layer delivers insights

+----------------------+
|  1. Raw Scraped Data    |
+----------------------+

- What this layer does

Collects raw property listings from external websites (e.g., Rightmove)
Contains unstructured or semi-structured data:
HTML content
Inconsistent formats
Missing or noisy values
Represents the source of truth before any transformation

- Tech stack used

requests → Fetch static web pages
BeautifulSoup → Parse HTML content
Selenium→ Handle JavaScript-rendered pages
Pydantic → Validate scraped records and enforce schema

- Why it matters

This layer determines data quality for the entire pipeline
Poor scraping = unreliable analytics downstream

+----------------------+
|  2. Cleaned CSV Files   |
+----------------------+

- What this layer does

Transforms raw scraped data into structured datasets
Performs:
Data cleaning (remove nulls, fix formats)
Standardization (consistent schema across cities)
Basic transformations (e.g., numeric conversion)
Outputs clean .csv files per city

- Tech stack used

Pandas → Data cleaning and transformation
NumPy → Numerical operations
SQLAlchemy (optional future) → Persist cleaned data into DB
SQLite / PostgreSQL (optional) → Structured storage

- Why it matters

Creates a reliable, reusable dataset
Decouples scraping from analysis
Enables reproducibility and faster iteration

+----------------------+
|  3.EDA Notebook        |
|  - Stats             |
|  - Aggregations      |
|  - Feature Eng       |
+----------------------+

 - What this layer does

Performs exploratory data analysis (EDA) and prepares data for modeling
Key responsibilities:
Statistical summaries (describe, info)
Data quality checks (null analysis)
Feature engineering (e.g., price_per_area)
Aggregations (city-level, property-type level)
Data transformation for ML (encoding, scaling)

- Tech stack used

Pandas → Core analysis and transformations
NumPy → Numerical operations
Matplotlib / Plotly → Visualization
scikit-learn → (Regression layer) feature preparation & modeling

- Why it matters

This is where raw data becomes insights

Bridges the gap between:

Data → Intelligence → Prediction
Forms the foundation for both analytics and machine learning

+----------------------+
|  4.Insights / Reports  |
+----------------------+

- What this layer does

Produces final outputs for stakeholders
Includes:
Aggregated metrics (mean/median price per area)
Visualizations (bar charts, comparisons)
Exported CSV reports
Model-ready datasets (for regression)

- Tech stack used

Matplotlib / Plotly → Charts and visual outputs
Pandas → Exporting reports (.csv)
File system (/reports/) → Persisting outputs
(Future) Streamlit / BI tools → Dashboarding

- Why it matters

Converts analysis into actionable business insights
Enables:
Decision-making
Reporting
Sharing results with non-technical stakeholders


