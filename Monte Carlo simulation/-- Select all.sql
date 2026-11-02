-- SQLite
SELECT id, ticker, start_date, end_date, num_simulations, num_days, round(annual_return, 4) AS annual_return, round(annual_volatility, 4) AS annual_volatility, round(mean_price, 2) AS mean_price, round(median_price, 2) AS median_price, round(chance_of_loss, 4) AS chance_of_loss
FROM simulation_results;