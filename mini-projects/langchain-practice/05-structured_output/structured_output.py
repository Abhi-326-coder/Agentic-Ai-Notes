from dotenv import load_dotenv

from pydantic import BaseModel

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash"
)

class TopicExplanation(BaseModel):
    concept: str

    difficulty: str

    important_topics: list[str]

    example: str
    
stuctured_model = model.with_structured_output(
    TopicExplanation
)

result = stuctured_model.invoke(
    """
        Explain RAG.
        
        Include:
        -Concept in single sentence
        -Difficulty
        -Impostant topics
        -one Real-world example 
    """
)

print("Concept:")
print(result.concept)

print("\nDifficulty:")
print(result.difficulty)

print("\nImportant Topics:")
print(result.important_topics)

print("\nExample:")
print(result.example)