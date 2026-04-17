#  CVP (Cost-Volume-Profit) Analysis Tool

##  Project Introduction

This is an interactive web application developed for the managerial accounting course assignment, built with the **Streamlit** framework. The tool is designed to automate full-process Cost-Volume-Profit (CVP) analysis, a core management accounting method for corporate profit forecasting, break-even point calculation, cost structure optimization, and business decision-making.

Users can customize core business parameters through the sidebar, and the tool will automatically complete the calculation of key indicators, visual chart rendering, industry benchmark comparison, and targeted strategic recommendation output. It helps users quickly complete professional CVP analysis without complex manual formula operations.

##  Core Features

1.  **Customizable Parameter Input**: Sidebar interactive input for core business parameters, including Fixed Cost (FC), Selling Price per Unit (SP), Variable Cost per Unit (VC), and sales volume range setting.
2.  **Fully Automatic CVP Core Calculation**: Real-time calculation of unit contribution margin, contribution margin ratio, break-even sales volume, break-even revenue, and other core CVP indicators.
3.  **Industry Benchmark Comparison Module**: Built-in 2023-2025 full-cycle industry average financial indicators, covering Manufacturing, Service Industry and Technology Industry, supporting one-click comparison between corporate indicators and industry benchmarks.
4.  **Professional Visual Analysis Chart**: Automatically generate a standard CVP analysis chart, including total revenue line, total cost line, fixed cost line, break-even point mark, profit & loss area filling, and dynamic industry benchmark reference line.
5.  **Full-cycle Detailed Data Table**: Output a complete data table of revenue, cost and profit under different sales volumes, supporting full data traceability.
6.  **Intelligent Analysis & Strategic Recommendation**: Automatically judge business status based on input parameters, and output targeted, actionable strategic optimization recommendations.

##  How to Run the Application

### Prerequisites
Please make sure you have Python 3.8 or above installed on your device.

### Method 1: Run with requirements.txt (Recommended)
1.  Clone or download this repository to your local device
2.  Open the terminal in the project folder, run the following command to install all required dependencies:
    ```bash
    pip install -r requirements.txt
Run the application with the following command:
```bash
streamlit run app.py
```
The application will automatically launch in your default browser, and you can start the CVP analysis immediately.
### Method 2: Install dependencies manually
If the first method fails, you can install the required libraries one by one with the following commands:
```bash
pip install streamlit
pip install pandas
pip install numpy
pip install matplotlib
```
Then repeat step 3 in Method 1 to run the application.
## Data Sources
The 2023-2025 industry average financial indicators built in this tool are for academic assignment demonstration only, and the data sources are:

Yahoo Finance Global Industry Financial Database (2023-2025): https://finance.yahoo.com/industries

National Bureau of Statistics of China Open Government Data (2023-2025): https://www.stats.gov.cn/tjsj/tjbz/

All data are real industry statistics, traceable through the above official channels.

## Project File Structure
```bash
cvp-analysis-tool/
├── app.py                 # Core code of the CVP analysis application, including all calculation logic and page design
├── requirements.txt       # Dependency library list of the project
└── README.md              # Project description document (this file)
```
## Author Information
**Name**: Ziyou Liao

**Student ID**: 2471574

**Course Name**: ACC102

**Major**: Accounting

**Submission Date**: 23th, April 2026
