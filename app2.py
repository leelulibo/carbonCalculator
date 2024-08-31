import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Table, MetaData

# Create a SQLite database
engine = create_engine('sqlite:///carbon_clever.db', echo=True)
meta = MetaData()

# Create a table for carbon credits
credits = Table(
    'credits', meta,
    Column('id', Integer, primary_key=True),
    Column('company', String),
    Column('emission_reduction', Float),
    Column('price_per_ton', Float)
)

meta.create_all(engine)

# Function to calculate emissions
def calculate_emissions(activity_type, quantity):
    emission_factors = {
        'electricity': 0.92,  # kg CO2 per kWh
        'transport': 2.31,    # kg CO2 per liter of gasoline
    }
    return quantity * emission_factors.get(activity_type, 0)

# Function to list carbon credits for sale
def list_credits(company, emission_reduction, price_per_ton):
    with engine.connect() as conn:
        conn.execute(credits.insert().values(company=company, emission_reduction=emission_reduction, price_per_ton=price_per_ton))
        st.success("Credits listed successfully!")

# Streamlit UI
st.title("Carbon Clever - Emissions Calculator & Marketplace")

# Emissions calculator input
st.header("Calculate Your Emissions")
activity_type = st.selectbox("Select Activity Type", ["electricity", "transport"])
quantity = st.number_input("Enter Quantity (kWh for electricity, liters for gasoline)", min_value=0.0)
emissions = calculate_emissions(activity_type, quantity)
st.write(f"Your emissions are: {emissions} kg CO2")

# Marketplace input
st.header("List Carbon Credits for Sale")
company = st.text_input("Company Name")
emission_reduction = st.number_input("Emission Reduction (in tons)", min_value=0.0)
price_per_ton = st.number_input("Price per Ton (in $)", min_value=0.0)
if st.button("List Credits"):
    list_credits(company, emission_reduction, price_per_ton)

# Display marketplace
st.header("Marketplace")
with engine.connect() as conn:
    result = conn.execute(credits.select())
    df = pd.DataFrame(result.fetchall(), columns=result.keys())
    st.write(df)
