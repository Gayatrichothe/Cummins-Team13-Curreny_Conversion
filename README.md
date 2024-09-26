# Cummins-Team13-Curreny_Conversion

# Currency Exchange Rate

The Currency Exchange Rate Analysis Dashboard allows users to analyze and visualize exchange rates between two currencies over a specified duration. This project uses historical exchange rate data and provides an interactive menu for users to select currencies, choose durations for analysis, and view trends through graphical representations.

# Features
-Dynamic Currency Selection: Users can select any two currencies from the available options.

-Flexible Time Durations: Options to view data in weekly, monthly, quarterly, or yearly formats.

-Graphical Visualization: Provides clear and informative graphs displaying exchange rate trends.

-Data Loading: Automatically loads exchange rate data from CSV files stored in a designated folder.

-Database Integration: A database has been created to store the processed data for efficient retrieval and analysis.

-Data Preprocessing: The dataset has been preprocessed to ensure accuracy, including handling missing values, removing duplicates, and formatting dates.

-The dashboard allows users to create a custom currency basket by selecting three currencies and assigning weights to each. It ensures that the total weights add up to 100% for accurate calculations. Based on the selected weights and current exchange rates, the dashboard computes the basket's value and displays it in USD.

#Prerequisites

-HTML

-CSS

-Python 3.0

-MySQL

-Required packages:Matplotlib,Pandas

#How to run

#Usage
-Clone the Repository or download the files.

-Ensure the CSV files are placed in the correct folder specified in the csv_folder variable.

-Run the Python script.

-Follow the on-screen prompts to:

    *Select Currency 1
    
    *Select Currency 2
    
    *Select year
    
    *Choose the duration for the graph
    
    *Display the graph
    
#To view exchange_rate.db 

Download https://sqlitebrowser.org/






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



