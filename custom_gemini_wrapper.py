from langchain.llms.base import LLM
from typing import Optional, List
import google.generativeai as gpt

class GeminiLLM(LLM):
    def __init__(self, api_key: str, model_name: str):
        # Set the api_key and model_name as attributes of the instance
        self._api_key = api_key
        self._model_name = model_name

        # Configure the Gemini API with the provided API key
        gpt.configure(api_key=self._api_key)

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        # Call the Gemini model and generate content
        response = gpt.generate_text(model=self._model_name, prompt=prompt)

        # Return the generated text from the response
        return response.candidates[0]['output']

    @property
    def _llm_type(self) -> str:
        return "google_gemini"
