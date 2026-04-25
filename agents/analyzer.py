from state import AgentState
import re
import json
from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from utils.llm_client import llm  # Import the LangChain LLM instance

# Global counter for stub mode
call_count = 0

SYSTEM_PROMPT = """You are an expert software debugger and analyzer.
Analyze the code, context, and executor output. Identify specific errors with line numbers.

Return ONLY valid JSON matching this exact schema:
{
  "is_correct": boolean,
  "summary": "Brief one-sentence explanation of the main issues",
  "issues": [
    {
      "line": number (1-based line number),
      "type": string ("SyntaxError", "RuntimeError", "AssertionError", "LogicError", "EdgeCase", "Performance"),
      "message": "Exact error message or description",
      "cause": "Why this error happened",
      "fix_hint": "Specific suggestion for how to fix it"
    }
  ]
}

If there are NO errors, set "is_correct": true and "issues": [].
If multiple errors, list them all with specific line numbers.
Be precise about line numbers. Use context to understand expected behavior."""


def analyze(state: AgentState) -> AgentState:
    global call_count
    call_count += 1
    
    # Use LangChain chain for analysis
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", f"Code:\n{state.current_code}\n\nContext: {state.context}\n\nExecution Output: {state.execution_output}"),
    ])
    parser = JsonOutputParser()
    chain = prompt | llm | parser
    analyzer_json = chain.invoke({})
    
    state.analyzer_json = analyzer_json
    state.log("analyzer", {"summary": f"Analyzer call #{call_count}, is_correct={analyzer_json.get('is_correct', False)}"})
    return state