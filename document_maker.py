import streamlit as st
import time
import re
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

# Streamed response emulator
def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.02)

def load_base():
    index_name = "all-data-v1"
    pc = Pinecone()
    index = pc.Index(index_name)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    text_field = "text"
    vectorstore = PineconeVectorStore(index, embeddings, text_field, namespace = "unstructured-data")
    return vectorstore

#Creates the retriever chain with the context retriever.
def get_context_retriever_chain(vector_store):
    llm = ChatOpenAI()
    retriever = vector_store.as_retriever()
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        ("user", "Dada la conversación anterior, respone la pregunta: {input}\
        Tu respuesta debe ser coherente con el contexto de la conversación \
        Teniendo como objetivo principal la creación del  Plan Integral de Seguridad \
        y Convivencia Ciudadana PISCC para mi municipio.")
    ])
    
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    return retriever_chain

#Creates the conversational RAG chain.
def get_conversational_rag_chain(retriever_chain): 
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un bot encargado de guiar a usuarios a la creación de \
        la sección de objetivos del PISCC e mi municipio\
	provisto por el usuario en el siguiente contexto: {context},\
        Para iniciar la ocnversación siempre consulta el municipio del cual es el usuario\
        Toma ne cuenta que el objetivos 2024  debe iniciar con un verbo en infinitivo, \
        como, por ejemplo: aumentar, fortalecer, mejorar, etc. \
        Ten presente que el objetivo general del PISCC debe determinar\
        las transformaciones al mediano y largo plazo que se pretenden \
        lograr en el municipio o departamento, según sea el caso.."),
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
    st.title("Crea la sección de Objetivos de tu PISCC")

    if "vector_store" not in st.session_state:
        st.session_state.vector_store = load_base()

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
