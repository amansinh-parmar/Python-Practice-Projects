import pandas as pd

df = pd.read_csv("daily_routine.csv")
# print(df)

header = df.head()      # First 5 rows
column = df.columns     # Column names
shape = df.shape        # Rows, Columns
print(shape)
