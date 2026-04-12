from google import genai
import os
from dotenv import load_dotenv
from prompt import PROMPT_TEMPLATE

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API key not found. Check your .env file.")

client = genai.Client(api_key=api_key)


def get_llm_response(user_input):
    try:
        prompt = PROMPT_TEMPLATE.format(input_text=user_input)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "temperature": 0.0
            }
        )

        return response.text

    except Exception as e:
        return f"ERROR: {str(e)}"