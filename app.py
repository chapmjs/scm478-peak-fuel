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
    return products, ingredients

products_df, ingredients_df = load_data()

# ---------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Ingredients", "Sales", "Purchasing", "Self-Check"])

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
# Sales Page (placeholder)
# ---------------------------------------------------------
elif page == "Sales":
    st.title("Sales")
    st.write("Sales and demand data will go here.")

# ---------------------------------------------------------
# Purchasing Page (placeholder)
# ---------------------------------------------------------
elif page == "Purchasing":
    st.title("Purchasing")
    st.write("Purchase orders and supplier info will go here.")



