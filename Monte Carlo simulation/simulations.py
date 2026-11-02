# Import required libraries
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

import warnings

warnings.filterwarnings(
    "ignore",
    message=".*inplace.*deprecated.*",
    category=Warning
)

def monte_carlo_simulation(ticker, start_date, end_date,
                           num_simulations, num_days,
                           annual_return, annual_volatility):

    # Retrieve historical stock price data
    price_data = ticker.history(
        start=start_date,
        end=end_date,
        auto_adjust=True
    )

    # Set the initial price equal to the last historical closing price
    close_price = price_data["Close"].iloc[-1]

    # Define the length of each time interval (in years)
    dt = 1 / 252

    # Generate random standard normal variables for each day and simulation
    # Each column represents one possible stock-price trajectory
    # Each row represents one trading day
    Z = np.random.standard_normal((num_days, num_simulations))

    # Apply the Geometric Brownian Motion equation to calculate
    # the daily price multipliers for all simulations
    daily_returns = np.exp(
        (annual_return - 0.5 * annual_volatility**2) * dt
        + annual_volatility * np.sqrt(dt) * Z
    )

    # Calculate cumulative products to obtain successive stock prices
    # Multiply by the initial stock price to obtain actual price levels
    predicted_price = close_price * daily_returns.cumprod(axis=0)

    # Calculate the mean simulated price at each time step
    mean_prices = predicted_price.mean(axis=1)

    # Calculate the median simulated price at each time step
    median_prices = np.median(predicted_price, axis=1)

    return predicted_price, mean_prices, median_prices

def predicted_annual_return(price_data):

    # Calculate daily percentage returns from historical closing prices
    returns = price_data["Close"].pct_change().dropna()

    # Calculate the arithmetic mean and standard deviation of daily returns
    mean_return = returns.mean()
    std_dev = returns.std()

    # Annualise the mean return and volatility using 252 trading days
    annual_return = mean_return * 252
    annual_volatility = std_dev * np.sqrt(252)

    # Display the estimated annual parameters
    print(f"Annual Return: {annual_return:.2%}")
    print(f"Annual Volatility: {annual_volatility:.2%}")

    return annual_return, annual_volatility

def plot_simulation(predicted_prices, graph_type="trajectory"):

    # Plot all simulated price trajectories
    if graph_type == "trajectory":

        plt.figure(figsize=(12, 6))

        plt.plot(predicted_prices, alpha=0.05)

        plt.xlabel("Trading Days")
        plt.ylabel("Stock Price ($)")
        plt.title("Monte Carlo Stock Price Simulation")

        plt.show()

    # Plot the distribution of final simulated prices
    elif graph_type == "histogram":

        final_prices = predicted_prices[-1, :]

        plt.figure(figsize=(10, 6))

        plt.hist(final_prices, bins=50, edgecolor="black")

        plt.xlabel("Final Stock Price ($)")
        plt.ylabel("Frequency")
        plt.title("Distribution of Simulated Final Prices")

        plt.show()

    else:
        raise ValueError("graph_type must be 'trajectory' or 'histogram'")

def statistics(predicted_prices, close_price):
    final_prices = predicted_prices[-1, :]

    print(f"Current Price: ${close_price:.2f}")

    print(f"5th percentile: ${np.percentile(final_prices, 5):.2f}")
    print(f"95th percentile: ${np.percentile(final_prices, 95):.2f}")

def theoretical_loss_probability(annual_return, annual_volatility, close_price, predicted_prices):

    T = 1

    # Theoretical probability of finishing below the initial price
    theoretical_loss = norm.cdf(
        (0.5 * annual_volatility**2 - annual_return)
        * np.sqrt(T) / annual_volatility
    )

    # Monte Carlo estimate
    final_prices = predicted_prices[-1, :]

    simulated_loss = np.mean(final_prices < close_price)

    print(f"Theoretical probability of loss: {theoretical_loss:.2%}")
    print(f"Simulated probability of loss: {simulated_loss:.2%}")
    
    return theoretical_loss, simulated_loss

