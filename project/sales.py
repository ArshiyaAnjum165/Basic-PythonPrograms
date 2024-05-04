import streamlit as st
import pandas as pd
import json

class InventoryManagementSystem:
    def __init__(self):
        self.inventory_file = 'inventory.json'
        self.load_inventory()
        self.revenue = 0
        self.expenditure = 0

    def load_inventory(self):
        try:
            with open(self.inventory_file, 'r') as file:
                data = json.load(file)
                self.inventory = data.get('inventory', [])
                self.revenue = data.get('revenue', 0)
                self.expenditure = data.get('expenditure', 0)
        except FileNotFoundError:
            self.inventory = []
            self.revenue = 0
            self.expenditure = 0

    def save_inventory(self):
        data = {'inventory': self.inventory, 'revenue': self.revenue, 'expenditure': self.expenditure}
        with open(self.inventory_file, 'w') as file:
            json.dump(data, file)

    def add_item(self, category, UID, name, color, size, quantity, price):
        for item in self.inventory:
            if item['category'] == category and item['UID'] == UID and item['name'] == name and item['color'] == color and item['size'] == size:
                item['quantity'] += quantity
                self.save_inventory()
                st.success("Item quantity updated successfully.")
                return
        self.inventory.append({'category': category, 'UID': UID, 'name': name, 'color': color,
                               'size': size, 'quantity': quantity, 'price': price})
        self.save_inventory()
        st.success("Item added to inventory.")

    def sell_item(self, category, UID, name, color, size, quantity):
        for item in self.inventory:
            if item['category'] == category and item['UID'] == UID and item['name'] == name \
                    and item['color'] == color and item['size'] == size:
                if item['quantity'] >= quantity:
                    item['quantity'] -= quantity
                    revenue_generated = quantity * item['price']
                    self.revenue += revenue_generated
                    self.expenditure += quantity * item['price']
                    self.save_inventory()
                    st.write(f"Sold {UID} {quantity} {size} {color} {name}(s).")
                    return
                else:
                    st.warning(f"Not enough {size} {color} {name}(s) available.")
                    return
        st.error("Item not found in inventory.")

    def remove_item(self, category, UID, name, color, size):
        for item in self.inventory:
            if item['category'] == category and item['UID'] == UID and item['name'] == name \
                    and item['color'] == color and item['size'] == size:
                self.inventory.remove(item)
                self.save_inventory()
                st.success("Item removed successfully.")
                return
        st.error("Item not found in inventory.")

    def remove_all_items(self):
        self.inventory = []
        self.save_inventory()
        st.success("All items removed from inventory.")

    def calculate_revenue(self, displayed_inventory):
        revenue = 0
        for item in displayed_inventory:
            revenue += item['quantity'] * item['price']
        return revenue

    def calculate_profit_loss(self, revenue, expenditure):
        return revenue - expenditure

# Initialize the Inventory Management System
ims = InventoryManagementSystem()

def display_inventory(inventory):
    if inventory:
        st.subheader('Inventory')
        df = pd.DataFrame(inventory)
        df.index += 1
        st.dataframe(df.style.format({'price': "${:.2f}"}))
    else:
        st.subheader('Inventory')
        st.write("Inventory is empty.")

# Streamlit app layout
st.title('Inventory Management System')

menu_choice = st.sidebar.selectbox('Menu', ['Add item', 'Sell item', 'Remove item', 'Remove all items', 'Display inventory', 'Calculate Profit/Loss'])

if menu_choice == 'Add item':
    st.subheader('Add Item to Inventory')
    category = st.text_input('Category')
    name = st.text_input('Name')
    UID = st.text_input('UID')
    color = st.text_input('Color')
    size = st.text_input('Size')
    quantity = st.number_input('Quantity', min_value=1, value=1)
    price = st.number_input('Price', min_value=0.01, step=0.01, format="%.2f")
    if st.button('Add'):
        ims.add_item(category, UID, name, color, size, quantity, price)

elif menu_choice == 'Sell item':
    st.subheader('Sell Item from Inventory')
    category = st.text_input('Category')
    name = st.text_input('Name')
    UID = st.text_input('UID')
    color = st.text_input('Color')
    size = st.text_input('Size')
    quantity = st.number_input('Quantity', min_value=1, value=1)
    if st.button('Sell'):
        ims.sell_item(category, UID, name, color, size, quantity)

elif menu_choice == 'Remove item':
    st.subheader('Remove Item from Inventory')
    category = st.text_input('Category')
    name = st.text_input('Name')
    UID = st.text_input('UID')
    color = st.text_input('Color')
    size = st.text_input('Size')
    if st.button('Remove'):
        ims.remove_item(category, UID, name, color, size)

elif menu_choice == 'Remove all items':
    st.subheader('Remove All Items from Inventory')
    if st.button('Remove All'):
        ims.remove_all_items()

elif menu_choice == 'Display inventory':
    ims.load_inventory()
    displayed_inventory = ims.inventory
    display_inventory(displayed_inventory)

elif menu_choice == 'Calculate Profit/Loss':
    ims.load_inventory()
    displayed_inventory = ims.inventory
    total_expenditure = st.number_input('Total Expenditure ($)', min_value=0.01, step=0.01, format="%.2f")
    total_revenue = ims.calculate_revenue(displayed_inventory)
    st.subheader('Financial Overview')
    st.write(f"Total Revenue: ${total_revenue}")
    st.write(f"Total Expenditure: ${total_expenditure}")
    if total_revenue >= total_expenditure:
        st.write(f"Profit: ${total_revenue - total_expenditure}")
    else:
        st.write(f"Loss: ${total_expenditure - total_revenue}")

st.write("Inventory data will be saved automatically when you close the app.")