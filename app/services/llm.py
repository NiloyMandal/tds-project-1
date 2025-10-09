"""Service to interact with LLMs via aipipe"""

from pathlib import Path
import requests
import json

from app.models import LLMResponse
from app.config import Environ
from app.services.llm_mock import generate_app_mock


def load_prompt(template: str) -> str:
    """Load a prompt from template file"""
    template_path = Path(__file__).parent / "prompts" / template
    with open(template_path, "r", encoding="utf-8") as tf:
        return tf.read()


def generate_app(brief: str, checks: str) -> LLMResponse:
    """Generate an app based on brief using aipipe API"""
    
    # Get the aipipe API key
    api_key = Environ.AIPIPE_API_KEY
    if not api_key:
        print("No aipipe API key found. Using mock LLM service...")
        return generate_app_mock(brief, checks)
    
    try:
        # Query the aipipe API
        print("Querying aipipe LLM...")
        
        instructions = load_prompt("instructions.txt").format(checks=checks)
        user_input = load_prompt("input.txt").format(brief=brief)
        
        # Prepare the request payload for aipipe
        payload = {
            "model": "gpt-4.1-nano",
            "messages": [
                {"role": "system", "content": instructions},
                {"role": "user", "content": user_input}
            ]
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Make the API request to aipipe
        response = requests.post(
            "https://aipipe.org/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            response_data = response.json()
            content = response_data["choices"][0]["message"]["content"]
            
            # Parse the response content as JSON and validate with pydantic model
            return LLMResponse.model_validate_json(content)
        else:
            print(f"aipipe API failed with status {response.status_code}: {response.text}")
            print("Falling back to mock LLM service...")
            return generate_app_mock(brief, checks)
            
    except Exception as e:
        print(f"aipipe API failed: {str(e)[:100]}...")
        print("Falling back to mock LLM service...")
        return generate_app_mock(brief, checks)
