import openai

class OpenAIAdapter:
    def __init__(self, api_key, model="gpt-4"):
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key

    def generate_sql(self, nl_request, schema_dict):
        """Convert natural language request to SQL using OpenAI API."""
        schema_info = "\n".join([
            f"Table: {table}\n" + "\n".join([f" - Column: {col[1]}, Type: {col[2]}" for col in schema])
            for table, schema in schema_dict.items()
        ])
        prompt = (
            f"Sqlite3 Database schema:\n{schema_info}\n\n"
            f"Convert the following natural language request to an sqlite3 SQL query: {nl_request}"
        )

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        sql_query = response['choices'][0]['message']['content'].strip()
        if "```sql" in sql_query:
            sql_query = sql_query.split("```sql")[1].strip()
            if "```" in sql_query:
                sql_query = sql_query.split("```")[0].strip()
        return sql_query
