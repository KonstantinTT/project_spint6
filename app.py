import pandas as pd
import streamlit as st
import plotly.express as px
import urllib.request
from PIL import Image
from urllib.request import urlopen
    
data=pd.read_csv('vehicles_us.csv')
    
st.title('Choose your car')
st.subheader('Use this app to find the best car for your wants and needs')



urllib.request.urlretrieve('https://c7.alamy.com/comp/J388K0/used-cars-for-sale-north-carolina-usa-J388K0.jpg', "used-cars-for-sale-north-carolina-usa-J388K0.jpg")
image = Image.open("used-cars-for-sale-north-carolina-usa-J388K0.jpg")
st.image(image)
    
st.caption(':red[Choose your parameters here]')
   
   
price_range = st.slider("What is your price range?",
                            value=(1, 375000))
actual_range=list(range(price_range[0], price_range[1] + 1))

odo_range = st.slider("What is your odometer range?",
                            value=(0, 990000))
actual_range=list(range(odo_range[0], odo_range[1] + 1))    
    
type_range = st.multiselect("What is your type?",
                            options=['SUV', 'bus', 'convertible', 'coupe', 'hatchback', 'mini-van', 'offroad', 'other', 'pickup', 'sedan', 'truck', 'van', 'wagon'],
                            default=['SUV'])
    
    
condition_range = st.multiselect("What is your condition?",
                           options=['excellent', 'fair', 'good', 'like new', 'new', 'poor', 'salvage'],
                           default=['excellent', 'good'])

##st.write("Selected conditions:", condition_range)

fwd_check=st.checkbox('4 wheel drive')

if fwd_check:
    filtered_data=data[data.is_4wd.isin(actual_range)]
    filtered_data=filtered_data[filtered_data.is_4wd=='1']
else:
    filtered_data=data[data.is_4wd.isin(actual_range)]
    # Filter the data based on user input
filtered_data = data[
     (data['type'].isin(type_range)) &
     (data['price'].between(price_range[0], price_range[1])) &
     (data['condition'].isin(condition_range)&
      (data['is_4wd'] == 1 if fwd_check else True))]
    
    # Display the filtered data
st.write("Filtered Data:", filtered_data)
    
    # Create a bar chart of the filtered data
fig = px.bar(filtered_data, x='price', y='condition')
st.plotly_chart(fig)
    
st.write('Here are your options with a split by price and condition')
    
fig2=px.scatter(filtered_data, x='price', y='condition')
st.plotly_chart(fig2)
    
#st.write('Here is the list of reccomended cars')
#try:
#    st.dataframe(filtered_data.sample(40))
#except ValueError:
#    st.write('No data available for the selected filters.')

st.write('Here is the list of reccomended cars include used filters')
#st.write('Here is the list of reccomended cars')
#try:
#    st.dataframe(filtered_data.sample(40))
#except ValueError:
#    st.write('No data available for the selected filters.')

st.write('Here is the list of reccomended cars include used filters')
try:
    top_10_avg_price = filtered_data.nsmallest(10, 'price')['price'].mean()
    top_10_avg_odometer = filtered_data.nsmallest(10, 'odometer')['odometer'].mean()

    st.write(f"Average price of top 10 cheapest cars: ${top_10_avg_price:.2f}")
    st.write(f"Average odometer of top 10 cars with lowest mileage: {top_10_avg_odometer:.2f} miles")
    
except ValueError:
    st.write('No data available for the selected filters.')
