import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# Function to fetch historical exchange rate data for a specific date compared to USD using CurrencyLayer API
def fetch_historical_currency_data(api_key, date):
    url = f"http://api.currencylayer.com/historical?access_key={api_key}&date={date}&source=USD"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()

        # Check if the API returned an error
        if 'error' in data:
            print(f"Error fetching data for {date}: {data['error']['info']}")
            return pd.DataFrame()  # Return empty DataFrame on error

        # Extract relevant data
        rates = data['quotes']
        records = [{'Currency': currency, 'Date': date, 'Exchange Rate': rate} for currency, rate in rates.items()]
        
        # Convert to DataFrame
        df = pd.DataFrame(records)
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

# Function to store data in SQLite database
def store_data_in_database(df):
    # Connect to SQLite database
    engine = create_engine('sqlite:///currency_data_2024.db')

    try:
        df.to_sql('currency_rates_2024', con=engine, if_exists='append', index=False)
        print("Historical currency exchange rates stored successfully in the database.")
    except Exception as e:
        print(f"Error storing data in the database: {e}")

# Main execution
if __name__ == "__main__":
    API_KEY = '10fe600d16883972f812e928150e08a3'  # Replace with your actual CurrencyLayer API key
    start_date = "2024-01-01"
    end_date = "2024-8-31"

    # Create a date range for the entire year of 2024
    date_range = pd.date_range(start=start_date, end=end_date)

    for date in date_range:
        date_str = date.strftime('%Y-%m-%d')
        currency_data = fetch_historical_currency_data(API_KEY, date_str)
        
        if not currency_data.empty:
            print(f"Fetched data for {date_str}:")
            print(currency_data)  # Print the fetched currency exchange rates
            store_data_in_database(currency_data)  # Store the data in the database
        else:
            print(f"No data fetched for {date_str}.")
