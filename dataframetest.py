import pandas as pd
import warnings
warnings.simplefilter("ignore", UserWarning)

df = pd.read_excel('gradereport.xlsx')

print(df.head())