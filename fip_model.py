import os
import re
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import AIMessage, HumanMessage
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_transformers import EmbeddingsClusteringFilter
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import DocumentCompressorPipeline
from pinecone import Pinecone
from langchain.retrievers import MergerRetriever
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_tool_calling_agent
from langchain_core.tools import tool
import pandas as pd
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import os
from glob import glob
import pandas as pd
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain_community.agent_toolkits import create_sql_agent

#os.environ["OPENAI_API_KEY"] = ""
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)


# Load bases from a list of namespaces
def load_bases(index_name="", bases_list=[]):
    #pc = Pinecone(api_key="")
    pc = Pinecone()
    index = pc.Index(index_name)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    text_field = "text"
    big_vector = []
    for i in bases_list:
        vectorstore = PineconeVectorStore(index, embeddings, text_field, namespace=i)
        big_vector.append(vectorstore)
        vectorstore = None
    return big_vector


def consultar_datos_por_municipio(query, municipio):
    print("step 1")
    print(query)

    print("step 2")
    print(municipio)

    engine = create_engine(
        "postgresql://clients:bZqbYHeEA2x$Qa6KxnYVkX@clients.cluster-c9w8clqzjjhu.us-east-2.rds.amazonaws.com:5432/fip_db_ai_model"
    )

    db = SQLDatabase(engine=engine)
    print(db.get_usable_table_names())

    agent_executor = create_sql_agent(
        llm, db=db, verbose=True, agent_type="openai-tools"
    )
    response = agent_executor.invoke(f"{query}, Mi Municipio: {municipio}")
    print(response)
    return response


# Función para cargar CSVs desde una carpeta
def load_csvs_from_folder(folder_path):
    csv_files = glob(os.path.join(folder_path, "*.csv"))
    data_frames = [pd.read_csv(file, low_memory=False) for file in csv_files]
    return pd.concat(data_frames, ignore_index=True)


# Create a Lorf Of the Retreivers from a vector collection.
def get_LOTR(big_vector):
    LOTR = []
    for vector_store in big_vector:
        LOTR.append(vector_store.as_retriever())
    retriever = MergerRetriever(retrievers=LOTR)
    return retriever


# Creates the retriever chain with the context LOTR.
def get_context_retriever_chain(big_vector):
    llm = ChatOpenAI()
    retriever = get_LOTR(big_vector)

    prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            (
                "user",
                """Dada la indicación anterior: {input} ten en cuenta que,\
        No eres un asistente, Tu tarea solo es crear 3 tipos de gráficos con Javascript utilizando Chart.js
        Los gráficos pueden ser de los siguientes tipos, no puedes utilizar otros tipos de gráficos: 
        - Line Chart
        - Pie Chart
        - Bar chart
        Por ejemplo recibirás como input las siguientes indicaciones:
        - Crear un gráfico de líneas que muestre la cantidad de personas por edad
        - Crear un gráfico de pastel que muestre la cantidad de personas por estado civil
        Deberás devolver solo el objeto para la construcción del gráfico en Javascript, por ejemplo:
        {
            type: 'line',
            data: {
                labels: ['2020', '2021', '2022', '2023'],
                datasets: [{
                    label: 'Secuestros en Bogotá',
                    data: [76.98, 73.14, 0, 0], // Datos de secuestros para los años 2020 y 2021, completar con datos de 2022 y 2023
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        }
        Solo en caso de que el usuario quiera crear una tabla, deberás devolverle ocdigo en HTML \
        de la tabla generada.""",
            ),
        ]
    )

    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    return retriever_chain


# Creates the conversational RAG chain.
def get_conversational_rag_chain(retriever_chain):
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "No eres un asistente, Tu tarea es crear 3 tipos de gráficos con Javascript Chart.js\
        o una tabla en HTML\
	    provisto por el usuario en el siguiente contexto: {context},\
        Tu tarea es devolver el texto en formato HTML de tablas o Javascript con los gráficos solicitados.",
            ),
            ("user", "{input}"),
        ]
    )

    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever_chain, stuff_documents_chain)


# Gets the response from the conversational RAG chain.
def get_response(query):
    vector_store = load_bases(
        index_name="all-data-v1",
        bases_list=[
            "1-Politica-Publica",
            "2-caracterizacion-municipal",
            "3-informacion-delitos-indicadores-mes-a-mes",
            "3-informacion-delitos-indicadores-tpcmh",
            "4-Base-estrategias",
        ],
    )
    retriever_chain = get_context_retriever_chain(vector_store)
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)

    response = conversation_rag_chain.invoke({"chat_history": [], "input": query})

    script_content_with_tags = re.findall(
        r"(<script>.*?</script>)", response["answer"], re.DOTALL
    )
    table_content_with_tags = re.findall(
        r"(<table>.*?</table>)", response["answer"], re.DOTALL
    )
    return (
        script_content_with_tags > 0
        if len(script_content_with_tags) > 0
        else table_content_with_tags
    )


# Modelo de chat
# Creates the retriever chain with the context LOTR.
def get_context_retriever_chain_chat_model(big_vector):
    llm = ChatOpenAI()
    LOFR = get_LOTR(big_vector)

    retriever = MergerRetriever(retrievers=LOFR)

    prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            (
                "user",
                """Dada la indicación anterior: {input}
        provee información detallada y precisa para la creación de piscc""",
            ),
        ]
    )

    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    return retriever_chain


# Creates the conversational RAG chain.
def get_conversational_rag_chain_chat_model(retriever_chain):
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Tu tarea es proveer información sobre la creación de piscc para los municipios,
                provisto por el usuario en el siguiente contexto: {context},
                Siempre que el usuario salude, deberás preguntarle de qué municipio es y darle toda la 
                información sobre ese municipio que necesite para la creación de piscc.
                Tu objetivo principal es ayudar al usuario a crear un PISCC para su municipio.""",
            ),
            ("user", "{input}"),
        ]
    )

    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever_chain, stuff_documents_chain)


# Gets the response from the conversational RAG chain.
def get_response_chat_model(query, conversation):

    vector_store = load_bases(
        index_name="all-data-v1",
        bases_list=[
            "1-Politica-Publica",
            "2-caracterizacion-municipal",
            "3-informacion-delitos-indicadores-mes-a-mes",
            "3-informacion-delitos-indicadores-tpcmh",
            "4-Base-estrategias",
        ],
    )
    retriever_chain = get_context_retriever_chain_chat_model(vector_store)
    conversation_rag_chain = get_conversational_rag_chain_chat_model(retriever_chain)

    chat_history = create_chat_history(conversation)

    response = conversation_rag_chain.invoke(
        {"chat_history": chat_history, "input": query}
    )

    return response["answer"]


def create_chat_history(conversation):
    chat_history = []
    for c in conversation:
        chat_history.append(
            HumanMessage(content=c["text_content"])
            if c["origin"] == "User"
            else AIMessage(content=c["text_content"])
        )
    return chat_history


introduction_prompt = """Eres un bot genera la sección de Introducción con los siguientes titulos como base:
                        1. Introducción
                        1.1 Contexto y justificación del PISCC 2024
                        1.2 Objetivos del PISCC
                        Tu tarea principal es generar el texto para cada una de estas secciones con la información del municipio de Bogotá.
                        Recuerda seguir el formato de la plantilla de la sección de Introducción del PISCC 2024.
                        Por ejemplo, si recibes la siguiente indicación:
                        - Genera la sección 1.1 Contexto y justificación del PISCC 2024
                        Deberás tomar en cuenta los siguientes puntos:
                        El Plan Integral de Seguridad y Convivencia Ciudadana (PISCC) 2024 es un instrumento de planificación y gestión que tiene como objetivo principal mejorar la seguridad y convivencia en el municipio de Bogotá.
                        enmarca en el Plan de Desarrollo Distrital 2020-2024, que establece las políticas y estrategias para el desarrollo integral y sostenible de la ciudad.
                        se fundamenta en el diagnóstico de seguridad y convivencia del municipio, que identifica los principales problemas y desafíos en esta materia.
                        se elabora de manera participativa, con la articulación de los diferentes actores sociales, institucionales y comunitarios del municipio.
                        se estructura en torno a los siguientes ejes estratégicos: prevención, control, atención y seguimiento, y participación ciudadana.
                        tiene como objetivo principal garantizar la seguridad y convivencia de los habitantes del municipio, promoviendo la cultura de la legalidad, la convivencia pacífica y el respeto por los derechos humanos.
                        se implementa a través de un enfoque integral, que articula las acciones de las diferentes entidades del municipio en materia de seguridad y convivencia.
                        El Contexto es el siguiente: {context}
                        Question: {user_input}"""

diagnostic_prompt = """Eres un bot genera la sección de Diagnóstico con los siguientes titulos como base:   
                        2. Diagnóstico de Seguridad y Convivencia Ciudadana
                        2.1 Análisis de la situación actual del municipio
                        2.2 Identificación de problemáticas prioritarias
                        2.3 Estadísticas y datos relevantes de seguridad
                        Tu tarea principal es generar el texto para cada una de estas secciones con la información del municipio de Bogotá.
                        Recuerda seguir el formato de la plantilla de la sección de Diagnóstico del PISCC 2024.
                        Deberás tomar en cuenta los siguientes puntos para generar esta sección:
                        El diagnóstico de seguridad y convivencia del municipio de Bogotá es un análisis detallado de la situación actual en esta materia, que permite identificar los principales problemas y desafíos en seguridad y convivencia.
                        se basa en la información recopilada a través de diferentes fuentes, como encuestas, estudios, informes, estadísticas, entre otros.
                        se enfoca en aspectos como la percepción de seguridad de la ciudadanía, la incidencia de delitos y faltas, la presencia de grupos armados ilegales, la violencia intrafamiliar, entre otros.
                        se realiza de manera participativa, con la articulación de los diferentes actores sociales, institucionales y comunitarios del municipio.
                        se estructura en torno a los siguientes ejes temáticos: delitos y faltas, violencia intrafamiliar, grupos armados ilegales, percepción de seguridad, entre otros.
                        se elabora con el objetivo de identificar las problemáticas prioritarias en seguridad y convivencia del municipio, para orientar la formulación de políticas y estrategias en esta materia.
                        El Contexto es el siguiente: {context}
                        Question: {user_input}"""

improve_prompt = """Eres un bot que mejora el texto de entrada: {user_input}
                    Con el sigueinte contexto sobre c: {context}
                    Tu tarea es mejorar el texto de netrada revisando la ortografía, gramática y coherencia del texto.
                    Recuerda seguir el formato de la plantilla PISCC 2024.
                    Además deberás aumentar la longitud del texto de entrada con coherencia con el user input."""

prompts = {
    "Introducción": introduction_prompt,
    "Diagnóstico": diagnostic_prompt,
    "Mejorar": improve_prompt,
}


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Gets the response from the conversational RAG chain.
def get_rag(prompt_template):
    llm = ChatOpenAI()
    vector_store = load_bases(
        index_name="all-data-v1",
        bases_list=[
            "1-Politica-Publica",
            "2-caracterizacion-municipal",
            "3-informacion-delitos-indicadores-mes-a-mes",
            "3-informacion-delitos-indicadores-tpcmh",
            "4-Base-estrategias",
        ],
    )
    LOFR = get_LOTR(vector_store)

    retriever = MergerRetriever(retrievers=LOFR)

    prompt = PromptTemplate.from_template(prompt_template)

    rag_chain = (
        {"context": retriever | format_docs, "user_input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


def get_response_chapter(prompt_template, user_input):
    rag = get_rag(prompt_template)
    return rag.invoke(user_input)


# texto_generado = get_response_chapter("Introducción",
#                               "1. Introducción \n\n 1.1 Contexto y justificación del PISCC 2024 \n\n 1.2 Objetivos del PISCC")


def CSV_agent(df, query):
    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )
    agent.invoke(query)


@tool
def get_crime_information_from_CSVs(consulta: str) -> str:
    """Consultar información de los delitos desde el CSV"""
    csv = load_csvs_from_folder("data\indicadores mes a mes")
    return CSV_agent(csv, consulta)


@tool
def get_general_information_from_PDFs(consulta: str) -> str:
    """Consultar información general de los documentos de política pública desde la base vectorial de Pinecone"""
    index_name = "all-data-v1"
    bases_list = [
        "1-Politica-Publica_PISCC-por-Municipio",
        "1-Politica-Publica_Fiscal",
        "1-Politica-Publica_Documentos-Politica",
        "1-Politica-Publica_Leyes-Decretos",
    ]

    big_vector = load_bases(index_name, bases_list)
    retriever_chain = get_LOTR(big_vector)
    filter_ordered_by_retriever = EmbeddingsClusteringFilter(
        embeddings=OpenAIEmbeddings(),
        num_clusters=5,
        num_closest=1,
        sorted=True,
    )
    pipeline = DocumentCompressorPipeline(transformers=[filter_ordered_by_retriever])
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=pipeline, base_retriever=retriever_chain
    )
    return compression_retriever.invoke(consulta)

@tool
def get_my_information_from_database(consulta: str, municipio: str) -> str:
    """Consultar información de los delitos desde la base de datos"""
    prompt = f"""
        Eres un asistente de datos, el usuario te va a solicitar una accion, lo unico que tienes que hacer es devolver la estructura de la informacion que necesita con base a las CATEGORIAS DE DELITOS y corregiendo el formato del municipio con base en FORMATOS DE MUNICIPIOS.
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
        FORMATOS DE MUNICIPIOS:
        
        Medellín (Ant) Cap.
        Victoria (Cal)
        Villamaría (Cal)
        Viterbo (Cal)
        Florencia (Caq) Cap.
        Albania (Caq)
        Belén de Los Andaquíes (Caq)
        Cartagena del Chairá (Caq)
        Curillo (Caq)
        El Doncello (Caq)
        El Paujil (Caq)
        La Montañita (Caq)
        Milán (Caq)
        Morelia (Caq)
        San José del Fragua (Caq)
        San Vicente del Caguán (Caq)
        Solano (Caq)
        Solita (Caq)
        Popayán (Cau) Cap.
        Almaguer (Cau)
        Balboa (Cau)
        Bolívar (Cau)
        Buenos Aires (Cau)
        Cajibío (Cau)
        Caldono (Cau)
        Caloto (Cau)
        Corinto (Cau)
        El Tambo (Cau)
        Florencia (Cau)
        Guachené (Cau)
        Guapi (Cau)
        Inzá (Cau)
        Jambaló (Cau)
        La Sierra (Cau)
        La Vega (Cau)
        López (Cau)
        Mercaderes (Cau)
        Miranda (Cau)
        Padilla (Cau)
        Paéz (Cau)
        Patía (Cau)
        Piamonte (Cau)
        Piendamó (Cau)
        Puerto Tejada (Cau)
        Puracé (Cau)
        Rosas (Cau)
        San Sebastián (Cau)
        Santander de Quilichao (Cau)
        Santa Rosa (Cau)
        Silvia (Cau)
        Sotará (Cau)
        Suárez (Cau)
        Sucre (Cau)
        Timbío (Cau)
        Timbiquí (Cau)
        Toribío (Cau)
        Villa Rica (Cau)
        Totoró (Cau)
        Valledupar (Ces) Cap.
        Aguachica (Ces)
        Agustín Codazzi (Ces)
        Astrea (Ces)
        Becerril (Ces)
        Bosconia (Ces)
        Chimichagua (Ces)
        Chiriguaná (Ces)
        Curumaní (Ces)
        El Copey (Ces)
        El Paso (Ces)
        Gamarra (Ces)
        González (Ces)
        La Gloria (Ces)
        La Jagua de Ibirico (Ces)
        Manaure (Ces)
        Pailitas (Ces)
        Pelaya (Ces)
        Pueblo Bello (Ces)
        Río de Oro (Ces)
        La Paz (Ces)
        San Alberto (Ces)
        San Diego (Ces)
        San Martín (Ces)
        Tamalameque (Ces)
        Montería (Cor) Cap.
        Ayapel (Cor)
        Buenavista (Cor)
        Canalete (Cor)
        Cereté (Cor)
        Morales (Cau)
        Valparaíso (Caq)
        Bogotá, D.C. Cap.
        Abejorral (Ant)
        Abriaquí (Ant)
        Alejandría (Ant)
        Amagá (Ant)
        Amalfi (Ant)
        Andes (Ant)
        Angelópolis (Ant)
        Angostura (Ant)
        Anorí (Ant)
        Santafé de Antioquia (Ant)
        Anzá (Ant)
        Apartadó (Ant)
        Arboletes (Ant)
        Armenia (Ant)
        Barbosa (Ant)
        Belmira (Ant)
        Bello (Ant)
        Betania (Ant)
        Betulia (Ant)
        Ciudad Bolívar (Ant)
        Briceño (Ant)
        Buriticá (Ant)
        Cáceres (Ant)
        Caicedo (Ant)
        Caldas (Ant)
        Campamento (Ant)
        Cañasgordas (Ant)
        Caracolí (Ant)
        Caramanta (Ant)
        Carepa (Ant)
        El Carmen de Viboral (Ant)
        Carolina (Ant)
        Caucasia (Ant)
        Chigorodó (Ant)
        Cisneros (Ant)
        Cocorná (Ant)
        Concepción (Ant)
        Concordia (Ant)
        Copacabana (Ant)
        Dabeiba (Ant)
        Don Matías (Ant)
        Ebéjico (Ant)
        El Bagre (Ant)
        Entrerrios (Ant)
        Envigado (Ant)
        Fredonia (Ant)
        Frontino (Ant)
        Giraldo (Ant)
        Gómez Plata (Ant)
        Granada (Ant)
        Guadalupe (Ant)
        Guarne (Ant)
        Guatapé (Ant)
        Heliconia (Ant)
        Hispania (Ant)
        Itagüí (Ant)
        Ituango (Ant)
        Jardín (Ant)
        Jericó (Ant)
        La Ceja (Ant)
        La Estrella (Ant)
        La Pintada (Ant)
        La Unión (Ant)
        Liborina (Ant)
        Maceo (Ant)
        Marinilla (Ant)
        Montebello (Ant)
        Murindó (Ant)
        Mutatá (Ant)
        Nariño (Ant)
        Necoclí (Ant)
        Nechí (Ant)
        Olaya (Ant)
        Peñol (Ant)
        Peque (Ant)
        Pueblorrico (Ant)
        Puerto Berrío (Ant)
        Puerto Nare (Ant)
        Puerto Triunfo (Ant)
        Remedios (Ant)
        Retiro (Ant)
        Rionegro (Ant)
        Sabanalarga (Ant)
        Sabaneta (Ant)
        Salgar (Ant)
        San Andrés de Cuerquía (Ant)
        San Carlos (Ant)
        San Francisco (Ant)
        San Jerónimo (Ant)
        San José de La Montaña (Ant)
        San Juan de Urabá (Ant)
        San Luis (Ant)
        San Pedro de Los Milagros (Ant)
        San Pedro de Urabá (Ant)
        San Rafael (Ant)
        San Roque (Ant)
        San Vicente (Ant)
        Santa Rosa de Osos (Ant)
        Santo Domingo (Ant)
        El Santuario (Ant)
        Segovia (Ant)
        Sonsón (Ant)
        Sopetrán (Ant)
        Támesis (Ant)
        Tarazá (Ant)
        Tarso (Ant)
        Zaragoza (Ant)
        Titiribí (Ant)
        Toledo (Ant)
        Turbo (Ant)
        Uramita (Ant)
        Urrao (Ant)
        Valdivia (Ant)
        Vegachí (Ant)
        Venecia (Ant)
        Vigía del Fuerte (Ant)
        Yalí (Ant)
        Yarumal (Ant)
        Yolombó (Ant)
        Yondó (Ant)
        Barranquilla (Atl) Cap.
        Baranoa (Atl)
        Campo de La Cruz (Atl)
        Candelaria (Atl)
        Galapa (Atl)
        Juan de Acosta (Atl)
        Luruaco (Atl)
        Malambo (Atl)
        Manatí (Atl)
        Palmar de Varela (Atl)
        Piojó (Atl)
        Polonuevo (Atl)
        Ponedera (Atl)
        Puerto Colombia (Atl)
        Repelón (Atl)
        Sabanagrande (Atl)
        Sabanalarga (Atl)
        Santa Lucía (Atl)
        Santo Tomás (Atl)
        Soledad (Atl)
        Suan (Atl)
        Usiacurí (Atl)
        Tubará (Atl)
        Cartagena De Indias (Bol) Cap.
        Achí (Bol)
        Altos del Rosario (Bol)
        Arenal (Bol)
        Arjona (Bol)
        Arroyohondo (Bol)
        Barranco de Loba (Bol)
        Calamar (Bol)
        Cantagallo (Bol)
        Cicuco (Bol)
        Córdoba (Bol)
        Clemencia (Bol)
        El Carmen de Bolívar (Bol)
        El Guamo (Bol)
        El Peñón (Bol)
        Hatillo de Loba (Bol)
        Magangué (Bol)
        Mahates (Bol)
        Margarita (Bol)
        María La Baja (Bol)
        Montecristo (Bol)
        Mompós (Bol)
        Norosí (Bol)
        Pinillos (Bol)
        Regidor (Bol)
        Río Viejo (Bol)
        San Cristóbal (Bol)
        San Estanislao (Bol)
        San Fernando (Bol)
        San Jacinto (Bol)
        San Jacinto del Cauca (Bol)
        San Juan Nepomuceno (Bol)
        San Martín de Loba (Bol)
        San Pablo (Bol)
        Santa Catalina (Bol)
        Santa Rosa (Bol)
        Morales (Bol)
        Valparaíso (Ant)
        Santa Rosa del Sur (Bol)
        Simití (Bol)
        Soplaviento (Bol)
        Talaigua Nuevo (Bol)
        Tiquisio (Bol)
        Turbaco (Bol)
        Turbaná (Bol)
        Villanueva (Bol)
        Zambrano (Bol)
        Tunja (Boy) Cap.
        Almeida (Boy)
        Aquitania (Boy)
        Arcabuco (Boy)
        Belén (Boy)
        Berbeo (Boy)
        Betéitiva (Boy)
        Boavita (Boy)
        Briceño (Boy)
        Buenavista (Boy)
        Busbanzá (Boy)
        Caldas (Boy)
        Campohermoso (Boy)
        Cerinza (Boy)
        Chinavita (Boy)
        Chiquinquirá (Boy)
        Chiscas (Boy)
        Chita (Boy)
        Chitaraque (Boy)
        Chivatá (Boy)
        Ciénega (Boy)
        Cómbita (Boy)
        Coper (Boy)
        Corrales (Boy)
        Covarachía (Boy)
        Cubará (Boy)
        Cucaita (Boy)
        Cuítiva (Boy)
        Chíquiza (Boy)
        Chivor (Boy)
        Duitama (Boy)
        El Cocuy (Boy)
        El Espino (Boy)
        Firavitoba (Boy)
        Floresta (Boy)
        Gachantivá (Boy)
        Gámeza (Boy)
        Garagoa (Boy)
        Guacamayas (Boy)
        Guateque (Boy)
        Argelia (Cau)
        Santa Bárbara (Ant)
        Puerto Rico (Caq)
        Guayatá (Boy)
        Güicán (Boy)
        Iza (Boy)
        Jenesano (Boy)
        Jericó (Boy)
        Labranzagrande (Boy)
        La Capilla (Boy)
        La Victoria (Boy)
        La Uvita (Boy)
        Villa de Leyva (Boy)
        Macanal (Boy)
        Maripí (Boy)
        Miraflores (Boy)
        Mongua (Boy)
        Monguí (Boy)
        Moniquirá (Boy)
        Motavita (Boy)
        Muzo (Boy)
        Nobsa (Boy)
        Nuevo Colón (Boy)
        Argelia (Ant)
        Santa Bárbara (Nar)
        Girardota (Ant)
        Oicatá (Boy)
        Otanche (Boy)
        Pachavita (Boy)
        Páez (Boy)
        Paipa (Boy)
        Pajarito (Boy)
        Panqueba (Boy)
        Pauna (Boy)
        Paya (Boy)
        Paz de Río (Boy)
        Pesca (Boy)
        Pisba (Boy)
        Puerto Boyacá (Boy)
        Quípama (Boy)
        Ramiriquí (Boy)
        Ráquira (Boy)
        Rondón (Boy)
        Saboyá (Boy)
        Sáchica (Boy)
        Samacá (Boy)
        San Eduardo (Boy)
        San José de Pare (Boy)
        San Luis de Gaceno (Boy)
        San Mateo (Boy)
        San Miguel de Sema (Boy)
        San Pablo de Borbur (Boy)
        Santana (Boy)
        Santa María (Boy)
        Santa Rosa de Viterbo (Boy)
        Santa Sofía (Boy)
        Sativanorte (Boy)
        Sativasur (Boy)
        Siachoque (Boy)
        Soatá (Boy)
        Socotá (Boy)
        Socha (Boy)
        Sogamoso (Boy)
        Somondoco (Boy)
        Sora (Boy)
        Sotaquirá (Boy)
        Soracá (Boy)
        Susacón (Boy)
        Sutamarchán (Boy)
        Sutatenza (Boy)
        Tasco (Boy)
        Tenza (Boy)
        Tibaná (Boy)
        Tibasosa (Boy)
        Tinjacá (Boy)
        Tipacoque (Boy)
        Toca (Boy)
        Togüí (Boy)
        Tópaga (Boy)
        Tota (Boy)
        Zetaquira (Boy)
        Tununguá (Boy)
        Turmequé (Boy)
        Tuta (Boy)
        Tutazá (Boy)
        Umbita (Boy)
        Ventaquemada (Boy)
        Viracachá (Boy)
        Manizales (Cal) Cap.
        Aguadas (Cal)
        Anserma (Cal)
        Aranzazu (Cal)
        Belalcázar (Cal)
        Chinchiná (Cal)
        Filadelfia (Cal)
        La Dorada (Cal)
        La Merced (Cal)
        Manzanares (Cal)
        Marmato (Cal)
        Marquetalia (Cal)
        Marulanda (Cal)
        Neira (Cal)
        Norcasia (Cal)
        Pácora (Cal)
        Palestina (Cal)
        Pensilvania (Cal)
        Riosucio (Cal)
        Risaralda (Cal)
        Salamina (Cal)
        Samaná (Cal)
        San José (Cal)
        Supía (Cal)
        Chimá (Cor)
        Chinú (Cor)
        Ciénaga de Oro (Cor)
        Cotorra (Cor)
        La Apartada (Cor)
        Lorica (Cor)
        Los Córdobas (Cor)
        Momil (Cor)
        Montelíbano (Cor)
        Moñitos (Cor)
        Planeta Rica (Cor)
        Pueblo Nuevo (Cor)
        Puerto Escondido (Cor)
        Puerto Libertador (Cor)
        Purísima (Cor)
        Sahagún (Cor)
        San Andrés Sotavento (Cor)
        San Antero (Cor)
        San Bernardo del Viento (Cor)
        San Carlos (Cor)
        San José de Ure (Cor)
        San Pelayo (Cor)
        Tierralta (Cor)
        Valencia (Cor)
        Tuchín (Cor)
        Agua de Dios (Cun)
        Albán (Cun)
        Anapoima (Cun)
        Anolaima (Cun)
        Arbeláez (Cun)
        Beltrán (Cun)
        Bituima (Cun)
        Bojacá (Cun)
        Cabrera (Cun)
        Cachipay (Cun)
        Cajicá (Cun)
        Caparrapí (Cun)
        Cáqueza (Cun)
        Carmen de Carupa (Cun)
        Chaguaní (Cun)
        Chía (Cun)
        Chipaque (Cun)
        Choachí (Cun)
        Chocontá (Cun)
        Cogua (Cun)
        Cota (Cun)
        Cucunubá (Cun)
        El Colegio (Cun)
        El Peñón (Cun)
        El Rosal (Cun)
        Facatativá (Cun)
        Fómeque (Cun)
        Fosca (Cun)
        Funza (Cun)
        Fúquene (Cun)
        Fusagasugá (Cun)
        Gachalá (Cun)
        Gachancipá (Cun)
        Gachetá (Cun)
        Gama (Cun)
        Girardot (Cun)
        Granada (Cun)
        Guachetá (Cun)
        Guaduas (Cun)
        Guasca (Cun)
        Guataquí (Cun)
        Guatavita (Cun)
        Guayabal de Síquima (Cun)
        Guayabetal (Cun)
        Gutiérrez (Cun)
        Jerusalén (Cun)
        Junín (Cun)
        La Calera (Cun)
        La Mesa (Cun)
        La Palma (Cun)
        La Peña (Cun)
        La Vega (Cun)
        Lenguazaque (Cun)
        Machetá (Cun)
        Madrid (Cun)
        Manta (Cun)
        Medina (Cun)
        Mosquera (Cun)
        Nariño (Cun)
        Nemocón (Cun)
        Nilo (Cun)
        Nimaima (Cun)
        Nocaima (Cun)
        Venecia (Cun)
        Pacho (Cun)
        Paime (Cun)
        Pandi (Cun)
        Paratebueno (Cun)
        Pasca (Cun)
        Puerto Salgar (Cun)
        Pulí (Cun)
        Quebradanegra (Cun)
        Quetame (Cun)
        Quipile (Cun)
        Apulo (Cun)
        Ricaurte (Cun)
        San Antonio del Tequendama (Cun)
        San Bernardo (Cun)
        San Cayetano (Cun)
        San Francisco (Cun)
        San Juan de Río Seco (Cun)
        Sasaima (Cun)
        Sesquilé (Cun)
        Sibaté (Cun)
        Silvania (Cun)
        Simijaca (Cun)
        Soacha (Cun)
        Sopó (Cun)
        Subachoque (Cun)
        Suesca (Cun)
        Supatá (Cun)
        Susa (Cun)
        Sutatausa (Cun)
        Tabio (Cun)
        Tausa (Cun)
        Tena (Cun)
        Tenjo (Cun)
        Tibacuy (Cun)
        Tibirita (Cun)
        Tocaima (Cun)
        Tocancipá (Cun)
        Topaipí (Cun)
        Ubalá (Cun)
        Ubaque (Cun)
        Villa de San Diego de Ubate (Cun)
        Une (Cun)
        Útica (Cun)
        Vergara (Cun)
        Vianí (Cun)
        Villagómez (Cun)
        Villapinzón (Cun)
        Villeta (Cun)
        Zipaquirá (Cun)
        Viotá (Cun)
        Yacopí (Cun)
        Zipacón (Cun)
        Quibdó (Cho) Cap.
        Acandí (Cho)
        Alto Baudó / Pie De Pato (Cho)
        Atrato / Yuto (Cho)
        Bagadó (Cho)
        Bahía Solano (Cho)
        Bajo Baudó / Pizarro (Cho)
        Bojayá / Bellavista (Cho)
        El Cantón del San Pablo / Managrú (Cho)
        Carmen del Darién (Cho)
        Cértegui (Cho)
        Condoto (Cho)
        El Carmen de Atrato (Cho)
        El Litoral del San Juan / Santa Genoveva De Docordó (Cho)
        Istmina (Cho)
        Juradó (Cho)
        Lloró (Cho)
        Medio Atrato / Beté (Cho)
        Medio Baudó / Puerto Meluk (Cho)
        Medio San Juan / Andagoya (Cho)
        Nóvita (Cho)
        Nuquí (Cho)
        Río Iró / Santa Rita (Cho)
        Río Quito / Paimadó (Cho)
        Riosucio (Cho)
        San José del Palmar (Cho)
        Sipí (Cho)
        Tadó (Cho)
        Unguía (Cho)
        Unión Panamericana / Ánimas (Cho)
        Neiva (Hui) Cap.
        Acevedo (Hui)
        Agrado (Hui)
        Aipe (Hui)
        Algeciras (Hui)
        Altamira (Hui)
        Baraya (Hui)
        Campoalegre (Hui)
        Colombia (Hui)
        Elías (Hui)
        Garzón (Hui)
        Gigante (Hui)
        Guadalupe (Hui)
        Hobo (Hui)
        Iquira (Hui)
        Isnos (Hui)
        La Argentina (Hui)
        La Plata (Hui)
        Nátaga (Hui)
        Oporapa (Hui)
        Paicol (Hui)
        Palermo (Hui)
        Palestina (Hui)
        Pital (Hui)
        Pitalito (Hui)
        Rivera (Hui)
        Saladoblanco (Hui)
        San Agustín (Hui)
        Santa María (Hui)
        Suaza (Hui)
        Tarqui (Hui)
        Tesalia (Hui)
        Tello (Hui)
        Teruel (Hui)
        Yaguará (Hui)
        Timaná (Hui)
        Villavieja (Hui)
        Riohacha (Lag) Cap.
        Albania (Lag)
        Barrancas (Lag)
        Dibulla (Lag)
        Distracción (Lag)
        El Molino (Lag)
        Fonseca (Lag)
        Hatonuevo (Lag)
        La Jagua del Pilar (Lag)
        Maicao (Lag)
        Manaure (Lag)
        San Juan del Cesar (Lag)
        Uribia (Lag)
        Urumita (Lag)
        Villanueva (Lag)
        Santa Marta (Mag) Cap.
        Algarrobo (Mag)
        Aracataca (Mag)
        Ariguaní (Mag)
        Cerro San Antonio (Mag)
        Chibolo (Mag)
        Ciénaga (Mag)
        Concordia (Mag)
        El Banco (Mag)
        El Piñón (Mag)
        El Retén (Mag)
        Fundación (Mag)
        Guamal (Mag)
        Nueva Granada (Mag)
        Pedraza (Mag)
        Pijiño del Carmen (Mag)
        Pivijay (Mag)
        Plato (Mag)
        Puebloviejo (Mag)
        Remolino (Mag)
        Sabanas de San Ángel (Mag)
        Salamina (Mag)
        San Sebastián de Buenavista (Mag)
        San Zenón (Mag)
        Santa Ana (Mag)
        Santa Bárbara de Pinto (Mag)
        Zona Bananera (Mag)
        Sitionuevo (Mag)
        Tenerife (Mag)
        Zapayán (Mag)
        Villavicencio (Met) Cap.
        Acacías (Met)
        Barranca de Upía (Met)
        Cabuyaro (Met)
        Castilla La Nueva (Met)
        Cubarral (Met)
        Cumaral (Met)
        El Calvario (Met)
        El Castillo (Met)
        El Dorado (Met)
        Fuente de Oro (Met)
        Granada (Met)
        Guamal (Met)
        Mapiripán (Met)
        Mesetas (Met)
        La Macarena (Met)
        Uribe (Met)
        Lejanías (Met)
        Puerto Concordia (Met)
        Puerto Gaitán (Met)
        Puerto López (Met)
        Puerto Lleras (Met)
        Restrepo (Met)
        San Carlos de Guaroa (Met)
        San Juan de Arama (Met)
        San Juanito (Met)
        Vistahermosa (Met)
        San Martín (Met)
        Pasto (Nar) Cap.
        Albán (Nar)
        Aldana (Nar)
        Ancuyá (Nar)
        Arboleda (Nar)
        Barbacoas (Nar)
        Belén (Nar)
        Buesaco (Nar)
        Colón (Nar)
        Consacá (Nar)
        Contadero (Nar)
        Córdoba (Nar)
        Cuaspud (Nar)
        Cumbal (Nar)
        Cumbitara (Nar)
        Chachagüí (Nar)
        El Charco (Nar)
        El Peñol (Nar)
        El Rosario (Nar)
        El Tablón de Gómez (Nar)
        El Tambo (Nar)
        Funes (Nar)
        Guachucal (Nar)
        Guaitarilla (Nar)
        Gualmatán (Nar)
        Iles (Nar)
        Imués (Nar)
        Ipiales (Nar)
        La Cruz (Nar)
        La Florida (Nar)
        La Llanada (Nar)
        La Tola (Nar)
        La Unión (Nar)
        Leiva (Nar)
        Linares (Nar)
        Los Andes (Nar)
        Magüi (Nar)
        Mallama (Nar)
        Mosquera (Nar)
        Olaya Herrera (Nar)
        Ospina (Nar)
        Francisco Pizarro (Nar)
        Policarpa (Nar)
        Potosí (Nar)
        Providencia (Nar)
        Puerres (Nar)
        Pupiales (Nar)
        Ricaurte (Nar)
        Roberto Payán (Nar)
        Samaniego (Nar)
        Yacuanquer (Nar)
        Sandoná (Nar)
        San Bernardo (Nar)
        San Lorenzo (Nar)
        San Pablo (Nar)
        San Pedro de Cartago (Nar)
        Santacruz (Nar)
        Sapuyes (Nar)
        Taminango (Nar)
        Tangua (Nar)
        San Andrés de Tumaco (Nar)
        Túquerres (Nar)
        Cúcuta (Nsa) Cap.
        Ábrego (Nsa)
        Arboledas (Nsa)
        Bochalema (Nsa)
        Bucarasica (Nsa)
        Cácota (Nsa)
        Cachirá (Nsa)
        Chinácota (Nsa)
        Chitagá (Nsa)
        Convención (Nsa)
        Cucutilla (Nsa)
        Durania (Nsa)
        El Carmen (Nsa)
        El Tarra (Nsa)
        El Zulia (Nsa)
        Puerto Rico (Met)
        Gramalote (Nsa)
        Hacarí (Nsa)
        Herrán (Nsa)
        Labateca (Nsa)
        La Esperanza (Nsa)
        La Playa (Nsa)
        Los Patios (Nsa)
        Lourdes (Nsa)
        Mutiscua (Nsa)
        Ocaña (Nsa)
        Pamplona (Nsa)
        Pamplonita (Nsa)
        Puerto Santander (Nsa)
        Ragonvalia (Nsa)
        Salazar (Nsa)
        San Calixto (Nsa)
        San Cayetano (Nsa)
        Santiago (Nsa)
        Sardinata (Nsa)
        Silos (Nsa)
        Teorama (Nsa)
        Tibú (Nsa)
        Toledo (Nsa)
        Villa del Rosario (Nsa)
        Villa Caro (Nsa)
        Armenia (Qui) Cap.
        Buenavista (Qui)
        Calarcá (Qui)
        Circasia (Qui)
        Córdoba (Qui)
        Filandia (Qui)
        Génova (Qui)
        La Tebaida (Qui)
        Montenegro (Qui)
        Pijao (Qui)
        Salento (Qui)
        Quimbaya (Qui)
        Pereira (Ris) Cap.
        Apía (Ris)
        Balboa (Ris)
        Belén de Umbría (Ris)
        Dosquebradas (Ris)
        Guática (Ris)
        La Celia (Ris)
        La Virginia (Ris)
        Marsella (Ris)
        Mistrató (Ris)
        Pueblo Rico (Ris)
        Quinchía (Ris)
        Santuario (Ris)
        Santa Rosa de Cabal (Ris)
        Bucaramanga (San) Cap.
        Aguada (San)
        Albania (San)
        Aratoca (San)
        Barbosa (San)
        Barichara (San)
        Barrancabermeja (San)
        Betulia (San)
        Bolívar (San)
        Cabrera (San)
        California (San)
        Capitanejo (San)
        Carcasí (San)
        Cepitá (San)
        Cerrito (San)
        Charalá (San)
        Charta (San)
        Chima (San)
        Chipatá (San)
        Cimitarra (San)
        Concepción (San)
        Confines (San)
        Contratación (San)
        Coromoro (San)
        Curití (San)
        El Carmen de Chucurí (San)
        El Guacamayo (San)
        El Peñón (San)
        El Playón (San)
        Encino (San)
        Enciso (San)
        Florián (San)
        Floridablanca (San)
        Galán (San)
        Gámbita (San)
        Girón (San)
        Guaca (San)
        Guadalupe (San)
        Guapotá (San)
        Guavatá (San)
        Güepsa (San)
        Hato (San)
        Jesús María (San)
        Jordán (San)
        La Belleza (San)
        Landázuri (San)
        La Paz (San)
        Lebrija (San)
        Los Santos (San)
        Macaravita (San)
        Málaga (San)
        Matanza (San)
        Mogotes (San)
        Molagavita (San)
        Ocamonte (San)
        Oiba (San)
        Onzaga (San)
        Palmar (San)
        Palmas del Socorro (San)
        Páramo (San)
        Piedecuesta (San)
        Pinchote (San)
        Puente Nacional (San)
        Puerto Parra (San)
        Puerto Wilches (San)
        Rionegro (San)
        Sabana de Torres (San)
        San Andrés (San)
        San Benito (San)
        San Gil (San)
        San Joaquín (San)
        San José de Miranda (San)
        San Miguel (San)
        San Vicente de Chucurí (San)
        Santa Helena del Opón (San)
        Zapatoca (San)
        Simacota (San)
        Socorro (San)
        Suaita (San)
        Sucre (San)
        Suratá (San)
        Tona (San)
        Valle de San José (San)
        Vélez (San)
        Vetas (San)
        Villanueva (San)
        Sincelejo (Suc) Cap.
        Buenavista (Suc)
        Caimito (Suc)
        Colosó (Suc)
        Corozal (Suc)
        Coveñas (Suc)
        Chalán (Suc)
        El Roble (Suc)
        Galeras (Suc)
        Guaranda (Suc)
        La Unión (Suc)
        Los Palmitos (Suc)
        Majagual (Suc)
        Morroa (Suc)
        Ovejas (Suc)
        Palmito (Suc)
        Sampués (Suc)
        San Benito Abad (Suc)
        San Juan de Betulia (Suc)
        San Marcos (Suc)
        San Onofre (Suc)
        Tolú Viejo (Suc)
        San Pedro (Suc)
        San Luis de Sincé (Suc)
        Santiago de Tolú (Suc)
        Ibagué (Tol) Cap.
        Alpujarra (Tol)
        Alvarado (Tol)
        Ambalema (Tol)
        Anzoátegui (Tol)
        Armero (Tol)
        Ataco (Tol)
        Cajamarca (Tol)
        Carmen de Apicalá (Tol)
        Casabianca (Tol)
        Chaparral (Tol)
        Coello (Tol)
        Coyaima (Tol)
        Cunday (Tol)
        Dolores (Tol)
        Espinal (Tol)
        Falan (Tol)
        Flandes (Tol)
        Fresno (Tol)
        Guamo (Tol)
        Herveo (Tol)
        Honda (Tol)
        Icononzo (Tol)
        Lérida (Tol)
        Líbano (Tol)
        San Sebastián de Mariquita (Tol)
        Melgar (Tol)
        Murillo (Tol)
        Natagaima (Tol)
        Ortega (Tol)
        Palocabildo (Tol)
        Piedras (Tol)
        Planadas (Tol)
        Prado (Tol)
        Purificación (Tol)
        Rioblanco (Tol)
        Roncesvalles (Tol)
        Rovira (Tol)
        Saldaña (Tol)
        San Antonio (Tol)
        San Luis (Tol)
        Santa Isabel (Tol)
        Suárez (Tol)
        Valle de San Juan (Tol)
        Villarrica (Tol)
        Venadillo (Tol)
        ###
        
        IMPORTANTE: 
        - Siempre que te consulten información sobre tasa por cada mil habitantes (tpcmh), debes utilizar la tabla tasa_de_delitos_por_cada_mil_habitantes.
        - Si solo te consultan información sobre delitos en un municipio, debes utilizar la tabla delitos_mes_a_mes.
        - Cuando te consulten información sobre estrategias o indicadores o acciones a problemáticas y/o delitos, debes utilizar la tabla problematicas_estrategias.
        - En caso de que el usuario solicite información de años anteriores, deberás devolver la información de la columna 'Año' de la base de datos.
        - La columna "PROBLEMÁTICA" hace referencia a delitos en la tablatasa_de_delitos_por_cada_mil_habitantes.
        - La columna llamada "Estadísticas (1)" representa delitos en la tabla delitos_mes_a_mes.
        

        Ejemplo 1:
        Usuario: Quiero saber cuales son los delitos mas recurrentes en Bogota, Mi Municipio Girardota (Ant)
        Asistente: Informacion de delitos mas recurrentes en Bogotá, D.C. Cap
        
        Ejemplo 2:
        Usuario: Quiero saber cuales es la cantidad de secuestros en mi municipio, Mi Municipio Girardota (Ant)
        Asistente: Informacion de Secuestro, Tema: "Secuestro _ Extorsión" | Estadísticas (1): "Secuestro ( Personas Víctimas )", en Mi Municipio Girardota (Ant)

        Ejemplo 3:
        Usuario: Quiero saber cuales es la cantidad de secuestros en mi municipio en año 2023 en mi Municipio Girardota (Ant)
        Asistente: Informacion de Secuestro el años 2023, Tema: "Secuestro _ Extorsión" | Estadísticas (1): "Secuestro ( Personas Víctimas )", en Mi Municipio Girardota (Ant), año 2023
        
        Usuario: {{pregunta}}, 
    """

    prompt_tp = ChatPromptTemplate.from_template(prompt)
    chain = prompt_tp | llm | StrOutputParser()

    response = chain.invoke({"pregunta": f"{consulta}. Mi Municipio: {municipio}"})
    # return response
    return consultar_datos_por_municipio(query=response, municipio=municipio)


# get_my_information_from_database(
#     consulta="quiero saber los principales delitos en BOGOTA",
#     municipio="Girardota (Ant)",
# )


# Build chain
def Chain_with_tool(municipio):
    tools = [get_my_information_from_database, get_general_information_from_PDFs]

    print(municipio)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"""
                    Eres un asistente diseñado para responder preguntas sobre la creación de Planes Integrales de Seguridad y Convivencia Ciudadana (PISCC) del municipio: {municipio}.
                    Tu tarea es extraer información desde:
                    1. Información sobre delitos: Si deseas obtener información sobre los delitos en un municipio, utiliza la base de datos.    
                    2. Información general de documentos de política pública: Si deseas obtener información general de creación de PISCC, leyes o política pública, utiliza información del retriever. 
                    
                    Utiliza las herramientas ("TOOLS") disponibles para proporcionar la información indicada que necesitas para crear un documento PISCC.
                    IMPORTANTE: 
                    - En caso de que no se especifique el año, se asumirá que se está hablando del año 2024.
                    - En caso de que no se especifique el municipio, se asumirá que se está hablando de {municipio}.
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


# query = "Cómo construir un piscc?"
# query = "cuantos municipios existen en la base de datos?"
# print(test_agent.invoke({"conversation_history": [], "input": query}))


def fip_model_with_tools(query, conversation, municipio):
    chat_history = create_chat_history(conversation)
    # response = conversation_rag_chain.invoke({
    #     "chat_history": chat_history,
    #     "input": query
    # })

    print(municipio)
    tool_agent = Chain_with_tool(municipio)
    response = tool_agent.invoke({"chat_history": chat_history, "input": query})
    return response["output"]

municipio = "Bogotá, D.C. Cap."
#query = "Cómo construir un piscc?"
#query = "cuantos municipios existen en la base de datos?"
#query = "3 delitos más frecuentes en el municipio de Giraldota el año 2024"
#query = "Cual es el objetivo de la estrategia Generación de conocimiento sobre el fenómeno del abigeato para el delito de Abigeato "
query = "cual es la tasa por cada mil habitantes del delito extorsión en año 2014"
conversation = [
        {
            "created_at": "2024-05-03 12:49:37.377881",
            "text_content": "si, estoy ubicado ahi",
            "conversation_id": 5,
            "origin": "User",
            "id": 177
        }]
# query = "cuantos municipios existen en la base de datos?"
# print(test_agent.invoke({"conversation_history": [], "input": query}))

print(fip_model_with_tools(query, conversation, municipio))