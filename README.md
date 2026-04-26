# E-commerce Interactive Data Analysis Dashboard
## Project Introduction
This is a professional, interactive web-based data analysis application developed for business and accounting analytics, built with the Python Streamlit framework. The tool is designed for end-to-end e-commerce retail data analysis, a core business scenario for management accounting, sales performance evaluation, customer behavior analysis, and operational decision-making.

The application addresses the practical pain point of non-technical business users needing to complete professional data analysis without complex manual formula operations or advanced coding skills. Users can flexibly filter business dimensions through the sidebar interactive controls, and the tool will automatically complete data cleaning, multi-table merging, indicator calculation, professional visualization, and real-time dynamic insight generation. It helps retail business analysts, marketing managers, operations teams, quickly complete full-dimensional e-commerce business analysis and output actionable, data-driven decision suggestions.

## Core Features
### 1. Multi-dimensional Interactive Filter System
The sidebar provides full-coverage interactive filter controls, supporting real-time data filtering and dynamic result refresh:
Date range filter (customizable start and end date of the analysis period)
Customer dimension filters: country/region, gender, membership tier
Product dimension filters: product category, minimum product rating
All filters are linked, and charts & insights will update automatically after filter adjustment
### 2. Full-cycle E-commerce Data Analysis Module
Covers 8 core business analysis scenarios, with complete analytical logic for the full e-commerce operation cycle:

(1) Monthly Revenue & Order Volume Trend Analysis

(2) Product Category Sales Performance & Concentration Analysis

(3) Customer Geographic Distribution & Market Concentration Analysis

(4) Product Rating vs. Sales Volume Correlation Analysis

(5) Customer Gender & Membership Tier Spending Behavior Analysis

(6) Order Status Distribution & Operational Risk Assessment

(7) Customer Age Group vs. Average Order Value Analysis

(8) Top 10 Best-selling Products Performance Analysis
### 3. Real-time Dynamic Business Insights
The core highlight of the tool: each analysis module is equipped with an intelligent insight engine, which automatically generates targeted analysis conclusions and operational suggestions based on the filtered data, rather than fixed template text:

(1) Automatic calculation of core business indicators (total revenue, peak sales period, top-performing segments)

(2) Quantitative risk assessment (market concentration risk, product dependency risk, high cancellation rate warning)

(3) Correlation analysis (rating vs. sales, age vs. spending, order volume vs. revenue)

(4) Actionable operational optimization suggestions for the current data performance
### 4. Professional Business-level Data Visualization
Built with matplotlib, the tool generates standard, publication-ready business charts that meet commercial report specifications:

(1) Dual-axis line & bar chart for monthly revenue and order volume comparison

(2) Bar chart for category sales and customer geographic distribution

(3) Pie chart for order status proportion analysis

(4) Scatter plot for product rating vs. sales correlation analysis

(5) Line chart for age group vs. average order value trend analysis

(6) Horizontal bar chart for top 10 product sales ranking
### 5. One-click Filtered Data Export
Supports one-click export of the filtered full dataset to a local CSV file, which enables users to:

(1) Perform further custom deep analysis

(2) Generate business reports and presentation materials

(3) Keep full traceability of the analysis data and process
### 6. Auto Data Cleaning & Multi-table Integration
The application has built-in automatic data preprocessing logic, which is out-of-the-box for users:

(1) Automatic identification of key column names in the dataset, compatible with different naming conventions

(2) Automatic missing value processing and data type standardization

(3) Automatic merging of 4 core datasets (customer, order, product, monthly revenue)

(4) Standardized data structure for consistent analysis logic
## How to Run the Application
### Prerequisites
Please ensure you have Python 3.8 or above installed on your device. You can check your Python version by running python --version in the command prompt.
### Step 1: Prepare the Project Files
Put all the following files in the same folder on your device (do not modify the file names):

app.py (core application code)

customers.csv (customer profile dataset)

orders.csv (order transaction dataset)

monthly_revenue.csv (monthly revenue dataset)

product_summary.csv (product information dataset)

requirements.txt (project dependency list)

### Step 2: Open Command Line in the Project Folder
Choose one of the following methods to open the Command Prompt (CMD) directly in your project folder:
#### Method 1 (Using command lines):
Open Windows Command Prompt (press Win + R, enter cmd, press Enter)

Run the following commands in sequence (replace the folder path with your actual file path):
```bash
cd Desktop
```
```bash
cd C:\Users\10675\Desktop\E-commerce_analysis_tool-main
```
#### Method 2 (Faster option for Windows):
Open your project folder in File Explorer

Type cmd in the address bar at the top of the window, then press Enter

The Command Prompt will launch directly, already located in your project folder
### Step 3: Install Required Dependencies
First, install all required Python libraries using the included requirements.txt file:
```bash
pip install -r requirements.txt
```
If the above command fails, you can install the libraries one by one with the following commands:
```bash
pip install streamlit
pip install pandas
pip install matplotlib
pip install numpy
```
Or install all libraries in one command:
```bash
pip install streamlit pandas matplotlib numpy
```
### Step 4: Launch the Application
Run the application with the following command:
```bash
streamlit run app.py
```
If you encounter a command error on Windows, use this compatible command instead:
```bash
python -m streamlit run app.py
```
### Step 5: Start Your Analysis
The application will automatically launch in your default browser. You can now adjust the filters, switch between analysis charts, view dynamic insights, and complete your e-commerce data analysis.
## Data Sources
The datasets used in this application are publicly available retail e-commerce datasets downloaded from Kaggle, accessed in April 2026. The dataset includes 4 core tables covering customer profile, order transaction, product information, and monthly revenue data.

The original dataset source and access information are as follows:

Platform: Kaggle (https://www.kaggle.com)

Access Date: April 2026

Dataset Type: Retail e-commerce transactional and customer data

All analysis logic and results are for academic assignment purposes only, and the use of the dataset complies with Kaggle's terms of use for educational and non-commercial research.
#### Project File Structure
```bash
e-commerce_analysis_tool
├── app.py                          # Core application code, including all analysis logic, interactive UI, visualization, and dynamic insight engine
├── customers.csv                   # Customer profile dataset (demographics, membership tier, geographic region, etc.)
├── orders.csv                      # Order transaction dataset (order ID, date, amount, product, status, customer ID, etc.)
├── monthly_revenue.csv             # Monthly aggregated revenue and profit dataset
├── product_summary.csv             # Product information dataset (product name, category, rating, price, etc.)
├── requirements.txt                # Project dependency library list
└── README.md                       # Project description, operation guide, and academic declaration (this file)
```
