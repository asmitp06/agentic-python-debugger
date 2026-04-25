from state import AgentState

call_count = 0

def analyze(state: AgentState) -> AgentState:
    global call_count
    call_count += 1
    is_correct = call_count > 1  # fails once, then passes

    state.analyzer_json = {
    "is_correct": False,
    "summary": "Stub: always failing",
    "issues": [
        {"line": 8, "type": "NameError", "message": "totl undefined", "fix_hint": "rename to total"}
    ]
    }
    
    state.log("analyzer", {"summary": f"STUB analyzer call #{call_count}, is_correct={is_correct}"})
    return state