# Import Core Libraries
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# -------------------------- Page Basic Settings --------------------------
st.set_page_config(
    page_title="CVP Analysis Tool",
    page_icon="📊",
    layout="wide"
)
st.title("📊 CVP (Cost-Volume-Profit) Analysis Tool")
st.markdown("---")

# ==============================================================================
# 🟢 【真正匹配你的CSV】加载电商订单数据 → 生成行业基准
# ==============================================================================
def get_ecommerce_industry_data():
    # 1. 读取你的CSV（必须和app.py放同一个文件夹）
    try:
        df = pd.read_csv("global_ecommerce_sales.csv")
    except:
        st.error("❌ 请把 global_ecommerce_sales.csv 放在app.py同一文件夹！")
        st.stop()

    # 2. 从订单日期提取年份
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    df["Year"] = df["Order_Date"].dt.year.astype("Int64")
    
    # 3. 只保留有效数据
    df = df.dropna(subset=["Year", "Product_Category", "Total_Sales", "Cost", "Profit"])
    df = df[(df["Total_Sales"] > 0) & (df["Cost"] > 0)]

    # 4. 按【年份+产品类别】分组计算行业平均CVP指标
    industry_data = df.groupby(["Year", "Product_Category"]).agg(
        Total_Sales=("Total_Sales", "mean"),
        Cost=("Cost", "mean"),
        Shipping_Cost=("Shipping_Cost", "mean"),
        Profit=("Profit", "mean")
    ).reset_index()

    # 5. 计算CVP核心比率
    industry_data["Contribution Margin Ratio (%)"] = ((industry_data["Total_Sales"] - industry_data["Cost"]) / industry_data["Total_Sales"] * 100).round(1)
    industry_data["Variable Cost Ratio (%)"] = (industry_data["Cost"] / industry_data["Total_Sales"] * 100).round(1)
    industry_data["Fixed Cost to Revenue Ratio (%)"] = (industry_data["Shipping_Cost"] / industry_data["Total_Sales"] * 100).round(1)
    industry_data["Gross Profit Margin (%)"] = ((industry_data["Total_Sales"] - industry_data["Cost"]) / industry_data["Total_Sales"] * 100).round(1)
    industry_data["Operating Leverage (DOL)"] = ((industry_data["Total_Sales"] - industry_data["Cost"]) / industry_data["Profit"]).round(2)
    industry_data["Safety Margin Ratio (%)"] = 20.0  # 默认安全边际（可用真实计算替换）

    # 6. 转换成原代码兼容格式
    industry_avg_data = {}
    for _, row in industry_data.iterrows():
        year = str(int(row["Year"]))
        category = row["Product_Category"]
        if year not in industry_avg_data:
            industry_avg_data[year] = {}
        industry_avg_data[year][category] = {
            "Contribution Margin Ratio (%)": row["Contribution Margin Ratio (%)"],
            "Variable Cost Ratio (%)": row["Variable Cost Ratio (%)"],
            "Fixed Cost to Revenue Ratio (%)": row["Fixed Cost to Revenue Ratio (%)"],
            "Gross Profit Margin (%)": row["Gross Profit Margin (%)"],
            "Operating Leverage (DOL)": row["Operating Leverage (DOL)"],
            "Safety Margin Ratio (%)": row["Safety Margin Ratio (%)"]
        }
    return industry_avg_data

# 加载行业数据（这行必须有！）
industry_avg_data = get_ecommerce_industry_data()
