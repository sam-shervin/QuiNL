from adapters.db.sqlite_adapter import SQLiteAdapter
from adapters.llm.llm_ollama import OllamaAdapter
from adapters.llm.llm_openai import OpenAIAdapter

def main(llm_adapter, db_adapter):
    while True:
        schema_dict = db_adapter.get_tables_and_schema()
        nl_request = input("\n\nEnter a natural language request (or 'exit' to quit): ")
        print("Processing request...\n\n")
        if nl_request.lower() == "exit":
            break
        try:
            sql_query = llm_adapter.generate_sql(nl_request, schema_dict)
            print("Generated SQL Query:", sql_query, "\n")
            result = db_adapter.execute_query(sql_query)
            if result["success"]:
                if len(result["results"]) != 0:
                    print("Query Results:")
                    for row in result["results"]:
                        print(row)
                else:
                    print("Query executed successfully.")
            else:
                print(f"Error: {result['error']}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    db_adapter = SQLiteAdapter(db_path="your_database.db")
    schema_dict = db_adapter.get_tables_and_schema()

    llm_choice = input("Choose LLM (1: Ollama, 2: OpenAI): ").strip()
    if llm_choice == "1":
        llm_adapter = OllamaAdapter(model="llama3.2") # You can choose a different model from https://ollama.com/library
    elif llm_choice == "2":
        api_key = input("Enter OpenAI API key: ").strip()
        llm_adapter = OpenAIAdapter(api_key=api_key)
    else:
        print("Invalid choice. Exiting.")
        quit()

    print("Schema loaded:")
    for table, schema in schema_dict.items():
        print(f"Table: {table}")
        for column in schema:
            print(f" - Column: {column[1]}, Type: {column[2]}")
        print("\n")

    main(db_adapter=db_adapter, llm_adapter=llm_adapter)
