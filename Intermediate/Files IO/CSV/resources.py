import pandas as pd
import requests
from io import StringIO

url = "https://raw.githubusercontent.com/cs109/2014_data/master/countries.csv"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers, timeout=30)

# Raise an error if the HTTP request fails
response.raise_for_status()

# Read the CSV data into a DataFrame
data = StringIO(response.text)
df = pd.read_csv(data)

# Display the first five rows
print(df.head())
