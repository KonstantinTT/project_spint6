import pandas as pd
import streamlit as st
import plotly.express as px
import urllib.request
import os

# === Load data with caching === #
@st.cache_data
def load_data():
    try:
        return pd.read_csv('vehicles_us.csv')
    except FileNotFoundError:
        st.error("File 'vehicles_us.csv' not found. Please add it to the directory.")
        return pd.DataFrame()

data = load_data()
if data.empty:
    st.stop()

# === Download and display image only once === #
image_url = 'https://c7.alamy.com/comp/J388K0/used-cars-for-sale-north-carolina-usa-J388K0.jpg'
image_path = "used-cars.jpg"
if not os.path.exists(image_path):
    urllib.request.urlretrieve(image_url, image_path)
st.image(image_path)

st.title('Choose Your Car')
st.subheader('Use this app to find the best car for your wants and needs')

# === Sidebar filter options === #
st.sidebar.header("Filter options")
price_min, price_max = int(data['price'].min()), int(data['price'].max())
odometer_min, odometer_max = int(data['odometer'].min()), int(data['odometer'].max())

price_range = st.sidebar.slider("Price range:", price_min, price_max, (price_min, price_max))
odometer_range = st.sidebar.slider("Odometer range:", odometer_min, odometer_max, (odometer_min, odometer_max))

vehicle_types = st.sidebar.multiselect("Vehicle type:", data['type'].dropna().unique(), default=list(data['type'].dropna().unique()))
conditions = st.sidebar.multiselect("Condition:", data['condition'].dropna().unique(), default=list(data['condition'].dropna().unique()))

fwd_only = st.sidebar.checkbox("Only 4WD")
exclude_unknowns = st.sidebar.checkbox("Exclude rows with unknown/NaN values (except paint_color)")

# === Apply filters === #
filtered_data = data[
    (data['price'].between(*price_range)) &
    (data['odometer'].between(*odometer_range)) &
    (data['type'].isin(vehicle_types)) &
    (data['condition'].isin(conditions))
]

if fwd_only:
    filtered_data = filtered_data[filtered_data['is_4wd'] == 1]

if exclude_unknowns:
    # Drop rows with NaN or 'unknown' values (except 'paint_color')
    clean_columns = [col for col in filtered_data.columns if col != 'paint_color']
    filtered_data = filtered_data.dropna(subset=clean_columns)
    filtered_data = filtered_data[~filtered_data[clean_columns].isin(['unknown', 'none', 'None']).any(axis=1)]

# === Display filtered data === #
st.header("Filtered Cars")
st.write(f"Number of matching cars: {len(filtered_data)}")
st.dataframe(filtered_data)

# === Visualizations === #
st.header("Visualizations")

# Histogram of price distribution
st.subheader("Price Distribution")
st.plotly_chart(px.histogram(filtered_data, x='price', nbins=30))

# Histogram of odometer distribution
st.subheader("Odometer Distribution")
st.plotly_chart(px.histogram(filtered_data, x='odometer', nbins=30))

# Scatter plot: Price vs Odometer
st.subheader("Price vs. Odometer")
st.plotly_chart(px.scatter(filtered_data, x='odometer', y='price'))

# Scatter plot: Model year vs Price
if 'model_year' in filtered_data.columns:
    st.subheader("Model Year vs. Price")
    st.plotly_chart(px.scatter(filtered_data, x='model_year', y='price'))

# Histogram: Count of cars by condition
st.subheader("Condition Breakdown")
st.plotly_chart(px.histogram(filtered_data, x='condition'))

# === Top 10 recommended cars === #
st.header("Top 10 Recommended Cars")
try:
    top_cars = (filtered_data.dropna(subset=['price', 'odometer', 'model_year'])
                .nsmallest(10, ['price', 'odometer', 'model_year']))
    st.dataframe(top_cars)
except ValueError:
    st.write("Not enough data available for recommendations.")
