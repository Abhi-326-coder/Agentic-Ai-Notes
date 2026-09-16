from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser


load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)


prompt = ChatPromptTemplate.from_template(

    """
    You are an AI teacher.

    Explain the following topic simply.

    Topic:
    {topic}
    """

)


parser = StrOutputParser()


chain = (

    prompt
    |
    model
    |
    parser

)


for chunk in chain.stream({

    "topic": "AI Agents"

}):

    print(
        chunk,
        end="",
        flush=True
    )
