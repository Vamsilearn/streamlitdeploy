import streamlit as st
import requests
import json

# Retrieve the endpoint URL and API key from Streamlit secrets.
endpoint_url = st.secrets["ENDPOINT_URL"]
api_key = st.secrets["ENDPOINT_API_KEY"]

# Add a welcoming title and description
st.title("House Price Checker")
st.write("Welcome to the House Price Checker! Enter the property details below to get your estimated price.")

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
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer " + api_key
    }
    
    # Send the POST request to the endpoint
    response = requests.post(endpoint_url, headers=headers, data=body)
    
    if response.status_code == 200:
        try:
            # Parse the response (handle double-encoded JSON if needed)
            result = json.loads(response.text)
            if isinstance(result, str):
                result = json.loads(result)
            prediction = result.get('prediction')
            st.success(f"Your estimated price is: {prediction}")
        except Exception as e:
            st.error("Error parsing the response")
            st.write(response.text)
            st.write(str(e))
    else:
        st.error(f"Error: {response.status_code}")
        st.write(response.text)
