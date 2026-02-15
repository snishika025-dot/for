
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

st.title('Tractor Sales: Original vs. Exponential Smoothing')

# Load the combined data
try:
    df_combined = pd.read_csv('tractor_sales_smoothed.csv', index_col='Month-Year', parse_dates=True)
except FileNotFoundError:
    st.error("Error: 'tractor_sales_smoothed.csv' not found. Please ensure the data file is in the same directory as the app.")
    st.stop()

st.write("### Data Preview")
st.dataframe(df_combined.head())

st.write("### Original vs. Smoothed Tractor Sales")

# Plotting the data
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df_combined['Original Sales'], label='Original Sales')
ax.plot(df_combined['Smoothed Sales'], label='Smoothed Sales', color='red', linestyle='--')
ax.set_title('Tractor Sales: Original vs. Exponential Smoothing Fitted Values')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Tractors Sold')
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.write("### Summary of Findings")
st.markdown("""
The plot above visualizes the monthly tractor sales data from 2003 to 2014, along with the exponentially smoothed fitted values. 
Key observations:

*   **Upward Trend**: There is a clear and consistent upward trend in tractor sales over the years, indicating market growth.
*   **Strong Seasonality**: A prominent seasonal pattern is evident, with sales peaking during certain months and dipping in others within each year. The exponential smoothing model effectively captures these recurring fluctuations.
*   **Model Fit**: The smoothed sales line closely follows the original data, demonstrating that the Exponential Smoothing model (with multiplicative trend and seasonality) provides a good representation of the underlying patterns.

This analysis highlights the dynamic nature of tractor sales, driven by both long-term market expansion and predictable seasonal demand.
""")
