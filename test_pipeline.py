# test_pipeline.py
from main import run_pipeline

print("TEST 1: Code that fails then gets fixed")
print("-" * 40)
state = run_pipeline("samples/broken_syntax.py", "adds two numbers")
assert state.fix_attempts > 0, "Should have attempted at least one fix"
print("✓ TEST 1 PASSED\n")