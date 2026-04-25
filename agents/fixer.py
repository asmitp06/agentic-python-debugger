import re
from langchain_core.prompts import ChatPromptTemplate
from utils.llm_client import llm  # Import the LangChain LLM instance
from state import AgentState

SYSTEM_PROMPT = """You are an expert software engineer and debugger.
You will be given code and a list of specific issues with exact line numbers.
Fix ONLY the listed issues. Do not change anything else.
Return ONLY the corrected code. No explanations, no markdown fences."""

STUB_MODE = True   # flip to False when ready for real LLM calls

def fix(state: AgentState) -> AgentState:
    if STUB_MODE:
        state.current_code = state.current_code + "\n# stub fix applied"
        state.fix_attempts += 1
        state.log("fixer", {"summary": f"STUB fix attempt {state.fix_attempts}"})
        return state
    
    # Decide which feedback to use: critic takes priority if present, else analyzer
    if state.critic_json and not state.critic_json.get("approved", True):
        issues = state.critic_json.get("review_items", [])
        feedback_label = "Code Review Feedback (style/quality)"
    else:
        issues = state.analyzer_json.get("issues", [])
        feedback_label = "Bug Report (correctness errors)"

    issues_text = "\n".join(
        f"  - Line {i.get('line', '?')}: [{i.get('type','?')}] {i.get('message','?')} → {i.get('fix_hint') or i.get('suggestion','')}"
        for i in issues
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", f"""## Code:
```python
{state.current_code}
```

## {feedback_label}:
{issues_text}

Return ONLY the fixed Python code. No markdown, no explanation."""),
    ])
    chain = prompt | llm
    fixed = chain.invoke({}).content.strip()
    # Strip accidental fences
    fixed = re.sub(r"^```(?:python)?\n?|```$", "", fixed.strip(), flags=re.MULTILINE).strip()

    state.current_code = fixed
    state.fix_attempts += 1
    state.log("fixer", {
        "summary": f"Fix attempt {state.fix_attempts}, used {'critic' if state.critic_json else 'analyzer'} feedback",
        "fixed_code_preview": fixed[:120]
    })
    return state