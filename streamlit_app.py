import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AI Smart Home Energy Saver", layout="wide")

st.title("🌱 AI Smart Home Energy Saver")
st.write("AI for Sustainability Project - 1M1B Internship")

name = st.text_input("Name", "Raj Yadav")
city = st.text_input("City", "Agra")
hh_size = st.slider("Household Size", 1, 10, 4)
rate_peak = st.number_input("Electricity Rate (₹/kWh)", value=8.0)

appliances = st.multiselect(
    "Select Appliances",
    [
        "air_conditioning",
        "heater",
        "fridge",
        "washing_machine",
        "lights",
        "computer",
        "tv",
        "microwave",
        "oven",
        "dishwasher"
    ],
    default=["air_conditioning", "fridge"]
)
if st.button("Generate AI Sustainability Plan"):
    payload = {
        "name": name,
        "city": city,
        "hh_size": hh_size,
        "rate_peak": rate_peak,
        "appliances_present": appliances
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/optimize-energy",
            json=payload
        )

        plan = response.json()

        st.success(plan["summary"])

        st.subheader("📊 AI Forecast Results")

        if plan["actions"]:
            df = pd.DataFrame(plan["actions"])

            # show full prediction table
            st.dataframe(df, use_container_width=True)

            # total predicted usage
            total_predicted = df["predicted_usage_kwh"].sum()

            # metrics
            col1, col2, col3 = st.columns(3)

            col1.metric("Predicted Usage (kWh)", round(total_predicted, 2))
            col2.metric("Potential Savings (kWh)", plan["total_estimated_kwh_saving"])
            col3.metric("Money Saved (₹)", plan["total_estimated_cost_saving"])

            # CO2 reduction
            co2_saved = round(plan["total_estimated_kwh_saving"] * 0.82, 2)
            st.metric("CO₂ Reduced (kg)", co2_saved)

            # bar chart for prediction visualization
            st.subheader("📈 Predicted Energy Usage by Appliance")
            st.bar_chart(df.set_index("appliance")["predicted_usage_kwh"])

        st.info("This AI plan helps reduce electricity consumption and carbon emissions, supporting sustainable living and SDG 7 (Affordable and Clean Energy).")

    except Exception as e:
        st.error(f"Backend not running: {e}")