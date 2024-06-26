# trading_app_no_talib.py
import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# Fetch historical data
def fetch_data(symbol, period='1y'):
    stock_data = yf.download(symbol, period=period)
    return stock_data

# Calculate moving averages manually using pandas
def calculate_moving_averages(df, short_window, long_window):
    df['short_ma'] = df['Close'].rolling(window=short_window).mean()
    df['long_ma'] = df['Close'].rolling(window=long_window).mean()
    return df

# Generate signals
def generate_signals(df):
    df['signal'] = 0
    df['signal'][short_window:] = np.where(df['short_ma'][short_window:] > df['long_ma'][short_window:], 1, 0)
    df['position'] = df['signal'].diff()
    return df

# Backtest strategy
def backtest_strategy(df, initial_balance=10000):
    balance = initial_balance
    shares = 0
    for i in range(len(df)):
        if df['position'][i] == 1:
            shares = balance / df['Close'][i]
            balance = 0
        elif df['position'][i] == -1:
            balance = shares * df['Close'][i]
            shares = 0
    final_balance = balance + shares * df['Close'].iloc[-1]
    return final_balance

# Calculate basic statistics
def calculate_statistics(df, initial_balance, final_balance):
    total_return = (final_balance - initial_balance) / initial_balance * 100
    daily_returns = df['Close'].pct_change().dropna()
    avg_daily_return = daily_returns.mean() * 100
    std_daily_return = daily_returns.std() * 100
    return total_return, avg_daily_return, std_daily_return

# Plot buy/sell signals
def plot_signals(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['Close'], label='Close Price')
    ax.plot(df['short_ma'], label='Short MA', alpha=0.7)
    ax.plot(df['long_ma'], label='Long MA', alpha=0.7)
    ax.scatter(df.index[df['position'] == 1], df['Close'][df['position'] == 1], marker='^', color='g', label='Buy Signal', alpha=1)
    ax.scatter(df.index[df['position'] == -1], df['Close'][df['position'] == -1], marker='v', color='r', label='Sell Signal', alpha=1)
    ax.set_title('Stock Price and Buy/Sell Signals')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    st.pyplot(fig)

# Streamlit UI
st.title("Simple Trading App")

# Stock selection
stock_options = ["AAPL","TSLA", "NVDA", "GOOGL", "AMZN"]
user_input = st.selectbox("Select Stock Symbol", stock_options)

# Period selection
period_input = st.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

# Moving average window settings
short_window = st.number_input("Short Moving Average Window", min_value=1, max_value=100, value=20)
long_window = st.number_input("Long Moving Average Window", min_value=1, max_value=100, value=50)

# Initial balance input
initial_balance = st.number_input("Initial Balance", min_value=1000, max_value=1000000, value=10000)

if st.button("Run Backtest"):
    df = fetch_data(user_input, period=period_input)
    df = calculate_moving_averages(df, short_window, long_window)
    df = generate_signals(df)
    final_balance = backtest_strategy(df, initial_balance)

    st.write(f"Final Balance: ${final_balance:.2f}")

    # Calculate and display statistics
    total_return, avg_daily_return, std_daily_return = calculate_statistics(df, initial_balance, final_balance)
    st.write(f"Total Return: {total_return:.2f}%")
    st.write(f"Average Daily Return: {avg_daily_return:.2f}%")
    st.write(f"Daily Return Standard Deviation: {std_daily_return:.2f}%")

    # Display historical data
    st.write("Historical Data")
    st.dataframe(df[['Close', 'short_ma', 'long_ma', 'signal', 'position']])

    # Plot signals
    plot_signals(df)
