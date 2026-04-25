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
issues array with line, type, message, cause, fix_hint fields.

If there are NO errors, set is_correct true and issues empty.
If multiple errors, list them all with specific line numbers.
Be precise about line numbers. Use context to understand expected behavior."""


def analyze(state: AgentState) -> AgentState:
    global call_count
    call_count += 1
    
    # Use LangChain chain for analysis
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "Code:\n{code}\n\nContext: {context}\n\nExecution Output: {execution}"),
    ])
    parser = JsonOutputParser()
    chain = prompt | llm | parser
    analyzer_json = chain.invoke({
        "code": state.current_code,
        "context": state.context,
        "execution": state.executor_json
    })
    
    state.analyzer_json = analyzer_json
    state.log("analyzer", {"summary": f"Analyzer call #{call_count}, is_correct={analyzer_json.get('is_correct', False)}"})
    return state