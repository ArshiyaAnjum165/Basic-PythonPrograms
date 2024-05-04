import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt

# Dummy data for sport merchandise invoices
invoices = []
for i in range(50):
    category = random.choice(["t-shirt", "Shoes", "bags"])
    name = random.choice(["NIKE", "Sketchers", "Puma"])
    UID = random.choice(["N001", "S002", "P003"])
    color = random.choice(["Blue", "Black", "Silver"])
    size = random.choice(["M", "10", "N/A"])
    quantity = random.randint(1, 10)
    # Introduce some variability in price to create curves in profit and loss
    price = random.uniform(10.0 + i * 2, 100.0 + i * 5)
    invoices.append({'Category': category, 'Name': name, 'UID': UID, 'Color': color, 'Size': size, 'Quantity': quantity, 'Price': price})

# Convert the invoices to a DataFrame
invoices_df = pd.DataFrame(invoices)

# Function to calculate revenue
def calculate_revenue(invoices_df):
    invoices_df = pd.DataFrame(invoices).copy()
    invoices_df.loc[:, 'Total'] = invoices_df['Quantity'] * invoices_df['Price']

    revenue = invoices_df['Total'].sum()
    return revenue

# Function to calculate profit or loss
def calculate_profit_loss(revenue, expenditure):
    return revenue - expenditure

# Sample expenditure data
expenditure = 1500

# Calculate revenue and profit/loss for weekly basis only
weekly_revenue = []
weekly_profit_loss = []

# Slider to select the number of weeks
num_weeks = st.slider('Select number of weeks', min_value=1, max_value=len(invoices_df) // 7, value=4)

for i in range(0, num_weeks * 7, 7):
    weekly_invoices_df = invoices_df[i:i+7]
    weekly_revenue.append(calculate_revenue(weekly_invoices_df) + random.uniform(-100, 100))  # Add random variability
    weekly_profit_loss.append(calculate_profit_loss(weekly_revenue[-1], expenditure) + random.uniform(-50, 50))  # Add random variability

# Create a Streamlit app
st.title("Sport Merchandise Invoices Analysis")

# Display the invoices DataFrame
st.write("Invoices Data")
st.write(invoices_df)

# Display the weekly revenue and profit/loss graphs
st.write("Weekly Revenue and Profit/Loss")
fig, ax = plt.subplots(2, 1, figsize=(12, 6))
weeks = range(1, num_weeks+1)
ax[0].plot(weeks, weekly_revenue, marker='o')
ax[0].set_title('Weekly Revenue')
ax[0].set_xlabel('Weeks')
ax[0].set_ylabel('Revenue')

ax[1].plot(weeks, weekly_profit_loss, marker='o')
ax[1].set_title('Weekly Profit/Loss')
ax[1].set_xlabel('Weeks')
ax[1].set_ylabel('Profit/Loss')

st.pyplot(fig)