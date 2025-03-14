import streamlit as st
import datetime
import requests
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="NY taxi fare", # => Quick reference - Streamlit
    page_icon="🚕",
    layout="centered", # wide
    initial_sidebar_state="auto") # collapsed



def get_map_data():

    return pd.DataFrame({
        "lat": np.array([pickup_lat, dropoff_lat]),
        "lon": np.array([pickup_lon, dropoff_lon]),
        "color": np.array(["#5ce488", "#e60f05"])
    })


'''
### 🚖 NY Taxi fare
'''
# Displaying
col_dates = st.columns(2)
# Date
d = str(col_dates[0].date_input(
    "Date",
    datetime.date(2025, 3, 14)))

# Time
t = str(col_dates[1].time_input(
    'Time',
    datetime.time(8, 45)))

columns_addresses = st.columns(2)
pickup_address = f"{columns_addresses[0].text_input('Pickup location', value='Times Square')} new york"
dropoff_address = f"{columns_addresses[1].text_input('Dropoff location', value='Central Park')} new york"


# Passenger count
passengers = st.slider("Passengers",
                       1,8,3)



# Calling the API and fetching fare prediction
url_fare = 'https://taxifare-159853074849.europe-west1.run.app/predict'
url_loc = "https://nominatim.openstreetmap.org/search.php"

if st.button("Price", icon="💲"):

    #1. Let's get the localisations for pickup
    params_loc_pickup = {
        "q": pickup_address,
        "format": "jsonv2"
    }
    headers = {
    "User-Agent": "Simonf/Myapp"
    }
    response_loc_pickup = requests.get(url_loc, params=params_loc_pickup, headers=headers).json()[0]
    pickup_lon = float(response_loc_pickup["boundingbox"][2])
    pickup_lat = float(response_loc_pickup["boundingbox"][0])
    # and for dropoff
    params_loc_dropoff = {
        "q": dropoff_address,
        "format": "jsonv2"
    }
    response_loc_dropoff = requests.get(url_loc, params=params_loc_dropoff, headers=headers).json()[0]
    dropoff_lon = float(response_loc_dropoff["boundingbox"][2])
    dropoff_lat = float(response_loc_dropoff["boundingbox"][0])

    #2. Let's build a dictionary containing the parameters for our API...
    params_fare = {
        "pickup_datetime": d + " " + t,
        "pickup_longitude": pickup_lon,
        "pickup_latitude": pickup_lat,
        "dropoff_longitude": dropoff_lon,
        "dropoff_latitude": dropoff_lat,
        "passenger_count": passengers
    }

    #3. Let's call our API using the `requests` package...
    response_fare = requests.get(url_fare, params=params_fare)

    #4. Let's retrieve the prediction from the **JSON** returned by the API...
    fare = round(response_fare.json()["fare"],2)

    ## Finally, we can display the prediction to the user
    st.markdown(f"""
    # $ {fare}
    """)

    # Displaying locations on a map
    df = get_map_data()
    st.map(df, color="color", size=50)
