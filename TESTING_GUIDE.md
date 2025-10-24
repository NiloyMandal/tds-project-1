# 🧪 Quick Test Guide

## ✅ Created 7 Test Payloads for Your TDS-PROJ-1 Application

### 📋 Test Scenarios

| #   | Test File                        | Task                 | Features Tested                    | Has Attachments |
| --- | -------------------------------- | -------------------- | ---------------------------------- | --------------- |
| 1   | `payload-sales-summary.json`     | Sales Calculator     | CSV loading, fetch(), calculations | ✅ sales.csv    |
| 2   | `payload-calculator.json`        | Calculator App       | UI buttons, interactive operations | ❌              |
| 3   | `payload-todo-list.json`         | To-Do List           | Forms, Bootstrap, dynamic lists    | ❌              |
| 4   | `payload-weather-dashboard.json` | Weather Dashboard    | Search, display, Bootstrap         | ❌              |
| 5   | `payload-json-viewer.json`       | JSON Viewer          | JSON loading, tree view, search    | ✅ data.json    |
| 6   | `payload-github-user.json`       | GitHub Lookup        | External API, form, date format    | ❌              |
| 7   | `payload-markdown-enhanced.json` | Markdown Editor (R2) | Tabs, word count, round 2          | ✅ input.md     |

---

## 🚀 Quick Start

### 1️⃣ Start Your Server

```bash
cd /home/niloy/tds-proj-1-main
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2️⃣ Run All Tests (New Terminal)

```bash
cd /home/niloy/tds-proj-1-main
./run_tests.sh
```

### 3️⃣ Or Test One Payload

```bash
curl -X POST http://127.0.0.1:8000/build \
  -H "Content-Type: application/json" \
  -d @test_payloads/payload-calculator.json
```

---

## 📊 Expected Output

### ✅ Success

```
Status: 200
{
  "message": "Request received. Buildling Application..."
}
```

Then check your server logs for:

- ✅ Querying aipipe LLM...
- ✅ Creating repository: {task-name}
- ✅ Repository created at {url}
- ✅ Pushing files to repository...
- ✅ Github pages enabled
- ✅ Posted to evaluation URL

---

## 🔍 What Gets Created

Each test creates:

1. **GitHub Repository** - Named after the `task` field
2. **README.md** - Professional documentation
3. **LICENSE** - MIT License
4. **index.html** - Complete working app
5. **Attachments** - Any files from the payload
6. **GitHub Pages** - Live at `https://username.github.io/task-name/`

---

## 💡 Pro Tips

✅ **Before Testing:**

- Ensure `.env` has `API_SECRET=11032003`
- Check `GITHUB_TOKEN` is valid
- Verify `AI_PIPE_API_KEY` is set

✅ **While Testing:**

- Watch server terminal for real-time logs
- Wait ~30-60 seconds per request
- GitHub Pages takes 1-2 minutes to go live

✅ **After Testing:**

- Check GitHub for new repositories
- Visit GitHub Pages URLs to see live apps
- Review README.md in each repo
- Clean up test repos if needed

---

## 🎯 All Commands

```bash
# Test all payloads
./run_tests.sh

# Test specific payload
curl -X POST http://127.0.0.1:8000/build \
  -H "Content-Type: application/json" \
  -d @test_payloads/payload-NAME.json

# List all test files
ls -l test_payloads/*.json

# View a payload
cat test_payloads/payload-calculator.json | jq '.'

# Check server health
curl http://127.0.0.1:8000/

# View API docs
open http://127.0.0.1:8000/docs
```

---

Happy Testing! 🚀
