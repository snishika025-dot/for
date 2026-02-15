import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Tractor Sales Dashboard",
                   layout="wide")

# ---------- Custom Professional Theme ----------
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to right, #1f4037, #99f2c8);
    }
    .stMetric {
        background-color: rgba(255,255,255,0.15);
        padding: 15px;
        border-radius: 12px;
        text-align: center;
    }
    h1, h2, h3 {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚜 Tractor Sales Forecast Dashboard")

# ---------- Load Data ----------
try:
    df = pd.read_csv("tractor_sales_smoothed.csv",
                     index_col="Month-Year",
                     parse_dates=True)
except FileNotFoundError:
    st.error("❌ Data file not found.")
    st.stop()

# ---------- Sidebar ----------
st.sidebar.header("📅 Filter Options")

start_date = st.sidebar.date_input("Start Date", df.index.min())
end_date = st.sidebar.date_input("End Date", df.index.max())

df_filtered = df.loc[start_date:end_date].copy()

# ---------- Forecast ----------
df_filtered["Forecast"] = df_filtered["Original Sales"].rolling(3).mean()

# ---------- KPI Section ----------
st.markdown("## 📊 Sales Overview")

col1, col2, col3 = st.columns(3)

col1.metric("📈 Latest Sales",
            int(df_filtered["Original Sales"].iloc[-1]))

col2.metric("📊 Average Sales",
            round(df_filtered["Original Sales"].mean(), 2))

col3.metric("🔮 Forecast (Next Est.)",
            round(df_filtered["Forecast"].iloc[-1], 2))

# ---------- Chart ----------
st.markdown("## 📈 Trend Analysis")

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df_filtered["Original Sales"], label="Original Sales")
ax.plot(df_filtered["Smoothed Sales"], label="Smoothed Sales")
ax.plot(df_filtered["Forecast"], label="Forecast (3M MA)", linestyle="--")

ax.set_title("Tractor Sales Forecast Analysis")
ax.set_xlabel("Month-Year")
ax.set_ylabel("Sales Volume")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# ---------- Summary ----------
st.markdown("""
## 🔎 Executive Summary

✅ Clear upward growth trend  
🔁 Strong seasonal pattern  
🔮 Moving average forecast gives short-term prediction  
📊 Suitable for business planning & inventory management  

---
Developed with Streamlit | MBA Business Analytics Project
""")
