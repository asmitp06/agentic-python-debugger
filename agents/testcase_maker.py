# agents/testcase_maker.py
import json
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.llm_client import call_llm_json

def make_test_cases(code: str, context: str) -> list:
    system_prompt = "You are a test case generator. Generate 3-5 test cases for the given code based on the context. Return only a JSON list of dicts with 'input' and 'expected' keys."
    user_prompt = f"Code:\n{code}\n\nContext: {context}\n\nGenerate test cases as: [{{'input': '...', 'expected': '...'}}]"
    
    try:
        result = call_llm_json(system_prompt, user_prompt)
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