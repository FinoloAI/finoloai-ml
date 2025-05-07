import pandas as pd
import numpy as np
import os

# Path to your folder with CSV files
folder_path = r'C:\Users\ANWESHA\OneDrive\Documents\A_FinalYrProj\Financial portfolio\finoloai-ml\Data'  # replace with your path

vol_dict = {}

# Loop through CSVs
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        stock = filename.replace('.csv', '')
        df = pd.read_csv(os.path.join(folder_path, filename))
        df=df.iloc[2:]

        df['Close'] = pd.to_numeric(df['Close'], errors='coerce') #Converting to numeric values

        close = df['Close']
        

        returns = np.log(close / close.shift(1)) # Calculate log returns
        returns = returns.dropna()

        
        vol_dict[stock] = returns.std() #Calculating volatility of each stocks

# Create a Series from volatilities
avg_volatility = pd.Series(vol_dict)

# Filter out top 25% most volatile
vol_threshold = avg_volatility.quantile(0.75)
filtered_stocks = avg_volatility[avg_volatility < vol_threshold].index.tolist()

print("Filtered (less volatile) stocks:")
print(filtered_stocks)

def calculate_cagr(start_price, end_price, years):
    return (end_price / start_price) ** (1 / years) - 1

