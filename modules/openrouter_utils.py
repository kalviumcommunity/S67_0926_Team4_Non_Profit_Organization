"""
FOLIO Platform - OpenRouter AI LLM Integration.
Provides support for OpenRouter API keys, selectable AI personas, customizable output formats,
and multimodal RAG query reasoning (text, PDF context, images, video frames).
"""

import os
import json
import base64
import requests
from typing import List, Dict, Any, Union, Optional
from PIL import Image

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import streamlit as st
from modules.utils import encode_image_to_base64

# Defining the persona and format instructions
PERSONA_PROMPTS = {
    "Default": "You are a helpful and intelligent grant intelligence assistant with deep knowledge of institutional compliance and donor agreements.",
    "Expert Analyst": "You are a world-class professional analyst. Your response should be formal, data-driven, and structured. Use bullet points and bold text to highlight key findings.",
    "Creative Brainstormer": "You are a creative partner. Your response should be imaginative and focus on generating new ideas, possibilities, or different angles based on the document's content.",
    "ELI5 (Explain Like I'm 5)": "You are a friendly teacher explaining things to a five-year-old. Your response must be extremely simple, use easy words, and short sentences. Use analogies if possible."
}

FORMAT_PROMPTS = {
    "Default": "Please format your response clearly.",
    "Bullet Points": "Please provide your entire answer as a well-structured bulleted list.",
    "JSON": "Please provide your entire answer as a single, valid JSON object. Do not include any text or formatting outside of the JSON structure.",
    "Short Paragraph": "Please provide your answer as a single, concise paragraph.",
    "Markdown Table": "Please format key findings as a structured Markdown table where applicable."
}

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_OPENROUTER_MODEL = "google/gemini-2.5-flash"

POPULAR_MODELS = [
    "google/gemini-2.5-flash",
    "google/gemini-1.5-flash",
    "google/gemini-1.5-pro",
    "openai/gpt-4o-mini",
    "openai/gpt-4o",
    "anthropic/claude-3.5-sonnet",
    "meta-llama/llama-3.3-70b-instruct",
    "deepseek/deepseek-chat"
]


def resolve_openrouter_api_key(custom_key: Optional[str] = None) -> Optional[str]:
    """Resolves the OpenRouter API key from parameters, st.session_state, st.secrets, or environment variables."""
    if custom_key and custom_key.strip():
        return custom_key.strip()
        
    if "openrouter_api_key" in st.session_state and st.session_state.openrouter_api_key:
        return st.session_state.openrouter_api_key.strip()

    try:
        if "OPENROUTER_API_KEY" in st.secrets:
            return st.secrets["OPENROUTER_API_KEY"].strip()
    except Exception:
        pass

    env_key = os.getenv("OPENROUTER_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()
        
    return None


def get_openrouter_response(
    base_prompt: Union[List[Any], str],
    persona: str = "Default",
    output_format: str = "Default",
    model: str = DEFAULT_OPENROUTER_MODEL,
    api_key: Optional[str] = None,
    temperature: float = 0.2
) -> str:
    """
    Sends a chat completion request to the OpenRouter API with persona and format instructions.
    Supports multimodal parts (text, PIL images, base64 strings).
    
    Args:
        base_prompt: Prompt string or list of text/image parts.
        persona: The selected persona key from PERSONA_PROMPTS.
        output_format: The selected output format key from FORMAT_PROMPTS.
        model: OpenRouter model identifier.
        api_key: Optional explicit API key.
        temperature: Model temperature (default: 0.2 for precise RAG).
        
    Returns:
        str: The generated text response from the model.
    """
    resolved_key = resolve_openrouter_api_key(api_key)
    if not resolved_key:
        return (
            "⚠️ **OpenRouter API Key Required**\n\n"
            "Please provide your OpenRouter API key in `.env`, `secrets.toml`, or via the settings panel.\n"
            "Get your key at [openrouter.ai](https://openrouter.ai/keys)."
        )

    persona_instruction = PERSONA_PROMPTS.get(persona, PERSONA_PROMPTS["Default"])
    format_instruction = FORMAT_PROMPTS.get(output_format, FORMAT_PROMPTS["Default"])

    system_message = (
        f"**System Persona & Guidelines**\n"
        f"Persona: {persona_instruction}\n"
        f"Output Format Instruction: {format_instruction}\n\n"
        f"Instructions: Ground your response strictly on the provided context. "
        f"If the context contains relevant numbers, deadlines, or clauses, cite them accurately. "
        f"Never hallucinate or extrapolate beyond the provided knowledge."
    )

    # Convert base_prompt into OpenRouter message content array
    user_content = []
    
    if isinstance(base_prompt, str):
        user_content.append({"type": "text", "text": base_prompt})
    elif isinstance(base_prompt, list):
        for item in base_prompt:
            if isinstance(item, str):
                if item.strip():
                    user_content.append({"type": "text", "text": item})
            elif isinstance(item, Image.Image):
                # PIL Image
                data_uri = encode_image_to_base64(item)
                user_content.append({
                    "type": "image_url",
                    "image_url": {"url": data_uri}
                })
            elif isinstance(item, dict) and "type" in item:
                user_content.append(item)
            elif isinstance(item, list):
                # Nested list (e.g. video frames)
                for sub_item in item:
                    if isinstance(sub_item, Image.Image):
                        data_uri = encode_image_to_base64(sub_item)
                        user_content.append({
                            "type": "image_url",
                            "image_url": {"url": data_uri}
                        })
            else:
                user_content.append({"type": "text", "text": str(item)})

    headers = {
        "Authorization": f"Bearer {resolved_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://folio-grants.internal",
        "X-Title": "FOLIO Grant Intelligence Platform"
    }

    payload = {
        "model": model or DEFAULT_OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_content}
        ],
        "temperature": temperature,
        "max_tokens": 2048
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            res_data = response.json()
            choices = res_data.get("choices", [])
            if choices and "message" in choices[0]:
                return choices[0]["message"].get("content", "")
            return "No response content generated by OpenRouter model."
        else:
            err_msg = response.text
            try:
                err_json = response.json()
                if "error" in err_json:
                    err_msg = err_json["error"].get("message", response.text)
            except Exception:
                pass
            return f"⚠️ OpenRouter API Error ({response.status_code}): {err_msg}"
            
    except requests.exceptions.Timeout:
        return "⚠️ OpenRouter API request timed out (60s). Please try again."
    except Exception as e:
        return f"⚠️ Error communicating with OpenRouter API: {e}"


def get_gemini_response(base_prompt, persona="Default", output_format="Default", model=DEFAULT_OPENROUTER_MODEL):
    """
    Backwards-compatible drop-in alias for get_gemini_response, routed via OpenRouter API.
    """
    return get_openrouter_response(base_prompt, persona, output_format, model=model)
