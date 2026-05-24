# Common API Error Codes

All responses include `X-Request-ID` and `X-Trace-ID` headers for correlation. See `GET /d/headers` to inspect inbound headers.

| Code | Endpoint | Trigger | Response | Trace Example |
|------|----------|---------|----------|---------------|
| **401** | `GET /api/v1/data` | No `Authorization` header sent | `{"detail":"Authorization header missing"}` | `tx-001` |
| **403** | `GET /api/v1/data` | Token valid but lacks admin scope | `{"detail":"Insufficient permissions — admin role required"}` | `tx-002` |
| **404** | `GET /api/v1/resource/{id}` | Resource ID doesn't exist | `{"detail":"Resource 999 not found"}` | `tx-004` |
| **500** | `GET /api/v1/trigger-error` | Uncaught `RuntimeError` | `{"detail":"Internal server error"}` (stack in server logs) | `tx-005` |
| **504** | Not directly returned | Upstream timeout pattern (client times out at 30s, server processes 45s) | No response — connection drops | `tx-006` (server-side) |

## How to Use

```bash
# Trigger a 401
curl -sv http://localhost:8000/api/v1/data 2>&1 | grep -E "< (HTTP|X-Request-ID|X-Trace-ID)"

# Trigger a 403
TOKEN=$(curl -s -X POST http://localhost:8000/login -H "Content-Type: application/json" -d '{"username":"admin","password":"password123"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/data
# → 403: user lacks admin scope (login endpoint doesn't assign it)

# Trigger a 404
curl -s http://localhost:8000/api/v1/resource/999

# Trigger a 500
curl -s http://localhost:8000/api/v1/trigger-error
```
