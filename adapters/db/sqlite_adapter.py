import sqlite3

class SQLiteAdapter:
    def __init__(self, db_path):
        self.db_path = db_path

    def __call__(self, *args, **kwds):
        return "sqlite3"
    
    def get_tables_and_schema(self):
        """Retrieve all tables and their schemas in the SQLite database."""
        conn = sqlite3.connect(self.db_path)
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

    def execute_query(self, sql_query):
        """Execute the given SQL query on the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.executescript(sql_query)
            results = []
            if "select" in sql_query.lower():
                sql_query = sql_query.split(";")
                for query in sql_query:
                    if "select" in query.lower():
                        cursor.execute(query)
                        results.extend(cursor.fetchall())
                    results.append("\n")
            conn.commit()
            return {"success": True, "results": results}
        except sqlite3.OperationalError as e:
            return {"success": False, "error": str(e)}
        finally:
            conn.close()
