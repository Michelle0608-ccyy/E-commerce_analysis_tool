import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration (MUST BE FIRST) ---
st.set_page_config(
    page_title="CVP Analysis Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS (Adapt to Light/Dark Theme) ---
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        margin-bottom: 0.5rem;
    }
    .stMetric {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid rgba(128, 128, 128, 0.2);
        background-color: rgba(128, 128, 128, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
st.title("📊 Cost-Volume-Profit (CVP) Analysis Tool")
st.caption("A professional tool for break-even analysis and scenario planning.")
st.divider()

# --- Sidebar Inputs (Organized in Groups) ---
st.sidebar.header("⚙️ Configuration")

with st.sidebar.expander("💰 Base Financials", expanded=True):
    price = st.number_input("Selling Price per Unit ($)", value=20.0, min_value=0.0, step=0.5, format="%.2f")
    variable_cost = st.number_input("Variable Cost per Unit ($)", value=12.0, min_value=0.0, step=0.5, format="%.2f")
    fixed_cost = st.number_input("Total Fixed Cost ($)", value=5000.0, min_value=0.0, step=100.0, format="%.2f")

with st.sidebar.expander("📦 Volume & Scenarios", expanded=True):
    volume = st.number_input("Base Sales Volume (Units)", value=1000, min_value=0, step=1)
    st.markdown("---")
    st.caption("Scenario Adjustments (% of Base)")
    opt_pct = st.slider("Optimistic Scenario", 100, 200, 120, help="Percentage of base volume")
    pes_pct = st.slider("Pessimistic Scenario", 20, 100, 80, help="Percentage of base volume")

# Calculate scenario volumes
opt_volume = int(volume * (opt_pct / 100))
neu_volume = volume
pes_volume = int(volume * (pes_pct / 100))

# --- Core Calculation Logic ---
def calculate_cvp(vol, p, vc, fc):
    revenue = vol * p
    total_variable_cost = vol * vc
    total_cost = total_variable_cost + fc
    profit = revenue - total_cost
    contribution_margin = p - vc
    cm_ratio = (contribution_margin / p) * 100 if p != 0 else 0
    bep_units = fc / contribution_margin if contribution_margin != 0 else 0
    bep_rev = bep_units * p
    return revenue, total_cost, profit, bep_units, bep_rev, contribution_margin, cm_ratio

# --- Main Content Area ---
# Top Row: Key Metrics Dashboard
st.subheader("🎯 Base Case Snapshot")
rev, tc, profit, bep_units, bep_rev, cm, cm_ratio = calculate_cvp(volume, price, variable_cost, fixed_cost)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Operating Profit", f"${profit:,.2f}")
with col2:
    st.metric("Total Revenue", f"${rev:,.2f}")
with col3:
    st.metric("Break-Even (Units)", f"{bep_units:,.0f}")
with col4:
    st.metric("Contribution Margin", f"{cm_ratio:.1f}%")

st.divider()

# Middle Section: Scenario Analysis
st.subheader("📈 Scenario Comparison")
st.caption("Compare financial outcomes across different sales volume assumptions.")

# Prepare data
scenarios = ["Pessimistic", "Base Case", "Optimistic"]
volumes_list = [pes_volume, neu_volume, opt_volume]
profits_list = []
revenues_list = []

for v in volumes_list:
    r, _, p, _, _, _, _ = calculate_cvp(v, price, variable_cost, fixed_cost)
    profits_list.append(p)
    revenues_list.append(r)

# Display scenario metrics in columns
scol1, scol2, scol3 = st.columns(3)
with scol1:
    st.warning(f"**Pessimistic**: {pes_volume} units")
    st.metric("Profit", f"${profits_list[0]:,.2f}", label_visibility="collapsed")
with scol2:
    st.success(f"**Base Case**: {neu_volume} units")
    st.metric("Profit", f"${profits_list[1]:,.2f}", label_visibility="collapsed")
with scol3:
    st.info(f"**Optimistic**: {opt_volume} units")
    st.metric("Profit", f"${profits_list[2]:,.2f}", label_visibility="collapsed")

# Scenario Chart
chart_df = pd.DataFrame({
    "Scenario": scenarios,
    "Sales Volume": volumes_list,
    "Profit": profits_list
})

fig = px.bar(
    chart_df, 
    x="Scenario", 
    y="Profit",
    title="Profit Comparison by Scenario",
    color="Scenario",
    color_discrete_map={"Pessimistic": "#FF9B9B", "Base Case": "#96CEB4", "Optimistic": "#9B72AA"},
    text_auto='$.2s'
)
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Bottom Section: Break-Even Chart
st.subheader("📉 Break-Even Visualization")
st.caption("The relationship between Total Revenue, Total Cost, and Sales Volume.")

# Generate data for the line chart
max_chart_vol = max(int(volume * 2), int(bep_units * 2))
chart_volumes = list(range(0, max_chart_vol + 100, 50))
rev_line = [v * price for v in chart_volumes]
tc_line = [(v * variable_cost) + fixed_cost for v in chart_volumes]

be_df = pd.DataFrame({
    "Sales Volume (Units)": chart_volumes,
    "Total Revenue": rev_line,
    "Total Cost": tc_line
})

fig_be = px.line(
    be_df, 
    x="Sales Volume (Units)", 
    y=["Total Revenue", "Total Cost"],
    title="Break-Even Chart",
    color_discrete_map={"Total Revenue": "#2E86AB", "Total Cost": "#A23B72"}
)
fig_be.update_layout(
    yaxis_title="Amount ($)",
    legend_title="",
    hovermode="x unified"
)
st.plotly_chart(fig_be, use_container_width=True)

st.divider()

# --- Intelligent Executive Summary & Recommendations ---
st.subheader("📝 Executive Summary & Recommendations")

# Calculate additional metrics for analysis
safety_margin = volume - bep_units
safety_margin_pct = (safety_margin / volume) * 100 if volume != 0 else 0

# Generate dynamic analysis text
analysis_text = ""

# 1. Overall Profit Status
if profit > 0:
    analysis_text += f"✅ **Current Status**: The business is operating profitably at the current sales volume of {volume:,} units. "
    analysis_text += f"It is generating a net operating profit of **${profit:,.2f}**. "
elif profit < 0:
    analysis_text += f"⚠️ **Current Status**: At the current sales volume of {volume:,} units, the business is operating at a loss of **${abs(profit):,.2f}**. "
else:
    analysis_text += f"ℹ️ **Current Status**: The business is currently operating exactly at its break-even point, with a net profit of $0. "

# 2. Break-Even & Safety Margin Analysis
if safety_margin > 0:
    analysis_text += f"\n\n🛡️ **Safety Margin**: Sales are currently **{safety_margin:,.0f} units** (or {safety_margin_pct:.1f}%) above the break-even point. "
    if safety_margin_pct > 30:
        analysis_text += "This is a strong safety buffer, indicating a relatively low risk of loss if sales decline slightly."
    elif safety_margin_pct > 10:
        analysis_text += "There is a moderate safety buffer. Caution is advised, as a moderate decline in sales could push the business into loss."
    else:
        analysis_text += "The safety margin is very thin. The business is highly vulnerable to any downturn in sales."
else:
    analysis_text += f"\n\n🛡️ **Safety Margin**: Sales are currently **{abs(safety_margin):,.0f} units** below the break-even point. "
    analysis_text += "Volume needs to increase significantly to reach profitability."

# 3. Cost Structure Analysis
if cm_ratio > 40:
    analysis_text += f"\n\n💎 **Cost Structure**: The contribution margin ratio is **{cm_ratio:.1f}%**, which is relatively high. "
    analysis_text += "This means that a large portion of each additional dollar of revenue goes directly to covering fixed costs and profit."
elif cm_ratio > 20:
    analysis_text += f"\n\n💎 **Cost Structure**: The contribution margin ratio is **{cm_ratio:.1f}%**, which is moderate. "
    analysis_text += "There is a balance between variable costs and profit per unit."
else:
    analysis_text += f"\n\n💎 **Cost Structure**: The contribution margin ratio is very low at **{cm_ratio:.1f}%**. "
    analysis_text += "Variable costs consume a large portion of revenue, making it harder to cover fixed costs."

# 4. Scenario Risk Analysis
analysis_text += f"\n\n🔮 **Scenario Outlook**: "
if profits_list[2] > 0 and profits_list[0] < 0:
    analysis_text += "There is significant volatility in the outlook. While the optimistic scenario is promising, the pessimistic scenario results in a loss. Risk management is key."
elif profits_list[0] > 0:
    analysis_text += "The outlook is robust. Even under the pessimistic scenario assumptions, the business remains profitable."
elif profits_list[2] < 0:
    analysis_text += "The outlook is challenging. Even under optimistic assumptions, the model does not project a profit. Structural changes may be needed."

# Display the analysis
st.markdown(analysis_text)

# --- Fixed Format: Strategic Recommendations (Full Left-Aligned) ---
st.markdown("---")
st.subheader("💡 Strategic Recommendations")

# Priority 1: Sales Volume (if needed)
if profit < 0 or safety_margin_pct < 15:
    st.markdown("**Priority 1: Increase Sales Volume**")
    st.markdown(f"- Focus marketing efforts on reaching the break-even point of {bep_units:,.0f} units.")
    st.markdown("- Consider promotional campaigns or volume discounts to stimulate customer demand.")
    st.markdown("- Explore new customer segments or distribution channels to expand market reach.")
    st.markdown("")

# Priority 2: Cost Structure Optimization (if needed)
if cm_ratio < 30:
    st.markdown("**Priority 2: Improve Cost Structure**")
    st.markdown("- Negotiate bulk pricing or long-term contracts with suppliers to reduce the variable cost per unit.")
    st.markdown("- Explore economies of scale to lower per-unit production and operational costs.")
    st.markdown("- Evaluate and eliminate non-essential variable expenses that do not drive revenue.")
    st.markdown("")

# Priority 3: Pricing Strategy Review
st.markdown("**Priority 3: Review Pricing Strategy**")
st.markdown(f"- Evaluate whether the current selling price of ${price:,.2f} adequately reflects the product's market value and cost structure.")
st.markdown("- A modest, well-communicated price increase could significantly improve the per-unit contribution margin.")
st.markdown("- Consider tiered pricing models to capture value from different customer segments.")
st.markdown("")

# Priority 4: Fixed Cost Management
st.markdown("**Priority 4: Monitor and Optimize Fixed Costs**")
st.markdown(f"- Ensure total fixed costs of ${fixed_cost:,.2f} are fully aligned with your current production capacity and sales scale.")
st.markdown("- Conduct a regular review of overhead expenses to identify opportunities for cost savings.")
st.markdown("- Avoid unnecessary fixed cost commitments until a consistent, healthy sales volume is established.")
