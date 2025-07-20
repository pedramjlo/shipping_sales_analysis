import pandas as pd
import streamlit as st
import psycopg2
import sqlparse


from database_utils.databaseUtils import Database



# Function to connect to PostgreSQL database
def connect_to_db():
    db = Database()
    return db.get_connection()



# Function to read SQL file and execute queries
def read_and_execute_sql_file(file_path, conn):
    try:
        with open(file_path, 'r') as f:
            sql_content = f.read()
        
        # Split the SQL content into individual queries
        queries = sqlparse.split(sql_content)
        
        results = []
        for query in queries:
            query = query.strip()
            if query:  # Ignore empty queries
                try:
                    with conn.cursor() as cur:
                        cur.execute(query)
                        if cur.description is not None:  # Query returned results (e.g., SELECT)
                            results.append((query, cur.fetchall(), cur.description))
                        else:  # Query did not return results (e.g., INSERT, UPDATE)
                            conn.commit()
                            results.append((query, f"Query executed successfully. Rows affected: {cur.rowcount}", None))
                except psycopg2.Error as e:
                    results.append((query, f"Error executing query: {e}", None))
        
        return results
    except FileNotFoundError:
        st.error("SQL file not found.")
        return []

# Streamlit app
st.title("SQL Query Executor")

# Load SQL file
sql_file_path = 'analysis/descriptive_analysis/sql/main.sql'

if st.button("Execute SQL Queries"):
    conn = connect_to_db()
    if conn is not None:
        results = read_and_execute_sql_file(sql_file_path, conn)
        for i, (query, result, description) in enumerate(results):
            st.write(f"### Query {i+1}")
            st.code(query, language='sql')
            if description is not None:
                columns = [desc[0] for desc in description]
                st.write(pd.DataFrame(result, columns=columns))
            else:
                st.write(result)
        conn.close()
