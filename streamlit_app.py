import pandas as pd
import streamlit as st
import yfinance as yf

st.title("Microsoft (MSFT) 5-Year Monthly Sharpe Ratio")
st.write("Calculated from five years of monthly MSFT closing prices using a 0.25% monthly risk-free rate.")

# Parameters from the assignment's example.
ticker = "MSFT"
rf_monthly = 0.0025

try:
    # Monthly stock-price observations over the last five years.
    data = yf.download(ticker, period="5y", interval="1mo", progress=False)

    if data.empty:
        st.error("No stock price data found for MSFT. Please try again later.")
    else:
        # yfinance may return a MultiIndex for downloaded stock prices.
        close_prices = data["Close"]
        if isinstance(close_prices, pd.DataFrame):
            close_prices = close_prices[ticker] if ticker in close_prices.columns else close_prices.iloc[:, 0]

        monthly_returns = close_prices.pct_change().dropna()
        excess_returns = monthly_returns - rf_monthly
        mean_excess_return = excess_returns.mean()
        std_dev_return = monthly_returns.std()

        if monthly_returns.empty or pd.isna(std_dev_return) or std_dev_return == 0:
            st.error("Not enough valid monthly returns to calculate a Sharpe ratio.")
        else:
            monthly_sharpe_ratio = mean_excess_return / std_dev_return
            st.metric(label="MSFT Monthly Sharpe Ratio", value=f"{monthly_sharpe_ratio:.3f}")
            st.caption(f"Based on {len(monthly_returns)} monthly returns. This is a monthly, not annualized, Sharpe ratio.")
except Exception as error:
    st.error("Unable to retrieve MSFT stock data right now. Please try again later.")
    st.caption(f"Details: {error}")
