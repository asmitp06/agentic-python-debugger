import sys
import os
from state import AgentState
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

def load_code(filepath: str) -> str:
    with open(filepath, "r") as f:
        return f.read()

def run_pipeline(filepath: str, context: str) -> AgentState:
    from agents.executor import execute
    from agents.analyzer import analyze
    from agents.fixer import fix
    from agents.critic import critique

    code = load_code(filepath)
    state = AgentState(original_code=code, current_code=code, context=context)

    print("\n" + "="*55)
    print("  AUTOMATED CODE DEBUGGER & REFACTORING AGENT")
    print("="*55)

    # ── CORRECTNESS LOOP ──────────────────────────────────
    while not state.passed and state.fix_attempts < state.max_fix_attempts:

        print(f"\n── Iteration {state.fix_attempts + 1} ──────────────────────────────")

        # Step 1: Execute
        state = execute(state)

        # Step 2: Analyze
        state = analyze(state)

        if state.analyzer_json.get("is_correct"):
            state.passed = True
            print("[PIPELINE] ✓ Code is functionally correct. Moving to Critic.")
            break

        # Step 3: Fix
        if state.fix_attempts < state.max_fix_attempts:
            state = fix(state)
        else:
            print(f"[PIPELINE] ✗ Max fix attempts ({state.max_fix_attempts}) reached. Exiting.")
            print_summary(state)
            return state

    if not state.passed:
        print("[PIPELINE] ✗ Could not fix code. See history for details.")
        print_summary(state)
        return state

    # ── QUALITY LOOP ──────────────────────────────────────
    while not state.approved and state.critic_attempts <= state.max_critic_attempts:

        # Step 4: Critic
        state = critique(state)

        if state.critic_json.get("approved"):
            state.approved = True
            print("[PIPELINE] ✓ Critic approved. Code is ready.")
            break

        # Step 5: Fix using critic feedback
        print("[PIPELINE] Critic rejected. Applying quality fixes...")
        state = fix(state)
        state.critic_attempts += 1

        # Re-validate after quality fix
        state = execute(state)
        state = analyze(state)
        if not state.analyzer_json.get("is_correct"):
            print("[PIPELINE] ✗ Quality fix broke correctness! Aborting critic loop.")
            break

    print_summary(state)
    return state


def print_summary(state: AgentState):
    print("\n" + "="*55)
    print("  FINAL SUMMARY")
    print("="*55)
    print(f"  Fix iterations:    {state.fix_attempts}")
    print(f"  Critic iterations: {state.critic_attempts}")
    print(f"  Passed execution:  {state.passed}")
    print(f"  Critic approved:   {state.approved}")
    print(f"  Steps taken:       {[h['step'] for h in state.history]}")
    print("\n── Original Code ──────────────────────────────────")
    print(state.original_code)
    print("\n── Final Code ─────────────────────────────────────")
    print(state.current_code)

    base_name = os.path.basename(filepath)
    name_without_ext = os.path.splitext(base_name)[0]
    corrected_filepath = f"corrected/{name_without_ext}.py"
    os.makedirs("corrected", exist_ok=True)
    with open(corrected_filepath, "w") as f:
        f.write(state.current_code)
    print(f"\n✓ Corrected code saved to: {corrected_filepath}")

class MultiLineInputDialog(simpledialog.Dialog):
    def __init__(self, parent, title, prompt):
        self.prompt = prompt
        self.result = None
        super().__init__(parent, title=title)

    def body(self, master):
        tk.Label(master, text=self.prompt).pack(padx=5, pady=5)
        self.text = tk.Text(master, width=60, height=10)
        self.text.pack(padx=5, pady=5)
        return self.text  # Focus the text widget

    def apply(self):
        # Retrieve the text from the widget on "OK"
        self.result = self.text.get("1.0", tk.END).strip()

def get_context_multiline():
    root = tk.Tk()
    root.withdraw()
    dialog = MultiLineInputDialog(root, "Context Input", "Enter detailed processing context:")
    root.destroy()
    return dialog.result if dialog.result else "No context provided."

# Usage in your main.py:
if __name__ == "__main__":
    if len(sys.argv) < 2:
        # File selector + Multi-line context dialog
        filepath = filedialog.askopenfilename(title="Select a file to process")
        if not filepath: sys.exit(1)
        context = get_context_multiline()
    else:
        # CLI args provided: use them directly
        filepath = sys.argv[1]
        context = sys.argv[2] if len(sys.argv) > 2 else "No context provided."
    
    run_pipeline(filepath, context)