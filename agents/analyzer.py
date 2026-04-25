from state import AgentState
import re
import json
from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from utils.llm_client import llm  # Import the LangChain LLM instance

# Global counter for stub mode behavior (optional, mirrors critic style)
analyzer_call_count = 0

SYSTEM_PROMPT = """You are an expert software debugger and code analyzer.
Your job is to analyze code execution results and identify errors. 
Focus on:
- Syntax errors
- Runtime errors (exceptions, crashes)
- Logic errors (incorrect output, wrong behavior)
- Type mismatches
- Missing variables or undefined names

Please fix the minimum viable error.
Ensure not to over complicate it, just fix core errors that impede the program from filling out its intended functionality.

Return ONLY valid JSON in this exact schema:
{{
  "is_correct": boolean,
  "summary": "One-sentence overall assessment.",
  "issues": [
    {{
      "line": number (1-based line number),
      "type": "Syntax" | "Runtime" | "Logic" | "Type" | "NameError" | "Other",
      "message": "Short description of the error.",
      "cause": "What caused this error.",
      "fix_hint": "Concrete suggestion for fixing it."
    }}
  ]
}}

If there are NO errors, set "is_correct": true and "issues": [].
Be specific about line numbers and causes. Do NOT include Markdown fences."""


STUB_MODE = False  # flip to False when ready for real LLM calls


def analyze(state: AgentState) -> AgentState:
    """
    Analyzer: detects errors in code based on execution results.
    Input:   state.current_code, state.context, state.executor_json
    Output:  state.analyzer_json with fields: is_correct, summary, issues[]
    """
    global analyzer_call_count
    analyzer_call_count += 1

    if STUB_MODE:
        # Simple stub: first time, find errors; later, code is correct
        if analyzer_call_count == 1:
            analyzer_json = {
                "is_correct": False,
                "summary": "Stub: code has syntax and logic errors.",
                "issues": [
                    {
                        "line": 1,
                        "type": "Syntax",
                        "message": "Missing colon after function definition.",
                        "cause": "Python function definitions require a colon.",
                        "fix_hint": "Add ':' at the end of the def line."
                    },
                    {
                        "line": 5,
                        "type": "NameError",
                        "message": "Variable 'result' is not defined.",
                        "cause": "Variable was never assigned before being used.",
                        "fix_hint": "Initialize 'result' before using it."
                    }
                ]
            }
        else:
            analyzer_json = {
                "is_correct": True,
                "summary": "Stub: code is now correct.",
                "issues": []
            }

        state.analyzer_json = analyzer_json
        state.log("analyzer", {
            "summary": analyzer_json["summary"],
            "is_correct": analyzer_json["is_correct"],
            "issue_count": len(analyzer_json["issues"]),
            "call": analyzer_call_count
        })
        return state

    # Real LLM mode using LangChain chain
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "## Code:\n```python\n{code}\n```\n\n## Context (optional high-level intent):\n{context}\n\n## Execution Output:\n```\n{execution}\n```\n\nAnalyze the code and execution output. Identify all errors with specific line numbers and causes."),
    ])
    parser = JsonOutputParser()
    chain = prompt | llm | parser
    analyzer_json = chain.invoke({
        "code": state.current_code,
        "context": state.context or "No additional context provided.",
        "execution": json.dumps(state.executor_json) if state.executor_json else "{}"
    })

    state.analyzer_json = analyzer_json
    state.log("analyzer", {
        "summary": analyzer_json["summary"],
        "is_correct": analyzer_json["is_correct"],
        "issue_count": len(analyzer_json["issues"]),
        "call": analyzer_call_count
    })
    return state