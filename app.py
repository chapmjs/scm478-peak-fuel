import streamlit as st
import pandas as pd
import self_check

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Peak Fuel Foods",
    page_icon="⚡",
    layout="wide"
)

# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
@st.cache_data
def load_data():
    products = pd.read_csv("Products_Pricing.csv")
    ingredients = pd.read_csv("Ingredient_Catalog.csv")
    sales = pd.read_csv("Sales_Log.csv", parse_dates=["Date"])
    return products, ingredients, sales

products_df, ingredients_df, sales_df = load_data()

# ---------------------------------------------------------
# Sales helpers
# ---------------------------------------------------------
def build_weekly_product_sales(df):
    sales = df.copy()
    sales["Revenue"] = sales["Quantity"] * sales["Unit Price"]

    iso = sales["Date"].dt.isocalendar()
    sales["ISO Year"] = iso.year.astype(int)
    sales["ISO Week"] = iso.week.astype(int)
    sales["Week Label"] = (
        sales["ISO Year"].astype(str)
        + "-W"
        + sales["ISO Week"].astype(str).str.zfill(2)
    )

    weekly = (
        sales.groupby(["Product Name", "ISO Year", "ISO Week", "Week Label"], as_index=False)
        .agg(
            Total_Units=("Quantity", "sum"),
            Total_Revenue=("Revenue", "sum")
        )
        .sort_values(["ISO Year", "ISO Week", "Product Name"])
    )
    return weekly


def build_units_pivot(weekly_df):
    pivot = weekly_df.pivot_table(
        index="Product Name",
        columns="Week Label",
        values="Total_Units",
        aggfunc="sum",
        fill_value=0,
    )
    pivot = pivot.reindex(sorted(pivot.columns), axis=1)
    return pivot


def identify_high_growth_products(pivot_df):
    growth_rows = []
    for product_name, row in pivot_df.iterrows():
        values = row.tolist()
        first_units = next((value for value in values if value > 0), 0)
        last_units = next((value for value in reversed(values) if value > 0), 0)
        absolute_growth = last_units - first_units
        growth_rows.append((product_name, absolute_growth))

    growth_df = pd.DataFrame(growth_rows, columns=["Product Name", "Absolute Growth"])
    top_growth = set(
        growth_df.sort_values(["Absolute Growth", "Product Name"], ascending=[False, True])
        .head(2)["Product Name"]
        .tolist()
    )
    return top_growth


def describe_trend(units_by_week):
    values = [int(v) for v in units_by_week.tolist()]
    start_avg = sum(values[:3]) / min(3, len(values))
    end_avg = sum(values[-3:]) / min(3, len(values))
    delta = end_avg - start_avg

    if start_avg == 0:
        if end_avg > 0:
            return "growing as weekly demand built over the eleven weeks."
        return "flat with little change across the eleven weeks."

    pct_change = delta / start_avg

    if pct_change > 0.15:
        return "growing as weekly demand trended upward over the eleven weeks."
    if pct_change < -0.15:
        return "declining as weekly demand softened over the eleven weeks."
    return "flat overall with only modest week-to-week movement."


def build_quick_scan(pivot_df):
    summary = pd.DataFrame({
        "Product Name": pivot_df.index,
        "Total Units": pivot_df.sum(axis=1).astype(int).values,
        "Trend": [describe_trend(pivot_df.loc[name]) for name in pivot_df.index],
    })
    summary = summary.sort_values(["Total Units", "Product Name"], ascending=[False, True]).reset_index(drop=True)
    summary.index = summary.index + 1
    return summary


# ---------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Ingredients", "Sales and Demand", "Purchasing", "Self-Check"])

st.sidebar.divider()
st.sidebar.caption("SCM 478 • BYU-Idaho")

# Self-Check Page:
if page == "Self-Check":
    self_check.run_self_check()

# ---------------------------------------------------------
# Dashboard Page
# ---------------------------------------------------------
if page == "Dashboard":
    st.title("⚡ Peak Fuel Foods")
    st.subheader("Product Catalog")

    st.dataframe(products_df, use_container_width=True)

# ---------------------------------------------------------
# Ingredients Page
# ---------------------------------------------------------
elif page == "Ingredients":
    st.title("Ingredient Catalog")

    # --- Filters ---
    supplier_list = ["All"] + sorted(ingredients_df["Primary Supplier Name"].dropna().unique())
    order_unit_list = ["All"] + sorted(ingredients_df["Order Unit"].dropna().unique())

    colA, colB = st.columns(2)
    selected_supplier = colA.selectbox("Filter by Primary Supplier Name", supplier_list)
    selected_order_unit = colB.selectbox("Filter by Order Unit", order_unit_list)

    # --- Apply filters ---
    filtered_df = ingredients_df.copy()

    if selected_supplier != "All":
        filtered_df = filtered_df[filtered_df["Primary Supplier Name"] == selected_supplier]

    if selected_order_unit != "All":
        filtered_df = filtered_df[filtered_df["Order Unit"] == selected_order_unit]

    # --- Metrics ---
    total_ingredients = len(filtered_df)
    unique_suppliers = filtered_df["Primary Supplier Name"].nunique()
    avg_cost = filtered_df["Cost Per Unit"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Ingredients", total_ingredients)
    col2.metric("Unique Suppliers", unique_suppliers)
    col3.metric("Avg Cost Per Unit", f"${avg_cost:,.2f}")

    # --- Table ---
    st.dataframe(filtered_df, use_container_width=True)

# ---------------------------------------------------------
# Sales and Demand Page
# ---------------------------------------------------------
elif page == "Sales and Demand":
    st.title("Sales and Demand")

    weekly_sales_df = build_weekly_product_sales(sales_df)
    units_pivot_df = build_units_pivot(weekly_sales_df)
    high_growth_products = identify_high_growth_products(units_pivot_df)
    quick_scan_df = build_quick_scan(units_pivot_df)

    def highlight_growth_rows(row):
        if row.name in high_growth_products:
            return ["background-color: #fff3b0; font-weight: 600;"] * len(row)
        return [""] * len(row)

    st.subheader("Weekly Units Pivot")
    st.dataframe(
        units_pivot_df.style.apply(highlight_growth_rows, axis=1),
        use_container_width=True,
    )

    st.write("**Highest-growth products:** " + ", ".join(sorted(high_growth_products)))

    st.subheader("Quick-Scan Summary")
    for rank, row in quick_scan_df.iterrows():
        st.write(f"{rank}. {row['Product Name']} — {row['Total Units']:,} total units — {row['Trend']}")

# ---------------------------------------------------------
# Purchasing Page (placeholder)
# ---------------------------------------------------------
elif page == "Purchasing":
    st.title("Purchasing")
    st.write("Purchase orders and supplier info will go here.")



