import streamlit as st
import datetime
import requests


# Page configuration
st.set_page_config(
    page_title="NY taxi fare", # => Quick reference - Streamlit
    page_icon="🚕",
    layout="centered", # wide
    initial_sidebar_state="auto") # collapsed



'''
# NY Taxi fare
'''



col_dates = st.columns(2)
# Date
d = str(col_dates[0].date_input(
    "Date",
    datetime.date(2025, 3, 14)))

# Time
t = str(col_dates[1].time_input(
    'Time',
    datetime.time(8, 45)))

columns_loc = st.columns(4)
# Pickup longitude
pickup_lon = columns_loc[0].number_input("Pickup longitude", key="picklon")
# Pickup latitude
pickup_lat = columns_loc[1].number_input("Pickup latitude", key="picklat")
# Dropoff longitude
dropoff_lon = columns_loc[2].number_input("Dropoff longitude", key="droplon")
# Dropoff latitude
dropoff_lat = columns_loc[3].number_input("Dropoff latitude", key="droplat")
# Passenger count
passengers = st.slider("Passengers",
                       1,10,3)


url = 'https://taxifare-159853074849.europe-west1.run.app/predict'


if st.button("Price", icon="🚖"):
    #2. Let's build a dictionary containing the parameters for our API...
    params = {
        "pickup_datetime": d + " " + t,
        "pickup_longitude": pickup_lon,
        "pickup_latitude": pickup_lat,
        "dropoff_longitude": dropoff_lon,
        "dropoff_latitude": dropoff_lat,
        "passenger_count": passengers
    }

    #3. Let's call our API using the `requests` package...
    response = requests.get(url, params=params)

    #4. Let's retrieve the prediction from the **JSON** returned by the API...
    fare = response.json()["fare"]

    ## Finally, we can display the prediction to the user
    st.write(f"""
    Fare is {fare}
    """)
