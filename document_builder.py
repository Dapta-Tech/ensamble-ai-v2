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
    print (cadena_resultado)
    return cadena_resultado

#Crear la función 
if __name__ == "__main__":
    llm = get_llm()

    question = "Genera el documento para la gestión 2024"
    municipio = "El Banco (Mag)"

    delitos_mes_a_mes = get_delitos_mes_a_mes(municipio)

    vector_bases = load_bases(index_name="all-data-v1", 
                            bases_list=["1-Politica-Publica",
                                        "4-Base-estrategias"])
    
    LOTR = get_LOTR(vector_bases)

    prompt = ChatPromptTemplate.from_template(prompts["Diagnostico 3.1"])

    chain = chain(LOTR, llm, prompt)

    response = get_response(question,delitos_mes_a_mes,municipio,chain)

    print(response)