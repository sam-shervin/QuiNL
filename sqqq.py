import sqlite3
import ollama

def get_tables_and_schema(db_path):
    """Retrieve all tables and their schemas in the SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]

    schema_dict = {}

    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        schema = cursor.fetchall()
        schema_dict[table] = schema

    conn.close()
    return schema_dict

def interpret_natural_language_request(nl_request, schema_dict):
    """
    Convert natural language request to SQL query using LLaMA 3.1 model via Ollama API.
    """
    schema_info = "\n".join([f"Table: {table}\n" + "\n".join([f" - Column: {col[1]}, Type: {col[2]}" for col in schema]) for table, schema in schema_dict.items()])
    prompt = f"Sqlite3 Database schema:\n{schema_info}\n\nConvert the following natural language request to an sqlite3 SQL query: {nl_request}"

    response = ollama.chat(model='llama3.2', messages=[     # change model to your desired model -  llama3.1, llama3.2, 
                                                            #                                       llama3, llama2, qwen2.5-coder:0.5b
                                                            #                                       qwen2.5-coder:1.5b, 
        {
            'role': 'user',
            'content': prompt,
        },
    ])

    sql_query = response['message']['content'].strip()
    return sql_query

# Example usage:
db_path = 'your_database.db'
schemas = get_tables_and_schema(db_path)

for table, schema in schemas.items():
    print(f"Table: {table}")
    for column in schema:
        print(f" - Column: {column[1]}, Type: {column[2]}")
    print("\n")

# Example of using the LLM integration
# nl_request = "Join the users table and the orders table using the user_id column and display the results"
# nl_request = "Get the names of all users who have placed an order"
# nl_request = "Get the total number of orders placed by each user"
# nl_request = "Insert a new user with the name 'Sam Shervin S' and age 20"
# nl_request = "Display everything in the users table"

while True:
    nl_request = input("Enter a natural language request: ")
    if nl_request.lower() == "exit":
        break
    sql_query = interpret_natural_language_request(nl_request, schemas)
    if "```sql" in sql_query:
        sql_query = sql_query.split("```sql")[1].strip()
        if "```" in sql_query:
            sql_query = sql_query.split("```")[0].strip()

    print("Generated SQL Query:", sql_query)

    # Execute the generated SQL query
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript(sql_query)

    # if select in sql_query, get all the select commands with the help of semicolons and send to cursor.execute()
    if "select" in sql_query.lower():
        sql_query = sql_query.split(";")
        for query in sql_query:
            if "select" in query.lower():
                print("Executing query:", query)
                cursor.execute(query)
                results = cursor.fetchall()

                for row in results:
                    print(row)

    conn.commit()
    conn.close()
    print("Command executed successfully.\n")
