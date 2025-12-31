from app.core.config import settings
from shared.config.logging import get_logger

logger = get_logger(__name__)

# -----------------------------
# Constants
# -----------------------------

GEMINI_MODEL = "gemini-2.5-flash-lite"
OPENAI_MODEL = "gpt-4o-mini"

# -----------------------------
# Provider Clients (lazy init)
# -----------------------------

_gemini_client = None
_openai_client = None


def _get_gemini_client():
    global _gemini_client

    if _gemini_client is not None:
        return _gemini_client

    if not settings.LLM_CONFIG.GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is required for Gemini LLM")

    from google import genai

    _gemini_client = genai.Client(api_key=settings.LLM_CONFIG.GEMINI_API_KEY)
    return _gemini_client


def _get_openai_client():
    global _openai_client

    if _openai_client is not None:
        return _openai_client

    if not settings.LLM_CONFIG.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI LLM")

    from openai import OpenAI

    _openai_client = OpenAI(api_key=settings.LLM_CONFIG.OPENAI_API_KEY)
    return _openai_client


# -----------------------------
# Public API
# -----------------------------


def call_llm(prompt: str) -> str:
    if settings.LLM_CONFIG.USE_MOCK_LLM:
        return _mock_llm(prompt)

    provider = settings.LLM_CONFIG.LLM_PROVIDER

    if provider == "gemini":
        return _call_gemini(prompt)

    if provider == "openai":
        return _call_openai(prompt)

    raise ValueError(f"Unsupported LLM provider: {provider}")


# -----------------------------
# Providers
# -----------------------------


def _call_gemini(prompt: str) -> str:
    from google.genai import types
    from google.api_core import exceptions as google_exceptions

    client = _get_gemini_client()
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=512,
            ),
        )
        return response.text.strip()
    except ValueError:
        logger.warning("Gemini response was blocked or did not contain text.")
        return ""
    except google_exceptions.GoogleAPIError as e:
        logger.error(f"Gemini API call failed: {e}")
        raise RuntimeError("LLM service failed to generate a response.") from e


def _call_openai(prompt: str) -> str:
    from openai import APIError as OpenAIAPIError

    client = _get_openai_client()
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=512,
        )
        if response.choices:
            return response.choices[0].message.content.strip()
        logger.warning("OpenAI response did not contain any choices.")
        return ""
    except OpenAIAPIError as e:
        logger.error(f"OpenAI API call failed: {e}")
        raise RuntimeError("LLM service failed to generate a response.") from e


# -----------------------------
# Mock
# -----------------------------


def _mock_llm(prompt: str) -> str:
    return "⚠️ MOCK LLM RESPONSE\n\n" "Prompt preview:\n\n" f"{prompt[:800]}..."
