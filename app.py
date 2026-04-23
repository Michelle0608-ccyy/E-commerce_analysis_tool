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

# ==============================================================================
# 下面是你原来的全部界面逻辑，完全不动，直接兼容！
# ==============================================================================
sample_case_data = {
    "Technology": {"fixed_cost": 50000.0, "unit_price": 100.0, "unit_var_cost": 60.0},
    "Office Supplies": {"fixed_cost": 20000.0, "unit_price": 50.0, "unit_var_cost": 25.0},
    "Furniture": {"fixed_cost": 80000.0, "unit_price": 200.0, "unit_var_cost": 120.0}
}

# -------------------------- Sidebar --------------------------
with st.sidebar:
    st.header("⚙️ Input Mode")
    input_mode = st.radio("Select Input Method", ["Manual Input", "Load Sample Case"])

    if input_mode == "Manual Input":
        fixed_cost = st.number_input("Fixed Cost", 0.0, 50000.0, 1000.0)
        unit_price = st.number_input("Unit Price", 0.1, 100.0, 1.0)
        unit_var_cost = st.number_input("Variable Cost per Unit", 0.0, 60.0, 1.0)
        min_volume = 0
        max_volume = 2000

    else:
        selected_case = st.selectbox("Sample Cases", list(sample_case_data.keys()))
        case = sample_case_data[selected_case]
        fixed_cost = case["fixed_cost"]
        unit_price = case["unit_price"]
        unit_var_cost = case["unit_var_cost"]
        min_volume = 0
        max_volume = 2000

    st.markdown("---")
    st.subheader("🏢 Industry Benchmark")
    if not industry_avg_data:
        st.error("No industry data!")
        st.stop()
    selected_year = st.selectbox("Year", list(industry_avg_data.keys()))
    selected_industry = st.selectbox("Industry", list(industry_avg_data[selected_year].keys()))

# -------------------------- CVP Calculation --------------------------
volume = np.arange(min_volume, max_volume + 1, 100)
total_revenue = unit_price * volume
total_var_cost = unit_var_cost * volume
total_cost = fixed_cost + total_var_cost
profit = total_revenue - total_cost

break_even_volume = fixed_cost / (unit_price - unit_var_cost) if (unit_price - unit_var_cost) > 0 else 0
cm_ratio = ((unit_price - unit_var_cost) / unit_price) * 100
var_ratio = (unit_var_cost / unit_price) * 100
fixed_ratio = (fixed_cost / (unit_price * 1000)) * 100
gross_margin = cm_ratio

safety_margin = volume - break_even_volume
with np.errstate(divide='ignore', invalid='ignore'):
    safety_ratio = np.where(volume > 0, (safety_margin / volume) * 100, 0)
    dol = np.where(profit != 0, (total_revenue - total_var_cost) / profit, 0)

avg_safety = np.mean(safety_ratio[safety_ratio > 0]) if (safety_ratio > 0).any() else 0
avg_dol = np.mean(dol[(dol > 0) & (dol < 10)]) if ((dol > 0) & (dol < 10)).any() else 0

# -------------------------- Display --------------------------
st.subheader("📊 Company VS Industry (From Your CSV)")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Your Company**")
    st.dataframe(pd.DataFrame({
        "Metrics": ["CM Ratio (%)", "Var Cost Ratio (%)", "Fixed Cost Ratio (%)", "Gross Margin (%)", "Safety Margin (%)", "DOL"],
        "Value": [round(cm_ratio,2), round(var_ratio,2), round(fixed_ratio,2), round(gross_margin,2), round(avg_safety,2), round(avg_dol,2)]
    }), hide_index=True)

with col2:
    st.markdown("**Industry (From Your CSV)**")
    ind = industry_avg_data[selected_year][selected_industry]
    st.dataframe(pd.DataFrame({
        "Metrics": list(ind.keys()),
        "Industry Avg": list(ind.values())
    }), hide_index=True)

st.success("✅ 成功从你的CSV读取电商数据并显示！")
