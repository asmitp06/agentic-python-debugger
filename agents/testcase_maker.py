# agents/testcase_maker.py
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from utils.llm_client import llm  # Import the LangChain LLM instance

def make_test_cases(code: str, context: str) -> list:
    system_prompt = "You are a test case generator. Generate 3-5 test cases for the given code based on the context. Return only a JSON list of dicts with 'input' and 'expected' keys."
    user_prompt = f"Code:\n{code}\n\nContext: {context}\n\nGenerate test cases as: [{{'input': '...', 'expected': '...'}}]"
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", user_prompt),
    ])
    parser = JsonOutputParser()
    chain = prompt | llm | parser
    
    try:
        result = chain.invoke({})
        if isinstance(result, list) and all(isinstance(tc, dict) and 'input' in tc and 'expected' in tc for tc in result):
            return result
        else:
            # Fallback to stub if LLM fails
            return [
                {"input": "5, 3", "expected": "8"},
                {"input": "0, 0", "expected": "0"},
                {"input": "-1, 1", "expected": "0"},
            ]
    except Exception as e:
        print(f"LLM error in testcase_maker: {e}")
        return [
            {"input": "5, 3", "expected": "8"},
            {"input": "0, 0", "expected": "0"},
            {"input": "-1, 1", "expected": "0"},
        ]