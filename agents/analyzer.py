from state import AgentState
import re
import json
from typing import Dict, Any, List
from utils.llm_client import call_llm  # Assuming you have this from fixer

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
    
    # Stub mode: fails first time, passes after
    if call_count == 1:
        is_correct = False
        analyzer_json = {
            "is_correct": False,
            "summary": "Stub: always failing",
            "issues": [
                {"line": 8, "type": "NameError", "message": "totl undefined", "fix_hint": "rename to total"}
            ]
        }
    else:
        is_correct = True
        analyzer_json = {
            "is_correct": True,
            "summary": "Stub: code now passes all tests",
            "issues": []
        }
    
    state.analyzer_json = analyzer_json
    state.log("analyzer", {"summary": f"STUB analyzer call #{call_count}, is_correct={is_correct}"})
    return state