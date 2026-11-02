import sqlite3
def create_database():
    connection = sqlite3.connect("monte_carlo.db")

    cursor = connection.cursor()


    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS simulation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            start_date TEXT,
            end_date TEXT,
            num_simulations INTEGER,
            num_days INTEGER,
            annual_return REAL,
            annual_volatility REAL,
            mean_price REAL,
            median_price REAL,
            chance_of_loss REAL
        )
        """
    )

def insert_simulation_result(ticker, start_date, end_date, num_simulations, num_days, annual_return, annual_volatility, mean_price, median_price, chance_of_loss):
    connection = sqlite3.connect("monte_carlo.db")

    cursor = connection.cursor()
    
    cursor.execute(
        """
        INSERT INTO simulation_results (
            ticker, start_date, end_date, num_simulations, num_days,
            annual_return, annual_volatility, mean_price, median_price, chance_of_loss
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            ticker, start_date, end_date, num_simulations, num_days,
            annual_return, annual_volatility, mean_price, median_price, chance_of_loss
        )
    )

    connection.commit()
    connection.close()


