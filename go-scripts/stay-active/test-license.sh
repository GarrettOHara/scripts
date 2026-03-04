#!/bin/bash

# Test script for Stay Active license system
echo "🧪 Testing Stay Active License System"
echo "====================================="

SERVER_URL="http://localhost:8080"

# Test 1: Generate a license
echo ""
echo "📋 Test 1: Generating a license for test user..."
RESPONSE=$(curl -s -X POST $SERVER_URL/v1/license/generate \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test-user@example.com"}')

echo "Response: $RESPONSE"

# Extract license ID from response
LICENSE_ID=$(echo $RESPONSE | jq -r '.license.id')
echo "Generated License ID: $LICENSE_ID"

# Test 2: Validate the license
echo ""
echo "🔍 Test 2: Validating the generated license..."
VALIDATION=$(curl -s -X POST $SERVER_URL/v1/license/validate \
  -H "Content-Type: application/json" \
  -d "{\"license_id\": \"$LICENSE_ID\"}")

echo "Validation Response: $VALIDATION"

# Test 3: Test invalid license
echo ""
echo "❌ Test 3: Testing invalid license validation..."
INVALID_VALIDATION=$(curl -s -X POST $SERVER_URL/v1/license/validate \
  -H "Content-Type: application/json" \
  -d '{"license_id": "invalid-license-123"}')

echo "Invalid License Response: $INVALID_VALIDATION"

# Test 4: Health check
echo ""
echo "🏥 Test 4: API Health check..."
HEALTH=$(curl -s $SERVER_URL/v1/health)
echo "Health Response: $HEALTH"

echo ""
echo "✅ License system tests completed!"
echo ""
echo "💡 To test the main binary with license checking:"
echo "   ./build/stay-active-test --delay 0.1"
echo ""
echo "🌐 View the website at: $SERVER_URL/v1/"
