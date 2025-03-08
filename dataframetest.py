import pandas as pd
import warnings
warnings.simplefilter("ignore", UserWarning)

df = pd.read_excel('gradereport.xlsx')




print(df.head().to_json(orient="records", indent=4))

# print(df.head())