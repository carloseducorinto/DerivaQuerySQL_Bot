import os
import mysql.connector
import pymysql
from config import Config
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.tools import QuerySQLDataBaseTool
import pandas as pd


def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data:
            cursor.executemany(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Exception as e:
        print(f"The error '{e}' occurred")    

#['clients', 'derivative_products', 'market_data', 'transactions', 'users']

def process_database():
       
    dbuser = Config.DB_user
    dbpassword = Config.DB_password
    dbname = Config.DB_name
    dbhost = Config.DB_host
    dbport = Config.DB_port

    #connection = mysql.connector.connect(
    #host=dbhost,
    #user=dbuser,
    #password=dbpassword,
    #database=dbname
    #)
    
    db = SQLDatabase.from_uri(f"mysql+pymysql://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbname}")
  
    print(db.dialect)
    print('-------------\n')
    print(db.get_usable_table_names())
    print('\n-------------')
    print(db.table_info)

    #query = "DELETE FROM users"
    #execute_query(connection, query, data=None)

    print("Batch job completed successfully")

def table_information_deatailed():
    # Define the detailed table information
    data = {
        "Table Name": ["clients", "derivative_products", "market_data", "transactions"],
        "Table Description": [
            "Stores information about clients. Columns: client_id (unique identifier, auto-incremented), client_name (name of the client), client_type (type of client, e.g., individual, corporate), contact_info (contact information).",
            "Stores information about derivative products. Columns: product_id (unique identifier, auto-incremented), product_name (name of the product), product_type (type of derivative product, e.g., option, future, swap), underlying_asset (underlying asset), contract_size (size of the contract), maturity_date (maturity date).",
            "Stores market data relevant to the derivative products. Columns: market_data_id (unique identifier, auto-incremented), product_id (references product_id in derivative_products), market_date (date of the market data), market_price (price on the market date), volume (trading volume).",
            "Stores information about transactions involving derivative products. Columns: transaction_id (unique identifier, auto-incremented), client_id (references client_id in clients), product_id (references product_id in derivative_products), transaction_date (date of the transaction), quantity (quantity involved), transaction_type (type of transaction, e.g., buy, sell), transaction_price (price of the transaction)."
        ]
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv(Config.CSV_FILE_PATH, index=False)
    print("Batch job completed successfully")



if __name__ == "__main__":
    #process_database()
    table_information_deatailed()