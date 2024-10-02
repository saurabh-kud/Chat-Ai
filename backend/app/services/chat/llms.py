from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from app.utils.config import configs

llm = ChatGoogleGenerativeAI(
    google_api_key=configs.GOOGLE_API_KEY,
    model="gemini-1.5-pro",
    temperature=0,
)


def get_result_from_llms(context: str, user_query):

    USER_PROMPT = f"Query: {user_query}\n\nResults:\n"

    SYSTEM_PROMPT = f"""
        You are a question answering system that is constantly learning and improving.
        You can process and comprehend vast amounts of text and utilize this knowledge to provide grounded, accurate, and as concise as possible answers to diverse queries.
        Your answer should be well-organized, featuring appropriate headers, subheaders, bullet points, lists, tables to enhance readability.
        You always clearly communicate ANY UNCERTAINTY in your answer. DO NOT echo any given command in your answer.
        Analyze the data properly and after give the result
        Context: {context}
        """

    messages = [
        ("system", SYSTEM_PROMPT),
        ("human", USER_PROMPT),
    ]
    response = llm.invoke(messages)
    res = response.content
    return res
