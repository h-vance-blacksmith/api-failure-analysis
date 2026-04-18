#!/bin/bash
# simulate-failures.sh
# Automates the testing of API failure modes to verify troubleshooting scripts.

BASE_URL # Target environment="http://localhost:8000"

echo "=== Starting API Failure Simulation ==="

# 1. Test 401 Unauthorized
echo -n "[TEST] POST /login (Invalid Credentials): "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/login" -d '{"username": "admin", "password": "wrong"}')
if [ "$STATUS" -eq 401 ]; then echo "PASS (HTTP 401)"; else echo "FAIL (HTTP $STATUS)"; fi

# 2. Test 403 Forbidden
echo -n "[TEST] GET /api/v1/data (Invalid Token): "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer invalid" "$BASE_URL/api/v1/data")
if [ "$STATUS" -eq 403 ]; then echo "PASS (HTTP 403)"; else echo "FAIL (HTTP $STATUS)"; fi

# 3. Test 404 Not Found
echo -n "[TEST] GET /api/v1/resource/999 (Missing Resource): "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/resource/999")
if [ "$STATUS" -eq 404 ]; then echo "PASS (HTTP 404)"; else echo "FAIL (HTTP $STATUS)"; fi

# 4. Test 500 Internal Error
echo -n "[TEST] GET /api/v1/trigger-error (Server Crash): "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/v1/trigger-error")
if [ "$STATUS" -eq 500 ]; then echo "PASS (HTTP 500)"; else echo "FAIL (HTTP $STATUS)"; fi

echo "=== Simulation Complete ==="
