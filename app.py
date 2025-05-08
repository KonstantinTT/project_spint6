import pandas as pd
import streamlit as st
import plotly.express as px
import urllib.request
from PIL import Image
from urllib.request import urlopen
    
data=pd.read_csv('vehicles_us.csv')
    
st.title('Choose your car')
st.subheader('Use this app to find the best car for your wants and needs')


## Display the image
urllib.request.urlretrieve('https://c7.alamy.com/comp/J388K0/used-cars-for-sale-north-carolina-usa-J388K0.jpg', "used-cars-for-sale-north-carolina-usa-J388K0.jpg")
image = Image.open("used-cars-for-sale-north-carolina-usa-J388K0.jpg")
st.image(image)
    
st.caption(':red[Choose your parameters here]')
   
 #  create a sidebars for user input   
#price slider
price_range = st.slider("Select desired price range", 
                            value=(1, 375000))
actual_range=list(range(price_range[0], price_range[1] + 1))

#odometer slider
odo_range = st.slider("Select desired mileage range?", 
                            value=(0, 990000))
actual_range=list(range(odo_range[0], odo_range[1] + 1))    
    
#type bar
type_range = st.multiselect("Select vehicle type", 
                            options=['SUV', 'bus', 'convertible', 'coupe', 'hatchback', 'mini-van', 'offroad', 'other', 'pickup', 'sedan', 'truck', 'van', 'wagon'],
                            default=['SUV', 'bus', 'convertible', 'coupe', 'hatchback', 'mini-van', 'offroad', 'other', 'pickup', 'sedan', 'truck', 'van', 'wagon'])
    
    
 #condition bar
condition_range = st.multiselect("Select vehicle condition",
                           options=['excellent', 'fair', 'good', 'like new', 'new', 'poor', 'salvage'],
                           default=['excellent', 'fair', 'good', 'like new', 'new', 'poor', 'salvage'])



fwd_check=st.checkbox('4 wheel drive') # checkbox for four wheel drive

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
        (data['price'].between(price_range[0], price_range[1])) &
        (data['condition'].isin(condition_range)) &
        (data['is_4wd'] == 1 if fwd_check else True)
    ]

    # Apply nan_unknown_check filter
    if nan_unknown_check:
        filtered_data = filtered_data.dropna(subset=[col for col in filtered_data.columns if col != 'paint_color'])
        filtered_data = filtered_data[~filtered_data[[col for col in filtered_data.columns if col != 'paint_color']].isin(['unknown', 'None', 'none']).any(axis=1)]
    
    # Display the filtered data
st.write("Filtered cars:", filtered_data)
    
    # Create a bars charts of the filtered data
st.write('Here are your options with a split by price and condition')
fig = px.bar(filtered_data, x='price', y='condition')
st.plotly_chart(fig)
    
st.write('Here are your options with a split by model_year and price')
    
fig2=px.scatter(filtered_data, x='model_year', y='price')
st.plotly_chart(fig2)

# Creating a top 10 recomended cars from filterd data    
st.write('Here is the list of recomended cars from selected list')
try:
    top_cars = filtered_data.nsmallest(10, ['price', 'odometer','model_year'])
    st.dataframe(top_cars)
except ValueError:
    st.write('No data available for the selected filters.')
