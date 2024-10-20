from langchain.llms.base import LLM
from typing import Optional, List
import google.generativeai as gpt

class GeminiLLM(LLM):
    def __init__(self, api_key: str, model_name: str):
        # Store the API key and model name
        self.api_key = api_key
        self.model_name = model_name

        # Configure the Gemini AI model
        gpt.configure(api_key=self.api_key)

    # Required method for LangChain LLM interface
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        # Call the Gemini model and generate content
        response = gpt.generate_text(model=self.model_name, prompt=prompt)

        # Return the generated text from the response
        return response.candidates[0]['output']  # Return the first candidate's text

    # Define the type of the LLM (text generation in this case)
    @property
    def _llm_type(self) -> str:
        return "google_gemini"
