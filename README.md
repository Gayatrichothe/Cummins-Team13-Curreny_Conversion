# Cummins-Team13-Curreny_Conversion

# Currency Exchange Rate

The Currency Exchange Rate Analysis Dashboard allows users to analyze and visualize exchange rates between two currencies over a specified duration. This project uses historical exchange rate data and provides an interactive menu for users to select currencies, choose durations for analysis, and view trends through graphical representations.

#Features
-Dynamic Currency Selection: Users can select any two currencies from the available options.

-Flexible Time Durations: View data in weekly, monthly, quarterly, or yearly formats.

-Graphical Visualization: Interactive graphs clearly display exchange rate trends, highlighting max and min values over time, with real-time updates for seamless analysis.

-Data Loading: Automatically loads exchange rate data from CSV files stored in a designated folder.

-Database Integration: Processed data is stored in a database for efficient retrieval and analysis.

-Data Preprocessing: The dataset is preprocessed to ensure accuracy, handling missing values, removing duplicates, and formatting dates.

-Custom Currency Basket: Users can create a custom currency basket by selecting three currencies and assigning weights, ensuring the total adds up to 100% for accurate calculations. The dashboard computes and displays the basket's value in USD.

-Frontend Service: A UI screen displays all currencies along with their short codes, descriptions, and current exchange rates against USD, providing a comprehensive view of FX rates considering a base currency like USD.

-Frontend and Backend Status: The frontend and backend code are both functional and robust. However, due to time constraints, we were unable to fully integrate them. Despite this, the individual components work effectively, and integration will be prioritized in future updates.

-AP_Fetch Functionality: We’ve implemented an ap_fetch function that handles API requests to fetch the latest exchange rates. This ensures that the dashboard remains up-to-date with current market data.

#Prerequisites

-HTML

-CSS

-Python 3.0

-MySQL

-Required packages:Matplotlib,Pandas

#How to run

1.Clone the Repository or download the files.

2.Ensure the CSV files are placed in the correct folder specified in the csv_folder variable.

3.Run the Python script.



## Deployment

To run this project run

1.Clone the repository to your local machine.
```bash
  git clone <repository-url>
  cd proj
```
2.Install the required packages.
```bash
  pip intall flask
```
3.Run the application.
```bash
  python app.py
```
4.Follow On-Screen Prompts:

-Select Currency 1

-Select Currency 2

-Select Year

-Choose the Duration for the Graph

-Display the Graph

5.View Exchange Rate Database:

Download and use SQLite Browser to view exchange_rate.db.



