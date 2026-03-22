import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="RetailPulse | Sales Analytics Dashboard",
    page_icon="📈",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    .main {
        background: linear-gradient(180deg, #f8fbff 0%, #eef4ff 100%);
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    .hero-box {
        background: linear-gradient(135deg, #1e3a8a, #2563eb);
        padding: 28px;
        border-radius: 20px;
        color: white;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.25);
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        opacity: 0.95;
        line-height: 1.6;
    }

    .kpi-card {
        background: white;
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
        border: 1px solid #e5e7eb;
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #111827;
        margin-top: 0.3rem;
        margin-bottom: 0.7rem;
    }

    .insight-box {
        background: white;
        border-left: 6px solid #2563eb;
        padding: 16px;
        border-radius: 14px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
        margin-bottom: 12px;
    }

    .footer-box {
        background: #111827;
        color: white;
        padding: 18px;
        border-radius: 16px;
        text-align: center;
        margin-top: 18px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    base_path = Path(__file__).resolve().parent.parent
    file_path = base_path / "data" / "processed" / "cleaned_superstore.csv"
    df = pd.read_csv(file_path, encoding="latin1")
    return df

df = load_data()

# ---------------- DATA PREP ----------------
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

if "Year" not in df.columns:
    df["Year"] = df["Order Date"].dt.year

df["month"] = df["Order Date"].dt.strftime("%Y-%m")

if "Profit_Margin" not in df.columns:
    df["Profit_Margin"] = (df["Profit"] / df["Sales"].replace(0, pd.NA)) * 100

# ---------------- SIDEBAR ----------------
st.sidebar.title("🎯 Dashboard Filters")
st.sidebar.markdown("Use filters to explore business performance.")

selected_category = st.sidebar.multiselect(
    "Category",
    options=sorted(df["Category"].dropna().unique())
)

selected_region = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Region"].dropna().unique())
)

year_options = sorted(df["Year"].dropna().unique())
selected_year = st.sidebar.multiselect(
    "Year",
    options=year_options,
    default=year_options
)

filtered_df = df.copy()

if selected_category:
    filtered_df = filtered_df[filtered_df["Category"].isin(selected_category)]

if selected_region:
    filtered_df = filtered_df[filtered_df["Region"].isin(selected_region)]

if selected_year:
    filtered_df = filtered_df[filtered_df["Year"].isin(selected_year)]

# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero-box">
    <div class="hero-title">RetailPulse: Sales & Profit Intelligence Dashboard</div>
    <div class="hero-subtitle">
        An interactive analytics dashboard built using Python, Pandas, Streamlit, and Plotly
        to track revenue, profitability, regional trends, customer behavior, and product performance.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- KPI CALCULATIONS ----------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
aov = total_sales / total_orders if total_orders != 0 else 0
avg_margin = filtered_df["Profit_Margin"].dropna().mean() if "Profit_Margin" in filtered_df.columns else 0

# ---------------- CUSTOMER CALCULATIONS ----------------
customer_summary = (
    filtered_df.groupby(["Customer ID", "Customer Name"], as_index=False)
    .agg({
        "Sales": "sum",
        "Order ID": "nunique"
    })
)

customer_summary = customer_summary.rename(columns={"Order ID": "Total Orders"})
customer_summary["Customer Type"] = customer_summary["Total Orders"].apply(
    lambda x: "Repeat" if x > 1 else "New"
)

total_customers = customer_summary["Customer ID"].nunique()
repeat_customers = customer_summary[
    customer_summary["Customer Type"] == "Repeat"
]["Customer ID"].nunique()

segment_sales = (
    filtered_df.groupby("Segment", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)

top_customers = (
    customer_summary.sort_values("Sales", ascending=False)
    .head(10)
)

# ---------------- EXTRA ANALYSIS TABLES ----------------
profit_margin_by_category = (
    filtered_df.groupby("Category", as_index=False)
    .agg({"Sales": "sum", "Profit": "sum"})
)

profit_margin_by_category["Profit Margin %"] = (
    profit_margin_by_category["Profit"] / profit_margin_by_category["Sales"].replace(0, pd.NA)
) * 100

profit_margin_by_category = profit_margin_by_category.sort_values(
    "Profit Margin %", ascending=False
)

category_sales = (
    filtered_df.groupby("Category", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)

region_sales = (
    filtered_df.groupby("Region", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)

monthly_sales = (
    filtered_df.groupby("month", as_index=False)["Sales"]
    .sum()
    .sort_values("month")
)

monthly_profit = (
    filtered_df.groupby("month", as_index=False)["Profit"]
    .sum()
    .sort_values("month")
)

top_products = (
    filtered_df.groupby("Product Name", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
    .head(10)
)

top_profit_products = (
    filtered_df.groupby("Product Name", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=False)
    .head(10)
)

# ---------------- KPI SECTION ----------------
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.metric("Revenue", f"${total_sales:,.0f}")
    st.markdown('</div>', unsafe_allow_html=True)

with k2:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.metric("Profit", f"${total_profit:,.0f}")
    st.markdown('</div>', unsafe_allow_html=True)

with k3:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.metric("Orders", f"{total_orders:,}")
    st.markdown('</div>', unsafe_allow_html=True)

with k4:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.metric("Avg Order Value", f"${aov:,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

with k5:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.metric("Avg Profit Margin", f"{avg_margin:,.2f}%")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 Overview", "📈 Trends", "🏆 Products", "👥 Customers", "📁 Data & Insights"]
)

# ---------------- TAB 1 OVERVIEW ----------------
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-title">Sales by Category</div>', unsafe_allow_html=True)
        fig1 = px.bar(
            category_sales,
            x="Category",
            y="Sales",
            text_auto=".2s"
        )
        fig1.update_layout(
            template="plotly_white",
            height=420,
            margin=dict(l=10, r=10, t=20, b=10)
        )
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.markdown('<div class="section-title">Regional Revenue Mix</div>', unsafe_allow_html=True)
        fig2 = px.pie(
            region_sales,
            names="Region",
            values="Sales",
            hole=0.5
        )
        fig2.update_layout(
            template="plotly_white",
            height=420,
            margin=dict(l=10, r=10, t=20, b=10)
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-title">Profit Margin by Category</div>', unsafe_allow_html=True)
    fig_margin = px.bar(
        profit_margin_by_category,
        x="Category",
        y="Profit Margin %",
        text_auto=".2f"
    )
    fig_margin.update_layout(
        template="plotly_white",
        height=420,
        margin=dict(l=10, r=10, t=20, b=10)
    )
    st.plotly_chart(fig_margin, use_container_width=True)

# ---------------- TAB 2 TRENDS ----------------
with tab2:
    c3, c4 = st.columns(2)

    with c3:
        st.markdown('<div class="section-title">Monthly Sales Trend</div>', unsafe_allow_html=True)
        fig3 = px.line(
            monthly_sales,
            x="month",
            y="Sales",
            markers=True
        )
        fig3.update_layout(
            template="plotly_white",
            height=420,
            margin=dict(l=10, r=10, t=20, b=10)
        )
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        st.markdown('<div class="section-title">Monthly Profit Trend</div>', unsafe_allow_html=True)
        fig4 = px.area(
            monthly_profit,
            x="month",
            y="Profit"
        )
        fig4.update_layout(
            template="plotly_white",
            height=420,
            margin=dict(l=10, r=10, t=20, b=10)
        )
        st.plotly_chart(fig4, use_container_width=True)

# ---------------- TAB 3 PRODUCTS ----------------
with tab3:
    c5, c6 = st.columns(2)

    with c5:
        st.markdown('<div class="section-title">Top 10 Products by Sales</div>', unsafe_allow_html=True)
        fig5 = px.bar(
            top_products,
            x="Sales",
            y="Product Name",
            orientation="h",
            text_auto=".2s"
        )
        fig5.update_layout(
            template="plotly_white",
            height=500,
            yaxis={"categoryorder": "total ascending"},
            margin=dict(l=10, r=10, t=20, b=10)
        )
        st.plotly_chart(fig5, use_container_width=True)

    with c6:
        st.markdown('<div class="section-title">Top 10 Products by Profit</div>', unsafe_allow_html=True)
        fig6 = px.bar(
            top_profit_products,
            x="Profit",
            y="Product Name",
            orientation="h",
            text_auto=".2s"
        )
        fig6.update_layout(
            template="plotly_white",
            height=500,
            yaxis={"categoryorder": "total ascending"},
            margin=dict(l=10, r=10, t=20, b=10)
        )
        st.plotly_chart(fig6, use_container_width=True)

# ---------------- TAB 4 CUSTOMERS ----------------
with tab4:
    c7, c8 = st.columns(2)

    with c7:
        st.markdown('<div class="section-title">Customer Overview</div>', unsafe_allow_html=True)
        cc1, cc2 = st.columns(2)
        cc1.metric("Total Customers", f"{total_customers:,}")
        cc2.metric("Repeat Customers", f"{repeat_customers:,}")

        fig7 = px.bar(
            segment_sales,
            x="Segment",
            y="Sales",
            title="Sales by Customer Segment",
            text_auto=".2s"
        )
        fig7.update_layout(
            template="plotly_white",
            height=420,
            margin=dict(l=10, r=10, t=50, b=10)
        )
        st.plotly_chart(fig7, use_container_width=True)

    with c8:
        st.markdown('<div class="section-title">Top Customers by Sales</div>', unsafe_allow_html=True)
        fig8 = px.bar(
            top_customers,
            x="Sales",
            y="Customer Name",
            orientation="h",
            text_auto=".2s"
        )
        fig8.update_layout(
            template="plotly_white",
            height=500,
            yaxis={"categoryorder": "total ascending"},
            margin=dict(l=10, r=10, t=20, b=10)
        )
        st.plotly_chart(fig8, use_container_width=True)

# ---------------- TAB 5 INSIGHTS ----------------
with tab5:
    st.markdown('<div class="section-title">Dataset Preview</div>', unsafe_allow_html=True)
    st.dataframe(filtered_df.head(10), use_container_width=True)

    st.markdown('<div class="section-title">Business Insights</div>', unsafe_allow_html=True)

    top_category = category_sales.iloc[0]["Category"] if not category_sales.empty else "N/A"
    top_region = region_sales.iloc[0]["Region"] if not region_sales.empty else "N/A"
    best_product = top_products.iloc[0]["Product Name"] if not top_products.empty else "N/A"

    low_profit_categories = (
        filtered_df.groupby("Category", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=True)
    )
    weakest_category = low_profit_categories.iloc[0]["Category"] if not low_profit_categories.empty else "N/A"
    best_margin_category = (
        profit_margin_by_category.iloc[0]["Category"]
        if not profit_margin_by_category.empty else "N/A"
    )

    i1, i2 = st.columns(2)

    with i1:
        st.markdown(
            f'<div class="insight-box"><b>Top Revenue Category</b><br>{top_category} is the strongest category by sales in the current filtered view.</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="insight-box"><b>Top Performing Region</b><br>{top_region} contributes the largest share of revenue.</div>',
            unsafe_allow_html=True
        )

    with i2:
        st.markdown(
            f'<div class="insight-box"><b>Best Selling Product</b><br>{best_product} leads all products in total sales.</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="insight-box"><b>Profitability Watch</b><br>{weakest_category} currently appears to be the weakest category by profit and may need pricing or discount review.</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="insight-box"><b>Best Margin Category</b><br>{best_margin_category} has the strongest profit margin, showing better profitability efficiency.</div>',
            unsafe_allow_html=True
        )

    st.markdown('<div class="section-title">Download Filtered Data</div>', unsafe_allow_html=True)
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="filtered_superstore_data.csv",
        mime="text/csv"
    )

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer-box">
    Built by Mehak | Data Analyst Portfolio Project <br>
    Tools used: Python, Pandas, Streamlit, Plotly, DuckDB
</div>
""", unsafe_allow_html=True)