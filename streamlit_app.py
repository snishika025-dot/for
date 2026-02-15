import streamlit as st
import pandas as pd
import numpy as np

# ---------------- Page Config ----------------
st.set_page_config(page_title="Tractor Sales Forecast Dashboard",
                   layout="wide")

st.title("🚜 Tractor Sales Forecast (2010–2015)")

# ---------------- Load Data ----------------
try:
    df = pd.read_csv("tractor_sales_smoothed.csv",
                     index_col="Month-Year",
                     parse_dates=True)
except FileNotFoundError:
    st.error("❌ Data file not found.")
    st.stop()

# ---------------- Filter 2010–2014 ----------------
df = df["2010":"2014"].copy()

# ---------------- Forecast for 2015 ----------------
df["Time"] = range(len(df))

X = df["Time"]
Y = df["Original Sales"]

coeff = np.polyfit(X, Y, 1)
trend_model = np.poly1d(coeff)

future_periods = 12
last_time = df["Time"].iloc[-1]

future_time = np.arange(last_time + 1, last_time + 1 + future_periods)
future_forecast = trend_model(future_time)

future_dates = pd.date_range(start="2015-01-01",
                             periods=12,
                             freq="MS")

# Create dynamic forecast table
forecast_df = pd.DataFrame({
    "Month": future_dates.strftime("%B"),
    "Year": future_dates.year,
    "Forecast Sales": future_forecast.round(2)
})

# ---------------- Display Section ----------------
st.markdown("## 📊 2015 Monthly Forecast (Dynamic)")

st.dataframe(forecast_df, use_container_width=True)

# ---------------- KPI Section ----------------
st.markdown("## 📌 Summary Metrics")

col1, col2 = st.columns(2)

avg_forecast = future_forecast.mean()
avg_actual = df["Original Sales"].mean()

col1.metric("🔮 Avg Forecast (2015)", round(avg_forecast, 2))

growth_percent = ((avg_forecast - avg_actual) / avg_actual) * 100
col2.metric("📈 Expected Growth %", round(growth_percent, 2))

st.success("✅ Dynamic Month-Year Forecast Generated Successfully!")
