import streamlit as st
import requests
import numpy as np
import streamlit.components.v1 as components
import asyncio
import re
import pandas as pd

st.title('LINEAR-QUADRATIC SYSTEMS')
st.write('This is a table of the quadratic function')
st.latex('f(x) = x^2')

# Create the first column
first_column = list(np.arange(-50, 50))

# Create the DataFrame
df = pd.DataFrame({
    'x': first_column,
    'f(x)': [x ** 2 for x in first_column]  # Calculate the square of each value in first_column
})

# Reset the index to start at x = 0
df = df.reset_index(drop=True)  # Reset the index to ensure smooth scrolling

st.dataframe(df)