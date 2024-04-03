import streamlit as st
from pinecone import Pinecone
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

suggestion_list = ['¿Cómo pueden los responsables político-administrativos garantizar la alineación y coordinación de esfuerzos para la formulación del Plan Integral de Seguridad y Convivencia Ciudadana (PISCC), considerando los referentes de política del sector defensa, interior y justicia, con el fin de mantener la coherencia y la capacidad de acción integral en el manejo de la seguridad y la convivencia ciudadana en cada territorio?',
                    '¿Por qué representantes están conformados a nivel territorial los comités municipales, distritales y departamentales de convivencia escolar, que son de carácter permanente?']

def load_base():
    index_name = "ensamble-v2"
    pc = Pinecone()
    index = pc.Index(index_name)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    text_field = "text"
    vectorstore = PineconeVectorStore(index, embeddings, text_field)
    retriever = vectorstore.as_retriever()
    return retriever

def load_llm():
    llm = ChatOpenAI(
        model_name='gpt-3.5-turbo',
        temperature=0.5)
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
    #prompt = hub.pull("rlm/rag-prompt")
    prompt = ChatPromptTemplate.from_template('''Como asistente encargado de proporcionar información sobre la 'GUÍA METODOLÓGICA PARA LA FORMULACIÓN, IMPLEMENTACIÓN, SEGUIMIENTO Y EVALUACIÓN DE LOS PLANES INTEGRALES DE SEGURIDAD Y CONVIVENCIA CIUDADANA', tu objetivo es brindar ayuda detallada a los representantes de cada municipio. Tu función principal es proporcionar información precisa y objetiva, sin emitir opiniones personales. En caso de desconocer alguna información específica, responderás con 'No estás seguro al respecto, consulta a un experto'.
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
    docs_dict = {}
    for i in source:
        doc = i.metadata['source'][40:]
        page = i.metadata['page']
        docs_dict[doc] = page
    return  docs_dict

def get_answer(source):
    return source['answer']

if __name__ == "__main__":
    st.session_state.user_question = None
    st.session_state.feedback = None

    qa = load_llm()

    st.image('dapta-portada.png')
    st.title(' 🤖 Ensamble AI 2.0  🤖 ')
    st.divider()
    st.write('Hola, soy el asistente en generación de PISCC. Pregúntame lo que necesites.')
    st.divider()
    st.write("Aquí te dejo algunas preguntas que puedes realizarme como sugerencia:")

    for elemento in suggestion_list:
        st.write("- " + elemento)

    st.divider()

    question = st.text_input('Realizar pregunta:')


    if st.button('Enviar Pregunta'):
        source = get_source(question)
        docs = get_documents(source)
        answer = get_answer(source)
        st.write('Respuesta: ')
        st.write(answer)


    