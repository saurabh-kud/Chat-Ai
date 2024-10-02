from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from app.utils.config import configs
from fastapi import HTTPException
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI

# Initialize the models
print(configs.OPENAI_API_KEY)
llms = {
    "gemini": ChatGoogleGenerativeAI(
        google_api_key=configs.GOOGLE_API_KEY,
        model="gemini-1.5-pro",
        temperature=0,
    ),
    "chatgpt": ChatOpenAI(
        api_key=configs.OPENAI_API_KEY,
        model="gpt-4o",
        temperature=0,
    ),
}


def get_result_from_llms(
    model_name: str, context: str, user_query: str, stream: bool = False
):
    try:
        if model_name not in llms:
            raise HTTPException(status_code=400, detail="Invalid model name")

        USER_PROMPT = f"Query: {user_query}\n\nResults:\n"
        # SYSTEM_PROMPT = f"""
        #     You are a question answering system that is constantly learning and improving.
        #     You can process and comprehend vast amounts of text and utilize this knowledge to provide grounded, accurate, and as concise as possible answers to diverse queries.
        #     Your answer should be well-organized, featuring appropriate headers, subheaders, bullet points, lists, tables to enhance readability.
        #     You always clearly communicate ANY UNCERTAINTY in your answer. DO NOT echo any given command in your answer.
        #     Analyze the data properly and after give the result
        #     \n\n
        #     Context: {context}
        # """
        SYSTEM_PROMPT = f"""
            You are an advanced AI system specialized in answering questions based on user input and provided context. Your primary goal is to deliver clear, concise, and well-structured answers using the following guidelines:

            1. **Accuracy:** Base your responses on the context provided and your internal knowledge. If unsure, acknowledge uncertainty without guessing.
            2. **Clarity:** Provide explanations in simple and clear language, suitable for a wide audience. Avoid jargon unless necessary, and explain any complex terms.
            3. **Structure:** Organize your answers with:
                - Headings
                - Subheadings
                - Bullet points
                - Numbered lists
                - Tables (where applicable)

            4. **Focus:** Directly answer the question without unnecessary details. Offer additional relevant insights only when useful to the user query.

            5. **Context-Aware:** Incorporate the provided context when forming your answers. Do not repeat or rephrase the context unnecessarily, but make sure your answer is informed by it.

            6. **Uncertainty:** If there is any ambiguity or missing information in the query, clearly state the assumptions you are making or request further clarification.

            7. **Data Handling:** When presenting data:
                - Use tables for comparative analysis.
                - Provide concise summaries for complex data sets.
                - Offer actionable insights based on the analysis.

            8. **Avoid Echoing:** Do not repeat the user's question or provided context unnecessarily.

            ### Context:
            {context}

            ### User Query:
            {user_query}

            Your task is to analyze the user query in the given context and provide the most accurate, well-organized, and clear response possible.
            """

        messages = [("system", SYSTEM_PROMPT), ("human", USER_PROMPT)]

        llm = llms[model_name]
        if stream:
            # Use streaming logic if enabled
            result = ""
            for chunk in llm.stream(messages):
                result += chunk.content
            return result
        else:
            # Regular invocation without streaming
            try:
                response = llm.invoke(messages)
                return response.content
            except Exception as e:
                print(str(e))
                raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
