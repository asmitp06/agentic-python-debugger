# agents/executor.py  — chains TestCaseMaker → CodeRunner
from state import AgentState
from agents.testcase_maker import make_test_cases
from agents.code_runner import run_code

def execute(state: AgentState) -> AgentState:
    # Step 1: Generate test cases from code + context
    test_cases = make_test_cases(state.current_code, state.context)

    # Step 2: Run code against those test cases
    state = run_code(state, test_cases)

    return state