"""Minimal customer-support agent (intentionally insecure, for scanner testing)."""

import pickle
import subprocess

import requests
from openai import OpenAI

# Hardcoded provider credential committed to source.
OPENAI_API_KEY = "sk-proj-FAKEKEYdonotuse-aBcDeF1234567890ghijkl"
client = OpenAI(api_key=OPENAI_API_KEY)


def llm(prompt: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content


def handle(user_message: str):
    # The model decides the next action and we run it as Python.
    plan = llm(f"Decide the next action for: {user_message}")
    return eval(plan)


def run_command(user_message: str) -> None:
    # The model proposes a shell command and we execute it.
    cmd = llm(f"What shell command resolves: {user_message}")
    subprocess.run(cmd, shell=True)


def fetch_reference(user_message: str) -> str:
    # The model returns a URL and we fetch whatever it points at.
    url = llm(f"Return a documentation URL for: {user_message}")
    return requests.get(url, timeout=10).text


def save_note(user_message: str) -> None:
    # The model picks the destination path; we write there unconditionally.
    path = llm(f"Where should this note be stored? {user_message}")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(user_message)


def load_session(blob: bytes):
    # Restore a session from a serialized blob.
    return pickle.loads(blob)
