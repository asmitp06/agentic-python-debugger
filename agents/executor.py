# agents/executor.py
import json
import os
import subprocess
import sys
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from agents.testcase_maker import make_test_cases
from state import AgentState

def run_executor(file_path: str, context: str) -> dict:
    with open(file_path, 'r') as f:
        code = f.read()
    
    test_cases = make_test_cases(code, context)
    
    # Check compilation
    try:
        compile(code, file_path, 'exec')
        compiled = True
        error_type = None
        error_message = None
        traceback = None
    except SyntaxError as e:
        compiled = False
        error_type = "SyntaxError"
        error_message = str(e)
        traceback = ""
        return {
            "compiled": compiled,
            "ran": False,
            "generated_tests": test_cases,
            "test_results": [],
            "error_type": error_type,
            "error_message": error_message,
            "traceback": traceback,
            "stdout": "",
            "stderr": ""
        }
    
    # Raw run
    ran = False
    stdout = ""
    stderr = ""
    try:
        result = subprocess.run(["python", file_path], capture_output=True, text=True, timeout=10)
        ran = result.returncode == 0
        stdout = result.stdout
        stderr = result.stderr
        if not ran:
            error_type = "RuntimeError"
            error_message = stderr.strip()
            traceback = ""
    except subprocess.TimeoutExpired:
        error_type = "TimeoutError"
        error_message = "Raw run timed out"
        traceback = ""
    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)
        traceback = ""
    
    # Run tests
    test_results = []
    for i, test in enumerate(test_cases):
        try:
            result = subprocess.run(["python", file_path], input=test["input"], capture_output=True, text=True, timeout=10)
            actual = result.stdout.strip()
            status = "pass" if actual == test["expected"] else "fail"
            test_results.append({
                "test_id": i + 1,
                "status": status,
                "input": test["input"],
                "expected": test["expected"],
                "actual": actual
            })
        except subprocess.TimeoutExpired:
            test_results.append({
                "test_id": i + 1,
                "status": "fail",
                "input": test["input"],
                "expected": test["expected"],
                "actual": "TimeoutError"
            })
        except Exception as e:
            test_results.append({
                "test_id": i + 1,
                "status": "fail",
                "input": test["input"],
                "expected": test["expected"],
                "actual": str(e)
            })
    
    return {
        "compiled": compiled,
        "ran": ran,
        "generated_tests": test_cases,
        "test_results": test_results,
        "error_type": error_type,
        "error_message": error_message,
        "traceback": traceback,
        "stdout": stdout,
        "stderr": stderr
    }

def execute(state: AgentState) -> AgentState:
    # Write current_code to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(state.current_code)
        temp_file = f.name
    try:
        state.executor_json = run_executor(temp_file, state.context)
    finally:
        os.unlink(temp_file)
    state.log("executor", {"summary": f"Executed code, compiled={state.executor_json['compiled']}, ran={state.executor_json['ran']}"})
    return state

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python agents/executor.py <file> <context>")
        sys.exit(1)
    file_path = sys.argv[1]
    context = sys.argv[2]
    result = run_executor(file_path, context)
    print(json.dumps(result, indent=2))