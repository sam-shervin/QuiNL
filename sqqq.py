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
    prompt = f"Database schema:\n{schema_info}\n\nConvert the following natural language request to an SQL query: {nl_request}"

    response = ollama.chat(model='llama3.1', messages=[
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
nl_request = "List all users with an age above 30."
sql_query = interpret_natural_language_request(nl_request, schemas)
print("Generated SQL Query:", sql_query)

# Execute the generated SQL query
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute(sql_query)
results = cursor.fetchall()

for row in results:
    print(row)

conn.close()