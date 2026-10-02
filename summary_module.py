
from google import genai
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Set up Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def summarize_text(text: str) -> str:
    try:
        prompt = f"Summarize the following text in simple language:\n\n{text}"

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text.strip() if response.text else "No summary generated."

    except Exception as e:
        return f"⚠️ Error in Summary: {e}"