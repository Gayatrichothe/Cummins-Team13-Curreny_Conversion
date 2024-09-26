import sqlite3
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.models import ColumnDataSource, HoverTool, Label
import pandas as pd

def fetch_exchange_rate_data(db_path, selected_columns, year):
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    table_name = f"Exchange_Rate_Report_{year}"
    column_string = ', '.join(selected_columns)
    # Query
    query = f"SELECT Date, {column_string} FROM {table_name}"  
    cursor.execute(query)
    # Fetch all results
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    df = pd.DataFrame(rows, columns=['Date'] + selected_columns)

    df['Date'] = pd.to_datetime(df['Date'])
    
    return df

# Function to create plot
def create_bokeh_plot(df, currency_column):
    # Calculate the min and max 
    min_value = df[currency_column].min()
    max_value = df[currency_column].max()
    min_date = df.loc[df[currency_column] == min_value, 'Date'].values[0]
    max_date = df.loc[df[currency_column] == max_value, 'Date'].values[0]

    #datetime object
    min_date = pd.to_datetime(min_date)
    max_date = pd.to_datetime(max_date)

    # Print the min and max values
    print(f"Minimum {currency_column} exchange rate: {min_value:.2f} on {min_date.strftime('%Y-%m-%d')}")
    print(f"Maximum {currency_column} exchange rate: {max_value:.2f} on {max_date.strftime('%Y-%m-%d')}")

    # Prepare output file
    output_file("exchange_rates.html")

    source = ColumnDataSource(data=dict(date=df['Date'], **{currency_column: df[currency_column]}))

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
    hover.formatters = {'@date': 'datetime'}  
    p.add_tools(hover)

    p.line('date', currency_column, source=source, line_width=2, color='blue', legend_label=currency_column, alpha=0.7)

    # Customize grid lines
    p.xgrid.grid_line_color = "lightgray"
    p.ygrid.grid_line_color = "lightgray"

    # Use scatter for min and max markers
    p.scatter(x=min_date, y=min_value, size=8, color='red', legend_label='Min Value', alpha=0.8)
    p.scatter(x=max_date, y=max_value, size=8, color='green', legend_label='Max Value', alpha=0.8)

    # Add labels for min and max values
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

    #axis
    p.title.text_font_size = "16pt"
    p.xaxis.axis_label_text_font_size = "12pt"
    p.yaxis.axis_label_text_font_size = "12pt"

    #tick label fonts
    p.xaxis.major_label_text_font_size = "10pt"
    p.yaxis.major_label_text_font_size = "10pt"


    show(p)

    # Generate the centered HTML file
    generate_centered_html(currency_column)

def generate_centered_html(currency_column):
    # HTML for centering
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{currency} Exchange Rates</title>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh; /* Full height */
                margin: 0;
                background-color: #f0f0f0; /* Optional background color */
            }}
            #plot {{
                max-width: 800px; /* Max width for the plot */
                width: 100%; /* Full width */
            }}
        </style>
    </head>
    <body>
        <div id="plot">
            {plot_script}
        </div>
    </body>
    </html>
    """

    # Read HTML
    with open("exchange_rates.html", "r") as file:
        bokeh_html = file.read()

    # Write the combined HTML to a new file
    with open("centered_exchange_rates.html", "w") as file:
        file.write(html_template.format(plot_script=bokeh_html, currency=currency_column))

    print("Centered plot saved to 'centered_exchange_rates.html'")

# Main 
if __name__ == "__main__":
    db_path = 'mydb5.db'
    
    # user input 
    currency_column = input("Enter the currency code (e.g., 'USD'): ").strip().upper()
    
    #input for the year
    year = input("Enter the year (e.g.'2013'): ").strip()
    
    # Check if the input is valid
    valid_columns = ['DZD', 'AUD', 'BHD', 'VEF', 'BWP', 'BRL', 'BND', 'CAD', 'CLP', 'CNY',  
                     'COP', 'CZK', 'DKK', 'EUR', 'HUF', 'ISK', 'INR', 'IDR', 'IRR', 'ILS', 
                     'JPY', 'KZT', 'KRW', 'KWD', 'LYD', 'MYR', 'MUR', 'MXN', 'NPR', 'NZD', 
                     'NOK', 'OMR', 'PKR', 'PEN', 'PHP', 'PLN', 'QAR', 'RUB', 'SAR', 'SGD', 
                     'ZAR', 'LKR', 'SEK', 'CHF', 'THB', 'TTD', 'TND', 'AED', 'GBP', 'UYU']
    
    if currency_column in valid_columns:
        selected_columns = [currency_column]  # Only analyze the specified currency
        # Fetch the exchange rate data
        df = fetch_exchange_rate_data(db_path, selected_columns, year)

        # Create and save the Bokeh plot
        create_bokeh_plot(df, currency_column)
    else:
        print("Invalid currency code. Please run the program again with a valid currency code.")
