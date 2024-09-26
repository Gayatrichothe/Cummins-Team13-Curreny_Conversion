from flask import Flask, render_template, request, session, jsonify
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Directory where your CSV files are stored
CSV_DIR = "data"

# Helper function to read CSV data for a given year
def read_csv(year):
    file_path = os.path.join(CSV_DIR, f"Exchange_Rate_Report_{year}.csv")
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame()  # Handle the case where the file doesn't exist

# Route for the main page to accept user input for currency and time period
@app.route("/", methods=["GET", "POST"])
def index():
    year = session.get("year", "2012")  # Default year
    df = read_csv(year)
    currencies = df.columns[1:]  # Assuming first column is Date, rest are currencies

    if request.method == "POST":
        session["currency1"] = request.form["currency1"]
        session["currency2"] = request.form["currency2"]
        session["year"] = request.form["year"]
        return jsonify({"status": "success"})

    currency1 = session.get("currency1", currencies[0])
    currency2 = session.get("currency2", currencies[1])

    return render_template("index.html", currencies=currencies, currency1=currency1, currency2=currency2, year=year)

# Route for calculating basket value
@app.route("/calculate_basket", methods=["POST"])
def calculate_basket():
    data = request.get_json()
    currencies = data.get("currencies")  # List of selected currencies
    weights = data.get("weights")  # List of corresponding weights (in percentages)
    year = data.get("year")  # The year for exchange rate data

    # Read the exchange rate data for the specified year
    df = read_csv(year)

    # Check if the dataframe is empty
    if df.empty:
        return jsonify({"error": "No data available for the selected year."}), 400

    # Initialize the total basket value
    total_value = 0

    for currency, weight in zip(currencies, weights):
        # Ensure weight is a valid number and currency exists in the dataframe
        if weight < 0 or weight > 100:
            return jsonify({"error": "Weights must be between 0 and 100."}), 400

        if currency not in df.columns:
            return jsonify({"error": f"{currency} not available in the exchange rate data."}), 400

        # Assume the base currency is the first currency in your DataFrame
        base_currency = df.columns[1]  # Replace with your base currency logic
        exchange_rate = df[currency].iloc[-1]  # Get the latest exchange rate for the currency
        
        # Calculate contribution and accumulate it to total value
        contribution = (exchange_rate * (weight / 100))
        total_value += contribution

    return jsonify({"basket_value": total_value})

# Route for generating graphs
@app.route("/generate_graph", methods=["POST"])
def generate_graph():
    year = request.json.get("year")
    currency1 = request.json.get("currency1")
    currency2 = request.json.get("currency2")

    # Read the exchange rate data for the specified year
    df = read_csv(year)

    if df.empty:
        return jsonify({"error": "No data available for the selected year."}), 400

    # Create a line plot for the selected currencies
    fig = px.line(df, x='Date', y=[currency1, currency2], title=f'Exchange Rates: {currency1} vs {currency2} ({year})')
    graph_html = pio.to_html(fig, full_html=False)

    return jsonify({"graph": graph_html})

# Main function to run the application
if __name__ == "__main__":
    app.run(debug=True)
