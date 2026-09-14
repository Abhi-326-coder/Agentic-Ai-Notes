from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert AI teacher.

        Explain concepts simply in 1 sentence.

        Use real-world examples.
        """
    ),
    (
        "human",
        "Explain {topic}"
    )
])

messages = prompt.invoke({
    "topic":"Vectore Database"
})

response = model.invoke(messages)

print(response.content)