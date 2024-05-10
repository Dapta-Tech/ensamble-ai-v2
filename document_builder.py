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
from prompts import prompts_dict
from langchain_core.prompts import ChatPromptTemplate

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
def get_chain(LOTR, llm, prompt):
    llm = get_llm()
    retriever = LOTR
    chain = (
    {
        "context": itemgetter("question") | retriever,
        "question": itemgetter("question"),
        "delitos_mes_a_mes": itemgetter("delitos_mes_a_mes"),
        "tpcmh": itemgetter("tpcmh"),
        "municipio": itemgetter("municipio"),
        "seccion_context": itemgetter("seccion_context")
    }
    | prompt
    | llm
    | StrOutputParser())
    return chain

def get_response(question,delitos_mes_a_mes,tpcmh,municipio,seccion_context, chain):

    response = chain.invoke({"question": question, 
                            "delitos_mes_a_mes": delitos_mes_a_mes,
                            "tpcmh": tpcmh,
                            "municipio": municipio,
                            "seccion_context": seccion_context})
    return response

def get_delitos_mes_a_mes(municipio):
    file_path = "data/indicadores mes a mes/"

    archivos_csv = [archivo for archivo in os.listdir(file_path) if archivo.endswith('.csv')]

    datos = pd.concat([pd.read_csv(os.path.join(file_path, archivo), sep=',') for archivo in archivos_csv])

    datos = datos[datos['Municipio'] == municipio]

    datos.rename(columns={'Estadísticas (1)': 'delito'}, inplace=True)

    # Seleccionar las columnas requeridas
    columnas_requeridas = ["Tema", "delito", "Municipio", "Σ Cantidad", 
                        "Mayor de Edad", "Menor de edad", "Edad n.d.", "Masculino", 
                        "Femenino", "Año"]
    datos_seleccionados = datos[columnas_requeridas]

    suma_cantidad_por_año = datos_seleccionados.groupby(["Año", "delito", "Municipio"])["Σ Cantidad"].sum().reset_index()
    
    for index, row in suma_cantidad_por_año.iterrows():
        cadena = f"El   delito {row['delito']}, del municipio de {row['Municipio']} es igual a {row['Σ Cantidad']} en el año {row['Año']}"
        print(cadena)
    
    return cadena

def get_prompt_result(vectors, prompt, question, llm, delitos_mes_a_mes, tpcmh, municipio, seccion_context):
    
    vector_bases = load_bases(index_name="all-data-v1", bases_list=vectors)
    LOTR = get_LOTR(vector_bases)
    prompt = ChatPromptTemplate.from_template(prompt)
    chain = get_chain(LOTR, llm, prompt)

    response = get_response(question, 
                            delitos_mes_a_mes,
                            tpcmh,
                            municipio,
                            seccion_context,
                            chain)
    return response

#Crear la función 
if __name__ == "__main__":
    llm = get_llm()

    #municipio = "Ábrego (Nsa)"
    municipio = "Bogotá, D.C. Cap."
    #Pasar en minísculas, volver minúsculas

    delitos_mes_a_mes = get_delitos_mes_a_mes(municipio)

    question_1 = """Generar la sección 1. de Introducción del documento 
    piscc 2024-2027 en el municipio de {municipio} mencionando los principales retos del municipio"""

    prompt_result_1 = get_prompt_result(vectors = ["1-Politica-Publica_PISCC-por-Municipio",
                                        "4-Base-estrategias"],
                                        prompt = prompts_dict["1 Introducción"],
                                        question = question_1,
                                        llm = llm,
                                        delitos_mes_a_mes = delitos_mes_a_mes,
                                        tpcmh = "No hay registros",
                                        municipio = municipio,
                                        seccion_context = "")
    print(prompt_result_1)

    question_2 = """Generar la sección 2.Marco Normativo, donde se Menciona los 
    pilares constitucionales y normativos asociados a la convivencia y la seguridad 
    ciudadana en Colombia, sobre los cuales se debe alinear el PISCC.
    piscc 2024-2027 en el municipio de {municipio} mencionando los principales retos
    del municipio, incluye la infomración sobre Enfoque de discapacidad, Enfoque étnico 
    Enfoque de género del municipio de {municipio}"""

    prompt_result_2 = get_prompt_result(vectors = ["1-Politica-Publica_PISCC-por-Municipio",
                                        "1-Politica-Publica_Leyes-Decretos",
                                        "1-Politica-Publica_Documentos-Politica",
                                        "4-Base-estrategias"],
                                        prompt = prompts_dict["2 Marco Normativo"],
                                        question = question_2,
                                        llm = llm,
                                        delitos_mes_a_mes = delitos_mes_a_mes,
                                        tpcmh = "No hay registros",
                                        municipio = municipio,
                                        seccion_context = prompt_result_1)
    print(prompt_result_2)

    question_3 = """Generar la sección 3. Diagnóstico de la Situación de Seguridad y Convivencia Ciudadana 
    de el municipio de {municipio} donde darás información del actual alcalde de {municipio} y sus responsabilidades para 
    ejecutar el plan piscc 2024-2027"""
    prompt_result_3 = get_prompt_result(vectors = ["1-Politica-Publica",
                                        "4-Base-estrategias"],
                                        prompt = prompts_dict["3 Diagnostico 3.2"],
                                        question = question_3,
                                        llm = llm,
                                        delitos_mes_a_mes = delitos_mes_a_mes,
                                        tpcmh = "No hay registros",
                                        municipio = municipio,
                                        seccion_context = prompt_result_1)
    print(prompt_result_3)

    question_3_1 = """Generar la sección 3.1 Diagnóstico de la Situación de Seguridad y 
    Convivencia Ciudadana. de el municipio de {municipio}\
    con base en los siguientes delitos: {delitos_mes_a_mes}"""
    prompt_result_3_1 = get_prompt_result(vectors = ["1-Politica-Publica",
                                        "4-Base-estrategias"],
                                        prompt = prompts_dict["3 Diagnostico 3.1"],
                                        question = question_3_1,
                                        llm = llm,
                                        delitos_mes_a_mes = delitos_mes_a_mes,
                                        tpcmh = "No hay registros",
                                        municipio = municipio,
                                        seccion_context = prompt_result_3)
    print(prompt_result_3_1)

    question_3_2 = """Generar la sección 3.2 Diagnóstico de conflictividades. 
    de el municipio de {municipio} en el documento piscc 2024 \
    con base en los siguientes delitos: {delitos_mes_a_mes}"""

    prompt_result_3_2 = get_prompt_result(vectors = ["1-Politica-Publica",
                                            "4-Base-estrategias",
                                            "1-Politica-Publica_Fiscal" ],
                                            prompt = prompts_dict["3 Diagnostico 3.2"],
                                            question = question_3_2,
                                            llm = llm,
                                            delitos_mes_a_mes = delitos_mes_a_mes,
                                            tpcmh = "No hay registros",
                                            municipio = municipio,
                                            seccion_context = prompt_result_3_1)
    print(prompt_result_3_2)

    question_3_3 = """Generar la sección 3.3 Diagnóstico de comportamientos contrarios a la convivencia. 
    Tomando en cuenta principalmente comportamientos contrarios a la convivencia del municipio de {municipio}"""	

    prompt_result_3_3 = get_prompt_result(vectors = ["1-Politica-Publica",
                                            "4-Base-estrategias",
                                            "1-Politica-Publica_Fiscal" ],
                                            prompt = prompts_dict["3 Diagnostico 3.2"],
                                            question = question_3_3,
                                            llm = llm,
                                            delitos_mes_a_mes = delitos_mes_a_mes,
                                            tpcmh = "No hay registros",
                                            municipio = municipio,
                                            seccion_context = prompt_result_3_2)
    print(prompt_result_3_3)

    question_3_4 = """Generar la sección 3.4 Diagnóstico de delitos. 
    En esta sección realizarás un detalle minucioso sobre los delitos detallados en
    y en la tasa por cada cien mil habitantes (tpcmh) del municipio de {municipio} 
    enfocandose en el tema de género y etnia del municipio de {municipio} ."""	

    prompt_result_3_4 = get_prompt_result(vectors = ["1-Politica-Publica",
                                            "4-Base-estrategias",
                                            "1-Politica-Publica_Fiscal" ],
                                            prompt = prompts_dict["3 Diagnostico 3.4"],
                                            question = question_3_3,
                                            llm = llm,
                                            delitos_mes_a_mes = delitos_mes_a_mes,
                                            tpcmh = "No hay registros",
                                            municipio = municipio,
                                            seccion_context = prompt_result_3_3)
    print(prompt_result_3_4)


    question_4 = """Generar la sección 4. Focalización y Priorización para la Planeación. 
    para el municipio de {municipio}. donde identificarás factores para seleccionar los 3 delitos más frecuentes
    detallados en {delitos_mes_a_mes}, además de las leyes que respaldan dicha selección."""	

    prompt_result_4 = get_prompt_result(vectors = ["1-Politica-Publica",
                                            "1-Politica-Publica_Leyes_Politicas-Planes",
                                            "1-Politica-Publica_Fiscal",
                                            "4-Base-estrategias"],
                                            prompt = prompts_dict["4 Focalización"],
                                            question = question_4,
                                            llm = llm,
                                            delitos_mes_a_mes = delitos_mes_a_mes,
                                            tpcmh = "No hay registros",
                                            municipio = municipio,
                                            seccion_context = prompt_result_3_4)
    print(prompt_result_4)

    question_5 = """Generar la sección 5. Formulación Estratégica del PISCC 2024-2027. 
    para el municipio de {municipio}, donde identificarás las estrategias y planes que se deben tomar en cuenta basandose en los 
    delitos seleccionados en la sección anterior :{prompt_result_3_4}. Por ultimo menciona las responsabilidades con las estrategias
    del alclade de {municipio}."""	

    prompt_result_5 = get_prompt_result(vectors = ["1-Politica-Publica",
                                            "1-Politica-Publica_Leyes_Politicas-Planes",
                                            "4-Base-estrategias"],
                                            prompt = prompts_dict["4 Focalización"],
                                            question = question_5,
                                            llm = llm,
                                            delitos_mes_a_mes = delitos_mes_a_mes,
                                            tpcmh = "No hay registros",
                                            municipio = municipio,
                                            seccion_context = prompt_result_4)
    print(prompt_result_5)

    question_6 = """Generar la sección 6. Planeación Financiera y Operativa. del PISCC 2024-2027. 
    para el municipio de {municipio}, Usarás el presupuesto asignado para la gestión."""	

    prompt_result_6 = get_prompt_result(vectors = ["1-Politica-Publica",
                                            "1-Politica-Publica_Leyes_Politicas-Planes",
                                            "4-Base-estrategias",
                                            "2-Caracterizaion_Social_Presupuesto-General"],
                                            prompt = prompts_dict["4 Focalización"],
                                            question = question_6,
                                            llm = llm,
                                            delitos_mes_a_mes = delitos_mes_a_mes,
                                            tpcmh = "No hay registros",
                                            municipio = municipio,
                                            seccion_context = (prompt_result_1 + prompt_result_4 + prompt_result_5 ))
    print(prompt_result_6)
