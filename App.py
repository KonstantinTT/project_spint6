import pandas as pd
import streamlit as st
import plotly.express as px
    
    data=pd.read_csv('vehicles_us.csv')
    import plotly.express as px
    
    import streamlit as st
    
    st.title('Choose your car')
    st.subheader('Use this app to find the best car for your wants and needs')
    
    
  import urllib.request
  from PIL import Image
    
  urllib.request.urlretrieve("\\Users\Alex\project_spint6\project_spint6\1036511252.jpg")
  image = Image.open("1036511252.jpg")
    
  st.Image(img)
    
    st.caption(':red[Choose your parameters here]')
   
   
    price_range = st.slider("What is your price range?",
                            value=(1, 375000))
    actual_range=list(range(price_range[0], price_range[1])+1)
    
    
    type_range = st.slider("What is your type?",
                            value=('SUV', 'bus','convertible', 'coupe', 'hatchback', 'mini-van','offroad', 'other', 'pickup', 'sedan', 'truck', 'van','wagon'))
    
    
  condition_checkbox = st.checkbox("What is your condition?",
                            value=('excellent', 'fair', 'good', 'like new', 'new', 'poor', 'salvage'))
    condition_range = st.multiselect("Select the conditions you want to include:", options=condition_checkbox, default=condition_checkbox)
   
    st.write("Selected conditions:", condition_range)
    
    # Filter the data based on user input
    filtered_data = data[
        (data['type'].isin(type_range)) &
        (data['price'].between(price_range[0], price_range[1])) &
        (data['condition'].isin(condition_range))
    ]
    
    # Display the filtered data
    st.write("Filtered Data:", filtered_data)
    
    # Create a bar chart of the filtered data
    fig = px.bar(filtered_data, x='make', y='price', color='condition')
    st.plotly_chart(fig)
    
    st.write('Here are your options with a split by price and condition')
    
    fig=px.scatter(filtered_data, x='price', y='condition')
    sp.plotly_chart(fig2)
    
    st.write('Here is the list of reccomended cars')
    st.dataframe(filtered_data.sample(40))
    