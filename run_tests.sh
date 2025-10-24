#!/bin/bash
# Test runner for TDS-PROJ-1 application
# This script tests all payload files against the local API

echo "🧪 TDS-PROJ-1 Test Suite"
echo "============================================================"
echo ""

API_URL="http://127.0.0.1:8000/build"
TEST_DIR="./test_payloads"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if server is running
echo "🔍 Checking if server is running at $API_URL..."
if ! curl -s -f -o /dev/null "$API_URL" 2>/dev/null; then
    if ! curl -s -f -o /dev/null "http://127.0.0.1:8000/" 2>/dev/null; then
        echo -e "${RED}❌ Server not running!${NC}"
        echo "Please start the server first:"
        echo "  python -m uvicorn main:app --host 0.0.0.0 --port 8000"
        exit 1
    fi
fi
echo -e "${GREEN}✅ Server is running${NC}"
echo ""

# Function to test a payload
test_payload() {
    local file=$1
    local name=$(basename "$file" .json)
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 Testing: $name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Send request
    response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -d @"$file")
    
    # Extract status code (last line)
    status_code=$(echo "$response" | tail -n1)
    # Extract body (everything except last line)
    body=$(echo "$response" | sed '$d')
    
    echo "📤 Request file: $file"
    echo "📊 Status code: $status_code"
    echo "📄 Response:"
    echo "$body" | jq '.' 2>/dev/null || echo "$body"
    echo ""
    
    if [ "$status_code" = "200" ]; then
        echo -e "${GREEN}✅ Test PASSED${NC}"
    elif [ "$status_code" = "401" ]; then
        echo -e "${RED}❌ Test FAILED - Unauthorized (check secret)${NC}"
    else
        echo -e "${RED}❌ Test FAILED - Status: $status_code${NC}"
    fi
    echo ""
    
    # Wait a bit between tests
    sleep 2
}

# Check if test directory exists
if [ ! -d "$TEST_DIR" ]; then
    echo -e "${RED}❌ Test directory not found: $TEST_DIR${NC}"
    exit 1
fi

# Count test files
total_tests=$(ls -1 "$TEST_DIR"/*.json 2>/dev/null | wc -l)
if [ "$total_tests" -eq 0 ]; then
    echo -e "${RED}❌ No test files found in $TEST_DIR${NC}"
    exit 1
fi

echo "📁 Found $total_tests test payload(s)"
echo ""

# Run tests
passed=0
failed=0

for payload in "$TEST_DIR"/*.json; do
    test_payload "$payload"
    # Simple pass/fail tracking based on last test
    if [ $? -eq 0 ]; then
        ((passed++))
    else
        ((failed++))
    fi
done

# Summary
echo "============================================================"
echo "📊 TEST SUMMARY"
echo "============================================================"
echo "Total Tests: $total_tests"
echo -e "${GREEN}Passed: $passed${NC}"
if [ "$failed" -gt 0 ]; then
    echo -e "${RED}Failed: $failed${NC}"
fi
echo ""

if [ "$failed" -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests completed! Check your GitHub for created repositories.${NC}"
else
    echo -e "${YELLOW}⚠️  Some tests may have issues. Check the output above.${NC}"
fi
echo ""
echo "💡 Tips:"
echo "   - Each request creates a GitHub repository"
echo "   - Check logs in the server terminal for detailed processing info"
echo "   - Repositories are named based on the 'task' field in each payload"
echo "   - GitHub Pages will be enabled for each repository"
echo "============================================================"
