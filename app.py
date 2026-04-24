import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ======================= 页面配置 =======================
st.set_page_config(
    page_title="E-commerce Full-Analysis Tool (ACC102 Track4)",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .reportview-container { background: #f5f7fa; }
    .sidebar .sidebar-content { background: #2d3748; color: white; padding: 20px 15px; }
    .sidebar .widget-label { color: #e2e8f0 !important; font-size: 1rem; }
    h1 { color: #2d3748; font-weight: 700; margin-bottom: 20px; }
    h2 { color: #2d3748; font-weight: 600; margin-top: 30px; }
</style>
""", unsafe_allow_html=True)

# ======================= 加载所有4个文件（无调试信息）=======================
@st.cache_data
def load_all_4_files():
    # 1. 读取所有4个文件
    df_customers = pd.read_csv("customers.csv")
    df_orders = pd.read_csv("orders.csv")
    df_monthly = pd.read_csv("monthly_revenue.csv")
    df_products = pd.read_csv("product_summary.csv")

    # 2. 安全检测列名（后台运行，不显示）
    # 客户数据
    cust_id_col = [col for col in df_customers.columns if 'customer_id' in col.lower() or 'id' in col.lower()][0]
    country_col = [col for col in df_customers.columns if 'country' in col.lower() or 'region' in col.lower()][0] if any('country' in col.lower() or 'region' in col.lower() for col in df_customers.columns) else None
    gender_col = [col for col in df_customers.columns if 'gender' in col.lower() or 'sex' in col.lower()][0] if any('gender' in col.lower() or 'sex' in col.lower() for col in df_customers.columns) else None
    tier_col = [col for col in df_customers.columns if 'tier' in col.lower() or 'membership' in col.lower()][0] if any('tier' in col.lower() or 'membership' in col.lower() for col in df_customers.columns) else None

    # 订单数据
    order_id_col = [col for col in df_orders.columns if 'order_id' in col.lower() or 'order' in col.lower()][0]
    date_col = [col for col in df_orders.columns if 'date' in col.lower()][0]
    amount_col = [col for col in df_orders.columns if 'amount' in col.lower() or 'total' in col.lower()][0]
    product_name_col = [col for col in df_orders.columns if 'product_name' in col.lower() or 'name' in col.lower()][0]
    category_col = [col for col in df_orders.columns if 'category' in col.lower() or 'product_type' in col.lower()][0] if any('category' in col.lower() or 'product_type' in col.lower() for col in df_orders.columns) else None
    status_col = [col for col in df_orders.columns if 'status' in col.lower()][0] if any('status' in col.lower() for col in df_orders.columns) else None

    # 月度收入数据
    date_m_col = [col for col in df_monthly.columns if 'month' in col.lower() or 'date' in col.lower()][0] if any('month' in col.lower() or 'date' in col.lower() for col in df_monthly.columns) else df_monthly.columns[0]
    revenue_col = [col for col in df_monthly.columns if 'revenue' in col.lower() or 'sales' in col.lower()][0] if any('revenue' in col.lower() or 'sales' in col.lower() for col in df_monthly.columns) else df_monthly.columns[1] if len(df_monthly.columns)>=2 else df_monthly.columns[0]
    profit_col = [col for col in df_monthly.columns if 'profit' in col.lower() or 'net' in col.lower()][0] if any('profit' in col.lower() or 'net' in col.lower() for col in df_monthly.columns) else None

    # 产品数据
    prod_name_col = [col for col in df_products.columns if 'product_name' in col.lower() or 'name' in col.lower()][0] if any('product_name' in col.lower() or 'name' in col.lower() for col in df_products.columns) else None
    prod_category_col = [col for col in df_products.columns if 'category' in col.lower() or 'product_type' in col.lower()][0] if any('category' in col.lower() or 'product_type' in col.lower() for col in df_products.columns) else None
    rating_col = [col for col in df_products.columns if 'rating' in col.lower() or 'review' in col.lower()][0] if any('rating' in col.lower() or 'review' in col.lower() for col in df_products.columns) else None
    price_col = [col for col in df_products.columns if 'price' in col.lower() or 'cost' in col.lower()][0] if any('price' in col.lower() or 'cost' in col.lower() for col in df_products.columns) else None

    # 3. 数据清洗
    # 客户数据
    dropna_cols_cust = [col for col in [cust_id_col, country_col, gender_col, tier_col] if col]
    df_customers = df_customers.dropna(subset=dropna_cols_cust)
    
    # 订单数据
    df_orders[date_col] = pd.to_datetime(df_orders[date_col], errors='coerce')
    df_orders = df_orders.dropna(subset=[order_id_col, date_col, amount_col, product_name_col])
    df_orders['month_str'] = df_orders[date_col].dt.strftime('%Y-%m')
    
    # 月度收入数据
    df_monthly[date_m_col] = pd.to_datetime(df_monthly[date_m_col], errors='coerce')
    df_monthly = df_monthly.dropna(subset=[date_m_col, revenue_col])
    df_monthly['month_str'] = df_monthly[date_m_col].dt.strftime('%Y-%m')
    df_monthly.rename(columns={revenue_col: 'revenue'}, inplace=True)
    if profit_col:
        df_monthly.rename(columns={profit_col: 'profit'}, inplace=True)
    else:
        df_monthly['profit'] = df_monthly['revenue'] * 0.2

    # 产品数据
    dropna_cols_prod = [col for col in [prod_name_col, prod_category_col, rating_col, price_col] if col]
    if dropna_cols_prod:
        df_products = df_products.dropna(subset=dropna_cols_prod)
    if prod_name_col:
        df_orders['product_name'] = df_orders['product_name'].str.strip().str.lower()
        df_products[prod_name_col] = df_products[prod_name_col].str.strip().str.lower()
        df_products.rename(columns={prod_name_col: 'product_name'}, inplace=True)
        if prod_category_col:
            df_products.rename(columns={prod_category_col: 'product_category'}, inplace=True)
        if rating_col:
            df_products.rename(columns={rating_col: 'rating'}, inplace=True)
        if price_col:
            df_products.rename(columns={price_col: 'price'}, inplace=True)
        df_order_product = pd.merge(df_orders, df_products, on='product_name', how='left')
    else:
        df_order_product = df_orders.copy()
    
    # 合并客户数据
    df_customers.rename(columns={cust_id_col: 'customer_id'}, inplace=True)
    if country_col:
        df_customers.rename(columns={country_col: 'country'}, inplace=True)
    if gender_col:
        df_customers.rename(columns={gender_col: 'gender'}, inplace=True)
    if tier_col:
        df_customers.rename(columns={tier_col: 'membership_tier'}, inplace=True)
    df_full = pd.merge(df_order_product, df_customers, on='customer_id', how='left')

    return df_customers, df_orders, df_monthly, df_products, df_full

# 加载数据（带加载提示，无调试信息）
with st.spinner("Loading data..."):
    df_customers, df_orders, df_monthly, df_products, df_full = load_all_4_files()

# ======================= 侧边栏交互控件（仅保留功能，无多余信息）=======================
st.sidebar.header("⚙️ Controls")
st.sidebar.markdown("---")

# 1. 时间筛选
st.sidebar.subheader("📅 Date Range")
min_date = df_orders['order_date'].min().date()
max_date = df_orders['order_date'].max().date()
start_date = st.sidebar.date_input("Start Date", min_date)
end_date = st.sidebar.date_input("End Date", max_date)

# 2. 客户筛选
st.sidebar.subheader("👥 Customer Filters")
selected_countries = st.sidebar.multiselect("Countries", sorted(df_customers['country'].unique()), default=df_customers['country'].unique()[:3]) if 'country' in df_customers.columns else None
selected_genders = st.sidebar.multiselect("Gender", df_customers['gender'].unique(), default=df_customers['gender'].unique()) if 'gender' in df_customers.columns else None
selected_tiers = st.sidebar.multiselect("Membership Tier", df_customers['membership_tier'].unique(), default=df_customers['membership_tier'].unique()) if 'membership_tier' in df_customers.columns else None

# 3. 产品筛选
st.sidebar.subheader("🏷️ Product Filters")
cat_col = 'product_category' if 'product_category' in df_full.columns else 'category' if 'category' in df_full.columns else None
selected_prod_cats = st.sidebar.multiselect("Product Categories", sorted(df_full[cat_col].unique()), default=df_full[cat_col].unique()[:4]) if cat_col else None
min_rating = st.sidebar.slider("Min Product Rating", 1.0, 5.0, 2.5, 0.5) if 'rating' in df_full.columns else None

# 4. 图表选择
st.sidebar.subheader("📈 Charts")
chart_options = [
    "1. Monthly Revenue & Order Volume",
    "2. Product Category Sales",
    "3. Customer Country Distribution",
    "4. Product Rating vs Sales",
    "5. Gender-Membership Spending",
    "6. Order Status Distribution",
    "7. Customer Age Group vs Spend",
    "8. Top 10 Products by Sales"
]
selected_chart = st.sidebar.selectbox("Choose Chart", chart_options)

# ======================= 数据筛选 =======================
df_filtered = df_full[
    (df_full['order_date'].dt.date >= start_date) &
    (df_full['order_date'].dt.date <= end_date)
]
if selected_countries and 'country' in df_filtered.columns:
    df_filtered = df_filtered[df_filtered['country'].isin(selected_countries)]
if selected_genders and 'gender' in df_filtered.columns:
    df_filtered = df_filtered[df_filtered['gender'].isin(selected_genders)]
if selected_tiers and 'membership_tier' in df_filtered.columns:
    df_filtered = df_filtered[df_filtered['membership_tier'].isin(selected_tiers)]
if selected_prod_cats and cat_col:
    df_filtered = df_filtered[df_filtered[cat_col].isin(selected_prod_cats)]
if min_rating and 'rating' in df_filtered.columns:
    df_filtered = df_filtered[df_filtered['rating'] >= min_rating]

# ======================= 图表展示 =======================
st.title("E-commerce Full-Dataset Analysis")
st.markdown(f"Filters: {start_date}~{end_date}")
st.markdown("---")

plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False

    # 1. Monthly Revenue & Order Volume
if selected_chart == chart_options[0]:
    st.subheader("1. Monthly Revenue & Order Volume")
    df_month = df_filtered.groupby('month_str').agg({
        'total_amount_usd': 'sum',
        'order_id': 'nunique'
    }).reset_index().sort_values('month_str')

    fig, ax1 = plt.subplots(figsize=(14, 6))
    ax1.bar(df_month['month_str'], df_month['total_amount_usd'], color='#3182ce', alpha=0.7, label='Revenue')
    ax1.set_ylabel('Revenue ($)', color='#2b6cb0')
    ax1.tick_params(axis='x', rotation=45)

    ax2 = ax1.twinx()
    ax2.plot(df_month['month_str'], df_month['order_id'], color='#e53e3e', marker='o', label='Orders')
    ax2.set_ylabel('Order Count', color='#c53030')

    fig.tight_layout()
    st.pyplot(fig)


    st.markdown("### 📊 Dynamic Insights")
    total_revenue = df_month['total_amount_usd'].sum()
    peak_month = df_month.loc[df_month['total_amount_usd'].idxmax(), 'month_str']
    peak_revenue = df_month['total_amount_usd'].max()
    avg_revenue = df_month['total_amount_usd'].mean()
    peak_orders = df_month['order_id'].max()
    correlation = df_month['total_amount_usd'].corr(df_month['order_id'])

    st.markdown(f"- Total revenue in selected period: **${total_revenue:,.2f}**")
    st.markdown(f"- Highest revenue month: **{peak_month}** (${peak_revenue:,.2f})")
    st.markdown(f"- Average monthly revenue: **${avg_revenue:,.2f}**")
    st.markdown(f"- Peak order volume: **{peak_orders} orders** in a single month")

    if correlation > 0.7:
        st.markdown("- ✅ Revenue and order volume are **strongly correlated**, indicating steady efficiency.")
    elif correlation > 0.3:
        st.markdown("- ⚠️ Revenue and order volume show **moderate correlation**, suggesting some order value variation.")
    else:
        st.markdown("- ❗ Revenue and order volume are **weakly correlated**, indicating inconsistent average order values.")

    st.markdown(f"- 💡 Consider increasing inventory and marketing efforts in **{peak_month}** to capitalize on peak demand.")

elif selected_chart == chart_options[1]:
    if cat_col:
        st.subheader("2. Product Category Sales")
        df_cat = df_filtered.groupby(cat_col)['total_amount_usd'].sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(14, 6))
        df_cat.plot(kind='bar', color='#805ad5', ax=ax)
        ax.set_ylabel('Total Sales ($)')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

        st.markdown("### 📊 Dynamic Insights")
        
        top_category = df_cat.index[0]
        top_sales = df_cat.iloc[0]
        total_sales = df_cat.sum()
        top_share = (top_sales / total_sales) * 100
        bottom_category = df_cat.index[-1]
        bottom_sales = df_cat.iloc[-1]
        
        st.markdown(f"- Top performing category: **{top_category}** (${top_sales:,.2f}, {top_share:.1f}% of total sales)")
        st.markdown(f"- Lowest performing category: **{bottom_category}** (${bottom_sales:,.2f})")
        
        if top_share > 50:
            st.markdown("- ⚠️ **High concentration risk**: Over half of sales come from one category. Diversify your product mix to reduce dependency.")
        elif top_share > 30:
            st.markdown("- ℹ️ Moderate category concentration. Continue nurturing the top performer while exploring growth in other categories.")
        else:
            st.markdown("- ✅ Balanced category distribution. Your sales are spread evenly across different categories.")

        st.markdown(f"- 💡 Consider targeted promotions for **{bottom_category}** to boost its performance.")

    else:
        st.warning("⚠️ No product category data available.")

# 3. 客户国家分布
elif selected_chart == chart_options[2]:
    if 'country' in df_filtered.columns:
        st.subheader("3. Customer Distribution by Country")
        cty = df_filtered.groupby('country')['customer_id'].nunique().sort_values(ascending=False).head(10)

        fig, ax = plt.subplots(figsize=(12, 6))
        cty.plot(kind='bar', color='#dd6b20', ax=ax)
        ax.set_ylabel('Number of Customers')
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.markdown("### 📊 Dynamic Insights")
        
        # 计算关键指标
        top_country = cty.index[0]
        top_count = cty.iloc[0]
        bottom_country = cty.index[-1]
        bottom_count = cty.iloc[-1]
        total_customers_top10 = cty.sum()
        top_share = (top_count / total_customers_top10) * 100
        
        # 输出动态文本
        st.markdown(f"- Largest customer base: **{top_country}** ({top_count} customers, {top_share:.1f}% of top 10 customers)")
        st.markdown(f"- Smallest customer base in top 10: **{bottom_country}** ({bottom_count} customers)")
        
        # 动态市场集中度建议
        if top_share > 50:
            st.markdown("- ⚠️ **High market concentration risk**: Over half of your top customers are from one country. Diversify your geographic presence to reduce dependency.")
        elif top_share > 30:
            st.markdown("- ℹ️ Moderate geographic concentration. Continue nurturing your primary market while testing localized strategies in other regions.")
        else:
            st.markdown("- ✅ Healthy geographic distribution. Your customer base is spread evenly across multiple countries.")

        # 运营建议
        st.markdown(f"- 💡 Prioritize logistics and customer support in **{top_country}** to retain your largest market.")
        st.markdown(f"- 📈 Consider targeted marketing campaigns in **{bottom_country}** to explore untapped potential.")
    else:
        st.warning("⚠️ No country data available.")

# 4. 产品评分vs销量
elif selected_chart == chart_options[3]:
    if 'rating' in df_filtered.columns:
        st.subheader("4. Product Rating vs Sales Volume")
        df_rating = df_filtered.groupby('rating').agg({
            'order_id': 'nunique',
            'total_amount_usd': 'mean'
        }).reset_index()

        fig, ax = plt.subplots(figsize=(10, 5))
        scatter = ax.scatter(df_rating['rating'], df_rating['order_id'], c=df_rating['total_amount_usd'], cmap='viridis', s=100)
        ax.set_xlabel('Product Rating')
        ax.set_ylabel('Number of Orders')
        plt.colorbar(scatter, label='Avg Sales ($)')
        st.pyplot(fig)

        st.markdown("### 📊 Dynamic Insights")
        
        # 计算关键指标
        corr_rating_orders = df_rating['rating'].corr(df_rating['order_id'])
        top_rating_by_orders = df_rating.loc[df_rating['order_id'].idxmax(), 'rating']
        top_rating_by_avg = df_rating.loc[df_rating['total_amount_usd'].idxmax(), 'rating']
        high_rating_orders = df_rating[df_rating['rating'] >= 4.0]['order_id'].sum()
        total_orders = df_rating['order_id'].sum()
        high_rating_share = (high_rating_orders / total_orders) * 100 if total_orders > 0 else 0

        # 输出动态文本
        st.markdown(f"- Rating vs Sales Correlation: **{corr_rating_orders:.2f}**")
        st.markdown(f"- Highest sales volume occurs at **{top_rating_by_orders:.1f} stars**")
        st.markdown(f"- Highest average order value occurs at **{top_rating_by_avg:.1f} stars**")
        st.markdown(f"- Products with rating ≥4.0 account for **{high_rating_share:.1f}%** of total orders")

        # 动态相关性建议
        if corr_rating_orders > 0.7:
            st.markdown("- ✅ **Strong positive correlation**: Higher-rated products consistently drive more sales. Prioritize maintaining and improving product ratings.")
        elif corr_rating_orders > 0.3:
            st.markdown("- ℹ️ **Moderate correlation**: Ratings impact sales but are not the sole driver. Focus on both quality improvements and other marketing efforts.")
        else:
            st.markdown("- ❗ **Weak correlation**: Product ratings have little impact on sales. Other factors like pricing or visibility are likely more important.")

        # 运营建议
        if high_rating_share > 60:
            st.markdown("- 💡 Consider expanding your high-rated product line to capture more market share.")
        else:
            st.markdown("- 📈 Implement review campaigns to boost ratings of mid-performing products.")
    else:
        st.warning("⚠️ No product rating data available.")

# 5. 性别-会员消费
elif selected_chart == chart_options[4]:
    if 'gender' in df_filtered.columns and 'membership_tier' in df_filtered.columns:
        st.subheader("5. Gender & Membership Spending")
        gen_mem = df_filtered.groupby(['gender', 'membership_tier'])['total_amount_usd'].sum().unstack()

        fig, ax = plt.subplots(figsize=(12, 6))
        gen_mem.plot(kind='bar', ax=ax)
        ax.set_ylabel('Total Spend ($)')
        plt.xticks(rotation=0)
        st.pyplot(fig)

        # 2. 输出动态文本
        st.markdown(f"- Highest spending group: **{top_gender} ({top_tier})** with ${top_spend:,.2f} total spend")
        st.markdown(f"- Dominant gender in spending: **{top_gender_overall}** ({top_gender_share:.1f}% of total)")
        if len(tier_totals) > 1:
            st.markdown(f"- Tier spending premium: **{tier_premium:.1f}x** higher for {top_tier_name} members vs base tier")
        
        # 3. 动态运营建议
        if tier_premium > 2:
            st.markdown("- ✅ **Strong membership premium**: Higher-tier members spend significantly more. Prioritize membership upsell campaigns.")
        elif tier_premium > 1.2:
            st.markdown("- ℹ️ Moderate membership premium. Consider tier-specific benefits to boost higher-tier spending.")
        else:
            st.markdown("- ⚠️ Low membership premium. Evaluate your tiered benefits to increase the value of higher membership levels.")
        
        if top_gender_share > 60:
            st.markdown(f"- 📈 Your customer base is skewed towards **{top_gender_overall}**. Develop targeted marketing to engage the underrepresented gender.")
        else:
            st.markdown("- ✅ Balanced gender spending distribution. Continue optimizing for both segments.")
        
        st.markdown(f"- 💡 Tailor exclusive promotions for **{top_gender} ({top_tier})** customers to retain your highest-value segment.")
        # --- 动态 Insights 结束 ---
    else:
        st.warning("⚠️ No gender or membership data available.")

# 6. 订单状态分布
elif selected_chart == chart_options[5]:
    if 'order_status' in df_filtered.columns:
        st.subheader("6. Order Status Distribution")
        status = df_filtered['order_status'].value_counts()
        # 👇 这行就是你漏掉的关键定义，我已经帮你加上了
        status_pct = df_filtered['order_status'].value_counts(normalize=True) * 100

        fig, ax = plt.subplots(figsize=(8, 8))
        status.plot(kind='pie', autopct='%1.1f%%', colors=['#38a169', '#e53e3e', '#dd6b20'], ax=ax)
        st.pyplot(fig)

        st.markdown("### 📊 Dynamic Insights")
        
        # 现在这些变量都有定义了
        total_orders = status.sum()
        top_status = status.index[0]
        top_status_pct = status_pct.iloc[0]
        
        cancelled_pct = status_pct.get('Cancelled', 0)
        pending_pct = status_pct.get('Pending', 0)
        failed_pct = status_pct.get('Failed', 0)
        abnormal_pct = cancelled_pct + pending_pct + failed_pct
        
        st.markdown(f"- Most common order status: **{top_status}** ({top_status_pct:.1f}% of all orders)")
        st.markdown(f"- Total orders in period: **{total_orders}**")
        if 'Cancelled' in status.index:
            st.markdown(f"- Cancelled orders: {status['Cancelled']} ({cancelled_pct:.1f}%)")
        if 'Pending' in status.index:
            st.markdown(f"- Pending orders: {status['Pending']} ({pending_pct:.1f}%)")
        
        if cancelled_pct > 20:
            st.markdown("- ⚠️ **High cancellation risk**: Over 20% of orders are cancelled. Investigate checkout process issues, payment failures, or customer dissatisfaction.")
        elif cancelled_pct > 10:
            st.markdown("- ℹ️ Moderate cancellation rate. Follow up with pending orders to reduce drop-offs.")
        else:
            st.markdown("- ✅ Healthy cancellation rate. Continue maintaining your checkout flow.")
        
        if pending_pct > 15:
            st.markdown(f"- 📞 Address the **high volume of pending orders ({pending_pct:.1f}%)** to prevent them from becoming cancellations.")
        else:
            st.markdown("- 💡 Monitor pending orders regularly to keep your order flow efficient.")
        
        if abnormal_pct > 30:
            st.markdown("- ❗ **High operational risk**: Over 30% of orders are in non-completed status. Prioritize resolving delays and cancellations.")
        else:
            st.markdown("- ✅ Order flow is stable with low abnormal status rates.")

    else:
        st.warning("⚠️ No order status data available.")

# 7. 客户年龄vs消费
elif selected_chart == chart_options[6]:
    if 'age' in df_filtered.columns:
        st.subheader("7. Customer Age Group vs Spend")
        df_filtered['age_group'] = pd.cut(df_filtered['age'], bins=[18,25,35,45,55,70], labels=['18-25','26-35','36-45','46-55','56-70'])
        age_spend = df_filtered.groupby('age_group')['total_amount_usd'].mean()

        fig, ax = plt.subplots(figsize=(10, 5))
        age_spend.plot(kind='line', marker='o', linewidth=3, color='#ff9800', ax=ax)
        ax.set_ylabel('Avg Order Value ($)')
        st.pyplot(fig)

        st.markdown("### 📊 Dynamic Insights")
        
        # 1. 计算关键指标
        top_age_group = age_spend.idxmax()
        top_avg_spend = age_spend.max()
        bottom_age_group = age_spend.idxmin()
        bottom_avg_spend = age_spend.min()
        spend_range = top_avg_spend - bottom_avg_spend
        
        # 计算年龄与消费的相关性（用年龄组中间值量化）
        age_midpoints = {
            '18-25': 21.5,
            '26-35': 30.5,
            '36-45': 40.5,
            '46-55': 50.5,
            '56-70': 63
        }
        numeric_ages = [age_midpoints[group] for group in age_spend.index]
        corr_age_spend = pd.Series(numeric_ages).corr(age_spend)
        
        # 2. 输出动态文本
        st.markdown(f"- Highest average spend: **{top_age_group}** (${top_avg_spend:.2f} per order)")
        st.markdown(f"- Lowest average spend: **{bottom_age_group}** (${bottom_avg_spend:.2f} per order)")
        st.markdown(f"- Spend gap between groups: **${spend_range:.2f}**")
        
        # 3. 动态趋势分析与建议
        if corr_age_spend > 0.5:
            st.markdown("- ✅ **Positive correlation**: Older customers consistently spend more. Prioritize loyalty programs and premium offers for older age groups.")
        elif corr_age_spend < -0.5:
            st.markdown("- ⚠️ **Negative correlation**: Younger customers tend to spend more. Focus on student discounts, social media marketing, and Gen Z-friendly products.")
        else:
            st.markdown("- ℹ️ **No strong correlation**: Spending varies across age groups, indicating diverse customer preferences.")
        
        # 针对性运营建议
        if spend_range > 20:
            st.markdown(f"- 💡 Significant spend gap detected. Develop targeted promotions for **{bottom_age_group}** customers to lift their average order value.")
        else:
            st.markdown("- ✅ Balanced spending across age groups. Continue offering products that appeal to a broad audience.")
        # --- 动态 Insights 结束 ---
    else:
        st.warning("⚠️ No customer age data available.")

# 8. Top10产品
elif selected_chart == chart_options[7]:
    st.subheader("8. Top 10 Products by Sales")
    top_prod = df_filtered.groupby('product_name')['total_amount_usd'].sum().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(14, 8))
    top_prod.plot(kind='barh', color='#805ad5', ax=ax)
    ax.set_xlabel('Total Sales ($)')
    st.pyplot(fig)

    st.markdown("### 📊 Dynamic Insights")
    
    # 计算关键指标
    top1_product = top_prod.index[0]
    top1_sales = top_prod.iloc[0]
    top10_total = top_prod.sum()
    top1_share = (top1_sales / top10_total) * 100
    last_product = top_prod.index[-1]
    last_sales = top_prod.iloc[-1]
    sales_gap = top1_sales - last_sales

    # 输出动态文本
    st.markdown(f"- Top-selling product: **{top1_product}** (${top1_sales:,.2f}, {top1_share:.1f}% of Top 10 sales)")
    st.markdown(f"- Lowest-selling in Top 10: **{last_product}** (${last_sales:,.2f})")
    st.markdown(f"- Sales gap between #1 and #10: **${sales_gap:,.2f}**")

    # 动态集中度分析与建议
    if top1_share > 30:
        st.markdown("- ⚠️ **High concentration risk**: Over 30% of Top 10 sales come from a single product. This creates inventory and revenue risk.")
        st.markdown(f"- 💡 Consider expanding product lines or promoting alternatives to reduce dependency on **{top1_product}**.")
    elif top1_share > 20:
        st.markdown("- ℹ️ Moderate product concentration. The top product performs well without dominating the entire Top 10.")
        st.markdown(f"- 💡 Continue prioritizing inventory for **{top1_product}** while exploring growth for other top performers.")
    else:
        st.markdown("- ✅ Healthy product distribution. Sales are spread evenly across the Top 10, reducing dependency on any single item.")
        st.markdown("- 💡 Leverage cross-selling between these complementary products to boost overall average order value.")

# 数据导出
st.sidebar.markdown("---")
st.sidebar.subheader("💾 Export Data")
if st.sidebar.button("Download Filtered Data"):
    df_filtered.to_csv("filtered_ecommerce_data.csv", index=False)
    st.sidebar.success("✅ File saved!")