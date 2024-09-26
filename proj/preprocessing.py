import pandas as pd
import glob
import sqlite3
from sqlalchemy import create_engine
import os

# Function to preprocess data - filling missing values
def fill_missing_values():
    path = r"C:\Users\Gargee Patil\OneDrive\Desktop\Northern Trust Hackathon\Currency Conversion Rate Data"
    # Reading CSV files in folder
    files = glob.glob(path + "/*.csv")
    
    for file in files:
        print(f"Processing file: {file}")  # Print the file name being processed
        df = pd.read_csv(file)  # Read the CSV file
        
        # Fill missing values in each column except 'Date'
        for column in df.columns:
            if column == 'Date':
                continue  # Skip the Date column

            # Forward fill for the current column using ffill()
            df[column] = df[column].ffill()
            
            # Fill remaining NaNs with the column mean 
            if df[column].isnull().sum() > 0:  # Check if there are still missing values
                mean_value = df[column].mean()  # Calculate mean
                df[column].fillna(mean_value, inplace=True)  # Fill with mean value

        # Save the updated DataFrame back to the same CSV file
        try:
            df.to_csv(file, index=False)  # Save the DataFrame back to the original file
            print(f"Successfully saved: {file}")
        except Exception as e:
            print(f"Error saving file {file}: {e}")

def create_or_append_database():
    conn = sqlite3.connect('mydb5.db')
    engine = create_engine('sqlite:///mydb5.db')
    path = r"C:\Users\Gargee Patil\OneDrive\Desktop\Northern Trust Hackathon\Currency Conversion Rate Data"
    files = glob.glob(path + "/*.csv")

    for file in files:
        df = pd.read_csv(file)
        
        # Existing column check
        print(f"Processing file: {file}")
        print(f"DataFrame columns before renaming: {df.columns.tolist()}")

        # Check for whitespace and strip it from 'Date' column
        df['Date'] = df['Date'].str.strip()

        # Convert Date to datetime format
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Remove time component and keep only date
        df['Date'] = df['Date'].dt.date

        # Drop rows with NaT in 'Date'
        df = df.dropna(subset=['Date'])

        # Format table name based on file name
        table_name = os.path.basename(file).replace('.csv', '')

        # Drop existing table if it exists
        conn.execute(f'DROP TABLE IF EXISTS {table_name};')

        # Change column names to just the three-letter currency code (if available)
        new_column_names = {
            col: col.split('(')[-1].strip().replace(')', '').replace(' ', '') 
            for col in df.columns if col != 'Date'
        }

        # Rename the columns
        df.rename(columns=new_column_names, inplace=True)

        # Create table with new schema
        conn.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                Date DATE PRIMARY KEY,
                {', '.join([f'"{col}" REAL' for col in df.columns if col != 'Date'])}
            );
        ''')

        # Append new data
        new_data = df[~df['Date'].isin(pd.read_sql(f"SELECT Date FROM {table_name};", conn)['Date'])]
        if not new_data.empty:
            new_data.to_sql(table_name, con=engine, if_exists='append', index=False)
        else:
            print(f"No new data to append from {file} (all dates already exist in the database).")
    
    conn.close()

# Call the functions
fill_missing_values()  # Preprocess the CSV files
create_or_append_database()  # Create or append to the database
