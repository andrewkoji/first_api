import pandas as pd
import numpy as np
import requests 
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('screen_time.csv').head(20).sort_values(by='Average Screen Time (hours)')
st.write("Average Screen Time (hours)")
st.write("", ", ".join(map(str, df['Average Screen Time (hours)'].tolist())))
STATS = df['Average Screen Time (hours)'].describe().reset_index()
STATS.columns = ['Stats', 'Value']
STATS['Value'] = STATS['Value'].round(2)
STATS['Stats'] = STATS['Stats'].replace({
    'count': 'Count',
    'mean': 'Mean',
    'std': 'Standard Deviation',
    'min': 'Minimum',
    '25%': 'Q1',
    '50%': 'Median',
    '75%': 'Q3',
    'max': 'Maximum'
})
st.dataframe(STATS)

# Plot a bell curve
st.write("Bell Curve of Average Screen Time (hours)")
mean = df['Average Screen Time (hours)'].mean()
std = df['Average Screen Time (hours)'].std()

# Generate data for the bell curve
x = np.linspace(mean - 4*std, mean + 4*std, 100)
y = (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std) ** 2)

# Plot using matplotlib
fig, ax = plt.subplots()