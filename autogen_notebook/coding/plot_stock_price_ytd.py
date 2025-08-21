# filename: plot_stock_price_ytd.py
import datetime
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Get today's date and year start
today = datetime.date.today()
year_start = datetime.date(today.year, 1, 1)

# Step 2: Download historical data for META and TSLA
meta = yf.Ticker("META")
tsla = yf.Ticker("TSLA")

meta_hist = meta.history(start=year_start, end=today + datetime.timedelta(days=1))
tsla_hist = tsla.history(start=year_start, end=today + datetime.timedelta(days=1))

# Step 3: Prepare DataFrame for CSV
df = pd.DataFrame({
    'Date': meta_hist.index,
    'META_Close': meta_hist['Close'].values,
    'TSLA_Close': tsla_hist['Close'].reindex(meta_hist.index, method='ffill').values
})
df.set_index('Date', inplace=True)
df.to_csv('stock_price_ytd.csv')

# Step 4: Plot the data
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['META_Close'], label='META')
plt.plot(df.index, df['TSLA_Close'], label='TSLA')
plt.title('YTD Closing Prices: META vs TSLA')
plt.xlabel('Date')
plt.ylabel('Closing Price (USD)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('stock_price_ytd.png')
print("Saved stock_price_ytd.csv and stock_price_ytd.png")