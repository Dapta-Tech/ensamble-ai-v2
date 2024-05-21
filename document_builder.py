import os
import pandas as pd
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain.retrievers import (MergerRetriever,)
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAIEmbeddings
from operator import itemgetter
from prompts import prompts_dict
from langchain_core.prompts import ChatPromptTemplate
from glob import glob

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
    carpeta_csv = "data\indicadores mes a mes"
    # Lista para almacenar los DataFrames
    dfs = []
    
    # Leer todos los archivos CSV en la carpeta
    for archivo in os.listdir(carpeta_csv):
        if archivo.endswith('.csv'):
            df = pd.read_csv(os.path.join(carpeta_csv, archivo))
            dfs.append(df)
    
    # Concatenar todos los DataFrames
    df_total = pd.concat(dfs, ignore_index=True)
    
    # Filtrar por municipio
    df_municipio = df_total[df_total['Municipio'] == municipio]
    
    # Filtrar por años de interés
    df_municipio = df_municipio[df_municipio['Año'].between(2019, 2023)]
    
    # Agrupar por delito y año y realizar la sumatoria
    resumen = df_municipio.groupby(['Estadísticas (1)', 'Año']).agg(
        total=('Σ Cantidad', 'sum'),
        femeninos=('Femenino', 'sum'),
        lgtbiq=('LGTBIQ+', 'sum')
    ).reset_index()
    
    # Crear el texto resumen
    texto = ""
    for index, row in resumen.iterrows():
        delito = row['Estadísticas (1)']
        año = row['Año']
        total = row['total']
        femeninos = row['femeninos']
        lgtbiq = row['lgtbiq']
        
        texto += (
                f"El delito de: \"{delito}\", presentó el año: {año} un total de {total}, "
                f"{femeninos} eran mujeres.\n")
    
    return texto

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

def get_delitos_tpcmh(municipio):
    file_path = "data/indicadores tpcmh/"
    dfs = []

    # Definir los años a considerar
    años_relevantes = ['2019', '2020', '2021', '2022', '2023']

    for archivo in os.listdir(file_path):
        if archivo.endswith('.csv'):
            ruta_completa = os.path.join(file_path, archivo)

            try:
                # Leer el archivo, utilizando low_memory=False para evitar el DtypeWarning
                df = pd.read_csv(ruta_completa, low_memory=False)

                # Filtrar por municipio y añadir columna de tipo de delito
                df_municipio = df[df['Municipio'] == municipio].copy()
                tipo_delito = archivo.replace('.csv', '')
                df_municipio.loc[:, 'Tipo delito'] = tipo_delito

                # Transformar años en filas y filtrar solo los años relevantes
                df_melted = df_municipio.melt(id_vars=['Municipio', 'Tipo delito'], var_name='Año', value_name='Incidentes')
                df_melted = df_melted[df_melted['Año'].isin(años_relevantes)]

                # Convertir 'Incidentes' a tipo numérico, manejando valores no numéricos como NaN
                df_melted['Incidentes'] = pd.to_numeric(df_melted['Incidentes'], errors='coerce')

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
        cadena_resultado += f"El total del delitos por Tasa por cada mil habitantes: {row['Tipo delito']}, en el año: {row['Año']}, fue de: {round(row['Incidentes'], 2)}\n"
    #print ('------------------cadena_resultado TPCMH---------------------')
    #print (cadena_resultado)

    return cadena_resultado

def generate_text(paragraph_context, texto, prompt):
    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": """Eres un botón que mejorar el texto de un usuario y crea
        nuevos párrafos, recibirás como input el texto que el usuario quiere que mejores. debes aplicar la
        mejora que se solicita y devolver solo el párrafo generado.
        Solo debes devolver el texto mejorado y usar el contexto del párrafo anterior (en caso de que 
        exista) para dar  continuidad., no debes agregar nada más al texto."""},
        {"role": "user", "content": f"Texto '{texto}', Mejora: '{prompt}', párrafo anterior: {paragraph_context}, Texto mejorado: "}])
    
    return completion.choices[0].message.content

def get_delitos_new_section(delito, delitos, tpcmh, municipio):
    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": """Eres un botón que toma como contexto la información de delitos y 
        tasa por cada mil habitantes(tpcmh) de un municipio y redacta 10 párrafos en formato HTML de información detallada sobre
        la tendencia del delito principal {delito}, evolución a través de los años, y análisis estadístico y relación entre
        las cifras, no agregues un párrafo de resumen."""},
        {"role": "user", "content": f"delito principal: {delito}, Delitos '{delitos}', tpcmh: '{tpcmh}', Municipio: {municipio}, Texto generado en formato HTML: "}])
    
    return completion.choices[0].message.content


#Crear la función 
if __name__ == "__main__":
    
    # texto = "Objetivo general: Generar acciones y condiciones propicias para la seguridad y convivencia ciudadana en el municipio de Fortul, mediante la articulacion interinstitucional y comunitaria."
    # prompt = "Desarrolla 3 objetivos especificos a aprtir del texto anterior."
    # paragraph_context = ""
    # print(generate_text(paragraph_context, texto, prompt))
    
    # Uso de los prompts
    llm = get_llm()

    ##municipio = "Ábrego (Nsa)"
    municipio = "Bogotá, D.C. Cap."
    # #municipio = "Timaná (Hui)"

    delitos_mes_a_mes = get_delitos_mes_a_mes(municipio)
    print(delitos_mes_a_mes)
    print("--------------------")
    print("--------------------")
    print("--------------------")
    delitos_tpcmh = get_delitos_tpcmh(municipio)
    print(delitos_tpcmh)
    seccion_nueva = get_delitos_new_section("Violencia Intrafamiliar" , delitos_mes_a_mes, delitos_tpcmh, municipio)
    print("Sección nueva")
    print(seccion_nueva)

    print("--------------------")

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
    print("Sección 1")
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
    print("Sección 2")
    print(prompt_result_2)

    question_3 = """Generar la sección 3. Diagnóstico de la Situación de Seguridad y Convivencia Ciudadana 
    de el municipio de {municipio} donde darás información del actual alcalde de {municipio} y sus responsabilidades para 
    ejecutar el plan piscc 2024-2027 enfocándote en las métricas de delitos y tasa cada mil habitantes."""
    prompt_result_3 = get_prompt_result(vectors = ["1-Politica-Publica",
                                        "4-Base-estrategias"],
                                        prompt = prompts_dict["3 Diagnostico 3.2"],
                                        question = question_3,
                                        llm = llm,
                                        delitos_mes_a_mes = delitos_mes_a_mes,
                                        tpcmh = delitos_tpcmh,
                                        municipio = municipio,
                                        seccion_context = prompt_result_1)
    print("Sección 3")
    print(prompt_result_3)

    question_3_1 = """Generar la sección 3.1 Diagnóstico de la Situación de Seguridad y 
    Convivencia Ciudadana. de el municipio de {municipio} donde realizarás un estudio
    estadístico minucioso de la situación de delitos y la tasa por cada cien mil habitantes (tpcmh)"""
    prompt_result_3_1 = get_prompt_result(vectors = ["1-Politica-Publica",
                                        "4-Base-estrategias"],
                                        prompt = prompts_dict["3 Diagnostico 3.1"],
                                        question = question_3_1,
                                        llm = llm,
                                        delitos_mes_a_mes = delitos_mes_a_mes,
                                        tpcmh = delitos_tpcmh,
                                        municipio = municipio,
                                        seccion_context = prompt_result_3)
    print("Sección 31")
    print(prompt_result_3_1)

    question_3_2 = """Generar la sección 3.2 Identificación de Problemas Prioritarios
    de el municipio de {municipio} en el documento piscc 2024 donde seleccionarás y argumentarás
    los 3 delitos más importantes en cuando a la información de delitos y tasa por cada cien mil habitantes (tpcmh),
    incluye métricas claves para su identificación."""

    prompt_result_3_2 = get_prompt_result(vectors = ["1-Politica-Publica",
                                            "4-Base-estrategias",
                                            "1-Politica-Publica_Fiscal" ],
                                            prompt = prompts_dict["3 Diagnostico 3.2"],
                                            question = question_3_2,
                                            llm = llm,
                                            delitos_mes_a_mes = delitos_mes_a_mes,
                                            tpcmh = delitos_tpcmh,
                                            municipio = municipio,
                                            seccion_context = prompt_result_3_1)
    print("Sección 3 2")
    print(prompt_result_3_2)

    question_3_3 = """Generar la sección 3.3 Consulta a la Comunidad y Actores Clave.
    Tomando en cuenta principalmente comportamientos contrarios a la convivencia del municipio de {municipio}"""	

    prompt_result_3_3 = get_prompt_result(vectors = ["1-Politica-Publica",
                                            "4-Base-estrategias",
                                            "1-Politica-Publica_Fiscal" ],
                                            prompt = prompts_dict["3 Diagnostico 3.2"],
                                            question = question_3_3,
                                            llm = llm,
                                            delitos_mes_a_mes = delitos_mes_a_mes,
                                            tpcmh = delitos_tpcmh,
                                            municipio = municipio,
                                            seccion_context = prompt_result_3_2)
    print("Sección 3 3")
    print(prompt_result_3_3)

    question_3_4 = """Generar la sección 3.4 Diagnóstico de delitos. 
    En esta sección realizarás un detalle minucioso sobre los delitos más frecuentes
    y la tasa por cada cien mil habitantes (tpcmh) del municipio de {municipio} 
    enfocandose en el tema de género y etnia del municipio de {municipio}."""	

    prompt_result_3_4 = get_prompt_result(vectors = ["1-Politica-Publica",
                                            "4-Base-estrategias",
                                            "1-Politica-Publica_Fiscal" ],
                                            prompt = prompts_dict["3 Diagnostico 3.4"],
                                            question = question_3_3,
                                            llm = llm,
                                            delitos_mes_a_mes = delitos_mes_a_mes,
                                            tpcmh = delitos_tpcmh,
                                            municipio = municipio,
                                            seccion_context = prompt_result_3_3)
    print("Sección 3 4 ")
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
    print("Secccón 4")
    print(prompt_result_4)

    question_5 = """Generar la sección 5. Formulación Estratégica del PISCC 2024-2027. 
    para el municipio de {municipio}, donde identificarás las estrategias y planes que se deben tomar en cuenta basandose en los 
    delitos seleccionados en la sección anterior :{prompt_result_3_4}. Por ultimo menciona las responsabilidades con las estrategias
    del alclade de {municipio}."""	

    prompt_result_5 = get_prompt_result(vectors = ["1-Politica-Publica",
                                            "1-Politica-Publica_Leyes_Politicas-Planes",
                                            "4-Base-estrategias"],
                                            prompt = prompts_dict["5 Formulación"],
                                            question = question_5,
                                            llm = llm,
                                            delitos_mes_a_mes = delitos_mes_a_mes,
                                            tpcmh = "No hay registros",
                                            municipio = municipio,
                                            seccion_context = "prompt_result_5")
    print("Sección 5")
    print(prompt_result_5)

    question_6 = """
    Generar la sección 6 6. Planeación Financiera y Operativa del PISCC 2024-2027. 
    para el municipio de {municipio}, donde guiarás al usuario a cómo crear tablas de presupuesto y
    estrategias enfocadas a cada delito"""
    prompt_result_6 = get_prompt_result(vectors = ["1-Politica-Publica_Documentos-Politica",
                                            "1-Politica-Publica_Leyes_Politicas-Planes",
                                            "1-Politica-Publica_PISCC-por-Municipio",
                                            "4-Base-estrategias"],
                                            prompt = prompts_dict["6 Financiamiento"],
                                            question = question_6,
                                            llm = llm,
                                            delitos_mes_a_mes = delitos_mes_a_mes,
                                            tpcmh = delitos_tpcmh,
                                            municipio = municipio,
                                            seccion_context = prompt_result_5)
    print("Sección 6")
    print(prompt_result_6)

    question_7 = """
        Generar la sección 7. Implementación del PISCC
        para el municipio de {municipio}, donde guiarás al usuario a cómo crear tablas de presupuesto y
        estrategias enfocadas a cada delito"""
    prompt_result_7 = get_prompt_result(vectors = ["1-Politica-Publica_Documentos-Politica",
                                                "1-Politica-Publica_Leyes_Politicas-Planes",
                                                "1-Politica-Publica_PISCC-por-Municipio",
                                                "4-Base-estrategias"],
                                                prompt = prompts_dict["7 Implementación"],
                                                question = question_7,
                                                llm = llm,
                                                delitos_mes_a_mes = delitos_mes_a_mes,
                                                tpcmh = delitos_tpcmh,
                                                municipio = municipio,
                                                seccion_context = prompt_result_6)

    print("Sección 7")
    print(prompt_result_7)

    question_8 = """
        Generar la sección 8. Seguimiento de seguimiento de piscc para el municipio de {municipio}, 
        donde guiarás al usuario donde el objetivo es Asegurar que el PISCC se implemente de forma efectiva, 
        se logren los resultados esperados y se mejoren las estrategias de forma continua."""
    
    prompt_result_8 = get_prompt_result(vectors = ["1-Politica-Publica_Documentos-Politica",
                                                "1-Politica-Publica_Leyes_Politicas-Planes",
                                                "1-Politica-Publica_PISCC-por-Municipio",
                                                "4-Base-estrategias"],
                                                prompt = prompts_dict["8 Seguimiento"],
                                                question = question_8,
                                                llm = llm,
                                                delitos_mes_a_mes = delitos_mes_a_mes,
                                                tpcmh = delitos_tpcmh,
                                                municipio = municipio,
                                                seccion_context = prompt_result_7)
    print("Sección 8")
    print(prompt_result_8)

    question_9 = """
        Generar la sección 9. Evaluación del PISCC para el municipio de {municipio}, 
        donde guiarás al usuario a definir qué documentos pueden servir de apoyo para la evaluación del PISCC."""
    prompt_result_9 = get_prompt_result(vectors = ["1-Politica-Publica_PISCC-por-Municipio"],
                                                prompt = prompts_dict["9 Anexos"],
                                                question = question_9,
                                                llm = llm,
                                                delitos_mes_a_mes = delitos_mes_a_mes,
                                                tpcmh = delitos_tpcmh,
                                                municipio = municipio,
                                                seccion_context = prompt_result_8)
    print("Sección 9")
    print(prompt_result_9)
