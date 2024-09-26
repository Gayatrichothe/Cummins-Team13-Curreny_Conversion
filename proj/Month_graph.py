import sqlite3
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import ColumnDataSource, HoverTool, Label, Select
import pandas as pd

# Function to fetch exchange rate data based on specified columns and month
def fetch_exchange_rate_data(db_path, selected_columns, year, month=None):
  
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    table_name = f"Exchange_Rate_Report_{year}"
    column_string = ', '.join(selected_columns)
    
    # Query to select the date and specified exchange rates
    if month:
        query = f"SELECT Date, {column_string} FROM {table_name} WHERE strftime('%m', Date) = '{month}'"
    else:
        query = f"SELECT Date, {column_string} FROM {table_name}"  
    
    cursor.execute(query)

    # Fetch all results
    rows = cursor.fetchall()

    # Close 
    cursor.close()
    conn.close()
    df = pd.DataFrame(rows, columns=['Date'] + selected_columns)
    df['Date'] = pd.to_datetime(df['Date'])
    
    return df

def create_bokeh_plot(df, currency_column):
    # Calculate the min and max values 
    min_value = df[currency_column].min()
    max_value = df[currency_column].max()
    min_date = df.loc[df[currency_column] == min_value, 'Date'].values[0]
    max_date = df.loc[df[currency_column] == max_value, 'Date'].values[0]
    min_date = pd.to_datetime(min_date)
    max_date = pd.to_datetime(max_date)

    # Print the min and max values along with their dates
    print(f"Minimum {currency_column} exchange rate: {min_value:.2f} on {min_date.strftime('%Y-%m-%d')}")
    print(f"Maximum {currency_column} exchange rate: {max_value:.2f} on {max_date.strftime('%Y-%m-%d')}")

    output_file("exchange_rates.html")

    source = ColumnDataSource(data=dict(date=df['Date'], **{currency_column: df[currency_column]}))

    # Create a figure 
    p = figure(title=f"{currency_column} Exchange Rates Over Time", 
               x_axis_label='Date', y_axis_label='Exchange Rate', 
               x_axis_type='datetime', height=400, width=800, align='center',
               tools='pan,wheel_zoom,box_zoom,reset,save', 
               background_fill_color='#f9f9f9')

    # Add hover tool
    hover = HoverTool()
    hover.tooltips = [
        ("Date", "@date{%F}"),
        (f"{currency_column} Exchange Rate", f"@{currency_column}{{0.2f}}"),
    ]
    hover.formatters = {'@date': 'datetime'}  # Use 'datetime' formatter for date
    p.add_tools(hover)

    p.line('date', currency_column, source=source, line_width=2, color='blue', legend_label=currency_column, alpha=0.7)

    p.xgrid.grid_line_color = "lightgray"
    p.ygrid.grid_line_color = "lightgray"

    #scatter for min and max
    p.scatter(x=min_date, y=min_value, size=8, color='red', legend_label='Min Value', alpha=0.8)
    p.scatter(x=max_date, y=max_value, size=8, color='green', legend_label='Max Value', alpha=0.8)

    #labels for min and max 
    p.add_layout(Label(x=min_date, y=min_value, text=f'Min: {min_value:.2f}', text_color='red', 
                       text_align='center', text_baseline='bottom'))
    p.add_layout(Label(x=max_date, y=max_value, text=f'Max: {max_value:.2f}', text_color='green', 
                       text_align='center', text_baseline='bottom'))

    # legend
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    p.legend.title = "Legend"
    p.legend.title_text_font_size = "12pt"
    p.legend.label_text_font_size = "10pt"

    #axis label 
    p.title.text_font_size = "16pt"
    p.xaxis.axis_label_text_font_size = "12pt"
    p.yaxis.axis_label_text_font_size = "12pt"

    #tick label 
    p.xaxis.major_label_text_font_size = "10pt"
    p.yaxis.major_label_text_font_size = "10pt"

    show(p)

# Main execution
if __name__ == "__main__":
    # Define the database path
    db_path = 'mydb5.db'
    
    # input for the currency
    currency_column = input("Enter the currency code (e.g., 'USD'): ").strip().upper()
    
    # input for the year
    year = input("Enter the year (e.g. '2013'): ").strip()
    
    # Check if valid
    valid_columns = ['DZD', 'AUD', 'BHD', 'VEF', 'BWP', 'BRL', 'BND', 'CAD', 'CLP', 'CNY',  
                     'COP', 'CZK', 'DKK', 'EUR', 'HUF', 'ISK', 'INR', 'IDR', 'IRR', 'ILS', 
                     'JPY', 'KZT', 'KRW', 'KWD', 'LYD', 'MYR', 'MUR', 'MXN', 'NPR', 'NZD', 
                     'NOK', 'OMR', 'PKR', 'PEN', 'PHP', 'PLN', 'QAR', 'RUB', 'SAR', 'SGD', 
                     'ZAR', 'LKR', 'SEK', 'CHF', 'THB', 'TTD', 'TND', 'AED', 'GBP', 'UYU']
    
    if currency_column in valid_columns:
        selected_columns = [currency_column]  
        
        
        month = input("Enter the month (01-12) to filter data or press Enter to include all months: ").strip() or None

        # Fetch the exchange rate data
        df = fetch_exchange_rate_data(db_path, selected_columns, year, month)

        # Create and save the Bokeh plot
        create_bokeh_plot(df, currency_column)
    else:
        print("Invalid currency code. Please run the program again with a valid currency code.")
