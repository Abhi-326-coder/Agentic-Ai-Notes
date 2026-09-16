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