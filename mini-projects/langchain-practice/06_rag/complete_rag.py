from dotenv import load_dotenv
from pathlib import Path

from langchain_core.tools import tool

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)

from pypdf import PdfReader
from langchain_core.documents import Document

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_chroma import Chroma

from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_core.runnables import (
    RunnablePassthrough
)

from langchain_core.output_parsers import (
    StrOutputParser
)


# Load environment variables
load_dotenv()


# --------------------------------
# 1. LOAD GEMINI MODEL
# --------------------------------

model = ChatGoogleGenerativeAI(

    model="gemini-2.5-flash"

)


# --------------------------------
# 2. LOAD DOCUMENT
# --------------------------------

pdf_path = Path(__file__).with_name("internship-programs.pdf")
reader = PdfReader(pdf_path)
documents = [
    Document(page_content=page.extract_text() or "", metadata={"source": str(pdf_path), "page": i})
    for i, page in enumerate(reader.pages)
]


# --------------------------------
# 3. SPLIT DOCUMENT
# --------------------------------

splitter = RecursiveCharacterTextSplitter(

    chunk_size=1000,

    chunk_overlap=200

)


chunks = splitter.split_documents(

    documents

)


# --------------------------------
# 4. CREATE EMBEDDINGS
# --------------------------------

embeddings = GoogleGenerativeAIEmbeddings(

    model="models/gemini-embedding-001"

)


# --------------------------------
# 5. CREATE VECTOR DATABASE
# --------------------------------

vector_store = Chroma.from_documents(

    documents=chunks,

    embedding=embeddings

)


# --------------------------------
# 6. CREATE RETRIEVER
# --------------------------------

retriever = vector_store.as_retriever(

    search_kwargs={

        "k": 3

    }

)


# --------------------------------
# 7. FORMAT DOCUMENTS
# --------------------------------

def format_docs(docs):

    return "\n\n".join(

        doc.page_content

        for doc in docs

    )


# --------------------------------
# 8. CREATE PROMPT
# --------------------------------

prompt = ChatPromptTemplate.from_template(

    """
    You are a helpful AI assistant.

    Answer the question using ONLY
    the context provided below.

    If the answer is not present
    in the context, say:

    "I don't know based on the
    provided document."


    CONTEXT:

    {context}


    QUESTION:

    {question}
    """

)


# --------------------------------
# 9. CREATE RAG CHAIN
# --------------------------------

rag_chain = (

    {

        "context":

            retriever
            |
            format_docs,


        "question":

            RunnablePassthrough()

    }

    |

    prompt

    |

    model

    |

    StrOutputParser()

)



# --------------------------------
# 10. ASK QUESTION
# --------------------------------

question = input(

    "\nAsk a question: "

)


answer = rag_chain.invoke(

    question

)


print(

    "\nANSWER:\n"

)

print(

    answer

)
