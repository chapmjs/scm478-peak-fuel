import streamlit as st

st.set_page_config(page_title="Peak Fuel Foods", page_icon="⚡", layout="wide")

st.title("⚡ Peak Fuel Foods")
st.subheader("Supply Chain Management System")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Ingredients", "Sales", "Purchasing"])

if page == "Dashboard":
    st.write("Welcome to Peak Fuel Foods! Built by chapmjs.")
    st.write("Use the sidebar to navigate between modules.")
elif page == "Ingredients":
    st.write("Ingredient catalog will go here.")
elif page == "Sales":
    st.write("Sales and demand data will go here.")
elif page == "Purchasing":
    st.write("Purchase orders and supplier info will go here.")

st.sidebar.divider()
st.sidebar.caption("SCM 478 • BYU-Idaho")
