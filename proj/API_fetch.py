import requests
import sqlite3
from datetime import datetime, timedelta

api_key = 'd7f24e4cc52a970f4bdf109f'

#Base currency 
base_currency = 'USD'

#List of target currencies
target_currencies = [
    'DZD', 'AUD', 'BHD', 'BWP', 'BRL', 'BND', 'CAD', 'CLP', 
    'CNY', 'COP', 'CZK', 'DKK', 'EUR', 'HUF', 'ISK', 'INR', 'IDR', 
    'IRR', 'ILS', 'JPY', 'KZT', 'KRW', 'KWD', 'LYD', 'MYR', 'MUR', 
    'MXN', 'NPR', 'NZD', 'NOK', 'OMR', 'PKR', 'PEN', 'PHP', 'PLN', 
    'QAR', 'RUB', 'SAR', 'SGD', 'ZAR', 'LKR', 'SEK', 'CHF', 'THB', 
    'TTD', 'TND', 'AED', 'GBP', 'UYU'
]

#Time period to retrieve data
start_date = '2023-01-04'
end_date = '2023-03-31'

#Convert string dates to datetime objects
start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

#Connection
conn = sqlite3.connect('exchange_rate.db')
cursor = conn.cursor()

#Dynamically create table columns based on the target currencies
cursor.execute('''CREATE TABLE IF NOT EXISTS exchange_rates (
    date TEXT PRIMARY KEY,
    {}
)'''.format(', '.join([f"{currency} REAL" for currency in target_currencies])))

# Function to fetch exchange rate for a specific currency
def fetch_exchange_rate(base_currency, target_currency):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_currency}/{target_currency}"
    try:
        response = requests.get(url)
        
        # if successful
        if response.status_code == 200:
            data = response.json()
            return data.get('conversion_rate', None)
        else:
            print(f"Error fetching data for {target_currency} (Status Code: {response.status_code})")
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

#Loop through the date range
current_date = start_date_obj
while current_date <= end_date_obj:
    formatted_date = current_date.strftime('%Y-%m-%d')
    
    # Dictionary to hold the exchange rates for the day
    exchange_rates_for_day = {'date': formatted_date}
    
    for target_currency in target_currencies:
        # Fetch the exchange rate
        exchange_rate = fetch_exchange_rate(base_currency, target_currency)
        
        # If the exchange rate is valid, store it in the dictionary
        if exchange_rate is not None:
            exchange_rates_for_day[target_currency] = exchange_rate
        else:
            exchange_rates_for_day[target_currency] = None  # Handle missing rates
    
    #inserting into the database
    cursor.execute(f'''
        INSERT OR REPLACE INTO exchange_rates (date, {', '.join(target_currencies)})
        VALUES (?, {', '.join(['?' for _ in target_currencies])})
    ''', (exchange_rates_for_day['date'], *[exchange_rates_for_day[currency] for currency in target_currencies]))
    
    print(f"Stored data for {formatted_date}: {exchange_rates_for_day}")

    # Commit the changes to the database after each date
    conn.commit()
    
    
    current_date += timedelta(days=1)

# Close connection
conn.close()

print("Exchange rate data stored in the database 'exchange_rates.db'")
