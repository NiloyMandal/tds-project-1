# Test Payloads for TDS-PROJ-1

This directory contains JSON payload files to test your TDS-PROJ-1 application with various scenarios.

## 📁 Available Test Payloads

### 1. `payload-sales-summary.json`

**Task:** Sum of Sales Calculator

- Tests CSV file handling from attachments
- Validates fetch() usage
- Checks dynamic calculation and display
- **Attachment:** `sales.csv` with product sales data

### 2. `payload-calculator.json`

**Task:** Basic Calculator

- Tests interactive UI creation
- Validates multiple button elements
- Checks for display element and math operations
- **Attachment:** None

### 3. `payload-todo-list.json`

**Task:** To-Do List Application

- Tests form input handling
- Validates Bootstrap integration
- Checks dynamic list manipulation
- **Attachment:** None

### 4. `payload-weather-dashboard.json`

**Task:** Weather Dashboard

- Tests search functionality
- Validates display areas
- Checks Bootstrap styling
- **Attachment:** None

### 5. `payload-json-viewer.json`

**Task:** JSON Data Viewer

- Tests JSON file loading from attachments
- Validates tree view rendering
- Checks search/filter functionality
- **Attachment:** `data.json` with sample user data

### 6. `payload-github-user.json`

**Task:** GitHub User Lookup

- Tests external API integration (GitHub API)
- Validates form handling
- Checks date formatting
- **Attachment:** None

### 7. `payload-markdown-enhanced.json`

**Task:** Enhanced Markdown Editor (Round 2)

- Tests round 2 functionality
- Validates tab switching UI
- Checks word count feature
- **Attachment:** `input.md` with sample markdown

## 🚀 How to Use

### Option 1: Run All Tests (Automated)

```bash
# Make sure your server is running first:
# Terminal 1:
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2:
./run_tests.sh
```

### Option 2: Test Individual Payloads

```bash
# Test a specific payload
curl -X POST http://127.0.0.1:8000/build \
  -H "Content-Type: application/json" \
  -d @test_payloads/payload-sales-summary.json

# With pretty output
curl -X POST http://127.0.0.1:8000/build \
  -H "Content-Type: application/json" \
  -d @test_payloads/payload-calculator.json | jq '.'
```

### Option 3: Test with Python

```bash
# Using the test_live_api.py script
python test_live_api.py

# Or use Python requests directly
python3 -c "
import requests
import json

with open('test_payloads/payload-todo-list.json') as f:
    payload = json.load(f)

response = requests.post(
    'http://127.0.0.1:8000/build',
    json=payload
)

print(f'Status: {response.status_code}')
print(f'Response: {response.json()}')
"
```

## 📊 Understanding Test Results

### ✅ Success Response (HTTP 200)

```json
{
  "message": "Request received. Buildling Application..."
}
```

### ❌ Unauthorized (HTTP 401)

```json
{
  "message": "Unauthorized: Invalid secret key."
}
```

**Fix:** Check that your `.env` file has `API_SECRET=11032003`

### ⚠️ Validation Error (HTTP 422)

```json
{
  "detail": [...]
}
```

**Fix:** Check the payload structure matches the Pydantic model

## 🔍 What Happens After Testing

For each successful test request:

1. ✅ **Request Accepted** - Returns HTTP 200
2. 🤖 **LLM Processing** - Generates app based on brief
3. 📦 **GitHub Repo Created** - Creates repository with task name
4. 📝 **Code Pushed** - Pushes README.md, LICENSE, index.html
5. 🌐 **Pages Enabled** - Activates GitHub Pages
6. 📤 **Evaluation Sent** - Posts results to evaluation_url

## 📁 Created Repositories

After running tests, check your GitHub account for repositories named:

- `sum-of-sales-test-001`
- `calculator-app-test-002`
- `todo-list-test-003`
- `weather-dashboard-test-004`
- `json-viewer-test-005`
- `github-user-lookup-test-006`
- `markdown-editor-test-007`

Each will be live at: `https://your-username.github.io/repo-name/`

## 🛠️ Creating Your Own Test Payloads

Template structure:

```json
{
  "email": "your-email@example.com",
  "secret": "11032003",
  "task": "unique-task-id",
  "round": 1,
  "nonce": "unique-nonce",
  "brief": "Description of what app should do...",
  "checks": ["JavaScript validation check 1", "JavaScript validation check 2"],
  "evaluation_url": "http://127.0.0.1:8000/_eval",
  "attachments": [
    {
      "name": "filename.ext",
      "url": "data:mime/type;base64,BASE64_ENCODED_CONTENT"
    }
  ]
}
```

### Encoding Attachments

```bash
# Encode a file to base64
base64 -w 0 myfile.csv

# Or with data URI prefix
echo "data:text/csv;base64,$(base64 -w 0 myfile.csv)"
```

## 💡 Tips

1. **Test Locally First** - Always test on `localhost:8000` before deploying
2. **Check Server Logs** - Monitor the uvicorn terminal for detailed processing info
3. **One at a Time** - Run tests one by one to avoid GitHub API rate limits
4. **Clean Up** - Delete test repositories from GitHub after testing
5. **Secret Match** - Ensure `.env` has `API_SECRET=11032003`

## 🐛 Troubleshooting

**Server not responding?**

```bash
# Check if server is running
curl http://127.0.0.1:8000/

# Restart server
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

**401 Unauthorized?**

```bash
# Check environment variable
cat .env | grep API_SECRET

# Should show: API_SECRET=11032003
```

**JSON parsing errors?**

- Check recent fixes to `llm.py` are applied
- Verify prompts in `app/services/prompts/` are updated
- Fall back to mock service if aipipe fails

## 📚 Related Files

- `/test_live_api.py` - Tests live Hugging Face deployment
- `/test_functionality.py` - Runs comprehensive functionality tests
- `/run_tests.sh` - Automated test runner for all payloads
- `/payload.markdown-to-html.json` - Original example payload

Happy Testing! 🚀
