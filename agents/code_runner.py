# agents/code_runner.py  (STUB — Shashank replaces)
from state import AgentState
def run_code(state: AgentState, test_cases: list) -> AgentState:
    state.executor_json = {
        "ran": False,
        "generated_tests": test_cases,
        "test_results": [
            {"test_id": 1, "status": "fail", "input": "5, 3", "expected": "8", "actual": "NameError"}
        ],
        "error_type": "NameError",
        "error_message": "name 'totl' is not defined",
        "traceback": "",
        "stdout": "",
        "stderr": "NameError: name 'totl' is not defined"
    }
    state.log("code_runner", {"summary": "STUB code_runner ran"})
    return state