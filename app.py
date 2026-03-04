import streamlit as st
import fastf1
import matplotlib.pyplot as plt
import os

# Create cache folder
os.makedirs("cache", exist_ok=True)
fastf1.Cache.enable_cache("cache")

st.title("🏎 F1 Telemetry Dashboard")

year = st.selectbox("Season", [2021, 2022, 2023])
race = st.text_input("Race Name", "Monza")

driver1 = st.text_input("Driver 1 (VER, HAM, LEC)", "VER")
driver2 = st.text_input("Driver 2 (optional)", "")

if st.button("Load Telemetry"):

    session = fastf1.get_session(year, race, 'Q')
    session.load()

    lap1 = session.laps.pick_driver(driver1).pick_fastest()
    tel1 = lap1.get_car_data().add_distance()

    fig, ax = plt.subplots(3, 1, figsize=(10,10))

    # Speed
    ax[0].plot(tel1["Distance"], tel1["Speed"], label=driver1)
    ax[0].set_title("Speed")
    ax[0].set_ylabel("km/h")

    # Throttle
    ax[1].plot(tel1["Distance"], tel1["Throttle"], label=driver1)
    ax[1].set_title("Throttle")

    # Brake
    ax[2].plot(tel1["Distance"], tel1["Brake"], label=driver1)
    ax[2].set_title("Brake")
    ax[2].set_xlabel("Distance")

    if driver2 != "":
        lap2 = session.laps.pick_driver(driver2).pick_fastest()
        tel2 = lap2.get_car_data().add_distance()

        ax[0].plot(tel2["Distance"], tel2["Speed"], label=driver2)
        ax[0].legend()

    st.pyplot(fig)