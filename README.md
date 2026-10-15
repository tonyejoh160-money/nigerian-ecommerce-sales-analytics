Nigerian E-Commerce Sales Analytics

An end-to-end data analytics portfolio project exploring sales performance, product profitability, customer purchasing behavior, payment methods, and regional performance using a synthetic Nigerian e-commerce dataset.

Project Overview

This project demonstrates a data analytics workflow using Python, Pandas, SQL, SQLite, and data visualization.

The workflow includes data generation, cleaning, validation, exploratory analysis, business reporting, customer segmentation, SQL analysis, and visualization.

Data disclaimer: The dataset is synthetic and was generated for educational and portfolio purposes. It does not represent verified commercial transactions or actual Nigerian e-commerce market trends.

Business Questions
How does delivered sales revenue change over time?
Which products generate the highest revenue and profit?
Which states contribute the most delivered sales?
Which product categories perform best?
How do customers differ in purchasing frequency and value?
What proportion of customers make repeat purchases?
Which payment methods appear most frequently?
How are orders distributed across different statuses?
How do customer recency, frequency, and monetary value differ?
What data-quality issues could affect the analysis?
Technology Stack
Python
Pandas
NumPy
Matplotlib
Seaborn
SQLite
SQL
Git and GitHub

Power BI is a potential future extension for an interactive dashboard.

Project Structure
nigerian-ecommerce-sales-analytics/
├── data/
├── database/
├── docs/
│   └── data_dictionary.md
├── reports/
├── sql/
├── src/
├── visualizations/
├── requirements.txt
├── .gitignore
└── README.md

Generated reports, charts, and the database are created by running the corresponding scripts.

Installation
1. Create a virtual environment
python -m venv .venv
2. Activate it on Windows PowerShell
.\.venv\Scripts\Activate.ps1
3. Install dependencies
python -m pip install -r requirements.txt
Running the Analysis

Run commands from the project root.

Examples:

python src/check_data.py
python src/clean_data.py
python src/eda.py
python src/monthly_sales.py
python src/product_profitability.py
python src/customer_segmentation.py
python src/data_quality_report.py
python src/master_analytics_report.py

Create the SQLite database:

python src/create_database.py

Run the basic SQL analysis:

python src/run_sql_analysis.py

Run the advanced SQL analysis:

python src/run_advanced_sql.py

The full pipeline runner is:

python src/run_pipeline.py

Run the full pipeline only after confirming that all scripts referenced by the runner exist and work correctly.

Reports and Visualizations

The project produces reports covering:

Monthly sales and revenue growth.
Product profitability.
State-level performance.
Category performance.
Payment methods.
Customer behavior.
Order-status distribution.
Repeat purchasing.
RFM customer segments.
Data quality.
Executive and master analytics summaries.
SQL query results.

Charts are stored in visualizations/, while tabular outputs and summaries are stored in reports/.

Analytical Assumptions

Delivered orders are used as a simplified proxy for completed sales.

Profit is calculated as net revenue minus total product cost.

This is an educational assumption, not a complete accounting policy. The dataset does not model all operating expenses, taxes, logistics costs, refunds, and return adjustments.

See docs/data_dictionary.md for detailed definitions and limitations.

Limitations
The dataset is synthetic.
Results are not evidence of actual Nigerian market conditions.
Customer behavior is generated rather than observed.
Profit excludes costs not represented in the dataset.
Descriptive analysis does not establish causation.
Skills Demonstrated
Data generation and preparation.
Data cleaning and validation.
Exploratory data analysis.
Business KPI calculations.
Customer segmentation.
Repeat-purchase analysis.
SQL querying and aggregation.
SQLite database creation.
Data visualization.
Report generation.
Git-based project organization.
Future Improvements
Interactive Power BI dashboard.
Automated data-quality tests.
More realistic returns and refunds.
Customer lifetime value analysis.
Time-series forecasting.
Interactive analytics dashboard.
Author

Data Science Student | Python | SQL | Data Analytics

GitHub: tonyejoh160-money