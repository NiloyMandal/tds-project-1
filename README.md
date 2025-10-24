---
title: TDS Project Evaluator
emoji: ⚙️
colorFrom: gray
colorTo: blue
sdk: docker
app_port: 8000
sdk_version: "1.0"
app_file: main.py
pinned: false
---

# 🚀 TDS Project Evaluator - LLM App Builder

A powerful FastAPI application that generates and deploys web applications using Large Language Models (LLMs) via aipipe API. The service accepts natural language descriptions, creates complete applications, hosts them on GitHub, and automatically deploys to GitHub Pages.

## ✨ Features

- 🤖 **AI-Powered Code Generation** - Uses aipipe LLM API to generate complete applications
- 🔧 **Automatic GitHub Integration** - Creates repositories and enables GitHub Pages
- 📊 **Real-time Evaluation** - Built-in evaluation system with custom checks
- 🐳 **Docker Ready** - Containerized for easy deployment
- 📚 **Interactive API Documentation** - Built-in Swagger UI
- 🔒 **Secure** - API key authentication and request validation

## 🏃‍♂️ Quick Start

### Prerequisites

Before you begin, make sure you have:

- **Python 3.10+** installed on your system
- **Git** for version control
- A **GitHub account** and personal access token
- An **aipipe API key** (from https://aipipe.org/login)

### Option 1: Run Locally (Recommended for Development)

#### Step 1: Clone the Repository

```bash
git clone https://huggingface.co/spaces/NiloyMondal/TDS_Project_1
cd TDS_Project_1
```

#### Step 2: Set Up Python Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 3: Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env  # If example exists, or create manually
```

Add these variables to your `.env` file:

```env
API_SECRET=your_secret_key_here
GITHUB_TOKEN=your_github_personal_access_token
AI_PIPE_API_KEY=your_aipipe_api_key_here
PORT=8000
```

#### Step 4: Run the Application

```bash
# Using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using Python module
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Step 5: Access the Application

- **API Documentation**: http://localhost:8000/docs
- **Home Endpoint**: http://localhost:8000
- **Health Check**: http://localhost:8000 (should return welcome message)

### Option 2: Run with Docker

#### Step 1: Build the Docker Image

```bash
docker build -t tds-evaluator .
```

#### Step 2: Run the Container

```bash
# Run with environment file
docker run --env-file .env -p 8000:8000 tds-evaluator

# Or run with inline environment variables
docker run -e API_SECRET=your_secret \
           -e GITHUB_TOKEN=your_token \
           -e AI_PIPE_API_KEY=your_key \
           -p 8000:8000 tds-evaluator
```

### Option 3: Deploy on Hugging Face Spaces

This repository is already configured for Hugging Face Spaces. Simply:

1. Fork or import this repository to your Hugging Face account
2. Set your environment variables in the Space settings
3. The Space will automatically build and deploy

## 📁 Project Structure

```
TDS_Project_1/
├── 🚀 main.py                    # FastAPI application entry point
├── 📋 requirements.txt           # Python dependencies
├── 🐳 Dockerfile               # Container configuration
├── ⚙️ pyproject.toml            # Project configuration
├── 📝 README.md                # This documentation
├── 🔧 .env                     # Environment variables (create this)
└── 📦 app/                     # Main application package
    ├── __init__.py
    ├── 🔧 config.py            # Environment & configuration
    ├── 📊 models.py            # Pydantic data models
    ├── 🛣️ routes.py             # API route handlers
    ├── 🔧 helpers.py           # Utility functions
    └── 🏢 services/            # Business logic services
  ├── 🤖 llm.py           # aipipe LLM integration (no mock fallback)
        ├── 🐙 gh_actions.py    # GitHub integration
        └── 📝 prompts/         # LLM prompt templates
            ├── input.txt
            └── instructions.txt
```

## 🔧 Configuration Guide

### Required Environment Variables

Create a `.env` file in the root directory with these variables:

| Variable          | Description                       | Example                     | Required |
| ----------------- | --------------------------------- | --------------------------- | -------- |
| `API_SECRET`      | Secret key for API authentication | `"my-secret-key-123"`       | ✅ Yes   |
| `GITHUB_TOKEN`    | GitHub Personal Access Token      | `"ghp_xxxxxxxxxxxx"`        | ✅ Yes   |
| `AI_PIPE_API_KEY` | aipipe API key for LLM access     | `"eyJhbGciOiJIUzI1NiJ9..."` | ✅ Yes   |
| `PORT`            | Server port (optional)            | `8000`                      | ❌ No    |

### How to Get Required Tokens

#### 1. GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with these permissions:
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Action workflows)
   - `write:packages` (Upload packages to GitHub Package Registry)
3. Copy the token and add to your `.env` file

#### 2. aipipe API Key

1. Visit https://aipipe.org/login
2. Sign up or log in to your account
3. Navigate to API settings or dashboard
4. Generate or copy your API key
5. Add the key to your `.env` file

### Example .env File

```env
API_SECRET=my-super-secret-key
GITHUB_TOKEN=ghp_1234567890abcdefghijklmnopqrstuvwxyz
AI_PIPE_API_KEY=eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InRlc3QiLCJ1c2VyIjoidGVzdCJ9.test123
PORT=8000
```

## 🧪 Testing the Application

### 1. Check if the Server is Running

```bash
curl http://localhost:8000
# Expected response: {"message": "Welcome to Kalika's App Builder"}
```

### 2. View API Documentation

Open your browser and go to: http://localhost:8000/docs

This will show the interactive Swagger UI where you can test all endpoints.

### 3. Test the Build Endpoint

## 🔌 API Usage

### Main Endpoint: `POST /build`

This is the primary endpoint that generates applications based on natural language descriptions.

#### Request Format

```bash
curl -X POST http://localhost:8000/build \
    -H "Content-Type: application/json" \
    -d '{
        "email": "your-email@example.com",
        "secret": "your-api-secret",
        "task": "unique-task-id",
        "round": 1,
        "nonce": "unique-nonce",
        "brief": "Create a simple calculator web app",
        "checks": [
            "document.querySelector(\"input[type=text]\")",
            "document.querySelector(\"button\")",
            "typeof calculate === \"function\""
        ],
        "evaluation_url": "http://localhost:8000/_eval",
        "attachments": []
    }'
```

#### Request Parameters

| Field            | Type    | Required | Description                             |
| ---------------- | ------- | -------- | --------------------------------------- |
| `email`          | string  | ✅       | Your email address                      |
| `secret`         | string  | ✅       | Must match `API_SECRET` env var         |
| `task`           | string  | ✅       | Unique identifier for the task          |
| `round`          | integer | ✅       | Attempt number (usually 1)              |
| `nonce`          | string  | ✅       | Unique string for this request          |
| `brief`          | string  | ✅       | Natural language description of the app |
| `checks`         | array   | ✅       | JavaScript validation checks            |
| `evaluation_url` | string  | ✅       | URL to receive results                  |
| `attachments`    | array   | ❌       | Optional files/data                     |

#### Example Applications You Can Generate

```bash
# Simple Calculator
"brief": "Create a calculator with basic math operations (+, -, *, /)"

# To-Do List
"brief": "Build a to-do list app where users can add, delete, and mark tasks complete"

# Weather Dashboard
"brief": "Create a weather dashboard showing current conditions with a search function"

# Quiz App
"brief": "Build a multiple choice quiz with scoring and results display"
```

#### Response Codes

| Code  | Status              | Description                                |
| ----- | ------------------- | ------------------------------------------ |
| `200` | ✅ Success          | Request accepted, processing in background |
| `401` | ❌ Unauthorized     | Invalid `secret` key                       |
| `422` | ❌ Validation Error | Missing or invalid request fields          |

#### Success Response Example

```json
{
  "message": "Request received. Building Application...",
  "status": "accepted"
}
```

### Evaluation Endpoint: `POST /_eval`

This endpoint receives the results after application generation is complete.

```json
{
  "status": "success",
  "message": "Evaluation data received successfully",
  "task": "your-task-id",
  "pages_url": "https://username.github.io/repository-name"
}
```

## 🐳 Docker Deployment

### Build the Image

```bash
docker build -t tds-evaluator .
```

### Run with Environment File

```bash
docker run --env-file .env -p 8000:8000 tds-evaluator
```

### Run with Individual Environment Variables

```bash
docker run \
    -e API_SECRET=your-secret \
    -e GITHUB_TOKEN=your-github-token \
    -e AI_PIPE_API_KEY=your-aipipe-key \
    -p 8000:8000 \
    tds-evaluator
```

### Docker Compose (Optional)

Create a `docker-compose.yml` file:

```yaml
version: "3.8"
services:
  tds-evaluator:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
```

Run with:

```bash
docker-compose up -d
```

## 🚨 Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError" when starting

**Solution**: Make sure you're in the virtual environment and have installed dependencies:

```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### 2. "Port 8000 already in use"

**Solution**: Either stop the other service or use a different port:

```bash
uvicorn main:app --port 8001
```

#### 3. "API key authentication failed"

**Solution**: Check your `.env` file has the correct aipipe API key and it's properly formatted.

#### 4. "GitHub token permission denied"

**Solution**: Ensure your GitHub token has the required permissions (repo, workflow, write:packages).

### Getting Help

If you encounter issues:

1. Check the terminal output for error messages
2. Verify all environment variables are set correctly
3. Test with the interactive documentation at `/docs`
4. Check the GitHub repository for issues and discussions

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

- **Repository**: https://huggingface.co/spaces/NiloyMondal/TDS_Project_1
- **Issues**: Create an issue in the repository for bug reports
- **Discussions**: Use the community tab for questions and discussions
