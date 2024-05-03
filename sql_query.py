from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

def connect_to_database(uri):
    return SQLDatabase.from_uri(uri)

def get_table_names(database):
    return database.get_usable_table_names()

def run_sql_query(database, query):
    return database.run(query)

def create_chat_chain(model, database):
    return create_sql_query_chain(model, database)

def ask_question(chain, question):
    return chain.invoke({"question": question})

if __name__ == "__main__":
    URI = "sqlite:///Chinook.db"
    
    db = connect_to_database(URI)

    print(get_table_names(db))
    print(run_sql_query(db, "SELECT * FROM Artist LIMIT 10;"))

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    chain = create_chat_chain(llm, db)
    response = ask_question(chain, "How many employees are there")
    print(response)