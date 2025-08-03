import os
import requests
from typing import List, Dict, Any

class LLMBackend:
    """
    Connects to Gemini or OpenAI for LLM responses.
    """
    def __init__(self, provider: str = "gemini", api_key: str = None):
        self.provider = provider
        self.api_key = api_key or os.getenv("LLM_API_KEY")

    def query(self, prompt: str) -> str:
        if self.provider == "gemini":
            return self._query_gemini(prompt)
        elif self.provider == "openai":
            return self._query_openai(prompt)
        else:
            raise ValueError("Unsupported provider")

    def _query_gemini(self, prompt: str) -> str:
        # Example Gemini API call (replace with real endpoint)
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        resp = requests.post(url, headers=headers, params=params, json=data)
        if resp.ok:
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        return "Error: Unable to get response from Gemini."

    def _query_openai(self, prompt: str) -> str:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512
        }
        resp = requests.post(url, headers=headers, json=data)
        if resp.ok:
            return resp.json()["choices"][0]["message"]["content"]
        return "Error: Unable to get response from OpenAI."
