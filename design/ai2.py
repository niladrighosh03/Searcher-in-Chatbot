import nltk
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import NLTKTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough




# Download NLTK data
nltk.download('punkt')

# Google API key and models
key='AIzaSyDE_ldK9alrl9f0QkgrchtwpGMILTVr2qQ'
chat_model = ChatGoogleGenerativeAI(google_api_key=key, model="gemini-1.5-pro-latest")
embedding_model = GoogleGenerativeAIEmbeddings(google_api_key=key, model="models/embedding-001")

# Text splitter
text_splitter = NLTKTextSplitter(chunk_size=500, chunk_overlap=100)

# Function to dynamically process a video
def process_video(video_url):
    loader = YoutubeLoader.from_youtube_url(video_url)
    pages = loader.load_and_split()
    chunks = text_splitter.split_documents(pages)
    db = Chroma.from_documents(chunks, embedding_model, persist_directory="./chroma_db_")
    db.persist()
    return Chroma(persist_directory="./chroma_db_", embedding_function=embedding_model)

# RAG chain setup
def create_rag_chain(db_connection):
    retriever = db_connection.as_retriever(search_kwargs={"k": 5})

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chat_template = ChatPromptTemplate.from_messages([
        SystemMessage(content="""You are a Helpful AI Bot. Given a context and question from user, you should answer based on the given context."""),
        HumanMessagePromptTemplate.from_template("""Answer the question based on the given context.
        Context: {context}
        Question: {question}
        Answer: """)
    ])

    output_parser = StrOutputParser()

    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | chat_template
        | chat_model
        | output_parser
    )





def get_response(video_url, question):
    if not video_url or not question:
        return "Both video_url and question are required."

    try:
        db_connection = process_video(video_url)
        rag_chain = create_rag_chain(db_connection)
        answer_to_prompt = rag_chain.invoke(question)
        return answer_to_prompt
    except Exception as e:
        return f"Error: {str(e)}"
    