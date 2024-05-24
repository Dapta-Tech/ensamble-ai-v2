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
import os
from glob import glob
import pandas as pd
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain_community.agent_toolkits import create_sql_agent

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

def consultar_datos_por_municipio(consulta, query, municipio):
    print("step 1")

    print("step 2")

    engine = create_engine(
        "postgresql://clients:bZqbYHeEA2x$Qa6KxnYVkX@clients.cluster-c9w8clqzjjhu.us-east-2.rds.amazonaws.com:5432/fip_db_ai_model"
    )

    db = SQLDatabase(engine=engine)
    print(db.get_usable_table_names())

    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
    response = agent_executor.invoke(f"{query}, Municipio: {municipio}")
    print(response)
    return response

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

@tool
def get_my_information_from_database(consulta: str, municipio:str) -> str:
    """Consultar información de los delitos desde el CSV"""
    return consultar_datos_por_municipio("",consulta, municipio)


#Build chain
def Chain_with_tool(municipio):
    tools = [get_my_information_from_database, get_general_information_from_PDFs]

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"""
                Eres un asistente diseñado para responder preguntas sobre la creación de Planes Integrales de Seguridad y Convivencia Ciudadana (PISCC) del municipio de {municipio}.
                    1. Información sobre delitos: Si deseas obtener información sobre los delitos en un municipio, puedo utilizar los datos de los archivos CSV disponibles.    
                    2. Información general de documentos de política pública: Si deseas obtener información general de creación de PISCC, leyes o política pública, puedo utilizar la base vectorial de Pinecone. 
                    Puedo utilizar las herramientas ("TOOLS") disponibles para proporcionar la información indicada que necesitas para crear un documento PISCC para mi municipio.
                    IMPORTANTE: 
                    - La columna llamada "Estadísticas (1)" representa delitos.
                    - En caso de que no se especifique el municipio, se asumirá que se está hablando de {municipio}.
                    
                    ###
                    Municipios disponibles: Input === Nombre de columna en el CSV
                    Bogotá === Bogotá, D.C. Cap.
                    Abrego === Ábrego (Nsa)
                    Bolivar === Bolívar (Vac)
                    Buenavista === Buenavista (Cor)

                    ###
                    Columnas.
                    Delitos === Estadísticas (1)

                    ###
                    CATERGORIAS DE DELITOS:
                    
                    Delito sexual === Tema: "Agresiones contra la Integridad Personal" | Estadísticas (1): "Delito Sexual ( Exámenes medicolegales )"
                    Extorsión === Tema: "Secuestro _ Extorsión" | Estadísticas (1): "Extorsión ( Personas Víctimas )"
                    Homicidio (incluye abatidos) === Tema: "Agresiones contra la Integridad Personal" | Estadísticas (1): "idio - incluye abatidos (INML) ( Personas Víctimas )"
                    Homicidio (Totales) === Tema: "Agresiones contra la Integridad Personal" | Estadísticas (1): "Homicidio - Totales (Min Def) ( Personas Víctimas )"
                    Hurto a personas === Tema: "Hurto _ Delitos contra el patrimonio económico" | Estadísticas (1): "Hurto a Personas ( Personas Víctimas )"
                    Hurto a comercios === Tema: "Hurto _ Delitos contra el patrimonio económico" | Estadísticas (1): "Hurto a Comercios ( Personas Víctimas )"
                    Hurto a residencias === Tema: "Hurto _ Delitos contra el patrimonio económico" | Estadísticas (1): "Hurto a Residencias ( Personas Víctimas )"
                    Hurto a automoviles === Tema: "Hurto _ Delitos contra el patrimonio económico" | Estadísticas (1): "Hurto de Automotores ( Unidades )"
                    Lesiones violencia interpersonal === Tema: "Agresiones contra la Integridad Personal" | Estadísticas (1): "Lesiones Violencia Interpersonal ( Personas Víctimas )"
                    Secuestro === Tema: "Secuestro _ Extorsión" | Estadísticas (1): "Secuestro ( Personas Víctimas )"
                    Violencia intrafamiliar === Tema: "Agresiones contra la Integridad Personal" | Estadísticas (1): "Violencia Intrafamiliar ( Personas Víctimas )"
        
                    ###
                    Ejemplo de consulta:
                    Input === "3 delitos más frecuentes el año 2021 en Bogotá" ||| municipio === "Bogotá D.C." query === "3 delitos más frecuentes el año 2021"
                    Output: "Los 3 delitos más frecuentes en Bogotá D.C. el año 2021 son: ..."
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

test_agent = Chain_with_tool(municipio="Ábrego (Nsa)")

#query = "Cómo construir un piscc?"
query = "Delito más frecuentes el año 2021 en Bogotá"
print(test_agent.invoke({"conversation_history": [], "input": query}))