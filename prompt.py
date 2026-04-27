import os
import time
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from parser import parser
from langfuse import get_client

load_dotenv()
langfuse = get_client()

FALLBACK_PROMPT = """You are an expert meeting notes analyzer. Your job is to extract clear, structured action items from unstructured meeting notes.

Rules:
- Extract ONLY tasks that are explicitly mentioned
- Do NOT guess or fabricate missing information
- If owner is not mentioned, use "not_available"
- If deadline is not mentioned, use "not_available"
- Assign priority: urgent/asap/critical = High, soon/this week = Medium, default = Medium, eventually/later = Low
- Return ONLY valid JSON, no extra text

Meeting Notes: {meeting_notes}

{format_instructions}"""


def get_prompt():
    try:
        lf_prompt = langfuse.get_prompt("meeting_notes_extractor")
        template = lf_prompt.prompt
        print("Loaded prompt from Langfuse")
    except Exception as e:
        template = FALLBACK_PROMPT
        print(f"Using fallback prompt: {e}")

    return PromptTemplate(
        template=template,
        input_variables=["meeting_notes"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        }
    )


def get_llm():
    api_key = None
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        pass
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing!")
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=api_key,
        temperature=0
    )


def generate_with_retry(chain, meeting_notes, retries=3, wait=5):
    for attempt in range(retries):
        try:
            return chain.invoke({"meeting_notes": meeting_notes})
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                if attempt < retries - 1:
                    time.sleep(wait)
                else:
                    raise Exception(
                        "Gemini overloaded. Please wait and try again."
                    )
            else:
                raise