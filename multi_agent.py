import os
from glob import glob
import pandas as pd
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from pinecone import Pinecone
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import pandas as pd
from langchain.retrievers import (MergerRetriever,)

llm = ChatOpenAI(model_name="gpt-4-turbo", temperature=0)

# Función para cargar CSVs desde una carpeta
def load_csvs_from_folder(folder_path):
    csv_files = glob(os.path.join(folder_path, "*.csv"))
    data_frames = [pd.read_csv(file, low_memory=False) for file in csv_files]
    return pd.concat(data_frames, ignore_index=True)

#Función para crear el agente CSV
def CSV_agent(df, query):
    agent = create_pandas_dataframe_agent(
    llm,
    df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,)
    agent.invoke(query)

#Función para cargar múltiples bases de datos desde Pinecone
def load_bases():
    index_name= "all-data-v1"
    bases_list = ["1-Politica-Publica_PISCC-por-Municipio",
                "1-Politica-Publica_Fiscal",
                "1-Politica-Publica_Documentos-Politica",
                "1-Politica-Publica_Leyes-Decretos"]
    pc = Pinecone()
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    text_field = "text"
    big_vector = []
    for i in bases_list:
        vectorstore = PineconeVectorStore(pc.Index(index_name), embeddings, text_field, namespace = i)
        big_vector.append(vectorstore)
        vectorstore = None
    return big_vector

#Función para obtener el Lord of the retrievers
def get_retriever(big_vector):
    big_vector = load_bases()
    LOTR = []
    
    for vector_store in big_vector:
        LOTR.append(vector_store.as_retriever())
    retriever = MergerRetriever(retrievers=LOTR)
    return retriever

@tool
def get_crime_information_from_CSVs(consulta: str) -> str:
    """Consultar información de los delitos desde el CSV"""
    csv = load_csvs_from_folder("data\indicadores mes a mes")
    return CSV_agent(csv, consulta)

@tool   
def get_general_information_from_PDFs(consulta: str) -> str:
    """Consultar información general de los documentos de política pública desde la base vectorial de Pinecone"""
    big_vector = load_bases()
    retriever_chain = get_retriever(big_vector)
    return retriever_chain.invoke(consulta)

#Build chain
def Chain_with_tool():
    tools = [get_crime_information_from_CSVs, get_general_information_from_PDFs]

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                Eres un asistente diseñado para responder preguntas sobre la creación de Planes Integrales de Seguridad y Convivencia Ciudadana (PISCC).
                    1. Información sobre delitos: Si deseas obtener información sobre los delitos en un municipio, puedo utilizar los datos de los archivos CSV disponibles.    
                    2. Información general de documentos de política pública: Si deseas obtener información general de creación de PISCC, leyes o política pública, puedo utilizar la base vectorial de Pinecone. 
                    Puedo utilizar las herramientas ("TOOLS") disponibles para proporcionar la información indicada que necesitas para crear un documento PISCC para mi municipio.
                    IMPORTANTE: la columna llamada "Estadísticas (1)" representa delitos
                """,
            ),
            ("placeholder", "{conversation_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor

test_agent = Chain_with_tool()

#query = "Cómo construir un piscc?"
query = "cuantos municipios existen en la base de datos?"
print(test_agent.invoke({"conversation_history": [], "input": query}))