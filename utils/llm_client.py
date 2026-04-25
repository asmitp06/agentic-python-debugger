import os
import json
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

# Initialize LangChain's Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY_2"),
    temperature=0.0,  # For deterministic responses in debugging
)

def call_llm(system_prompt: str, user_prompt: str, **kwargs) -> str:
    # Use LangChain's prompt template for structured prompting
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", user_prompt),
    ])
    chain = prompt | llm
    response = chain.invoke({})
    return response.content.strip()

def call_llm_json(system_prompt: str, user_prompt: str, **kwargs) -> dict:
    # Use LangChain's JSON output parser for reliable parsing
    parser = JsonOutputParser()
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt + "\n\nReturn ONLY valid JSON matching the schema."),
        ("human", user_prompt),
    ])
    chain = prompt | llm | parser
    for _ in range(2):
        try:
            return chain.invoke({})
        except Exception as e:
            continue
    raise ValueError(f"LLM returned invalid JSON after 2 attempts")