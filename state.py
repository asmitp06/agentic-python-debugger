from dataclasses import dataclass, field
from typing import Optional

@dataclass
class AgentState:
    original_code: str
    current_code: str
    context: str
    executor_json: Optional[dict] = None
    analyzer_json: Optional[dict] = None
    critic_json: Optional[dict] = None
    fix_attempts: int = 0
    critic_attempts: int = 0
    max_fix_attempts: int = 3
    max_critic_attempts: int = 1
    passed: bool = False
    approved: bool = False
    history: list = field(default_factory=list)

    def log(self, step: str, data: dict):
        self.history.append({"step": step, **data})
        print(f"[{step.upper()}] {data.get('summary', data)}")