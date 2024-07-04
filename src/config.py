import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    GOAHEAD = "Go Ahead"
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    MODEL_NAME_llama = "llama3-70b-8192"
    MODEL_NAME_35 = "gpt-3.5-turbo"
    MODEL_NAME_4o = "gpt-4o"
  
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_FILE_PATH = os.path.join(BASE_DIR, "staging", "detailed_table_descriptions.csv")
  

    
    examples = [
    {
        "input": "Find all market data entries recorded on 2024-03-28",
        "query": "SELECT * FROM market_data WHERE market_date = '2024-03-28';"
    },
    {
        "input": "List all clients who are of type 'Coporate'",
        "query": "SELECT * FROM clients WHERE client_type = 'Coporate';"
    },
    {
        "input": "Show the names and contact information of clients",
        "query": "SELECT client_name, contact_info FROM clients;"
    },
    {
        "input": "Get the details of derivative products that mature after January 1, 2025",
        "query": "SELECT * FROM derivative_products WHERE maturity_date > '2025-01-01';"
    },
    {
        "input": "Retrieve market data for the product with product_id 55",
        "query": "SELECT * FROM market_data WHERE product_id = 55;"
    },
    {
        "input": "Find all transactions that were 'buy' transactions",
        "query": "SELECT * FROM transactions WHERE transaction_type = 'buy';"
    },
    {
        "input": "List the names of all users",
        "query": "SELECT name FROM users;"
    },
    {
        "input": "Get the transaction details where the client_id is 124",
        "query": "SELECT * FROM transactions WHERE client_id = 124;"
    },
    {
        "input": "Show the product names and their underlying assets",
        "query": "SELECT product_name, underlying_asset FROM derivative_products;"
    },
    {
        "input": "List all clients along with their transactions",
        "query": "SELECT clients.client_name, transactions.* FROM clients JOIN transactions ON clients.client_id = transactions.client_id;"
    },
    {
        "input": "Summarize the total financial volume of transactions for each client",
        "query": "SELECT clients.client_name, SUM(transactions.transaction_price * transactions.quantity) AS total_volume FROM transactions JOIN clients ON transactions.client_id = clients.client_id GROUP BY clients.client_name;"
    },
    {
        "input": "Find the top clients by transaction volume for each product",
        "query": "SELECT derivative_products.product_name, clients.client_name, SUM(transactions.quantity) AS total_quantity FROM transactions JOIN clients ON transactions.client_id = clients.client_id JOIN derivative_products ON transactions.product_id = derivative_products.product_id GROUP BY derivative_products.product_name, clients.client_name ORDER BY derivative_products.product_name, total_quantity DESC;"
    },
    {
        "input": "Show the total transaction volume for each product type",
        "query": "SELECT product_type, SUM(quantity) AS total_volume FROM transactions JOIN derivative_products ON transactions.product_id = derivative_products.product_id GROUP BY product_type;"
    },
    {
        "input": "List the top 5 clients by total transaction volume",
        "query": "SELECT clients.client_name, SUM(transactions.quantity) AS total_volume FROM transactions JOIN clients ON transactions.client_id = clients.client_id GROUP BY clients.client_name ORDER BY total_volume DESC LIMIT 5;"
    },
    {
        "input": "Find the average transaction price for each product type",
        "query": "SELECT derivative_products.product_type, AVG(transactions.transaction_price) AS avg_price FROM transactions JOIN derivative_products ON transactions.product_id = derivative_products.product_id GROUP BY derivative_products.product_type;"
    },
    {
        "input": "Calculate the total volume of market data for each product",
        "query": "SELECT derivative_products.product_name, SUM(market_data.volume) AS total_volume FROM market_data JOIN derivative_products ON market_data.product_id = derivative_products.product_id GROUP BY derivative_products.product_name;"
    },
    {
        "input": "Show the maximum transaction price for each client",
        "query": "SELECT clients.client_name, MAX(transactions.transaction_price) AS max_price FROM transactions JOIN clients ON transactions.client_id = clients.client_id GROUP BY clients.client_name;"
    },
    {
        "input": "Get the number of transactions for each product type",
        "query": "SELECT derivative_products.product_type, COUNT(transactions.transaction_id) AS transaction_count FROM transactions JOIN derivative_products ON transactions.product_id = derivative_products.product_id GROUP BY derivative_products.product_type;"
    },
    {
        "input": "Find the minimum market price recorded for each product",
        "query": "SELECT derivative_products.product_name, MIN(market_data.market_price) AS min_price FROM market_data JOIN derivative_products ON market_data.product_id = derivative_products.product_id GROUP BY derivative_products.product_name;"
    },
    {
        "input": "Calculate the average volume of market data for currency products",
        "query": "SELECT AVG(market_data.volume) AS avg_volume FROM market_data JOIN derivative_products ON market_data.product_id = derivative_products.product_id WHERE derivative_products.product_type = 'Currency';"
    },
    {
        "input": "Show the total quantity of transactions for each client and product",
        "query": "SELECT clients.client_name, derivative_products.product_name, SUM(transactions.quantity) AS total_quantity FROM transactions JOIN clients ON transactions.client_id = clients.client_id JOIN derivative_products ON transactions.product_id = derivative_products.product_id GROUP BY clients.client_name, derivative_products.product_name;"
    }
]

    system_prefix = """You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct MYSQL query to run, then look at the results of the query and return the answer.
    Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
    You can order the results by a relevant column to return the most interesting examples in the database.
    Never query for all the columns from a specific table, only ask for the relevant columns given the question.
    You have access to tools for interacting with the database.
    Only use the given tools. Only use the information returned by the tools to construct your final answer.
    You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

    If the question does not seem related to the database, just return "I don't know the answer" as the answer.

    Here are some examples of user inputs and their corresponding SQL queries:"""

    evaluator_agent_template = """
    Please evaluate the following user input and determine if it is appropriate for further processing. Your task is to analyze the input for any signs of offensive content, irrelevance to the query, bias, or inappropriate language (including slurs or insults). Based on your analysis, return one of the following responses:

    - "Stop" if the input contains any offensive, irrelevant, biased, or inappropriate language.
    - "Go Ahead" if the input is appropriate and relevant.

    User Input: {user_input}

    Evaluation Criteria:
    1. Offensive Content: Check if the input contains any offensive language or slurs.
    2. Relevance: Ensure the input is relevant to the query or topic being discussed.
    3. Bias: Identify any biased statements or discriminatory language.
    4. Inappropriate Language: Look for any inappropriate or unprofessional language.
    5. Negative sentiment analysis

    YOU MUST RESPOND ONLY ONE OF THE OPTIONS BELOW:

    - "Stop" if any of the criteria above are met.
    - "Go Ahead" if none of the criteria above are met.
    """
