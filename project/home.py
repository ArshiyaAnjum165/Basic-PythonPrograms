import streamlit as st

# Add a title to the app
st.header("Sales Management")

st.write("##")
# Create two columns
col1, col2 = st.columns(2)

# Add text to the left column
col1.markdown("### Description")
col1.write("""
           Sales management software is a tool that aids sales reps
            in managing their sales operations. It's where they 
           record their day-to-day activities, keep track of their 
           pipelines, interact with their leads and prospects, 
           and much more. It also helps sales managers assign 
           leads, analyze individual rep performance, and make better decisions.
           Having such a system in place can be extremely 
           beneficial to your business, as it can help boost productivity,
            save time, improve collaboration, and—most importantly—save you money.
           """)

# Add an image to the right column
col2.image("C:/Users/Dell/Desktop/ayeesha/WhatsApp Image 2024-05-04 at 10.43.30.jpeg", width=500)