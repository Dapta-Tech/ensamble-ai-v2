import streamlit as st
import time
import re
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain.retrievers import (MergerRetriever,)

# Streamed response emulator
def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.02)

#Load bases from a list of namespaces
def load_bases(index_name= "",bases_list = []):
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
def get_LOFR(big_vector):
    LOFR = []
    for vector_store in big_vector:
        LOFR.append(vector_store.as_retriever())
    return LOFR

#Creates the retriever chain with the context LOTR.
def get_context_retriever_chain(big_vector):
    llm = ChatOpenAI()
    LOFR = get_LOFR(big_vector)

    retriever = MergerRetriever(retrievers=LOFR)

    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", """Dada la indicación anterior: {input} ten en cuenta que,\
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
        de la tabla generada.""")])
    
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    return retriever_chain

#Creates the conversational RAG chain.
def get_conversational_rag_chain(retriever_chain): 
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "No eres un asistente, Tu tarea es crear 3 tipos de gráficos con Javascript Chart.js\
        o una tabla en HTML\
	    provisto por el usuario en el siguiente contexto: {context},\
        Tu tarea es devolver el texto en formato HTML de tablas o Javascript con los gráficos solicitados."),
        ("user", "{input}"),
    ])
    
    stuff_documents_chain = create_stuff_documents_chain(llm,prompt)
    return create_retrieval_chain(retriever_chain, stuff_documents_chain)

#Gets the response from the conversational RAG chain.
def get_response(user_input):
    retriever_chain = get_context_retriever_chain(st.session_state.vector_store)
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)
    
    response = conversation_rag_chain.invoke({
        "chat_history": st.session_state.chat_history,
        "input": user_input
    })
    
    return response['answer']

#Completes the URL with 'https://' and 'www.' if not present.
def complete_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://www." + url
    elif url.startswith("www."):
        url = "https://" + url
    return url

#Checks if the URL is valid.
def is_valid_url(url):
    pattern = r'^(https?:\/\/)(www\.)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$'
    return re.match(pattern, url) is not None

if __name__ == "__main__":
    st.set_page_config(page_title="Ensamble V2", page_icon="🤖")
    st.title("Crea un gráfico para tu PISCC")

    if "vector_store" not in st.session_state:
        st.session_state.vector_store = load_bases(index_name = "all-data-v1",
                                                    bases_list = 
                                                    ["unstructured-data",
                                                    "1-Politica-Publica",
                                                    "2-caracterizacion-municipal",
                                                    "4-Base-estrategias"])

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Habla con el bot..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write_stream(response_generator(prompt))

        response = get_response(prompt)
        with st.chat_message("assistant"):
            st.write_stream(response_generator(response))
        st.session_state.messages.append({"role": "assistant", "content": response})
