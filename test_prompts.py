#!/usr/bin/env python3
"""
Quick test to check if the prompts are loaded correctly
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, '/home/niloy/tds-proj-1-main')

os.environ['API_SECRET'] = 'test'
os.environ['GITHUB_TOKEN'] = 'test'
os.environ['AI_PIPE_API_KEY'] = 'test'

from pathlib import Path

def load_prompt(template: str) -> str:
    """Load a prompt from template file"""
    template_path = Path('/home/niloy/tds-proj-1-main/app/services/prompts') / template
    with open(template_path, "r", encoding="utf-8") as tf:
        return tf.read()

# Test loading prompts
print("📋 Testing Prompt Templates")
print("=" * 60)

instructions = load_prompt("instructions.txt")
user_input = load_prompt("input.txt")

print("\n✅ INSTRUCTIONS TEMPLATE:")
print("-" * 60)
print(instructions[:500])
print("...")
print("-" * 60)

print("\n✅ USER INPUT TEMPLATE:")
print("-" * 60)
print(user_input[:500])
print("...")
print("-" * 60)

# Test with sample data
checks = "- document.title === 'Test'\n- document.querySelector('#test')"
brief = "Create a simple test page"

final_instructions = instructions.replace("{checks}", checks)
final_input = user_input.replace("{brief}", brief)

print("\n✅ FINAL SYSTEM PROMPT:")
print("-" * 60)
print(final_instructions[:400])
print("...")
print("-" * 60)

print("\n✅ FINAL USER PROMPT:")
print("-" * 60)
print(final_input[:400])
print("...")
print("-" * 60)

print("\n✅ Prompts loaded successfully!")
print("\n🔍 Key points to verify:")
print("   ✓ Instructions mention exact JSON schema")
print("   ✓ Required fields: README.md, LICENSE, index.html")
print("   ✓ No extra fields allowed")
print("   ✓ Clear formatting rules")
