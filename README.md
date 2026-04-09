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

 # 6. Data Flow / Workflow
 
 # 1. Data Loading

Where it happens in the code

df_birmingham = pd.read_csv("CLEANED_DATA/rightmove/rm_properties_birmingham.csv")

and later, for all cities:

list_cities = ["Leicester", "Birmingham", "London", "Glasgow", "Edinburgh", "Newcastle", "Bristol", "Manchester", "Nottingham", "Sheffield", "Liverpool", "Cardiff", "Belfast", "Leeds", "Southampton"]

df_list = []

for city in list_cities:
    df_temp = pd.read_csv(f"CLEANED_DATA/rightmove/rm_properties_{city.lower()}.csv")
    df_temp["city"] = city
    df_list.append(df_temp)

What it shows
This is the data ingestion step. The notebook first loads individual city CSV files and then scales that pattern into a loop that reads multiple city-level datasets and appends them into a shared list for combination.

# 2. Initial Exploration

Where it happens in the code

df_birmingham.info()
df_birmingham.describe()

What it shows
This is the first-pass exploration layer:

info() checks schema, column types, and non-null counts
describe() gives summary statistics such as count, mean, std, min, max, and quartiles

This is how the notebook validates that the data loaded correctly and starts understanding distribution and completeness.

# 3. Data Quality Analysis

Where it happens in the code
The notebook has an explicit section:

## 3.8 Data Quality Metrics

and shows missingness outputs like:

title             0.000000
location          0.000000
price             0.900901
property_type     0.000000
bedrooms          7.507508
bathrooms         7.807808

What it shows
This is the data quality step. It measures how complete each field is and highlights missing values in important columns such as:

price
bedrooms
bathrooms
and especially area

This is where the notebook identifies that some fields are sparse and may affect downstream analysis.

# 4. Feature Engineering

Where it happens in the code

df_birmingham["price_per_area"] = df_birmingham["price"] / df_birmingham["area"]

What it shows
This creates the derived metric:

price_per_area = price / area

That is the core engineered feature in the notebook. It converts raw listing price into a normalized metric that makes properties more comparable across different sizes.

# 5. Aggregation

Where it happens in the code

Group by city
df_all_cities_groupby_city_mean = df_all_cities.groupby("city")["price_per_area"].mean().reset_index().rename(columns={"price_per_area": "mean_price_per_area"}).sort_values(by="mean_price_per_area", ascending=False)

df_all_cities_groupby_city_median = df_all_cities.groupby("city")["price_per_area"].median().reset_index().rename(columns={"price_per_area": "median_price_per_area"}).sort_values(by="median_price_per_area", ascending=False)
Group by property type
df_all_cities_groupby_property_mean = df_all_cities.groupby("property_type")["price_per_area"].mean().reset_index().rename(columns={"price_per_area": "median_price_per_area"}).sort_values(by="median_price_per_area", ascending=False)
df_all_cities_groupby_property_median = df_all_cities.groupby("property_type")["price_per_area"].median().reset_index().rename(columns={"price_per_area": "median_price_per_area"}).sort_values(by="median_price_per_area", ascending=False)
Group by property type within each city
for city in list_cities:
    df_city = df_all_cities[df_all_cities["city"] == city]
    df_city_groupby_property_median = df_city.groupby("property_type")["price_per_area"].median().reset_index().rename(columns={"price_per_area": "median_price_per_area"}).sort_values(by="median_price_per_area", ascending=False)

What it shows
This is the aggregation layer. The notebook computes:

average price per area by city
median price per area by city
average/median price per area by property type
city-specific property-type comparisons

This is where raw rows become business-level summaries.

# 6. Visualization

Where it happens in the code

Property type comparison
df_all_cities_groupby_property_mean.plot(x="property_type", y="median_price_per_area", kind="bar", figsize=(12, 6), title=f"Average Price per Area by Property Type")
df_all_cities_groupby_property_median.plot(x="property_type", y="median_price_per_area", kind="bar", figsize=(12, 6), title=f"Median Price per Area by Property Type")
City-specific property comparison
df_city_groupby_property_median.plot(x="property_type", y="median_price_per_area", kind="bar", figsize=(12, 6), title=f"Median Price per Area by Property Type for {city}")

What it shows
This is the visualization step. The notebook converts aggregated tables into bar charts so the user can visually compare:

pricing trends across property types
pricing differences within each city
ranking patterns more easily than by reading tables alone

# 7. Insights Generation

Where it happens in the code
The notebook prints and displays ranked outputs like:

print("Mean price per area by city:")
display(df_all_cities_groupby_city_mean)

print("Median price per area by city:")
display(df_all_cities_groupby_city_median)

It also exports the findings:

df_all_cities_groupby_city_mean.to_csv("reports/mean_price_per_area_by_city.csv", index=False)
df_all_cities_groupby_city_median.to_csv("reports/median_price_per_area_by_city.csv", index=False)

And the displayed output shows ranked city patterns such as:

London highest median price per area
Manchester, Bristol, Edinburgh, Leeds, and Liverpool following behind
Birmingham and Belfast much lower in the ranking

What it shows
This is the insight generation layer. The notebook is not just calculating metrics; it is surfacing patterns and anomalies through ranked outputs and report exports. For example, the displayed city-level medians make it easy to identify:

premium markets,
mid-tier markets,
and low-price outliers

 # 7. Design Decisions

# 1. Use of price_per_area as Primary Metric

What I chose
Used:

price_per_area = price / area

as the core analytical metric instead of raw price.

Why I chose it

Raw price is not comparable across properties of different sizes
A £1M 5-bedroom house and a £1M studio are fundamentally different
Normalizing by area creates a fair, comparable benchmark

Alternative options

Raw price → simple but misleading
Price per bedroom → ignores usable space
Hedonic pricing models (multi-variable regression) → more accurate but complex
Price per square meter (same concept, different unit)

What is best

For EDA / business insights → price_per_area is best
For production pricing → regression models outperform single metrics

Senior insight
This decision intentionally balances simplicity + interpretability, making insights explainable to non-technical stakeholders.

# 2. Notebook-Based Architecture

What I chose
Used EDA.ipynb and regression_analysis.ipynb as the main execution layer.

Why I chose it

Enables rapid iteration
Ideal for:
exploring datasets
testing hypotheses
visualizing results
Reduces development friction in early-stage projects

Alternative options

Modular Python scripts (src/, .py files)
Pipeline frameworks (Airflow, Prefect DAGs)
Production ML pipelines (MLflow, FastAPI services)

What is best

Exploration phase → Notebooks (best choice)
Production phase → Modular pipelines + services

Senior insight
This is a deliberate phase-based decision:

Notebook → Prototype → Pipeline → Production System

# 3. City-wise Dataset Separation

What I chose
Stored and processed data as:

rm_properties_london.csv
rm_properties_birmingham.csv
...

Why I chose it

Keeps datasets modular and manageable
Allows:
independent processing
easier debugging
selective reprocessing of cities
Makes scaling simple (just add another city file)

Alternative options

Single large unified dataset
Database-first design (all cities in one table)
Data lake / partitioned storage

What is best

Small to medium scale → City-wise CSVs (best for simplicity)
Large scale → Partitioned database tables or data lake

Senior insight
This design follows a horizontal partitioning mindset, which scales naturally as data grows.

# 4. Handling Missing Data

What I chose

For EDA:
Skip calculations where area is missing
For regression:
Apply imputation (mean/median)

Why I chose it

Avoids introducing false assumptions early
Keeps analysis truthful to available data
Separates:
analysis logic (clean, unbiased)
modeling logic (requires completeness)

Alternative options

Mean/median imputation everywhere
Advanced imputation (KNN, regression-based)
Dropping rows with missing values
External data enrichment

What is best

EDA → Avoid imputation (best for accuracy)
ML models → Use imputation (required for completeness)

Senior insight
This is a context-aware decision:

EDA prioritizes truth → ML prioritizes completeness

# 8. Error Handling and Logging

 - # 1. Schema Validation → df.info()

Where it happens in the code

df_birmingham.info()

What it is checking

Column names (e.g., price, area, bedrooms)
Data types (float, object, etc.)
Non-null counts per column

Why this matters

Ensures the dataset matches expectations before processing
Detects issues like:
Wrong data types (e.g., price as string)
Missing columns
Unexpected null distributions

What it effectively logs

A snapshot of dataset health
Acts as a lightweight “schema validation log”

# 2. Null Checks for Critical Fields

Where it happens in the code

Data quality section
## 3.8 Data Quality Metrics

Output example:

price        0.900901
bedrooms     7.507508
bathrooms    7.807808
Regression notebook
y.isnull().sum()
X.isnull().sum()

What it is checking

Whether critical fields contain missing values:
price (target variable)
area, bedrooms, bathrooms (features)

Why this matters

Missing values can:
Break calculations
Bias analysis
Crash ML models

What it effectively logs

Percentage or count of missing values
Identifies which columns are unreliable

 - # 3. Implicit Safeguards (Safe Calculations)

Where it happens in the code

df_birmingham["price_per_area"] = df_birmingham["price"] / df_birmingham["area"]

and later in regression:

df_all_cities["area"] = df_all_cities["area"].fillna(df_all_cities["area"].median())

What it is checking / preventing

Avoids invalid calculations such as:
Division by null (NaN)
Division by zero (implicitly avoided if data is clean)

Why this matters

Ensures derived metrics like price_per_area are meaningful
Prevents runtime errors or corrupted outputs

Important nuance

In EDA → rows with missing area naturally result in NaN
In regression → missing values are explicitly filled before modeling

# 4. Data Cleaning as Error Prevention

Where it happens in the code

df_all_cities = df_all_cities.dropna(subset=['price'])
df_all_cities["bedrooms"] = df_all_cities["bedrooms"].fillna(df_all_cities["bedrooms"].mean())

What it is checking

Ensures:
Target variable (price) is always present
Feature columns are complete for modeling

Why this matters

Prevents:
Model training failures
Incorrect statistical outputs

What it effectively logs

Guarantees that:

X → no nulls
y → no nulls

# 5. Warnings as Implicit Logging

Where it happens in the code (output)

ChainedAssignmentError: A value is being set on a copy of a DataFrame...

What it is checking

Detects unsafe pandas operations (chained assignment)

Why this matters

Highlights potential bugs where:
Data may not be updated as expected
Silent failures could occur

What it effectively logs

Runtime warnings that signal data mutation risks

# 9. Challenges & Solutions (with Code References)

# Challenge 1: Missing Area Data

Problem
Many listings do not have area, which is required to compute price-per-area.

Where this shows up in the code

In your dataset:

df_birmingham

You can see:

area → NaN (many rows)

Also confirmed in data quality checks:

## 3.8 Data Quality Metrics

Solution implemented in code

For EDA:

df_birmingham["price_per_area"] = df_birmingham["price"] / df_birmingham["area"]

What this does

If area is missing → result becomes NaN
No forced imputation → avoids introducing false values

For regression:

df_all_cities["area"] = df_all_cities["area"].fillna(df_all_cities["area"].median())

What this does

Fills missing values using median
Ensures model can train without null errors

Why this works

EDA → preserves data integrity
ML → ensures completeness for modeling

# Challenge 2: Data Inconsistency Across Cities

Problem
Different cities have very different price ranges (e.g., London vs smaller cities), making raw comparisons misleading.

Where this shows up in the code

Raw data:

df_all_cities["price"]

You observe:

London → very high values
Other cities → much lower

Solution implemented in code

df_birmingham["price_per_area"] = df_birmingham["price"] / df_birmingham["area"]

and applied across all cities:

df_all_cities["price_per_area"]

What this does

Normalizes price by property size
Makes cross-city comparison fair

Why this works

Removes scale bias
Enables apples-to-apples comparison


# #Challenge 3: Small Sample Sizes (Per City)

Problem
Individual city datasets are small → unreliable statistics

Where this shows up in the code

Single dataset:

df_birmingham

→ limited number of rows

Solution implemented in code

df_list = []

for city in list_cities:
    df_temp = pd.read_csv(f"CLEANED_DATA/rightmove/rm_properties_{city.lower()}.csv")
    df_temp["city"] = city
    df_list.append(df_temp)

df_all_cities = pd.concat(df_list, ignore_index=True)

What this does

Combines all city datasets into one unified dataset

Then aggregation:

df_all_cities.groupby("city")["price_per_area"].mean()

Why this works

Increases sample size
Produces more stable and reliable statistics


# Challenge 4: Outliers (e.g., London Prices)

Problem
Extreme values (especially London) skew averages

Where this shows up in the code

When using mean:

df_all_cities.groupby("city")["price_per_area"].mean()

→ results heavily influenced by high-value cities

Solution implemented in code

Use median:

df_all_cities.groupby("city")["price_per_area"].median()

Also for property types:

df_all_cities.groupby("property_type")["price_per_area"].median()

What this does

Median reduces impact of extreme values
Provides more robust central tendency

Why this works

Median is resistant to outliers
Better reflects “typical” property value

 # 10. Trade-offs (with Alternatives)
 
 # 1. Use of Notebooks

What I chose
Used Jupyter notebooks (EDA.ipynb, regression_analysis.ipynb) as the primary development environment.

Trade-off

 Very fast for exploration, visualization, and iteration
Not ideal for:
production pipelines
code reuse
version control (diffing notebooks is hard)

Alternative: Modular Python Scripts

src/
  data_loader.py
  preprocessing.py
  modeling.py

Why the alternative could be better

Cleaner separation of concerns
Easier testing (pytest)
Better maintainability and scalability
Can be deployed as APIs or pipelines

What is best

Exploration → Notebooks (best choice)
Production → Modular scripts (better long-term)

# 2. Ignoring Missing Area (in EDA)

What I chose
Did not impute missing area values during EDA:

price_per_area = price / area  # results in NaN if area missing

Trade-off

Keeps analysis honest (no artificial assumptions)
Loses data:
rows with missing area are excluded from analysis

Alternative: Imputation Models

area = area.fillna(area.median())

or more advanced:

KNN imputation
Regression-based imputation

Why the alternative could be better

Retains more data → larger sample size
Improves model performance in ML pipelines
Enables full dataset utilization

What is best

EDA → Avoid imputation (truth > completeness)
ML → Use imputation (completeness > purity)

# 3. Using Pandas Only

What I chose
Used pandas for all data processing:

df.groupby(...)
df.merge(...)
df.plot(...)

Trade-off

Simple, fast, and easy to use
Limited scalability:
struggles with very large datasets (millions+ rows)
single-machine processing only

Alternative: Spark / Dask

Spark
Distributed processing across clusters
Dask
Parallelized pandas-like operations

Why the alternative could be better

Handles large-scale data (GBs → TBs)
Enables distributed computation
Better suited for production data pipelines

What is best

Small/medium datasets → Pandas (best choice)
Large-scale systems → Spark/Dask (better scalability)

# 4. Static CSV Files

What I chose
Stored data as CSV files:

rm_properties_london.csv
rm_properties_birmingham.csv

Trade-off

Easy to:
read
share
debug

Limitations:
no indexing
slow querying
no concurrency support
difficult to scale

Alternative: Database (PostgreSQL)

Store data in structured tables:
SELECT * FROM properties WHERE city = 'London';

Why the alternative could be better

Faster querying and filtering
Supports large datasets efficiently
Enables:
concurrent access
indexing
joins across datasets
Integrates well with APIs and production systems

What is best

Early-stage / small data → CSV (best for simplicity)
Production / scalable systems → PostgreSQL (better choice)

# 11. Testing

# Current Testing

The current project does not show a formal automated test suite such as pytest. Instead, the notebooks use manual validation to verify that the data and outputs look correct before moving to the next step. This includes schema inspection, summary statistics, null checks, outlier inspection, visualization review, and model sanity checks.

# A. Manual validation through data summaries
Code used
df_birmingham.info()
df_birmingham.describe()
What this tested
whether the CSV loaded correctly
whether expected columns exist
whether column types look right
whether there are missing values
whether numeric distributions are sensible
Why this is useful

This is a fast way to catch obvious data issues early, such as:

price loaded as text instead of numeric
too many missing values in area
impossible ranges in bedrooms or bathrooms

This is visible in the EDA notebook and acts as a basic validation step before feature engineering or aggregation.

# B. Manual validation through null checks
Code used
y.isnull().sum()
X.isnull().sum()
What this tested
whether the regression target (price) has any missing values
whether the model feature matrix has any missing values after preprocessing
Why this is useful

This validates that the regression dataset is model-ready. Linear regression cannot reliably train if required features or the target still contain nulls. The notebook shows y.isnull().sum() returning 0, and X.isnull().sum() showing zero nulls across all encoded columns.

# C. Manual validation through feature inspection
Code used
X = df_all_cities[["area", "bedrooms", "bathrooms", "property_type"]]
X = pd.get_dummies(X, columns=["property_type"], drop_first=True)
len(X.columns)
X.columns
What this tested
whether the correct regression features were selected
whether categorical encoding worked
whether the number of resulting columns is reasonable
Why this is useful

This confirms that the feature engineering and preprocessing logic produced the expected machine-learning input structure. In the notebook, the encoded feature matrix contains 22 columns.

# D. Manual validation through visual inspection
Code used
df_all_cities_groupby_property_mean.plot(
    x="property_type",
    y="median_price_per_area",
    kind="bar",
    figsize=(12, 6),
    title="Average Price per Area by Property Type"
)

and outlier inspection:

Q1 = df_all_cities["price_per_area"].quantile(0.25)
Q3 = df_all_cities["price_per_area"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df_all_cities[
    (df_all_cities["price_per_area"] < lower_bound) |
    (df_all_cities["price_per_area"] > upper_bound)
]
What this tested
whether city/property-type comparisons look sensible
whether there are obvious anomalies or outliers
whether the derived metric price_per_area behaves reasonably
Why this is useful

Visual inspection helps catch issues that summary tables may miss, such as highly skewed distributions, suspicious categories, or outlier-heavy segments. The IQR-based outlier logic also shows that you explicitly checked for extreme values instead of trusting all records equally.

# E. Manual validation through model sanity checks
Code used
model.coef_
model.intercept_
y_pred = model.predict(X)
table_df = pd.DataFrame({
    "Feature": X.columns,
    "Coefficient": model.coef_
})
table_df
What this tested
whether the model trained successfully
whether predictions can be generated
whether coefficients are available for interpretation
whether the feature-to-coefficient mapping looks reasonable
Why this is useful

This is not a full evaluation test, but it is a useful sanity check that the regression pipeline is functioning end to end and that the outputs are interpretable.

What tests are missing today

The notebooks show manual validation, but they do not show a structured automated test suite such as:

unit tests for feature calculations
tests for CSV loading expectations
schema validation tests
threshold-based data quality tests
regression training/evaluation assertions

That means the current testing approach is good for exploration, but weaker for long-term maintainability and production reliability.

# Recommended Testing

# 1. Unit tests for feature calculations
Why this would be good

Feature engineering is core business logic. If price_per_area is wrong, many downstream insights become wrong too. A unit test protects this logic from silent breakage.

Recommended test code
import pandas as pd

def add_price_per_area(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["price_per_area"] = df["price"] / df["area"]
    return df

def test_price_per_area_calculation():
    df = pd.DataFrame({
        "price": [100000, 200000],
        "area": [100, 400]
    })

    result = add_price_per_area(df)

    assert result["price_per_area"].tolist() == [1000.0, 500.0]

# 2. Unit tests for data loading
Why this would be good

Your whole pipeline depends on city CSVs having the expected columns. A loading test ensures that files are readable and structurally consistent.

Recommended test code
import pandas as pd

REQUIRED_COLUMNS = {
    "title", "location", "price", "property_type",
    "bedrooms", "bathrooms", "area", "link"
}

def load_city_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def test_city_csv_has_required_columns(tmp_path):
    sample = pd.DataFrame([{
        "title": "A",
        "location": "B",
        "price": 100000,
        "property_type": "Detached",
        "bedrooms": 3,
        "bathrooms": 2,
        "area": 120,
        "link": "http://example.com"
    }])

    file_path = tmp_path / "sample.csv"
    sample.to_csv(file_path, index=False)

    df = load_city_data(file_path)
    assert REQUIRED_COLUMNS.issubset(df.columns)

# 3. Data validation tests for schema checks
Why this would be good

Notebook inspection with df.info() is useful, but automated schema checks make validation repeatable and enforceable in CI/CD.

Recommended test code
import pandas as pd

def validate_schema(df: pd.DataFrame):
    expected_types = {
        "title": "object",
        "location": "object",
        "price": "number",
        "property_type": "object",
        "bedrooms": "number",
        "bathrooms": "number",
        "area": "number",
        "link": "object"
    }

    for col, kind in expected_types.items():
        assert col in df.columns, f"Missing required column: {col}"
        if kind == "number":
            assert pd.api.types.is_numeric_dtype(df[col]), f"{col} must be numeric"
        elif kind == "object":
            assert df[col].dtype == "object", f"{col} must be text-like"

def test_schema_validation():
    df = pd.DataFrame({
        "title": ["A"],
        "location": ["B"],
        "price": [100000],
        "property_type": ["Detached"],
        "bedrooms": [3],
        "bathrooms": [2],
        "area": [120],
        "link": ["http://example.com"]
    })

    validate_schema(df)

# 4. Data validation tests for null thresholds
Why this would be good

In your notebooks, you manually inspect nulls. A threshold-based test would automatically fail if data quality degrades too far, which is especially useful when scraping sources change.

Recommended test code
import pandas as pd

NULL_THRESHOLDS = {
    "price": 0.01,       # max 1% null
    "bedrooms": 0.10,    # max 10% null
    "bathrooms": 0.10,   # max 10% null
    "area": 0.50         # allow higher null rate if source is sparse
}

def validate_null_thresholds(df: pd.DataFrame):
    for col, max_null_rate in NULL_THRESHOLDS.items():
        actual_null_rate = df[col].isnull().mean()
        assert actual_null_rate <= max_null_rate, (
            f"{col} null rate too high: {actual_null_rate:.2%} > {max_null_rate:.2%}"
        )

def test_null_thresholds():
    df = pd.DataFrame({
        "price": [100000, 200000, None],
        "bedrooms": [3, 4, 5],
        "bathrooms": [2, 2, None],
        "area": [100, None, 150]
    })

    # Adjust sample data if you want this test to pass
    validate_null_thresholds(df)
 
 # 5. Regression pipeline tests
Why this would be good

Since the project now includes regression, it is valuable to test whether preprocessing and model fitting work end to end.

Recommended test code
import pandas as pd
from sklearn.linear_model import LinearRegression

def build_features(df: pd.DataFrame):
    X = df[["area", "bedrooms", "bathrooms", "property_type"]]
    X = pd.get_dummies(X, columns=["property_type"], drop_first=True)
    y = df["price"]
    return X, y

def test_regression_pipeline_runs():
    df = pd.DataFrame({
        "area": [100, 120, 150, 180],
        "bedrooms": [2, 3, 3, 4],
        "bathrooms": [1, 2, 2, 3],
        "property_type": ["Detached", "Detached", "Terraced", "Semi-Detached"],
        "price": [200000, 250000, 240000, 320000]
    })

    X, y = build_features(df)
    model = LinearRegression()
    model.fit(X, y)
    preds = model.predict(X)

    assert len(preds) == len(df)
Why adding these tests would improve the project

These automated tests would make the project better because they would:

catch data issues immediately when source files change
protect core business logic like price_per_area
make the pipeline safer to refactor
reduce reliance on manual notebook inspection
make the project more production-ready
support CI/CD and team collaboration

# 11. Scaling Strategy

# Short Term (Extend Current System)
# 1. Add More Cities

How I would do it

Extend the existing pattern:
list_cities = ["London", "Birmingham", "Manchester", ...]
Add new city CSVs or scraping targets
Ensure schema consistency across all datasets

Tech used

Pandas (existing)
Existing scraping stack (requests, BeautifulSoup)

Why this works

Your architecture is already modular by city
Scaling horizontally (more cities) requires minimal changes

Key benefit

Increases dataset size → better insights and future model performance

# 2. Automate Data Ingestion

How I would do it

Wrap scraping + cleaning into a function or script:
def run_scraper(city):
    data = scrape_city(city)
    cleaned = clean_data(data)
    save_to_csv(cleaned)
Run it on a schedule:
Cron job (simple)
Prefect flow (more robust)

Tech used

Prefect (recommended)
or cron (simpler alternative)

Why this works

Removes manual execution
Keeps data fresh and continuously updated

Key benefit

Transforms project from static analysis → dynamic data pipeline

# Medium Term (Pipeline Architecture)

# 3. Move to ETL Pipeline

How I would do it

Split logic into modules:

extract.py   → scraping
transform.py → cleaning + feature engineering
load.py      → save to DB

Then orchestrate:

def pipeline():
    raw = extract()
    clean = transform(raw)
    load(clean)

Tech used

Pandas (transform)
SQLAlchemy (load to DB)
Prefect / Airflow (orchestration)

Why this works

Separates concerns:
extraction
transformation
storage
Makes system:
testable
reusable
production-ready

# 4. Scheduled Runs

How I would do it

Define workflows:
@flow
def daily_pipeline():
    pipeline()
Schedule:
Run every 24 hours

Tech used

Prefect (preferred)
Airflow (enterprise alternative)

Why this works

Ensures consistent data refresh
Enables monitoring, retries, and logging

Key benefit

Moves from manual execution → reliable automation

# Long Term (Production Scale)

# 5. Use Distributed Systems (Spark / BigQuery)

How I would do it

Replace pandas with Spark:
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
df = spark.read.csv("data.csv")
Or move to BigQuery:
SELECT city, AVG(price_per_area)
FROM properties
GROUP BY city;

Tech used

Apache Spark (distributed compute)
BigQuery (serverless analytics)

Why this works

Handles:
millions → billions of rows
Enables parallel processing

Key benefit

Removes single-machine bottlenecks

# 6. Introduce APIs for Real-Time Insights

How I would do it

Build API:
from fastapi import FastAPI

app = FastAPI()

@app.get("/price-estimate")
def predict_price(area: float, bedrooms: int):
    return model.predict(...)

Tech used

FastAPI
scikit-learn (model serving)

Why this works

Enables:
real-time predictions
integration with apps/websites

Key benefit

Turns project into a product/service

# 12. Future Improvements

# 1. Build ML Model for Price Prediction

How

Extend current regression notebook:
model.fit(X_train, y_train)
Add evaluation:
r2_score(y_test, y_pred)

Why

Moves from:
Descriptive → Predictive analytics

# 2. Add Geospatial Analysis (Location Intelligence)

How

Extract coordinates from addresses
Use:
distance to city center
proximity to transport

Tech

geopandas
folium

Why

Location is a key driver of property price

# 3. Real-Time Scraping Pipelines

How

Trigger scraping:
on schedule
or via event (new listings)

Tech

Prefect
message queues (future: Kafka)

Why

Keeps data continuously updated

# 4. Dashboard (Streamlit / Power BI)

How

Build UI:
import streamlit as st
st.bar_chart(data)

Tech

Streamlit (fast)
Power BI (enterprise)

Why

Makes insights accessible to non-technical users

# 5. Data Warehouse (Snowflake / BigQuery)

How

Move from CSV:
CSV → Database → Data Warehouse

Tech

BigQuery
Snowflake

Why

Enables:
fast queries
historical analysis
scalable storage

# 6. Automated Anomaly Detection

How

Detect unusual prices:
z_score = (value - mean) / std

Tech

scikit-learn
statistical methods

Why

Flags:
overpriced listings
data errors

# 7. Data Enrichment APIs

How

Integrate external APIs:
postcode data
crime rates
school ratings

Tech

REST APIs
requests

Why

Improves model accuracy and insights
