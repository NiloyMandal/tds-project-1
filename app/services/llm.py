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
        
        instructions = load_prompt("instructions.txt").replace("VALIDATION_CHECKS_PLACEHOLDER", checks)
        user_input = load_prompt("input.txt").replace("BUILD_BRIEF_PLACEHOLDER", brief)
        
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
            try:
                response_data = response.json()
            except json.JSONDecodeError as jde:
                print(f"Failed to parse aipipe response as JSON: {jde}")
                print(f"Raw response text: {response.text[:1000]}")
                raise jde
            
            # Handle different possible response structures
            content = None
            if "choices" in response_data and len(response_data["choices"]) > 0:
                if "message" in response_data["choices"][0]:
                    content = response_data["choices"][0]["message"]["content"]
                elif "text" in response_data["choices"][0]:
                    content = response_data["choices"][0]["text"]
            elif "content" in response_data:
                content = response_data["content"]
            elif "text" in response_data:
                content = response_data["text"]
            
            if content is None:
                raise KeyError("No content found in aipipe response")
            
            # Clean and validate JSON content
            try:
                # Try to extract JSON from the response (in case there's extra text)
                content = content.strip()
                
                # Remove common LLM artifacts
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                
                content = content.strip()
                
                # Extract JSON object
                if not content.startswith('{'):
                    # Find the first { and last }
                    start_idx = content.find('{')
                    end_idx = content.rfind('}')
                    if start_idx != -1 and end_idx != -1:
                        content = content[start_idx:end_idx + 1]
                
                # Attempt to fix common JSON issues
                import re
                
                # Fix escaped property names (common LLM error)
                content = re.sub(r'\\("[\w.-]+"):', r'\1:', content)
                
                # Fix double-escaped newlines (\\\\n -> \\n)
                content = re.sub(r'\\\\\\\\n', r'\\\\n', content)
                
                # Fix other double escaping issues
                content = re.sub(r'\\\\\\\\', r'\\\\', content)
                
                # Remove trailing commas before } or ]
                content = re.sub(r',(\s*[}\]])', r'\1', content)
                
                # Fix invalid escape sequences like \a, \b, etc (except valid ones like \n, \t, \r, \\, \")
                content = re.sub(r'\\([^ntr"\\\/])', r'\\\\\\1', content)
                
                print(f"Cleaned JSON content: {content[:200]}...")
                
                # First validate it's proper JSON
                parsed_json = json.loads(content)
                
                # Fix literal \n characters in the actual content after JSON parsing
                for key, value in parsed_json.items():
                    if isinstance(value, str):
                        # Convert literal \n to actual newlines in the content
                        parsed_json[key] = value.replace('\\n', '\n').replace('\\t', '\t')
                
                # Then validate with pydantic model
                return LLMResponse.model_validate(parsed_json)
                
            except json.JSONDecodeError as je:
                print(f"JSON decode error: {str(je)}")
                print(f"Raw content causing error: {repr(content[:200])}")
                raise je
            except Exception as ve:
                print(f"Validation error: {str(ve)}")
                raise ve
        else:
            print(f"aipipe API failed with status {response.status_code}: {response.text}")
            print("Falling back to mock LLM service...")
            return generate_app_mock(brief, checks)
            
    except Exception as e:
        print(f"aipipe API failed: {str(e)}")
        print("Falling back to mock LLM service...")
        return generate_app_mock(brief, checks)
