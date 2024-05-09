import time
import os
import pandas as pd
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain.retrievers import (MergerRetriever,)
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from operator import itemgetter
from prompts import prompts
from langchain_core.prompts import ChatPromptTemplate

# Streamed response emulator
def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.02)

#Load bases from a list of namespaces
def load_bases(index_name= "", bases_list = []):
    pc = Pinecone()
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    text_field = "text"
    big_vector = []
    for i in bases_list:
        vectorstore = PineconeVectorStore(pc.Index(index_name), embeddings, text_field, namespace = i)
        big_vector.append(vectorstore)
        vectorstore = None
    return big_vector

#Create a Lorf Of the Retreivers from a vector collection.
def get_LOTR(big_vector):
    LOTR = []
    
    for vector_store in big_vector:
        LOTR.append(vector_store.as_retriever())
    
    return MergerRetriever(retrievers=LOTR)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_llm():
    llm = ChatOpenAI(
    model_name='gpt-4-turbo',
    temperature=0.5,
    max_tokens=4096)
    return llm

#Gets the response from the conversational RAG chain.
def chain(LOTR, llm, prompt):
    llm = get_llm()
    retriever = LOTR
    chain = (
    {
        "context": itemgetter("question") | retriever,
        "question": itemgetter("question"),
        "delitos_mes_a_mes": itemgetter("delitos_mes_a_mes"),
        "municipio": itemgetter("municipio")
    }
    | prompt
    | llm
    | StrOutputParser())
    return chain

def get_response(question,delitos_mes_a_mes,municipio,chain):

    response = chain.invoke({"question": question, 
                            "delitos_mes_a_mes": delitos_mes_a_mes, 
                            "municipio": municipio})
    return response

def get_delitos_mes_a_mes(municipio):
    file_path = "data/indicadores mes a mes/"
    dfs = []

    for archivo in os.listdir(file_path):
        if archivo.endswith('.csv'):
            ruta_completa = os.path.join(file_path, archivo)
            df = pd.read_csv(ruta_completa)
            df.rename(columns={'Estadísticas (1)': 'delitos'}, inplace=True)
            
            # Filtrar por municipio
            df_municipio = df[df['Municipio'] == municipio]
            
            dfs.append(df_municipio)
            
    df_completo = pd.concat(dfs)

    # Agrupar por año y delitos y calcular el total de delitos
    df_agrupado = df_completo.groupby(['Año', 'delitos']).size().reset_index(name='total')
    df_final = df_agrupado[['Año', 'delitos', 'total']]

    # Ordenar por delito y luego por año
    df_final = df_final.sort_values(by=['delitos', 'Año'])

    # Cadena con la estructura``
    cadena_resultado = ""
    for index, row in df_final.iterrows():
        cadena_resultado += f"El total del delito: {row['delitos']}, en el año: {row['Año']}, fue de: {row['total']}\n"
    print ('------------------cadena_resultado---------------------')
    print (cadena_resultado)
    return cadena_resultado

def get_delitos_tpcmh(municipio):
    file_path = "data/indicadores tpcmh/"
    dfs = []

    columnas_a_usar = ['Municipio', '2019', '2020', '2021', '2022', '2023']

    for archivo in os.listdir(file_path):
        if archivo.endswith('.csv'):
            ruta_completa = os.path.join(file_path, archivo)
            
            try:
                # Leer el archivo, suponiendo que todas las columnas son relevantes
                df = pd.read_csv(ruta_completa, low_memory=False)
                
                # Filtrar por municipio y añadir columna de tipo de delito
                df_municipio = df[df['Municipio'] == municipio].copy()
                tipo_delito = archivo.replace('.csv', '')
                df_municipio.loc[:, 'Tipo delito'] = tipo_delito
                
                # Melt para transformar años en filas
                df_melted = df_municipio.melt(id_vars=['Municipio', 'Tipo delito'], var_name='Año', value_name='Incidentes')
                dfs.append(df_melted)
            
            except Exception as e:
                print(f"Error al procesar {archivo}: {e}")

    # Concatenar todos los dataframes
    df_completo = pd.concat(dfs, ignore_index=True)
    
    # Agrupar por año y tipo de delito y calcular el total de incidentes
    df_agrupado = df_completo.groupby(['Año', 'Tipo delito']).sum().reset_index()
    df_final = df_agrupado[['Año', 'Tipo delito', 'Incidentes']]
    
    # Ordenar por tipo de delito y luego por año
    df_final = df_final.sort_values(by=['Tipo delito', 'Año'])
    
    # Construir la cadena de resultado
    cadena_resultado = ""
    for index, row in df_final.iterrows():
        cadena_resultado += f"El total del delitos por TPCMH: {row['Tipo delito']}, en el año: {row['Año']}, fue de: {row['Incidentes']}\n"
    print ('------------------cadena_resultado TPCMH---------------------')
    print (cadena_resultado)
    return cadena_resultado

#Crear la función 
if __name__ == "__main__":
    llm = get_llm()

    question = "Genera el documento para la gestión 2024"
    municipio = "El Banco (Mag)"

    delitos_mes_a_mes = get_delitos_mes_a_mes(municipio)
    delitos_tpcmh = get_delitos_tpcmh(municipio)

    vector_bases = load_bases(index_name="all-data-v1", 
                            bases_list=["1-Politica-Publica",
                                        "4-Base-estrategias"])
    
    LOTR = get_LOTR(vector_bases)

    prompt = ChatPromptTemplate.from_template(prompts["Diagnostico 3.1"])

    chain = chain(LOTR, llm, prompt)

    response = get_response(question,delitos_mes_a_mes,municipio,chain)

    print(response)