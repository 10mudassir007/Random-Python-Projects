from datetime import datetime
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split
import xgboost as xgb
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Streamlit UI for input
ticker_symbol = st.text_input(
    "Enter Stock Ticker or Currency Pair (e.g., 'AAPL' or 'USDPKR=X')"
)
asset_type = st.selectbox("Select Asset Type", ("Stock", "Currency Pair"))

if st.button("Predict") and ticker_symbol:
    if asset_type == "Stock":
        # Fetch stock data
        stock_data = yf.Ticker(ticker_symbol)
        history = stock_data.history(period="max")
    elif asset_type == "Currency Pair":
        # Fetch currency pair data (USD/PKR for example)
        history = yf.download(
            ticker_symbol,
            interval="1d",
            start="1900-01-01",
            end=str(datetime.now().date()),
        )

    # Feature engineering
    features_df = pd.DataFrame()
    features_df["dates"] = history.index
    features_df["years"] = features_df["dates"].dt.year
    features_df["months"] = features_df["dates"].dt.month
    features_df["days"] = features_df["dates"].dt.day
    features_df["day_week"] = features_df["dates"].dt.weekday
    features_df["day_year"] = features_df["dates"].dt.dayofyear
    features_df["timestamp"] = features_df["dates"].astype("int64") // 10**11

    X = features_df.drop("dates", axis=1).to_numpy()
    y = history[["Close", "High", "Low", "Open"]].to_numpy()

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Model training
    reg = xgb.XGBRegressor(random_state=42)
    reg.fit(X_train, y_train)

    # Display training and test scores
    st.header(f"{asset_type} Prices")
    st.markdown("###### Train Score: {}".format(round(reg.score(X_train, y_train), 8)))
    st.markdown("###### Test Score: {}".format(round(reg.score(X_test, y_test), 8)))

    # Display predictions for the test set
    st.markdown("#### Test Predictions")
    st.write(
        pd.DataFrame(reg.predict(X_test), columns=["Close", "High", "Low", "Open"])
    )

    # Function to create features for future predictions
    def create_features_from_dates(dates):
        dates_df = pd.DataFrame({"dates": dates})
        dates_df["years"] = dates_df["dates"].dt.year
        dates_df["months"] = dates_df["dates"].dt.month
        dates_df["days"] = dates_df["dates"].dt.day
        dates_df["day_week"] = dates_df["dates"].dt.weekday
        dates_df["day_year"] = dates_df["dates"].dt.dayofyear
        dates_df["timestamp"] = dates_df["dates"].astype("int64") // 10**11
        dates_df = dates_df.drop("dates", axis=1).to_numpy()
        return dates_df

    # Predicting for future dates (next 100 days)
    future_dates = pd.to_datetime(
        [features_df.iloc[-1]["dates"] + pd.Timedelta(days=x) for x in range(1, 101)]
    )
    future_features = create_features_from_dates(future_dates)
    future_preds = reg.predict(future_features)

    # Creating a DataFrame for future predictions
    predict_df = pd.DataFrame(
        future_preds, columns=["Close", "High", "Low", "Open"], index=future_dates
    )

    # Display future predictions
    st.markdown("#### Future 100 Days Predictions")
    st.write(predict_df)

    # Plotting the future predictions
    fig = go.Figure()

    # Add traces for each series
    fig.add_trace(
        go.Scatter(x=future_dates, y=predict_df["Open"], mode="lines", name="Open")
    )
    fig.add_trace(
        go.Scatter(x=future_dates, y=predict_df["High"], mode="lines", name="High")
    )
    fig.add_trace(
        go.Scatter(x=future_dates, y=predict_df["Low"], mode="lines", name="Low")
    )
    fig.add_trace(
        go.Scatter(x=future_dates, y=predict_df["Close"], mode="lines", name="Close")
    )

    # Update layout
    fig.update_layout(
        title=f"{asset_type} Prices for the Next 100 Days",
        xaxis_title="Dates",
        yaxis_title="Prices",
        legend_title="OHLC",
        template="plotly_dark",
    )

    # Show the plot
    st.plotly_chart(fig)
