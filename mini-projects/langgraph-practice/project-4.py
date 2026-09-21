from typing import TypedDict, Literal

from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from pydantic import BaseModel, Field

from langgraph.graph import (
    StateGraph,
    START,
    END
)


load_dotenv()

documents = [

    Document(
        page_content="""
        LangGraph is a framework for building
        stateful agent workflows using graphs.

        Workflows consist of state, nodes and edges.
        """
    ),

    Document(
        page_content="""
        LangGraph supports persistence through
        checkpointing.

        Checkpoints save graph state so workflows
        can resume across interactions.
        """
    ),

    Document(
        page_content="""
        Retrieval Augmented Generation combines
        retrieval with language models.

        Relevant documents are retrieved before
        generating an answer.
        """
    ),

    Document(
        page_content="""
        Vector databases store embeddings and
        support similarity search over vectors.
        """
    ),

    Document(
        page_content="""
        AI agents can use tools and make decisions
        about which actions to perform.
        """
    )
]


class GraphState(TypedDict):

    question: str

    rewritten_question: str

    documents: list

    documents_relevant: bool

    answer: str

    answer_grounded: bool

    attempts: int
    
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

vectorstore = FAISS.from_documents(
    documents,
    embeddings
)

retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 3
    }
)

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

def retrieve_node(state: GraphState):

    question = (
        state.get("rewritten_question")
        or state["question"]
    )

    docs = retriever.invoke(question)

    return {
        "documents": docs
    }
    
class DocumentGrade(BaseModel):

    relevant: bool = Field(
        description=(
            "Whether the retrieved documents "
            "contain information relevant to "
            "the question."
        )
    )
    
grader =  model.with_structured_output(DocumentGrade)

def grade_documents_node(state: GraphState):

    question = (
        state.get("rewritten_question")
        or state["question"]
    )

    context = "\n\n".join(
        doc.page_content
        for doc in state["documents"]
    )

    result = grader.invoke(
        f"""
        You are evaluating retrieved documents.

        Question:
        {question}

        Retrieved documents:
        {context}

        Determine whether the documents contain
        useful information for answering the
        question.
        """
    )

    return {
        "documents_relevant": result.relevant
    }
    
def route_after_grading(
    state: GraphState
):

    if state["documents_relevant"]:
        return "generate"

    if state["attempts"] >= 2:
        return "failed"

    return "rewrite"


def generate_node(state: GraphState):

    question = state["question"]

    context = "\n\n".join(
        doc.page_content
        for doc in state["documents"]
    )

    response = model.invoke(
        f"""
        Answer the user's question using only
        the provided context.

        Question:
        {question}

        Context:
        {context}

        If the context does not support an answer,
        say that the available context is
        insufficient.
        """
    )

    return {
        "answer": response.content
    }

def rewrite_node(state: GraphState):

    current_question = (
        state.get("rewritten_question")
        or state["question"]
    )

    response = model.invoke(
        f"""
        Rewrite the following question into a
        better search query for retrieving
        technical documentation.

        Preserve the original meaning.

        Question:
        {current_question}

        Return only the rewritten query.
        """
    )

    return {
        "rewritten_question":
            response.content.strip(),

        "attempts":
            state["attempts"] + 1
    }
    
def grade_answer_node(state: GraphState):

    context = "\n\n".join(
        doc.page_content
        for doc in state["documents"]
    )

    result = answer_grader.invoke(
        f"""
        Evaluate whether the generated answer
        is supported by the context.

        Context:
        {context}

        Answer:
        {state["answer"]}
        """
    )

    return {
        "answer_grounded":
            result.grounded
    }
    
def route_answer(state: GraphState):

    if state["answer_grounded"]:
        return "end"

    if state["attempts"] >= 2:
        return "failed"

    return "rewrite"

def failure_node(state: GraphState):

    return {
        "answer": (
            "I could not find enough relevant "
            "information in the knowledge base "
            "to answer the question reliably."
        )
    }
    
class AnswerGrade(BaseModel):

    grounded: bool = Field(
        description=(
            "Whether the answer is supported "
            "by the retrieved context."
        )
    )


answer_grader = model.with_structured_output(
    AnswerGrade
)

graph = StateGraph(
    GraphState
)

# NODES

graph.add_node(
    "retrieve",
    retrieve_node
)

graph.add_node(
    "grade_documents",
    grade_documents_node
)

graph.add_node(
    "rewrite",
    rewrite_node
)

graph.add_node(
    "generate",
    generate_node
)

graph.add_node(
    "grade_answer",
    grade_answer_node
)

graph.add_node(
    "failed",
    failure_node
)

# EDGES

graph.add_edge(
    START,
    "retrieve"
)

graph.add_edge(
    "retrieve",
    "grade_documents"
)

graph.add_conditional_edges(
    "grade_documents",
    route_after_grading,
    {
        "generate": "generate",
        "rewrite": "rewrite",
        "failed": "failed"
    }
)


graph.add_edge(
    "rewrite",
    "retrieve"
)

graph.add_edge(
    "generate",
    "grade_answer"
)

graph.add_conditional_edges(
    "grade_answer",
    route_answer,
    {
        "end":END,
        "rewrite":"rewrite",
        "failed":"failed"
    }
)

graph.add_edge(
    "failed",
    END
)

app = graph.compile()

result = app.invoke({
    "question":
        "What is a Langraph",

    "rewritten_question": "",

    "documents": [],

    "documents_relevant": False,

    "answer": "",

    "answer_grounded": False,

    "attempts": 0
})

print(
    result["answer"]
)