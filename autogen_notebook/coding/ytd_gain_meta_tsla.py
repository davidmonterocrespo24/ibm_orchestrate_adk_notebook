# filename: ytd_gain_meta_tsla.py
import datetime
import yfinance as yf

# Step 1: Get today's date
today = datetime.date.today()
print(f"Today's date: {today}")

# Step 2: Get the first trading day of the year
year_start = datetime.date(today.year, 1, 1)

# Step 3: Download historical data for META and TSLA
meta = yf.Ticker("META")
tsla = yf.Ticker("TSLA")

meta_hist = meta.history(start=year_start, end=today + datetime.timedelta(days=1))
tsla_hist = tsla.history(start=year_start, end=today + datetime.timedelta(days=1))

# Step 4: Find the first and last closing prices for YTD
meta_start = meta_hist['Close'].iloc[0]
meta_end = meta_hist['Close'].iloc[-1]
tsla_start = tsla_hist['Close'].iloc[0]
tsla_end = tsla_hist['Close'].iloc[-1]

# Step 5: Calculate YTD gain
meta_gain = ((meta_end - meta_start) / meta_start) * 100
tsla_gain = ((tsla_end - tsla_start) / tsla_start) * 100

print(f"META YTD gain: {meta_gain:.2f}%")
print(f"TSLA YTD gain: {tsla_gain:.2f}%")