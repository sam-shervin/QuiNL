import ollama

class OllamaAdapter:
    def __init__(self, model="llama3.2"):
        self.model = model

    def generate_sql(self, nl_request, schema_dict):
        """Convert natural language request to SQL using Ollama API."""
        schema_info = "\n".join([
            f"Table: {table}\n" + "\n".join([f" - Column: {col[1]}, Type: {col[2]}" for col in schema])
            for table, schema in schema_dict.items()
        ])
        prompt = (
            f"Sqlite3 Database schema:\n{schema_info}\n\n"
            f"Convert the following natural language request to an sqlite3 SQL query: {nl_request}"
        )

        response = ollama.chat(model=self.model, messages=[
            {"role": "user", "content": prompt}
        ])

        sql_query = response['message']['content'].strip()
        if "```sql" in sql_query:
            sql_query = sql_query.split("```sql")[1].strip()
            if "```" in sql_query:
                sql_query = sql_query.split("```")[0].strip()
        return sql_query
