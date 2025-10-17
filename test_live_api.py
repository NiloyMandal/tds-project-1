#!/usr/bin/env python3
"""
Test script to verify the live API endpoint works correctly
"""

import requests
import json
import base64

# Your API details from the email
API_URL = "https://niloymondal-tds-project-1.hf.space/build"
SECRET = "11032003"
EMAIL = "22f1001861@ds.study.iitm.ac.in"

# Sample CSV data (sales.csv)
csv_data = """category,sales
1,123.45
2,234.56
3,345.67
5,456.78
8,567.89
11,678.90
12,789.01"""

# Encode as base64 data URI
csv_b64 = base64.b64encode(csv_data.encode()).decode()
csv_data_uri = f"data:text/csv;base64,{csv_b64}"

# Test payload similar to what TDS server sends
test_payload = {
    "email": EMAIL,
    "secret": SECRET,
    "task": "SumOfSales-test",
    "round": 1,
    "nonce": "test-nonce-12345",
    "brief": "Publish a single-page site whose title is `Sales Summary 601`. It should use fetch() to load sales.csv (provided in the attachments), dynamically sum the `sales` column where the `category` <= 11, and displays the total inside an id=\"total-sales\" element, rounded to 2 decimals.",
    "checks": [
        "document.title === \"Sales Summary 601\"",
        "Math.abs(+document.querySelector('#total-sales').textContent - 734802.8099999999) < 0.01"
    ],
    "evaluation_url": "https://tds-llm-code-deploy.sanand.workers.dev/evaluate",
    "attachments": [
        {
            "name": "sales.csv",
            "url": csv_data_uri
        }
    ]
}

print("🧪 Testing TDS-PROJ-1 Live API")
print("=" * 60)
print(f"📍 API URL: {API_URL}")
print(f"🔑 Secret: {SECRET}")
print(f"📧 Email: {EMAIL}")
print("=" * 60)

try:
    print("\n📤 Sending POST request...")
    response = requests.post(
        API_URL,
        json=test_payload,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    
    print(f"\n📊 Response Status Code: {response.status_code}")
    print(f"📄 Response Headers: {dict(response.headers)}")
    print(f"📝 Response Body:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 200:
        print("\n✅ SUCCESS! Your API is working correctly!")
        print("✅ The request was accepted and will be processed in the background.")
        print("\n💡 You can now safely resubmit the Google Form with this URL:")
        print(f"   {API_URL}")
    elif response.status_code == 401:
        print("\n❌ UNAUTHORIZED! Check your secret key.")
        print(f"   Expected: {SECRET}")
        print("   Make sure API_SECRET environment variable matches.")
    elif response.status_code == 405:
        print("\n❌ METHOD NOT ALLOWED!")
        print("   This is the error from the trial test.")
        print("   Double-check the URL ends with /build")
    else:
        print(f"\n⚠️  Unexpected status code: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ CONNECTION ERROR!")
    print("   Could not connect to the API.")
    print("   Check if your Hugging Face Space is running.")
    
except requests.exceptions.Timeout:
    print("\n❌ TIMEOUT!")
    print("   The API took too long to respond.")
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"   {str(e)}")

print("\n" + "=" * 60)
print("🔍 Troubleshooting Tips:")
print("   1. Verify your Hugging Face Space is running")
print("   2. Check that API_SECRET environment variable is set to:", SECRET)
print("   3. Ensure the URL includes /build at the end")
print("   4. Test the API docs at: https://niloymondal-tds-project-1.hf.space/docs")
print("=" * 60)
