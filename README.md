# SaaS Customer Churn & MRR Analysis

## Project Overview
An end-to-end Power BI project focused on SaaS analytics. This dashboard tracks essential KPIs including Monthly Recurring Revenue (MRR), Customer Churn Rate, and discount impacts to provide actionable business insights.

## Technical Stack
- **Data Generation:** Python (Pandas/Numpy)
- **Data Transformation:** Power Query (M)
- **Data Modeling:** Star Schema (Fact/Dimension tables)
- **Analytics:** Custom DAX Measures

## Data Model
- **Fact Table:** `Fact_Subscriptions`
- **Dimension Tables:** `Dim_Customer`, `Dim_SubscriptionPlan`, `Dim_Date`

## Key DAX Measures
This project utilizes custom DAX measures to derive business insights, organized by their functional purpose. 

### 1. Foundational Metrics
These measures provide the core count and revenue calculations for the business.

**Total Customers:**
```dax
Total Customers = DISTINCTCOUNT(Fact_Subscriptions[CustomerID])
```
Baseline MRR:
```
Baseline MRR = 
SUMX(
    Fact_Subscriptions,
    RELATED(Dim_SubscriptionPlan[MonthlyPrice]) * (1 - Fact_Subscriptions[DiscountApplied])
)

```
2. Time Intelligence & Churn Analysis
These measures demonstrate advanced analytical logic.

Active Customers:
```
Active Customers = 
CALCULATE(
    DISTINCTCOUNT(Fact_Subscriptions[CustomerID]),
    REMOVEFILTERS(Dim_Date),
    Fact_Subscriptions[StartDate] <= MAX(Dim_Date[Date]),
    (Fact_Subscriptions[EndDate] > MAX(Dim_Date[Date]) || ISBLANK(Fact_Subscriptions[EndDate]))
)
```
Customer Churn Rate:
```
Customer Churn Rate = 
DIVIDE(
    [Cancellations],
    [Active Customers],
    0
)
```
## Project Documentation
Engineered a robust ETL process to handle relational data.

Built a dynamic Star Schema for scalability and performance.

Deployed version control via GitHub to document the development lifecycle.

## Dashboard Access
Due to Power BI public publishing restrictions, please view the project showcase PDF here: [https://drive.google.com/file/d/1zg_SVP2Os1_DgOkoRqt-qeFOEHAUMdaO/view?usp=sharing].
