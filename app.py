import io
import pytz
import datetime
import pandas as pd
import streamlit as st
from langchain import hub
from pinecone import Pinecone
from google.cloud import storage
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

suggestion_list = ['¿Cuándo se creó La Constitución Política de Colombia?',
                    '¿Cuál es la tasa de analfabetismo en el municipio de Paujil?',
                    '¿Dónde que la provincia de Arroyohondo?',
                    '¿Un policía puede expedir normas?',
                    '¿Qué objetivo tiene el proceso de reglamentación que debe iniciar el Ministerio de Educación Nacional?']

csv_file = 'fip_feedback.csv' 
bucket_name = 'taxo-pdfs'

def load_base():
    index_name = "all-data-v1"
    pc = Pinecone()
    index = pc.Index(index_name)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    text_field = "text"
    vectorstore = PineconeVectorStore(index, embeddings, text_field, namespace = "unstructured-data")
    retriever = vectorstore.as_retriever()
    return retriever

def load_llm():
    llm = ChatOpenAI(
        model_name='gpt-3.5-turbo',
        temperature=0)
    retriever = load_base()
    qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever)
    return qa

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def generate_response(query):
    return qa.run(query)

def get_source(q):
    prompt = ChatPromptTemplate.from_template('''Eres un asistente que provee información precisa sobre políticas, leyes, Caracterización Municipal, números sobre delitos y bases sobre estrategias, tu tarea es proveer información precisa y sin emitir opinión para que altos mandos de cada municipio o ciudad puedan tomar decisiones basados en tu informaicón para la construcción del PISCC, recuerda que tu respuesta debe ser directa y al punto.
                                            Pregunta: {question} 
                                            Contexto: {context}
                                            Respuesta:''')
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    retriever = load_base()
    rag_chain_from_docs = (
    RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
    | prompt
    | llm
    | StrOutputParser())
    rag_chain_with_source = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}).assign(answer=rag_chain_from_docs)
    source = rag_chain_with_source.invoke(q)
    return source

def get_documents(source):
    source = source['context']
    docs_list = []
    docs_list.append(source)
    return  docs_list

def download_csv_from_bucket(csv_file, bucket_name):
    """Downloads a CSV file from a Google Cloud Storage bucket and loads it into a DataFrame."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(csv_file)
        content = blob.download_as_string()
        df = pd.read_csv(io.BytesIO(content))
        return df
    except Exception as e:
        print("Error downloading CSV:", e)
        return pd.DataFrame()

def add_data_to_csv(df, data):
    """Adds new data to a DataFrame and saves it to a CSV file."""
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    return df

def upload_csv_to_bucket(df, csv_file, bucket_name):
    """Saves a DataFrame to a CSV file and uploads it to a Google Cloud Storage bucket."""
    try:
        with io.StringIO() as csv_buffer:
            df.to_csv(csv_buffer, index=False)
            new_content = csv_buffer.getvalue().encode()

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(csv_file)
        blob.upload_from_string(new_content, content_type='text/csv')
    except Exception as e:
        print("Error uploading CSV:", e)

def get_answer(source):
    return source['answer']

if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ''
if 'user_question' not in st.session_state:
    st.session_state['user_question'] = ''
if 'improvement_suggestions' not in st.session_state:
    st.session_state['improvement_suggestions'] = ''
if 'missing_details' not in st.session_state:
    st.session_state['missing_details'] = ''
if 'source_details' not in st.session_state:
    st.session_state['source_details'] = ''
if 'useful' not in st.session_state:
    st.session_state['useful'] = 'Sí'

if __name__ == "__main__":
    df = download_csv_from_bucket(csv_file, bucket_name)
    qa = load_llm()

    st.session_state.user_question = None
    st.session_state.feedback = None

    qa = load_llm()

    st.image('dapta-portada.png')
    st.title(' 🤖 Ensamble AI 2.0   🤖 ')
    st.divider()
    st.write('Hola, soy el asistente en construcción ⌛ para la generación de PISCC. Sigo entrenándome con los documentos estructurados como ser excels y bases de datos, pero también puedo responder preguntas generales sobre los documentos no estructurados que son todos los PDFs.')
    st.divider()
    st.write("Aquí te dejo algunas preguntas que puedes realizarme como sugerencia:")

    for elemento in suggestion_list:
        st.write("- " + elemento)

    st.divider()
    st.session_state.user_name = st.text_input('Ingrese su nombre:', value=st.session_state.user_name)
    st.session_state.user_question = st.text_input('Realizar pregunta:', value=st.session_state.user_question)
    if st.session_state.user_question:
        source = get_source(st.session_state.user_question)
        doc_string = get_documents(source)
        #doc_string = "\n".join([f"- {key} en la página {value}" for key, value in docs.items()])
    else:
        source = {'answer': ''}
        doc_string = ""

    if st.button('Enviar Pregunta'):
        answer = get_answer(source)
        st.write('Respuesta: ')
        st.write(answer)
        st.divider()

    st.session_state.useful = st.radio('¿La respuesta fue útil?', ['Sí', 'No'], index=('Sí', 'No').index(st.session_state.useful))
    if st.session_state.useful == 'No':
        st.write('Por favor, ingresa el motivo por el cual la respuesta no fue útil:')
        st.session_state.improvement_suggestions = st.text_input('Ingresar sugerencias de mejora:', value=st.session_state.improvement_suggestions, placeholder='Ejemplo: "Me gustaría que la respuesta fuera más detallada"')
        st.session_state.missing_details = st.text_input('Ingresar detalles faltantes:', value=st.session_state.missing_details, placeholder='Ejemplo: "Falta información sobre del banco Itaú"')
        st.session_state.source_details = st.text_input('Ingresar detalles de la fuente:', value=st.session_state.source_details, placeholder='Ejemplo: "Al pedir la fuente me da una errónea "')

    if st.button('Enviar feedback'):
        # Resetear las entradas después de enviar el feedback
        mexico_tz = pytz.timezone('America/Bogota')
        current_datetime = datetime.datetime.now(mexico_tz)
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        new_data = {
            "user": st.session_state.user_name, 
            "date": formatted_datetime, 
            "question": st.session_state.user_question, 
            "source": doc_string, 
            "answer": get_answer(source), 
            "useful": st.session_state.useful, 
            "improvement_suggestions": st.session_state.improvement_suggestions, 
            "missing_details": st.session_state.missing_details, 
            "source_details": st.session_state.source_details
        }

        df = add_data_to_csv(df, new_data)
        upload_csv_to_bucket(df, csv_file, bucket_name)
        st.success("¡Feedback enviado con éxito!")