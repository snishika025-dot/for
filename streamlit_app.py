import streamlit as st
import pandas as pd
import numpy as np

# ---------------- Page Config ----------------
st.set_page_config(page_title="Tractor Sales Forecast Dashboard",
                   layout="wide")

st.title("🚜 Dynamic Tractor Sales Forecast")

# ---------------- Load Data ----------------
try:
    df = pd.read_csv("tractor_sales_smoothed.csv",
                     index_col="Month-Year",
                     parse_dates=True)
except FileNotFoundError:
    st.error("❌ Data file not found.")
    st.stop()

# ---------------- Sidebar Options ----------------
st.sidebar.header("📅 Forecast Settings")

forecast_year = st.sidebar.number_input(
    "Select Forecast Year",
    min_value=2010,
    max_value=2035,
    value=2015
)

month_list = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

selected_month = st.sidebar.selectbox(
    "Select Forecast Month",
    month_list
)

# ---------------- Prepare Historical Data ----------------
historical_df = df[str(df.index.year.min()):str(forecast_year - 1)].copy()

historical_df["Time"] = range(len(historical_df))

X = historical_df["Time"]
Y = historical_df["Original Sales"]

coeff = np.polyfit(X, Y, 1)
trend_model = np.poly1d(coeff)

# ---------------- Forecast 12 Months ----------------
future_periods = 12
last_time = historical_df["Time"].iloc[-1]

future_time = np.arange(last_time + 1,
                        last_time + 1 + future_periods)

future_forecast = trend_model(future_time)

future_dates = pd.date_range(
    start=f"{forecast_year}-01-01",
    periods=12,
    freq="MS"
)

forecast_df = pd.DataFrame({
    "Month": future_dates.strftime("%B"),
    "Year": future_dates.year,
    "Forecast Sales": future_forecast.round(2)
})

# ---------------- Get Selected Month Forecast ----------------
result = forecast_df[
    (forecast_df["Month"] == selected_month) &
    (forecast_df["Year"] == forecast_year)
]

if not result.empty:
    forecast_value = result["Forecast Sales"].values[0]

    st.markdown("## 📊 Forecast Result")

    st.metric(
        label=f"🚜 Forecast for {selected_month} {forecast_year}",
        value=forecast_value
    )

else:
    st.warning("⚠ No forecast data available.")

st.success("✅ Dynamic Month & Year Forecast Generated!")
