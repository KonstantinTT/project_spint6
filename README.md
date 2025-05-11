# project_spint6

## Comments:
Replacing missing or unknown values in car listings with the average values from other listings may seem helpful for completing the dataset — but it can slightly distort the information, especially when you're trying to evaluate or compare a specific car.
For example:
If an individual car listing is missing its mileage or price, and you fill it with the average from all other listings, the car may appear more attractive or more typical than it actually is — which could lead to misleading conclusions during filtering or decision-making.

This kind of data imputation is useful for general analytics, but for precise filtering and recommendations, it’s often better to exclude incomplete or unknown entries to maintain data integrity and avoid bias.



https://github.com/KonstantinTT/project_spint6

https://project-spint6-4.onrender.com

## Step-by-step Guide

### Set Your Filters (on the left sidebar):
- **Price Range** – Use the slider to select your budget.
- **Mileage (Odometer) Range** – Choose how much mileage you're comfortable with.
- **Vehicle Type** – Select one or more types (SUV, sedan, truck, etc.).
- **Condition** – Choose the condition you're looking for (new, like new, fair, etc.).
- **4WD Only** – Check this box if you only want vehicles with four-wheel drive.
- **Exclude Unknown Values** – Check this box to remove listings with missing or unclear data (except paint color).
  - *Note:* This ensures cleaner results but may exclude some potentially relevant cars.

### View Filtered Results:
- After setting your filters, scroll down to the “Filtered Cars” section.
- You’ll see a table with all listings that match your criteria.

### Explore Visualizations:
- Graphs show price distribution, mileage trends, and the relationship between price, mileage, and model year.
- These help you understand the market and spot outliers or good deals.

### See Top 10 Recommendations:
- The app highlights 10 cars with the best combination of price, mileage, and model year.


## How to Run a Python Streamlit App Locally

The first of all checked than Python installed if not it can be downloaded from python.org

### **Step 1: Install Streamlit**
Open a terminal or command prompt and run:
```bash
pip install streamlit
```

### **Step 2: Navigate to Your App Folder**
Open your terminal and navigate to the folder where your app is located. For example:
```bash
cd C:\Users\<USERNAME>\Used_cars
```
(Replace `<USERNAME>` and the path with your actual folder path.)

### **Step 3: Run the App**
Make sure your script is named something like `app.py`. Then, use the following command to run the app:
```bash
streamlit run app.py
```

### **Step 4: Access the App**
Wait for the app to launch. Streamlit will start a local server and open the app in your browser at:
```
http://localhost:8501
```

### **Optional: Change the Port**
If port `8501` is busy, you can specify a different port:
```bash
streamlit run app.py --server.port 8502
```

### **If the Browser Doesn't Open Automatically**
Manually open your browser and go to:
```
http://localhost:8501
```



T



