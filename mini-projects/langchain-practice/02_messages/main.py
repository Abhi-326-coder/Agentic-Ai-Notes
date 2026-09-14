from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    AIMessage
)
from dotenv import load_dotenv


load_dotenv()

model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash"
)


messages = [
    SystemMessage(
        content="""
            you are an expert AI teacher
            
            explain concepts simply
            
            use real-world examples.
        """
    ),
    
    HumanMessage(
        content="What is rag"
        
    )
]


response = model.invoke(messages)

print(response.content, response.tool_calls, response.type)