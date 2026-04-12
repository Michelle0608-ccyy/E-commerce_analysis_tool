# Import core libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------- Original Code: Page Basic Settings (Fully Preserved) --------------------------
# Set page style (original format unchanged)
st.set_page_config(page_title="Data Visualization Analysis Tool", layout="wide")
st.title("📊 Preset Value Visualization Analysis Platform")
st.markdown("---")

# -------------------------- Original Code: User Input Preset Value Module (Fully Preserved) --------------------------
st.subheader("1. Enter Your Preset Values")
# Left input area (original layout unchanged)
col1, col2 = st.columns(2)
with col1:
    sales = st.number_input("Total Sales (¥)", min_value=0, value=50000, step=1000)
    cost = st.number_input("Total Operating Cost (¥)", min_value=0, value=30000, step=1000)
    new_user = st.number_input("New Users (Persons)", min_value=0, value=2000, step=100)
with col2:
    profit = sales - cost
    conversion_rate = st.slider("User Conversion Rate (%)", min_value=0.0, max_value=100.0, value=15.0, step=0.5)
    repurchase_rate = st.slider("User Repurchase Rate (%)", min_value=0.0, max_value=100.0, value=25.0, step=0.5)

# Display core input data (original function unchanged)
st.markdown("#### 🔍 Overview of Your Input Core Data")
data = pd.DataFrame({
    "Indicator": ["Total Sales", "Operating Cost", "Net Profit", "New Users", "Conversion Rate", "Repurchase Rate"],
    "Value": [sales, cost, profit, new_user, f"{conversion_rate}%", f"{repurchase_rate}%"]
})
st.dataframe(data, use_container_width=True)
st.markdown("---")

# -------------------------- Original Code: Chart Analysis Module (Fully Preserved) --------------------------
st.subheader("2. Data Chart Visualization Analysis")
# Display charts in columns (original layout unchanged)
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    # Bar chart: Revenue, Cost & Profit Comparison
    fig1, ax1 = plt.subplots(figsize=(5, 4))
    ax1.bar(["Total Sales", "Operating Cost", "Net Profit"], [sales, cost, profit], color=["#2E86AB", "#A23B72", "#F18F01"])
    ax1.set_title("Revenue Structure Comparison", fontsize=12)
    plt.tight_layout()
    st.pyplot(fig1)

with chart_col2:
    # Pie chart: User Conversion Distribution
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    user_labels = ["Converted Users", "Non-Converted Users"]
    user_values = [conversion_rate, 100 - conversion_rate]
    ax2.pie(user_values, labels=user_labels, autopct="%1.1f%%", colors=["#C73E1D", "#E8E8E8"])
    ax2.set_title("User Conversion Rate Distribution", fontsize=12)
    st.pyplot(fig2)

# Line chart: User Operation Indicator Trend
fig3, ax3 = plt.subplots(figsize=(10, 3))
ax3.plot(["New Users", "Conversion Rate", "Repurchase Rate"], [new_user/100, conversion_rate, repurchase_rate],
         color="#006400", marker="o", linewidth=2)
ax3.set_title("User Operation Indicator Trend", fontsize=12)
st.pyplot(fig3)
st.markdown("---")

# -------------------------- New Code: Overall Analysis + Optimization Suggestions --------------------------
st.subheader("3. 📝 Overall Situation Analysis & Recommendations")
st.markdown("#### I. Overall Situation Summary")

# Automatically generate text analysis based on input values
analysis_text = ""

# 1. Revenue & Profit Analysis
if profit > 0:
    profit_level = "profitable and operating in good condition"
elif profit == 0:
    profit_level = "breaking even with no profit or loss"
else:
    profit_level = "operating at a loss and under pressure"

# 2. Conversion Rate Analysis
if conversion_rate >= 20:
    convert_level = "excellent, with user conversion efficiency far above the industry average"
elif 10 <= conversion_rate < 20:
    convert_level = "moderate, with user conversion efficiency at the normal industry level"
else:
    convert_level = "low, and user conversion efficiency needs to be improved"

# 3. Repurchase Rate Analysis
if repurchase_rate >= 30:
    repurchase_level = "excellent, with extremely high user loyalty"
elif 15 <= repurchase_rate < 30:
    repurchase_level = "moderate, with user loyalty at a qualified level"
else:
    repurchase_level = "low, with insufficient user retention and repurchase capability"

# Overall analysis text
analysis_text = f"""
Based on the preset values you entered, the analysis results are as follows:
1. Overall Revenue: Total sales are ¥{sales:,}, total operating cost is ¥{cost:,}, and final net profit is ¥{profit:,},
   putting the business in a **{profit_level}**;
2. User Growth: The number of new users is {new_user}, with a user conversion rate of {conversion_rate}%,
   which is {convert_level};
3. User Retention: The user repurchase rate is {repurchase_rate}%, {repurchase_level};
4. Comprehensive Rating: The overall performance of the three core indicators (revenue & profit, user conversion,
   user retention) is **{'excellent' if (profit>0 and conversion_rate>=15 and repurchase_rate>=20) else 'average' if (profit>=0 and conversion_rate>=10 and repurchase_rate>=15) else 'poor'}**.
"""
st.write(analysis_text)

st.markdown("#### II. Targeted Optimization Suggestions")

# Generate suggestions based on data weaknesses
suggestions = []
if profit < 0:
    suggestions.append("⚠️ Focus on controlling operating costs, optimize the supply chain and operating expenses, improve product pricing, and quickly reverse losses.")
elif 0 < profit < sales * 0.2:
    suggestions.append("📉 Net profit margin is low. Consider streamlining unnecessary costs, expanding high-margin businesses/products, and improving profitability.")

if conversion_rate < 15:
    suggestions.append("🎯 User conversion rate is low. Optimize product landing pages, simplify purchase processes, add user guidance, and improve conversion efficiency.")

if repurchase_rate < 25:
    suggestions.append("🤝 User repurchase rate is insufficient. Launch membership systems, coupons, and exclusive activities for existing users to enhance user stickiness and loyalty.")

if profit > 0 and conversion_rate >= 15 and repurchase_rate >= 25:
    suggestions.append("✅ All indicators perform well. Maintain current operational strategies while exploring new growth channels to expand business scale.")

# Display suggestions
for i, sug in enumerate(suggestions, 1):
    st.write(f"{i}. {sug}")

st.markdown("---")
st.caption("✅ Analysis completed: The above content is automatically generated based on your preset values for reference only.")
