import streamlit as st
import sqlite3
from langchain_helper import get_few_shot_db_chain  # Assuming you have this function in langchain_helper

st.title("M Bazar: Database Q&A 👕")

question = st.text_input("Question: ")

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

if question:
    # Get the few-shot database chain
    chain = get_few_shot_db_chain()
    
    # Run the chain with the user's question
    response = chain.run(question)

    # Display the answer
    st.header("Answer")
    st.write(response)

    # Assuming response contains SQL query
    if response.startswith("SELECT"):
        # Execute the SQL query and fetch data
        data = read_sql_query(response, "clothing.db")
        
        # Display fetched data
        st.write("Fetched Data:")
        st.write(data)
