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

suggestion_list = ['¿Cuándo se creó La Constitución Política de Colombia?',
                    '¿Cuál es la tasa de analfabetismo en el municipio de Paujil?',
                    '¿Dónde que la provincia de Arroyohondo?',
                    '¿Un policía puede expedir normas?',
                    '¿Qué objetivo tiene el proceso de reglamentación que debe iniciar el Ministerio de Educación Nacional?']

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

    st.image('FIP.png')
    st.title(' 🤖 Ensamble AI 2.0  🤖 ')
    st.divider()
    st.write('Hola, soy el asistente en construcción ⌛ para la generación de PISCC. Sigo entrenándome con los documentos estructurados como ser excels y bases de datos, pero también puedo responder preguntas generales sobre los documentos no estructurados que son todos los PDFs.')
    st.divider()
    st.write("Aquí te dejo algunas preguntas que puedes realizarme como sugerencia:")

    for elemento in suggestion_list:
        st.write("- " + elemento)

    st.divider()

    question = st.text_input('Realizar pregunta:')


    if st.button('Enviar Pregunta'):
        source = get_source(question)
        answer = get_answer(source)
        st.write('Respuesta: ')
        st.write(answer)


    