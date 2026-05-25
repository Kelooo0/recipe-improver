from google import genai
from google.genai import types
from app.config import settings
import json


class AIService:
    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.API_KEY)
        self.model_id = "gemini-2.5-flash"

    def generate_recipes(self, ingredients) -> list:
        try:
            prompt = f"""
            Ingredients: {ingredients}

            TASK:
            Based on the provided ingredients, create exactly 3 different meal recipes.
            For each recipe provide a title (max length 100 characters), content, and preparation time.

            LANGUAGE:
            CRITICAL: You must detect the language of the provided ingredients and write the entire response (titles and contents) in that EXACT language.
            Examples:
            - If ingredients are in Polish -> response must be in Polish.
            - If ingredients are in English -> response must be in English.

            FORMAT:
            Return ONLY a JSON object. No preamble, no markdown code blocks.
            The root JSON structure MUST be a list containing exactly 3 recipe objects:
            [
                {{
                    "title": "string",
                    "content": "string",
                    "prep_time": 0
                }},
                {{
                    "title": "string",
                    "content": "string",
                    "prep_time": 0
                }},
                {{
                    "title": "string",
                    "content": "string",
                    "prep_time": 0
                }}
            ]
            """
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                ),
            )
            data = json.loads(response.text)
            return data
        except Exception as exc:
            print(f"AIService error, {exc}")
            return []


ai_service = AIService()
