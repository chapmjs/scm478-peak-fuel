import streamlit as st
import pandas as pd

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
page = st.sidebar.radio("Go to", ["Dashboard", "Ingredients", "Sales", "Purchasing"])

st.sidebar.divider()
st.sidebar.caption("SCM 478 • BYU-Idaho")

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

    # Supplier filter
    supplier_list = ["All"] + sorted(ingredients_df["Primary Supplier Name"].dropna().unique())
    selected_supplier = st.selectbox("Filter by Primary Supplier Name", supplier_list)

    # Apply filter
    if selected_supplier != "All":
        filtered_df = ingredients_df[ingredients_df["Primary Supplier Name"] == selected_supplier]
    else:
        filtered_df = ingredients_df

    # Metrics
    total_ingredients = len(filtered_df)
    unique_suppliers = filtered_df["Primary Supplier Name"].nunique()
    avg_cost = filtered_df["Cost Per Unit"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Ingredients", total_ingredients)
    col2.metric("Unique Suppliers", unique_suppliers)
    col3.metric("Avg Cost Per Unit", f"${avg_cost:,.2f}")

    # Display table
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
