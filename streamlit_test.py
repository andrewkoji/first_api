import streamlit as st
import requests
import numpy as np
import streamlit.components.v1 as components
import asyncio
import re
import pandas as pd

df = pd.read_excel('period1grades.xlsx').sort_values(by='MP3 Test (1x)')
print(df)