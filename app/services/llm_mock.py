"""Mock LLM service for testing without valid OpenAI API key"""

from app.models import LLMResponse


def generate_app_mock(brief: str, checks: str) -> LLMResponse:
    """Generate a mock app response for testing purposes"""
    print("Using MOCK LLM service - generating sample response...")
    
    # Create a sample HTML app that converts markdown to HTML
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown to HTML Converter</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/default.min.css">
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        #markdown-output { border: 1px solid #ddd; padding: 20px; margin-top: 20px; }
        textarea { width: 100%; height: 200px; margin-bottom: 10px; }
    </style>
</head>
<body>
    <h1>Markdown to HTML Converter</h1>
    <textarea id="markdown-input" placeholder="Enter your markdown here..."></textarea>
    <button onclick="convertMarkdown()">Convert to HTML</button>
    <div id="markdown-output"></div>
    
    <script>
        function convertMarkdown() {
            const input = document.getElementById('markdown-input').value;
            const output = document.getElementById('markdown-output');
            output.innerHTML = marked.parse(input);
            hljs.highlightAll();
        }
        
        // Auto-convert sample content
        document.addEventListener('DOMContentLoaded', function() {
            const sampleMarkdown = `# Markdown to HTML-

This is a sample markdown document.

### Code

\`\`\`js
console.log('Hello code');
\`\`\``;
            document.getElementById('markdown-input').value = sampleMarkdown;
            convertMarkdown();
        });
    </script>
</body>
</html>"""

    readme_content = """# Markdown to HTML Converter

This is a simple web application that converts Markdown text to HTML using the marked.js library.

## Features
- Real-time markdown to HTML conversion
- Syntax highlighting for code blocks
- Clean, responsive design

## Libraries Used
- marked.js - Markdown parser
- highlight.js - Syntax highlighting

## Usage
1. Enter your markdown text in the textarea
2. Click "Convert to HTML" button
3. View the rendered HTML output below
"""

    license_content = """MIT License

Copyright (c) 2025 TDS Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

    # Use the alias names as defined in the model
    return LLMResponse(**{
        "README.md": readme_content,
        "LICENSE": license_content,
        "index.html": html_content,
        "script.js": None,
        "main.py": None
    })