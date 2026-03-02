"""
📌 File: data_cleaning_feature_engineering.py
🎯 Purpose:
Clean the final vendor summary dataset and create new business metrics
for profitability and performance analysis.
"""

import pandas as pd
from sqlalchemy import create_engine

# 🔹 1. Database Connection
engine = create_engine(
    "postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/inventory"
)

# 🔹 2. Load Final Summary Table
df = pd.read_sql("SELECT * FROM vendor_sales_summary_small;", engine)

# =========================================================
# 🧹 DATA CLEANING
# =========================================================

# Convert volume column to numeric
df["volume"] = pd.to_numeric(df["volume"], errors="coerce")

# Fill missing values with 0
df.fillna(0, inplace=True)

# Remove extra spaces from vendor name
df["vendorname"] = df["vendorname"].str.strip()

# =========================================================
# 📊 FEATURE ENGINEERING (Business Metrics)
# =========================================================

# 🔹 Gross Profit
df["gross_profit"] = df["total_sales_dollars"] - df["total_purchase_dollars"]

# 🔹 Profit Margin (%)
df["profit_margin"] = (
    df["gross_profit"] / df["total_sales_dollars"]
) * 100

# 🔹 Stock Turnover (Sales Quantity / Purchase Quantity)
df["stock_turnover"] = (
    df["total_sales_quantity"] / df["total_purchase_quantity"]
)

# 🔹 Sales to Purchase Ratio
df["sales_purchase_ratio"] = (
    df["total_sales_dollars"] / df["total_purchase_dollars"]
)

# =========================================================
# 💾 EXPORT CLEAN DATA
# =========================================================

df.to_csv("final_vendor_summary.csv", index=False)

print("✅ Data cleaning & feature engineering completed")
print(df.head())