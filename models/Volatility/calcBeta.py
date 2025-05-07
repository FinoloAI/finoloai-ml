import yfinance as yf
import numpy as np
import pandas as pd
import os

folder_path = r'C:\Users\ANWESHA\OneDrive\Documents\A_FinalYrProj\Financial portfolio\finoloai-ml\Data'  # replace with your path

def calculate_beta(stock_data, market_data):
    # Drop NaNs and align dates
    df = pd.DataFrame({
        'stock': stock_data,
        'market': market_data
    }).dropna()

    # Calculate daily log returns
    df['stock_return'] = np.log(df['stock'] / df['stock'].shift(1))
    df['market_return'] = np.log(df['market'] / df['market'].shift(1))
    df = df.dropna()

    # Calculate covariance and variance
    covariance = np.cov(df['stock_return'], df['market_return'])[0][1]
    market_variance = np.var(df['market_return'])

    beta = covariance / market_variance
    return beta

beta_dict = {}
market= pd.read_csv(os.path.join(folder_path, 'NIFTY50.csv'))  # Assuming you have a market index CSV file
market = market.iloc[2:]  # Adjust as needed
market['Close'] = pd.to_numeric(market['Close'], errors='coerce')
market_data=market['Close']

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        stock = filename.replace('.csv', '')
        df = pd.read_csv(os.path.join(folder_path, filename))
        df=df.iloc[2:]

        df['Close'] = pd.to_numeric(df['Close'], errors='coerce') #Converting to numeric values

        close = df['Close']
        

        returns = np.log(close / close.shift(1)) # Calculate log returns
        returns = returns.dropna()

        
        beta_dict[stock] = calculate_beta(close,market_data) #Calculating volatility of each stocks
 
#print(beta_dict)
stable_stocks=[]
for stock in beta_dict:
    if beta_dict[stock]<1:
        stable_stocks.append(stock)
print("Filtered (less volatile) stocks:", stable_stocks)
