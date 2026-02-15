import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
# Create time index
df["Time"] = range(len(df))

X = df["Time"]
Y = df["Original Sales"]

# Linear regression trend model
coeff = np.polyfit(X, Y, 1)
trend_model = np.poly1d(coeff)

# Forecast next 12 months (2015)
future_periods = 12
last_time = df["Time"].iloc[-1]

future_time = np.arange(last_time + 1, last_time + 1 + future_periods)
future_forecast = trend_model(future_time)

# Create 2015 monthly dates
future_dates = pd.date_range(start="2015-01-01",
                             periods=12,
                             freq="MS")

forecast_df = pd.DataFrame({
    "Original Sales": np.nan,
    "Smoothed Sales": np.nan,
    "Forecast": future_forecast
}, index=future_dates)

# Add forecast column to historical data
df["Forecast"] = np.nan

# Combine historical + forecast
df_final = pd.concat([df.drop(columns="Time"), forecast_df])

# ---------------- KPI Section ----------------
st.markdown("## 📊 Key Metrics (2010–2015)")

col1, col2, col3 = st.columns(3)

col1.metric("📈 Avg Sales (2010–2014)",
            round(df["Original Sales"].mean(), 2))

col2.metric("🔮 Avg Forecast (2015)",
            round(future_forecast.mean(), 2))

col3.metric("📊 Growth Projection %",
            round(((future_forecast.mean() - df["Original Sales"].mean())
                   / df["Original Sales"].mean()) * 100, 2))

# ---------------- Chart ----------------
st.markdown("## 📈 Historical vs Forecast")

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df_final["Original Sales"], label="Original Sales")
ax.plot(df_final["Smoothed Sales"], label="Smoothed Sales")
ax.plot(df_final["Forecast"], linestyle="--", label="2015 Forecast")

# Forecast separation line
ax.axvline(pd.to_datetime("2015-01-01"),
           color="black",
           linestyle=":",
           label="Forecast Start (2015)")

ax.set_title("🚜 Tractor Sales: 2010–2015 Forecast")
ax.set_xlabel("Year")
ax.set_ylabel("Sales Volume")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# ---------------- Executive Summary ----------------
st.markdown("""
## 🔎 Executive Summary

📈 Historical data from 2010–2014 shows consistent upward growth.  
🔁 Seasonal fluctuations are visible across years.  
🔮 2015 forecast is generated using linear trend projection.  
📊 Model indicates continued expansion in tractor demand.  

This forecast can support production planning and inventory decisions.
""")
