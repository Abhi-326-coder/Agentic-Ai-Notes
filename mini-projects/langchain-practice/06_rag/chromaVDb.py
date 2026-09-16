from langchain_chroma import Chroma

from langchain_google_genai import(
    GoogleGenerativeAIEmbeddings
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_community.document_loaders import(
    PyPDFLoader
)

loader = PyPDFLoader(
    "internship-programs.pdf"
)

documents = loader.load()

splitter = RecursiveCharacterTextSplitter(

    chunk_size=1000,

    chunk_overlap=200

)


chunks = splitter.split_documents(
    documents
)


print(

    f"Number of chunks: {len(chunks)}"

)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

vector_store = Chroma.from_documents(

    documents=chunks,

    embedding=embeddings,

    persist_directory="./chroma_db"

)

results = vector_store.similarity_search(
    "what is rag?",
    k=3
)

for document in results:

    print(

        document.page_content

    )

    print(

        document.metadata

    )

    print("-" * 50)