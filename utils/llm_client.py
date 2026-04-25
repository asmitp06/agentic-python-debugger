import os
import json
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def call_llm(system_prompt: str, user_prompt: str, **kwargs) -> str:
    full_prompt = f"{system_prompt}\n\n{user_prompt}"
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )
    return response.text.strip()

def call_llm_json(system_prompt: str, user_prompt: str, **kwargs) -> dict:
    for _ in range(2):
        raw = call_llm(system_prompt, user_prompt)
        cleaned = re.sub(r"^```(?:json)?\n?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            continue
    raise ValueError(f"LLM returned invalid JSON after 2 attempts:\n{raw}")