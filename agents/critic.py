from state import AgentState
import re
import json
from typing import Dict, Any, List
from utils.llm_client import call_llm  # same client as fixer/analyzer

# Global counter for stub mode behavior (optional, mirrors analyzer style)
critic_call_count = 0

SYSTEM_PROMPT = """You are a senior code reviewer.
Your job is to review code that already passes tests and decide if it is good enough to ship.

Focus on:
- Readability and naming
- Comments and docstrings
- Structure and duplication
- Simplicity vs. unnecessary complexity
- Basic performance issues (e.g., obvious O(n^2) where O(n) is trivial)

Return ONLY valid JSON in this exact schema:
{
  "approved": boolean,
  "summary": "One-sentence overall assessment.",
  "review_items": [
    {
      "line": number (1-based line number),
      "type": "Naming" | "Style" | "Structure" | "Performance" | "Docs" | "Other",
      "message": "Short description of the issue.",
      "suggestion": "Concrete suggestion for improvement."
    }
  ]
}

If the code is good enough to ship, set "approved": true and "review_items": [].
Be specific about line numbers and suggestions. Do NOT include Markdown fences."""


STUB_MODE = True  # flip to False when ready for real LLM calls


def critic(state: AgentState) -> AgentState:
    """
    Critic: reviews code quality and optimization.
    Input:   state.current_code, state.context (optional)
    Output:  state.critic_json with fields: approved, summary, review_items[]
    """
    global critic_call_count
    critic_call_count += 1

    if STUB_MODE:
        # Simple stub: first time, reject with two review items; later, approve
        if critic_call_count == 1:
            critic_json = {
                "approved": False,
                "summary": "Stub: code works, but readability and maintainability need improvement.",
                "review_items": [
                    {
                        "line": 2,
                        "type": "Naming",
                        "message": "Variable name 'x' is unclear.",
                        "suggestion": "Rename to 'total_sum'."
                    },
                    {
                        "line": 6,
                        "type": "Docs",
                        "message": "Missing function docstring.",
                        "suggestion": "Add a short docstring describing purpose and inputs."
                    }
                ]
            }
        else:
            critic_json = {
                "approved": True,
                "summary": "Stub: code quality is acceptable.",
                "review_items": []
            }

        state.critic_json = critic_json
        state.log("critic", {
            "summary": critic_json["summary"],
            "approved": critic_json["approved"],
            "review_item_count": len(critic_json["review_items"]),
            "call": critic_call_count
        })
        return state

    # Real LLM mode
    user_prompt = f"""## Code:
```python
{state.current_code}
```

## Context (optional high-level intent or constraints):
{state.context or "No additional context provided."}

The code already passes its tests. Review it for readability, maintainability, and basic performance.
Be concrete and reference exact line numbers."""

    response = call_llm(SYSTEM_PROMPT, user_prompt)

    # Strip accidental markdown fences
    response = re.sub(r"^```(?:json|python)?\n?|```$", "", response.strip(), flags=re.MULTILINE).strip()

    try:
        critic_json = json.loads(response)

        # Minimal schema validation
        if not isinstance(critic_json.get("approved"), bool):
            raise ValueError("Missing or invalid 'approved' field")
        if not isinstance(critic_json.get("summary"), str):
            raise ValueError("Missing or invalid 'summary' field")
        if not isinstance(critic_json.get("review_items"), list):
            raise ValueError("Missing or invalid 'review_items' field")

    except (json.JSONDecodeError, ValueError) as e:
        # Fallback if LLM output is bad
        critic_json = {
            "approved": True,
            "summary": f"Critic failed to parse LLM output; auto-approving. Reason: {str(e)}",
            "review_items": []
        }
        state.log("critic", {
            "error": f"Invalid JSON from LLM: {str(e)}",
            "raw_output_preview": response[:200]
        })

    state.critic_json = critic_json
    state.log("critic", {
        "summary": critic_json["summary"][:120],
        "approved": critic_json["approved"],
        "review_item_count": len(critic_json["review_items"])
    })
    return state