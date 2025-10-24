"""Service to interact with LLMs via aipipe (no mock fallback)"""

from pathlib import Path
import requests
import json
import re

from app.models import LLMResponse
from app.config import Environ


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
        raise RuntimeError("AIPIPE_API_KEY is not set. Cannot generate app without a valid API key.")
    
    try:
        # Query the aipipe API
        print("Querying aipipe LLM...")
        
        instructions = load_prompt("instructions.txt").replace("{checks}", checks)
        user_input = load_prompt("input.txt").replace("{brief}", brief)
        
        # Helper to call API once with given messages and parse/normalize to LLMResponse
        def call_once(messages: list[dict]) -> LLMResponse:
            payload = {
                "model": "gpt-4.1-nano",
                "messages": messages,
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
                    if content.startswith('```'):
                        content = content[3:]
                    if content.endswith('```'):
                        content = content[:-3]
                    
                    content = content.strip()
                    
                    # Extract JSON object - find matching braces
                    if not content.startswith('{'):
                        start_idx = content.find('{')
                        if start_idx == -1:
                            raise ValueError("No JSON object found in response")
                        content = content[start_idx:]
                    
                    # Find the matching closing brace for the first opening brace
                    brace_count = 0
                    end_idx = -1
                    for i, char in enumerate(content):
                        if char == '{':
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                end_idx = i
                                break
                    
                    if end_idx != -1:
                        content = content[:end_idx + 1]
                    
                    # Attempt to fix common JSON issues
                    # Fix escaped property names (common LLM error)
                    content = re.sub(r'\\("[\w.-]+"):', r'\1:', content)
                    
                    # Fix double-escaped newlines (\\\\n -> \\n)
                    content = re.sub(r'\\\\\\\\n', r'\\\\n', content)
                    
                    # Fix other double escaping issues
                    content = re.sub(r'\\\\\\\\', r'\\\\', content)
                    
                    # Remove trailing commas before } or ]
                    content = re.sub(r',(\s*[}\]])', r'\1', content)
                    
                    # Fix invalid escape sequences like \a, \b, etc (except valid ones like \n, \t, \r, \\, \")
                    content = re.sub(r'\\([^ntr"\\\/bfuU])', r'\\\\\\1', content)
                    
                    print(f"Cleaned JSON content: {content[:200]}...")
                    
                    # First validate it's proper JSON
                    parsed_json = json.loads(content)
                    
                    # Normalize keys from common alternatives to required ones
                    def pick(d: dict, keys: list[str]) -> str | None:
                        for k in keys:
                            for existing in list(d.keys()):
                                if existing.lower() == k.lower():
                                    return d.pop(existing)
                        return None
                    
                    normalized: dict[str, str] = {}
                    tmp = dict(parsed_json)
                    readme = pick(tmp, ["README.md", "readme.md", "readme"]) or "# App\n\nGenerated by LLM."
                    license_txt = pick(tmp, ["LICENSE", "license"]) or "MIT License"
                    index_html = pick(tmp, ["index.html", "index", "index_html", "html"]) or "<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>App</title></head><body><h1>App</h1></body></html>"
                    normalized["README.md"] = readme
                    normalized["LICENSE"] = license_txt
                    normalized["index.html"] = index_html
                    
                    # Fix literal \n characters in the actual content after JSON parsing
                    for key, value in normalized.items():
                        if isinstance(value, str):
                            # Convert literal \n to actual newlines in the content
                            normalized[key] = value.replace('\\n', '\n').replace('\\t', '\t')
                    
                    # Then validate with pydantic model
                    return LLMResponse.model_validate(normalized)
                    
                except json.JSONDecodeError as je:
                    print(f"JSON decode error: {str(je)}")
                    print(f"Raw content causing error: {repr(content[:200])}")
                    raise je
                except Exception as ve:
                    print(f"Validation error: {str(ve)}")
                    raise ve
            else:
                # Include a short prefix of the response text for debugging
                snippet = response.text[:200].replace("\n", " ")
                raise RuntimeError(f"aipipe API failed with status {response.status_code}: {snippet}")

        def static_brief_checks(html: str, checks_text: str, brief_text: str) -> list[str]:
            """Heuristic static checks derived from checks/brief to catch obvious mismatches."""
            issues: list[str] = []
            # Title check: look for document.title expected string
            m = re.search(r"document\.title\s*===\s*[`\"]([^`\"]+)[`\"]", checks_text)
            if m:
                expected = m.group(1)
                if expected not in html:
                    issues.append(f"Missing expected title text: {expected}")
            # Bootstrap check
            if "bootstrap" in checks_text.lower() or "bootstrap" in brief_text.lower():
                if "bootstrap" not in html.lower():
                    issues.append("Bootstrap reference not found in HTML")
            # total-sales id check
            if "#total-sales" in checks_text or "#total-sales" in brief_text:
                if "id=\"total-sales\"" not in html and "#total-sales" not in html:
                    issues.append("#total-sales element not found")
            # fetch usage hint
            if "fetch(" in checks_text or "fetch(" in brief_text:
                if "fetch(" not in html:
                    issues.append("fetch( not found in script")
            return issues

        # First attempt
        base_messages = [
            {"role": "system", "content": instructions},
            {"role": "user", "content": user_input},
        ]
        result = call_once(base_messages)
        issues = static_brief_checks(result.html_code, checks, brief)
        if not issues:
            return result

        # Retry once with corrective instruction
        correction = (
            "Your previous JSON did not satisfy these checks: \n- "
            + "\n- ".join(issues)
            + "\nRegenerate strictly following the brief and checks. Return ONLY JSON with keys README.md, LICENSE, index.html."
        )
        retry_messages = base_messages + [{"role": "user", "content": correction}]
        result_retry = call_once(retry_messages)
        # Accept the second attempt as final
        return result_retry
            
    except Exception as e:
        # Surface the error to the caller. Background task will log this.
        raise
