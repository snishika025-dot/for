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

# ---------------- Sidebar Forecast Year Selection ----------------
st.sidebar.header("📅 Forecast Settings")

forecast_year = st.sidebar.number_input(
    "Select Forecast Year",
    min_value=2010,
    max_value=2030,
    value=2015
)

# ---------------- Use Historical Data Until Previous Year ----------------
historical_df = df[str(df.index.year.min()):str(forecast_year - 1)].copy()

# ---------------- Build Forecast Model ----------------
historical_df["Time"] = range(len(historical_df))

X = historical_df["Time"]
Y = historical_df["Original Sales"]

coeff = np.polyfit(X, Y, 1)
trend_model = np.poly1d(coeff)

# Forecast 12 months
future_periods = 12
last_time = historical_df["Time"].iloc[-1]

future_time = np.arange(last_time + 1,
                        last_time + 1 + future_periods)

future_forecast = trend_model(future_time)

# Create Future Dates
future_dates = pd.date_range(
    start=f"{forecast_year}-01-01",
    periods=12,
    freq="MS"
)

# ---------------- Create Dynamic Forecast Table ----------------
forecast_df = pd.DataFrame({
    "Month": future_dates.strftime("%B"),
    "Year": future_dates.year,
    "Forecast Sales": future_forecast.round(2)
})

# ---------------- Display Forecast ----------------
st.markdown(f"## 📊 Monthly Forecast for {forecast_year}")

st.dataframe(forecast_df, use_container_width=True)

# ---------------- KPI Section ----------------
st.markdown("## 📌 Forecast Summary")

col1, col2 = st.columns(2)

avg_forecast = future_forecast.mean()
avg_actual = historical_df["Original Sales"].mean()

col1.metric("🔮 Avg Forecast", round(avg_forecast, 2))

growth_percent = ((avg_forecast - avg_actual) / avg_actual) * 100
col2.metric("📈 Expected Growth %", round(growth_percent, 2))

st.success(f"✅ Forecast for {forecast_year} Generated Dynamically!")
