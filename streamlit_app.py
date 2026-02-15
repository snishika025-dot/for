import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

st.title("🚜 Tractor Sales Forecast Dashboard")

# Load data
try:
    df = pd.read_csv("tractor_sales_smoothed.csv", 
                     index_col="Month-Year", 
                     parse_dates=True)
except FileNotFoundError:
    st.error("❌ Data file not found. Please upload 'tractor_sales_smoothed.csv'")
    st.stop()

# Sidebar Filters
st.sidebar.header("📅 Filter Options")

start_date = st.sidebar.date_input("Start Date", df.index.min())
end_date = st.sidebar.date_input("End Date", df.index.max())

# Filter Data
df_filtered = df.loc[start_date:end_date]

st.write("### 📊 Data Preview")
st.dataframe(df_filtered.head())

# Forecast Calculation (Simple Example: 3 Month Moving Average)
df_filtered["Forecast"] = df_filtered["Original Sales"].rolling(3).mean()

st.write("### 📈 Original vs Smoothed vs Forecast")

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df_filtered["Original Sales"], label="Original Sales")
ax.plot(df_filtered["Smoothed Sales"], label="Smoothed Sales")
ax.plot(df_filtered["Forecast"], label="Forecast (3M MA)", linestyle="--")

ax.set_title("🚜 Tractor Sales Forecast Analysis")
ax.set_xlabel("Month-Year")
ax.set_ylabel("Sales Volume")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# Key Metrics
st.write("### 📌 Key Insights")

col1, col2, col3 = st.columns(3)

col1.metric("📈 Latest Sales", int(df_filtered["Original Sales"].iloc[-1]))
col2.metric("📊 Average Sales", round(df_filtered["Original Sales"].mean(), 2))
col3.metric("🔮 Forecast Value", round(df_filtered["Forecast"].iloc[-1], 2))

st.success("✅ Dashboard updated dynamically based on selected date range!")

st.markdown("""
### 🔎 Summary

- 🚀 Strong upward trend observed  
- 🔄 Seasonal fluctuations visible  
- 🔮 Forecast provides short-term prediction using moving average  
- 📊 Model captures demand pattern effectively  

This dynamic dashboard allows interactive sales analysis.
""")
