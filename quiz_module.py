
import json
import re
import os
from google import genai
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Set up Gemini client
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def clean_json_block(text):
    # Remove Markdown code fences
    return re.sub(r"```(?:json)?\s*|\s*```", "", text).strip()


def generate_quiz(text: str) -> list:
    try:
        prompt = f"""
You are a quiz generator.

From the following passage, create 3 multiple-choice questions.
Each question should include:
- A "question"
- A list of 4 "options"
- A correct "answer" that exactly matches one of the options.

Return only valid JSON in this format:
[
    {{
        "question": "What is ...?",
        "options": ["A", "B", "C", "D"],
        "answer": "A"
    }}
]

Passage:
{text}
"""

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        quiz_text = response.text or ""
        cleaned_text = clean_json_block(quiz_text)

        # Parse and return JSON list
        quiz = json.loads(cleaned_text)

        if not isinstance(quiz, list):
            raise ValueError("Quiz response is not a JSON list.")

        return quiz

    except Exception as e:
        print(f"Quiz error: {e}")
        return [{"error": f"⚠️ Error in Quiz: {e}"}]