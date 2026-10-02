
import os
import time
from google import genai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.5-flash"


def get_learning_recommendations(topic):
    if not topic or not topic.strip():
        raise ValueError("Please enter a topic for the learning roadmap.")

    prompt = f"""
You are EduGenie, an AI learning assistant.

Create a clear, structured and personalized learning
roadmap for the following topic:

Topic: {topic.strip()}

Make the roadmap suitable for a student.

Include the following sections:

1. Learning Goal
   - Explain what the student will achieve.

2. Prerequisites
   - List the basic knowledge required.

3. Step-by-Step Learning Path
   - Divide the topic into logical stages.
   - Explain what to learn at each stage.
   - Arrange topics from basic to advanced.

4. Practical Activities
   - Suggest exercises, examples or mini-projects.

5. Learning Resources
   - Suggest useful types of resources, such as
     documentation, tutorials and practice websites.
   - Do not invent specific links.

6. Estimated Timeline
   - Give a reasonable suggested duration for
     completing each stage.

7. Final Project
   - Suggest one project to apply the knowledge.

8. Tips for Success
   - Give practical study tips.

Use clear headings, numbered steps and simple
explanations. Make the roadmap useful for a
beginner, while adapting it to the requested level.
"""

    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )

            result = response.text

            if result and result.strip():
                return result.strip()

            raise ValueError("Gemini returned an empty response.")

        except Exception as e:
            error_message = str(e).lower()

            # Quota exhaustion usually won't be fixed by retrying.
            if "resource_exhausted" in error_message or (
                "429" in error_message and "quota" in error_message
            ):
                print(f"Learning Roadmap quota error: {e}")
                raise RuntimeError(
                    "Gemini API quota exceeded. Please try again "
                    "later or check your API usage limits."
                ) from e

            # Retry temporary server errors.
            is_temporary = any(
                term in error_message
                for term in ["503", "unavailable", "overloaded"]
            )

            if is_temporary and attempt < max_attempts - 1:
                wait_time = 2 ** (attempt + 1)
                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )
                time.sleep(wait_time)
                continue

            print(f"Learning Roadmap Error: {e}")
            raise RuntimeError(
                f"Unable to generate learning recommendations: {e}"
            ) from e