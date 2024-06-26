# Simple Trading App

This is a simple trading algorithm app implemented using Python, `pandas`, `yfinance`, and `streamlit`. It allows users to backtest a basic moving average crossover strategy on historical stock data.

## Features

- Fetch historical stock data using `yfinance`
- Calculate short and long moving averages
- Generate buy/sell signals based on moving average crossovers
- Backtest the strategy to compute the final balance
- Display key statistics such as total return, average daily return, and daily return standard deviation
- Plot stock price and buy/sell signals on a chart
- Interactive Streamlit UI to customize stock symbol, period, moving average windows, and initial balance
