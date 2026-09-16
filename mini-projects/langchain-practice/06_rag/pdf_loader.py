from langchain_community.document_loaders import PyPDFLoader


loader = PyPDFLoader(
    "internship-programs.pdf"
)


documents = loader.load()


for document in documents:

    print(document.page_content)

    print(document.metadata)
    

