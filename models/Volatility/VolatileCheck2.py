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

# cagr_dict = {}


# for filename in os.listdir(folder_path):
#     if filename.endswith('.csv'):
#         stock = filename.replace('.csv', '')
#         df = pd.read_csv(os.path.join(folder_path, filename))
#         df=df.iloc[2:]

#         df['Close'] = pd.to_numeric(df['Close'], errors='coerce') #Converting to numeric values

#         close = df['Close']
        

#         returns = np.log(close / close.shift(1)) # Calculate log returns
#         returns = returns.dropna()

        
#         vol_dict[stock] = returns.std() #Calculating volatility of each stocks
#         stock_prices = df.dropna()
#         if stock_prices.empty:
#             print(f"⚠️ No data for {stock}")
#             continue
#         start_price = stock_prices.iloc[0]
#         end_price = stock_prices.iloc[-1]
#         years = pd.to_numeric((stock_prices.index[-1] - stock_prices.index[0])) / 365
#         if years > 0:
#             cagr_dict[stock] = calculate_cagr(start_price, end_price, years)


# cagr_series = pd.Series(cagr_dict)

# # 7. Filter stocks with CAGR > 3.71%
# target_cagr = 0.0371
# qualified_stocks = cagr_series[cagr_series > target_cagr]

# # 8. Final selection = Low volatility + sufficient CAGR
# final_selection = avg_volatility[qualified_stocks.index].sort_values()

# # 9. Show results
# print("✅ Final Investment Candidates (Sorted by Volatility):\n")
# for stock in final_selection.index:
#     print(f"{stock}: CAGR = {cagr_series[stock]*100:.2f}%, Volatility = {avg_volatility[stock]*100:.2f}%")
# print(final_selection)