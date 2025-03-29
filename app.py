import streamlit as st
import requests
import json

# Retrieve the endpoint URL and API key from Streamlit secrets.
# In Streamlit Community Cloud, you can set these in the secrets.toml file.
endpoint_url = st.secrets["ENDPOINT_URL"]
api_key = st.secrets["ENDPOINT_API_KEY"]

st.title("Real Estate Price Prediction")
st.write("Enter the property details below:")

# Create input fields
square_feet = st.number_input("Square Feet", value=1200)
num_bedrooms = st.number_input("Number of Bedrooms", value=3)
num_bathrooms = st.number_input("Number of Bathrooms", value=2)
num_floors = st.number_input("Number of Floors", value=1)
year_built = st.number_input("Year Built", value=2000)
has_garden = st.selectbox("Has Garden", [0, 1])
has_pool = st.selectbox("Has Pool", [0, 1])
garage_size = st.number_input("Garage Size", value=1)
location_score = st.number_input("Location Score", value=80)
distance_to_center = st.number_input("Distance to Center", value=5)

# When the user clicks Predict, send the data to your endpoint
if st.button("Predict"):
    # Create the JSON payload from the input data
    data = {
        "Square_Feet": square_feet,
        "Num_Bedrooms": num_bedrooms,
        "Num_Bathrooms": num_bathrooms,
        "Num_Floors": num_floors,
        "Year_Built": year_built,
        "Has_Garden": has_garden,
        "Has_Pool": has_pool,
        "Garage_Size": garage_size,
        "Location_Score": location_score,
        "Distance_to_Center": distance_to_center
    }
    body = json.dumps(data)
    
    # Prepare headers with key-based authentication.
    # We use "Bearer" followed by the API key.
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer " + api_key
    }
    
    # Send the POST request to the endpoint
    response = requests.post(endpoint_url, headers=headers, data=body)
    
    # Process and display the response
    if response.status_code == 200:
    # Instead of using response.json(), try:
        result = json.loads(response.text)
        st.write("Type of result:", type(result))  # Debug: should show <class 'dict'>
        st.success(f"Prediction: {result.get('prediction')}")
    else:
        st.error(f"Error: {response.status_code}")
        st.write(response.text)

