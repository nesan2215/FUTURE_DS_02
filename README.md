# 📉 Customer Retention & Churn Analysis
### Future Interns — Data Science & Analytics Internship | Task 2 | FUTURE_DS_02

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green?style=flat&logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange?style=flat)
![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Plots-9cf?style=flat)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=flat)

---

## 🔍 Project Overview

This project analyzes **7,043 telecom customers** to uncover why customers churn, which segments are most at risk, and what actions can improve retention. The analysis mirrors real-world work done by data analysts in product, growth, and retention teams at SaaS and subscription businesses.

---

## ❓ Business Questions Answered

- What is the overall churn rate and monthly revenue at risk?
- Which contract types, internet services, and payment methods drive the most churn?
- When in the customer lifecycle is churn most likely to occur?
- How do cohorts differ in retention rates by signup month?
- What is the CLV difference between churned and retained customers?
- What actions can reduce churn and improve retention?

---

## 📁 Dataset

| Detail | Info |
|--------|------|
| **Name** | Telco Customer Churn Dataset |
| **Source** | [Kaggle — Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) |
| **Customers** | 7,043 |
| **Features** | 14 (demographics, services, billing, churn status) |

### Dataset Columns

| Column | Description |
|--------|-------------|
| `CustomerID` | Unique customer identifier |
| `Gender` | Customer gender |
| `SeniorCitizen` | Whether the customer is a senior citizen (1/0) |
| `Tenure` | Months the customer has been with the company |
| `Contract` | Contract type (Month-to-month, One year, Two year) |
| `InternetService` | Internet service type (DSL, Fiber optic, No) |
| `TechSupport` | Whether the customer has tech support |
| `PaymentMethod` | Payment method used |
| `MonthlyCharges` | Monthly bill amount ($) |
| `TotalCharges` | Total amount charged to date ($) |
| `Churn` | Whether the customer churned (Yes/No) |

---

## 🛠️ Tools & Libraries

| Tool | Purpose |
|------|---------|
| `Python 3.x` | Core programming language |
| `Pandas` | Data loading, cleaning, aggregation |
| `NumPy` | Numerical operations |
| `Matplotlib` | Plotting and figure layout |
| `Seaborn` | Statistical visualizations |
| `ReportLab` | PDF report generation |

---

## 🧹 Data Cleaning & Feature Engineering

- Checked for null values and data type mismatches
- Converted `TotalCharges` to numeric (handles blank strings)
- Created `Churn_Binary` column (Yes=1, No=0) for numerical analysis
- Extracted `SignupMonth` from `SignupDate` for cohort analysis
- Created `TenureBand` bins: 0-6m, 7-12m, 13-24m, 25-48m, 49-72m

---

## 📊 Key Performance Indicators

| KPI | Value |
|-----|-------|
| 🧑‍🤝‍🧑 Total Customers | 7,043 |
| ❌ Churned Customers | ~1,869 |
| 📉 Overall Churn Rate | ~26.5% |
| 💸 Monthly Revenue at Risk | ~$121,000 |
| 💰 Avg CLV (Active) | ~$2,800 |
| ⏱️ Avg Tenure (Active) | ~34 months |

---

## 📈 Key Insights

1. **Contract Type is the #1 Churn Driver** — Month-to-month customers churn at ~44% vs just ~5% for two-year contracts.
2. **First 6 Months are Critical** — Churn rate in the 0-6 month window is the highest of any tenure band (~55%).
3. **Fiber Optic Quality Issue** — Fiber optic customers churn more than DSL despite being the premium product (~37% vs ~25%).
4. **Electronic Check = High Risk** — Electronic check payment method users have the highest churn rate (~43%).
5. **CLV Gap is Massive** — Retained customers generate ~3x more lifetime value than churned customers.
6. **Cohort Patterns Show Seasonality** — Certain signup cohorts show lower retention, suggesting onboarding or product issues at specific periods.

---

## ✅ Actionable Recommendations

- Offer 15-20% discount to convert month-to-month customers to annual plans
- Launch 90-day structured onboarding for all new customers
- Investigate Fiber optic service quality through NPS surveys
- Incentivise auto-pay adoption with bill credits for electronic check users
- Build a monthly churn risk scoring model using tenure + contract + payment signals
- Run reactivation campaigns targeting customers who churned in the last 90 days

---

## 📂 Repository Structure

```
FUTURE_DS_02/
├── FUTURE_DS_02_Churn_Analysis.py    # Main Python analysis script
├── FUTURE_DS_02_Report.pdf           # Full client-ready analysis report
├── FUTURE_DS_02_Dashboard.png        # Dashboard visualization
├── telco_churn_sample.csv            # Sample dataset (full data from Kaggle)
└── README.md                         # Project documentation
```

---

## ▶️ How to Run

1. **Clone the repository**
```bash
git clone https://github.com/nesan2215/FUTURE_DS_02.git
cd FUTURE_DS_02
```

2. **Install dependencies**
```bash
pip install pandas numpy matplotlib seaborn reportlab
```

3. **Download the full dataset** from [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) and place `WA_Fn-UseC_-Telco-Customer-Churn.csv` in the folder

4. **Run the analysis**
```bash
python FUTURE_DS_02_Churn_Analysis.py
```

---

## 📄 Report Preview

The full analysis report (`FUTURE_DS_02_Report.pdf`) includes:
- Executive Summary
- KPI Dashboard with CLV comparison
- Churn Driver Analysis (contract, internet, payment, tenure)
- Cohort Retention Analysis by signup month
- Tenure & Monthly Charges distributions
- Key Insights with data-backed reasoning
- 6 Actionable Recommendations

---

## 🏢 About This Internship

This project was completed as part of the **Future Interns Data Science & Analytics Internship Program**.

- 🌐 Website: [futureinterns.com](https://futureinterns.com)
- 💼 LinkedIn: [Future Interns](https://www.linkedin.com/company/future-interns/)
- 📧 Contact: contact@futureinterns.com

---

## 👤 Author

**Nesan K**
- 💼 LinkedIn: [linkedin.com/in/nesan-k-bb995632b](https://www.linkedin.com/in/nesan-k-bb995632b)
- 🐙 GitHub: [github.com/nesan2215](https://github.com/nesan2215)

---

*This project is part of the Future Interns Internship Program — Task 2 of the Data Science & Analytics track.*
