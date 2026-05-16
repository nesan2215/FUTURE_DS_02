import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

np.random.seed(42)

n = 7043
tenure = np.random.exponential(scale=30, size=n).clip(1, 72).astype(int)
monthly_charges = np.random.normal(65, 30, n).clip(20, 120).round(2)
total_charges = (monthly_charges * tenure * np.random.uniform(0.85, 1.0, n)).round(2)

contract = np.random.choice(["Month-to-month","One year","Two year"], n, p=[0.55,0.24,0.21])
internet = np.random.choice(["DSL","Fiber optic","No"], n, p=[0.34,0.44,0.22])
payment  = np.random.choice(["Electronic check","Mailed check","Bank transfer","Credit card"], n, p=[0.34,0.23,0.22,0.21])
gender   = np.random.choice(["Male","Female"], n)
senior   = np.random.choice([0,1], n, p=[0.84,0.16])
partner  = np.random.choice(["Yes","No"], n, p=[0.48,0.52])
dependents = np.random.choice(["Yes","No"], n, p=[0.30,0.70])
tech_support = np.random.choice(["Yes","No","No internet service"], n, p=[0.29,0.49,0.22])
streaming_tv = np.random.choice(["Yes","No","No internet service"], n, p=[0.38,0.40,0.22])

churn_prob = np.zeros(n)
churn_prob += np.where(contract == "Month-to-month", 0.35, 0)
churn_prob += np.where(contract == "One year", 0.10, 0)
churn_prob += np.where(contract == "Two year", 0.03, 0)
churn_prob += np.where(internet == "Fiber optic", 0.12, 0)
churn_prob += np.where(payment == "Electronic check", 0.10, 0)
churn_prob += np.where(senior == 1, 0.08, 0)
churn_prob += np.where(tenure < 6, 0.15, 0)
churn_prob += np.where(tenure > 48, -0.12, 0)
churn_prob += np.where(tech_support == "Yes", -0.08, 0)
churn_prob = churn_prob.clip(0.02, 0.90)
churn = np.array(["Yes" if p > np.random.random() else "No" for p in churn_prob])

signup_base = pd.Timestamp("2020-01-01")
signup_dates = [signup_base + pd.DateOffset(months=np.random.randint(0, 36)) for _ in range(n)]
customer_ids = [f"CUST-{10000+i}" for i in range(n)]

df = pd.DataFrame({
    "CustomerID": customer_ids,
    "Gender": gender,
    "SeniorCitizen": senior,
    "Partner": partner,
    "Dependents": dependents,
    "Tenure": tenure,
    "Contract": contract,
    "InternetService": internet,
    "TechSupport": tech_support,
    "StreamingTV": streaming_tv,
    "PaymentMethod": payment,
    "MonthlyCharges": monthly_charges,
    "TotalCharges": total_charges,
    "Churn": churn,
    "SignupDate": signup_dates,
})

print(df.shape)
print(df.head())
print(df.isnull().sum())
print(df["Churn"].value_counts())
print(df.dtypes)

df["Churn_Binary"] = (df["Churn"] == "Yes").astype(int)
df["SignupDate"] = pd.to_datetime(df["SignupDate"])
df["SignupMonth"] = df["SignupDate"].dt.to_period("M")
df["TenureBand"] = pd.cut(df["Tenure"], bins=[0,6,12,24,48,72], labels=["0-6m","7-12m","13-24m","25-48m","49-72m"])

print(df.describe())

churn_rate = df["Churn_Binary"].mean() * 100
total_customers = len(df)
churned = df["Churn_Binary"].sum()
retained = total_customers - churned
avg_tenure_churned = df[df["Churn"]=="Yes"]["Tenure"].mean()
avg_tenure_retained = df[df["Churn"]=="No"]["Tenure"].mean()
avg_monthly_churned = df[df["Churn"]=="Yes"]["MonthlyCharges"].mean()
avg_monthly_retained = df[df["Churn"]=="No"]["MonthlyCharges"].mean()
revenue_lost = df[df["Churn"]=="Yes"]["MonthlyCharges"].sum()
clv_churned = df[df["Churn"]=="Yes"]["TotalCharges"].mean()
clv_retained = df[df["Churn"]=="No"]["TotalCharges"].mean()

print(f"Total Customers: {total_customers}")
print(f"Churned: {churned} ({churn_rate:.1f}%)")
print(f"Retained: {retained}")
print(f"Avg Tenure Churned: {avg_tenure_churned:.1f} months")
print(f"Avg Tenure Retained: {avg_tenure_retained:.1f} months")
print(f"Monthly Revenue at Risk: ${revenue_lost:,.2f}")
print(f"CLV Churned: ${clv_churned:,.2f}")
print(f"CLV Retained: ${clv_retained:,.2f}")

churn_by_contract = df.groupby("Contract")["Churn_Binary"].agg(["mean","sum","count"]).reset_index()
churn_by_contract.columns = ["Contract","ChurnRate","Churned","Total"]
churn_by_contract["ChurnRate"] = churn_by_contract["ChurnRate"] * 100

churn_by_internet = df.groupby("InternetService")["Churn_Binary"].agg(["mean","sum"]).reset_index()
churn_by_internet.columns = ["InternetService","ChurnRate","Churned"]
churn_by_internet["ChurnRate"] = churn_by_internet["ChurnRate"] * 100

churn_by_payment = df.groupby("PaymentMethod")["Churn_Binary"].agg(["mean","sum"]).reset_index()
churn_by_payment.columns = ["PaymentMethod","ChurnRate","Churned"]
churn_by_payment["ChurnRate"] = churn_by_payment["ChurnRate"] * 100

churn_by_tenure = df.groupby("TenureBand", observed=True)["Churn_Binary"].mean().reset_index()
churn_by_tenure.columns = ["TenureBand","ChurnRate"]
churn_by_tenure["ChurnRate"] = churn_by_tenure["ChurnRate"] * 100

cohort_df = df.groupby("SignupMonth").agg(
    Total=("CustomerID","count"),
    Churned=("Churn_Binary","sum")
).reset_index()
cohort_df["RetentionRate"] = (1 - cohort_df["Churned"] / cohort_df["Total"]) * 100
cohort_df["SignupMonth"] = cohort_df["SignupMonth"].astype(str)

print(churn_by_contract)
print(churn_by_internet)
print(churn_by_payment)

sns.set_style("darkgrid")
plt.rcParams.update({
    "figure.facecolor": "#0d0d1a",
    "axes.facecolor": "#13132b",
    "axes.labelcolor": "#f0f0ff",
    "xtick.color": "#f0f0ff",
    "ytick.color": "#f0f0ff",
    "text.color": "#f0f0ff",
    "grid.color": "#2a2a50",
    "axes.edgecolor": "#2a2a50",
})

fig = plt.figure(figsize=(22, 20))
fig.patch.set_facecolor("#0d0d1a")
fig.suptitle("Customer Retention & Churn Analysis Dashboard", fontsize=22, fontweight="bold", color="white", y=0.98)

ax1 = fig.add_subplot(3, 3, 1)
ax1.pie([churned, retained], labels=[f"Churned\n{churn_rate:.1f}%", f"Retained\n{100-churn_rate:.1f}%"],
        colors=["#ff4d6d","#00e096"], startangle=90,
        wedgeprops={"edgecolor":"#0d0d1a","linewidth":2},
        textprops={"color":"white","fontsize":9,"fontweight":"bold"})
ax1.set_title("Overall Churn vs Retention")

ax2 = fig.add_subplot(3, 3, 2)
bar_c2 = ["#ff4d6d" if v > 30 else "#f5a623" if v > 10 else "#00e096" for v in churn_by_contract["ChurnRate"]]
b2 = ax2.bar(churn_by_contract["Contract"], churn_by_contract["ChurnRate"], color=bar_c2, edgecolor="none", width=0.6)
ax2.set_title("Churn Rate by Contract Type")
ax2.set_ylabel("Churn Rate (%)")
for bar in b2:
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f"{bar.get_height():.1f}%", ha="center", fontsize=9, color="white")
ax2.grid(axis="y", alpha=0.2)

ax3 = fig.add_subplot(3, 3, 3)
bar_c3 = ["#ff4d6d" if v > 25 else "#f5a623" if v > 10 else "#00e096" for v in churn_by_internet["ChurnRate"]]
b3 = ax3.bar(churn_by_internet["InternetService"], churn_by_internet["ChurnRate"], color=bar_c3, edgecolor="none", width=0.6)
ax3.set_title("Churn Rate by Internet Service")
ax3.set_ylabel("Churn Rate (%)")
for bar in b3:
    ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f"{bar.get_height():.1f}%", ha="center", fontsize=9, color="white")
ax3.grid(axis="y", alpha=0.2)

ax4 = fig.add_subplot(3, 3, 4)
b4 = ax4.bar(churn_by_tenure["TenureBand"].astype(str), churn_by_tenure["ChurnRate"],
             color=["#ff4d6d","#f5a623","#00c8ff","#00e096","#9b59b6"], edgecolor="none", width=0.6)
ax4.set_title("Churn Rate by Tenure Band")
ax4.set_ylabel("Churn Rate (%)")
ax4.set_xlabel("Tenure (months)")
for bar in b4:
    ax4.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f"{bar.get_height():.1f}%", ha="center", fontsize=9, color="white")
ax4.grid(axis="y", alpha=0.2)

ax5 = fig.add_subplot(3, 3, 5)
ax5.hist(df[df["Churn"]=="No"]["MonthlyCharges"], bins=30, alpha=0.6, color="#00e096", label="Retained", edgecolor="none")
ax5.hist(df[df["Churn"]=="Yes"]["MonthlyCharges"], bins=30, alpha=0.6, color="#ff4d6d", label="Churned", edgecolor="none")
ax5.set_title("Monthly Charges Distribution")
ax5.set_xlabel("Monthly Charges ($)")
ax5.set_ylabel("Count")
ax5.legend(fontsize=8)
ax5.grid(axis="y", alpha=0.2)

ax6 = fig.add_subplot(3, 3, 6)
payment_short = [p.replace(" check","").replace(" transfer","").replace(" card","") for p in churn_by_payment["PaymentMethod"]]
bar_c6 = ["#ff4d6d" if v > 35 else "#f5a623" if v > 20 else "#00e096" for v in churn_by_payment["ChurnRate"]]
b6 = ax6.barh(payment_short, churn_by_payment["ChurnRate"], color=bar_c6, edgecolor="none")
ax6.set_title("Churn Rate by Payment Method")
ax6.set_xlabel("Churn Rate (%)")
for bar in b6:
    ax6.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2, f"{bar.get_width():.1f}%", va="center", fontsize=9, color="white")
ax6.grid(axis="x", alpha=0.2)

ax7 = fig.add_subplot(3, 3, 7)
ax7.plot(range(len(cohort_df)), cohort_df["RetentionRate"], color="#00c8ff", linewidth=2.5, marker="o", markersize=5)
ax7.fill_between(range(len(cohort_df)), cohort_df["RetentionRate"], alpha=0.15, color="#00c8ff")
ax7.set_xticks(range(len(cohort_df)))
ax7.set_xticklabels(cohort_df["SignupMonth"], rotation=40, fontsize=6.5)
ax7.set_title("Cohort Retention Rate by Signup Month")
ax7.set_ylabel("Retention Rate (%)")
ax7.set_ylim(0, 100)
ax7.grid(axis="y", alpha=0.2)

ax8 = fig.add_subplot(3, 3, 8)
ax8.hist(df[df["Churn"]=="No"]["Tenure"], bins=30, alpha=0.6, color="#00e096", label="Retained", edgecolor="none")
ax8.hist(df[df["Churn"]=="Yes"]["Tenure"], bins=30, alpha=0.6, color="#ff4d6d", label="Churned", edgecolor="none")
ax8.set_title("Tenure Distribution: Churned vs Retained")
ax8.set_xlabel("Tenure (months)")
ax8.set_ylabel("Count")
ax8.legend(fontsize=8)
ax8.grid(axis="y", alpha=0.2)

ax9 = fig.add_subplot(3, 3, 9)
ax9.axis("off")
kpi_text = (
    f"KPI SUMMARY\n\n"
    f"Total Customers      : {total_customers:,}\n\n"
    f"Churned              : {churned:,} ({churn_rate:.1f}%)\n\n"
    f"Retained             : {retained:,}\n\n"
    f"Avg Tenure Churned   : {avg_tenure_churned:.1f} months\n\n"
    f"Avg Tenure Active    : {avg_tenure_retained:.1f} months\n\n"
    f"Monthly Rev at Risk  : ${revenue_lost:,.0f}\n\n"
    f"CLV Churned          : ${clv_churned:,.0f}\n\n"
    f"CLV Active           : ${clv_retained:,.0f}"
)
ax9.text(0.05, 0.5, kpi_text, transform=ax9.transAxes, fontsize=9.5,
         verticalalignment="center", color="white", fontfamily="monospace",
         bbox=dict(facecolor="#13132b", edgecolor="#00c8ff", boxstyle="round,pad=1", linewidth=2))

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("FUTURE_DS_02_Dashboard.png", dpi=150, bbox_inches="tight", facecolor="#0d0d1a")
plt.show()

print(f"Overall Churn Rate: {churn_rate:.1f}%")
print(f"Month-to-month contract churn is the highest risk segment")
print(f"Fiber optic internet customers churn more than DSL customers")
print(f"Electronic check payment method users are most likely to churn")
print(f"First 6 months are the highest churn risk window")
print(f"Monthly revenue at risk from churn: ${revenue_lost:,.0f}")
print(f"Retained customers have {clv_retained/clv_churned:.1f}x higher CLV than churned customers")
print("Recommendation: Push month-to-month customers to annual contracts with discount incentives")
print("Recommendation: Introduce onboarding program for new customers in first 6 months")
print("Recommendation: Investigate Fiber optic service quality issues driving higher churn")
