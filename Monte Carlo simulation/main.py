# Import required libraries
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import sqlite3

from simulations import monte_carlo_simulation, predicted_annual_return, theoretical_loss_probability, statistics, plot_simulation
from database import insert_simulation_result, create_database

import warnings

warnings.filterwarnings(
    "ignore",
    message=".*inplace.*deprecated.*",
    category=Warning
)



start_date = "2013-01-01"
end_date = pd.Timestamp.now().strftime("%Y-%m-%d")
#num_simulations = int(input("Enter the number of simulations to run (e.g., 1000): "))
num_simulations = 1000

ticker_input = input("Enter the stock ticker symbol (e.g., AAPL, KO, MNTS, TTWO, NVDA, MSFT, AMZN, JNJ): ").upper()
ticker = yf.Ticker(ticker_input)

# Estimate annual return and volatility using historical Momentus data
annual_return, annual_volatility = predicted_annual_return(
    ticker.history(start=start_date, end=end_date, auto_adjust=True)
)

# Generate 1,000 possible price trajectories over 252 trading days
predicted_prices, mean_prices, median_prices = monte_carlo_simulation(
    ticker , start_date, end_date, num_simulations, 252,
    annual_return, annual_volatility
)

# Display the mean and median simulated prices after one year
theoretical_loss, simulated_loss = theoretical_loss_probability(annual_return, annual_volatility, ticker.history(start=start_date, end=end_date, auto_adjust=True)["Close"].iloc[-1], predicted_prices)
statistics(predicted_prices, ticker.history(start=start_date, end=end_date, auto_adjust=True)["Close"].iloc[-1])
#plot_simulation(predicted_prices, graph_type="trajectory")
#plot_simulation(predicted_prices, graph_type="histogram")

connection = sqlite3.connect("monte_carlo.db")
cursor = connection.cursor()
create_database()
insert_simulation_result(
    ticker_input,
    start_date,
    end_date,
    1000,
    252,
    annual_return,
    annual_volatility,
    mean_prices[-1],
    median_prices[-1],
    simulated_loss
)