import pandas as pd
import streamlit as st
import plotly.express as px
import urllib.request
from PIL import Image
from urllib.request import urlopen
import os
    
@st.cache_data
def load_data():
    return pd.read_csv('vehicles_us.csv')

data = load_data()

# Check if the image file already exists to avoid re-downloading
image_path = "used-cars-for-sale-north-carolina-usa-J388K0.jpg"
if not os.path.exists(image_path):
    urllib.request.urlretrieve('https://c7.alamy.com/comp/J388K0/used-cars-for-sale-north-carolina-usa-J388K0.jpg', image_path)
    
st.title('**Filters**')
st.title('Choose your car')
st.subheader('Use this app to find the best car for your wants and needs')


## Display the image
##urllib.request.urlretrieve('https://c7.alamy.com/comp/J388K0/used-cars-for-sale-north-carolina-usa-J388K0.jpg', "used-cars-for-sale-north-carolina-usa-J388K0.jpg")
##image = Image.open("used-cars-for-sale-north-carolina-usa-J388K0.jpg")
st.image_path(image)
    
st.caption(':red[Choose your parameters here]')
   
 #  create a sidebars for user input   
#price slider
price_range = st.slider("Select desired price range", 
                            value=(int(data['price'].min()), int(data['price'].max())))
actual_range=list(range(price_range[0], price_range[1] + 1))

#odometer slider
odo_range = st.slider("Select desired mileage range?", 
                            value=(int(data['odometer'].min()), int(data['odometer'].max())))
actual_range=list(range(odo_range[0], odo_range[1] + 1))    
    
#type bar
type_range = st.multiselect("Select vehicle type", 
                            options=['SUV', 'bus', 'convertible', 'coupe', 'hatchback', 'mini-van', 'offroad', 'other', 'pickup', 'sedan', 'truck', 'van', 'wagon'],
                            default=['SUV', 'bus', 'convertible', 'coupe', 'hatchback', 'mini-van', 'offroad', 'other', 'pickup', 'sedan', 'truck', 'van', 'wagon'])
    
    
 #condition bar
condition_range = st.multiselect("Select vehicle condition",
                           options=['excellent', 'fair', 'good', 'like new', 'new', 'poor', 'salvage'],
                           default=['excellent', 'fair', 'good', 'like new', 'new', 'poor', 'salvage'])



fwd_check = st.checkbox('4 wheel drive')  # checkbox for four wheel drive

if fwd_check:
    rows_before_fwd = len(data)
    filtered_data_temp = data[data['is_4wd'] == 1]
    rows_after_fwd = len(filtered_data_temp)
    st.write(f"Marking this checkbox will exclude {rows_before_fwd - rows_after_fwd} rows.")



if fwd_check:
    filtered_data=data[data.is_4wd.isin(actual_range)]
    filtered_data=filtered_data[filtered_data.is_4wd=='1']
else:
    filtered_data=data[data.is_4wd.isin(actual_range)]

nan_unknown_check = st.checkbox('Exclude rows with unknown values (except paint_color)') #checkbox for empty values
if nan_unknown_check:
    filtered_data = filtered_data.dropna(subset=[col for col in filtered_data.columns if col != 'paint_color'])
    filtered_data = filtered_data[~filtered_data[[col for col in filtered_data.columns if col != 'paint_color']].isin(['unknown', 'None', 'none']).any(axis=1)]    
  # Filter the data based on user input
    filtered_data = data[
        (data['type'].isin(type_range)) &
        (data['condition'].isin(condition_range)) &
        (data['odometer'].isin(odo_range)) &
        (data['price'].isin(price_range))) &
        (data['is_4wd'] == 1 if fwd_check else True)
    ]
    rows_before_nan = len(filtered_data)
    filtered_data_temp = filtered_data.dropna(subset=[col for col in filtered_data.columns if col != 'paint_color'])
    filtered_data_temp = filtered_data_temp[~filtered_data_temp[[col for col in filtered_data.columns if col != 'paint_color']].isin(['unknown', 'None', 'none']).any(axis=1)]
    rows_after_nan = len(filtered_data_temp)
    st.write(f"Marking this checkbox will exclude {rows_before_nan - rows_after_nan} rows.")
    # Apply nan_unknown_check filter
    if nan_unknown_check:
        filtered_data = filtered_data.dropna(subset=[col for col in filtered_data.columns if col != 'paint_color'])
        filtered_data = filtered_data[~filtered_data[[col for col in filtered_data.columns if col != 'paint_color']].isin(['unknown', 'None', 'none']).any(axis=1)]
 
 
st.title('**Filtered cars**')
    # Display the filtered data
st.write(filtered_data)
    
    # Create a bars charts of the filtered data
    
st.title('**Visualizations**')   
st.write('Here are your options with a split by price and condition')
fig = px.bar(filtered_data, x='price', y='condition', title='')
st.plotly_chart(fig)
    
st.write('Here are your options with a split by model_year and price')
    
# Create a histogram for price distribution
st.write('Price distribution of the filtered cars')
fig2 = px.histogram(filtered_data, x='price', nbins=30, title='')
st.plotly_chart(fig2)

# Create a histogram for odometer distribution
st.write('Odometer distribution of the filtered cars')
fig3 = px.histogram(filtered_data, x='odometer', nbins=30, title='')
st.plotly_chart(fig3)

# Create a scatter plot for price vs. odometer
st.write('Scatter plot of Price vs Odometer')
fig4 = px.scatter(filtered_data, x='odometer', y='price', title='')
st.plotly_chart(fig4)

# Create a scatter plot for model_year vs. price
st.write('Scatter plot of Model Year vs Price')
fig5 = px.scatter(filtered_data, x='model_year', y='price', title='')
st.plotly_chart(fig5)

# Creating a top 10 recomended cars from filterd data  
st.title('Recomendations')     
st.write('Here is the list of recomended cars from selected list')
try:
    top_cars = filtered_data.nsmallest(10, ['price', 'odometer','model_year'])
    st.dataframe(top_cars)
except ValueError:
    st.write('No data available for the selected filters.')
