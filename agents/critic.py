# agents/critic.py  (STUB — Xhaiden will replace this)
from state import AgentState
def critique(state: AgentState) -> AgentState:
    state.critic_json = {
        "approved": True,
        "summary": "Stub: approved",
        "review_items": []
    }
    state.log("critic", {"summary": "STUB critic ran"})
    return state