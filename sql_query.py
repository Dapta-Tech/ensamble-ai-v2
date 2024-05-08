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
    URI = "postgresql://clients:bZqbYHeEA2x$Qa6KxnYVkX@clients.cluster-c9w8clqzjjhu.us-east-2.rds.amazonaws.com:5432/fip_db_ai_model"

    db = connect_to_database(URI)

    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
    chain = create_chat_chain(llm, db)
    response = ask_question(chain, "Cuál es el objetivo macro de la estrategia llamada Generación de conocimiento sobre el fenómeno del abigeato ")
    print(response)
    #print("respuesta:", db.run(response))
