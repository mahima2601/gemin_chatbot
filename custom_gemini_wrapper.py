from langchain.llms.base import LLM
from typing import Optional, List

class GeminiLLM(LLM):
    def __init__(self, model):
        self.model = model

    # Required method for LangChain LLM interface
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        response = self.model.generate_content(prompt)
        return response.parts[0].text

    # Define the type of the LLM (here it's text-based)
    @property
    def _llm_type(self) -> str:
        return "google_gemini"
