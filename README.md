# api-failure-analysis

A structured laboratory for analyzing common API failure modes. This repository provides an intentional failure lab to practice diagnosing HTTP errors and understanding root causes in distributed systems.

## Failure Classification

| Status Code | Type | Common Support Root Causes |
| ----------- | ---- | -------------------------- |
| **401** | Unauthorized | Invalid API key, expired token, or missing header. |
| **403** | Forbidden | Valid token but insufficient permissions (e.g., scoping issue). |
| **404** | Not Found | Resource deleted, wrong endpoint path, or DNS propagation delay. |
| **500** | Internal Error | Code crash, database disconnection, or unhandled exception. |
| **504** | Gateway Timeout | Upstream service delay or Load Balancer idle timeout exceeded. |

## Debug Flow (Decision Tree)

1. **Does the request reach the server?**
   - No: Check DNS, VPC, and Security Group (4xx or Timeout).
   - Yes: Examine application logs (`journalctl` / `docker logs`).
2. **Is it a Client error (4xx) or Server error (5xx)?**
   - **401/403**: Verify credentials and header format (`Bearer` token prefix?).
   - **404**: Confirm URL path and parameters via documentation.
   - **500**: Check stack trace for code-level failures or resource exhaustion.
3. **Is it a latency issue (Timeout)?**
   - Check upstream dependencies and database query execution times.

## Scenario Analysis

### 1) `POST /login` -> 401 Unauthorized
- **Symptom**: User provides correct password but gets 401.
- **Root Cause**: Often a case-sensitivity issue in the username field or an extra space in the input.

### 2) `GET /api/v1/data` -> 403 Forbidden
- **Symptom**: Token is valid for `/api/v1/ping` but fails for `/api/v1/data`.
- **Root Cause**: The session token lacks the required `admin` scope required for this specific resource.

### 3) `GET /api/v1/resource/105` -> 404 Not Found
- **Symptom**: Client expects a resource but it's missing.
- **Root Cause**: The resource ID exceeds the database sequence or was manually removed from the system.

### 4) `GET /api/v1/trigger-error` -> 500 Internal Error
- **Symptom**: Service returns generic 500 error.
- **Root Cause**: Unhandled exception (e.g., `ZeroDivisionError` or `DatabaseConnectionLost`) during request processing.

## Practice Lab

1. Launch the lab: `python app/api.py`
2. Test scenarios using `curl`:
   ```bash
   # Test 401
   curl -X POST http://localhost:8000/login -d '{"username": "admin", "password": "wrong-password"}'
   
   # Test 403
   curl -H "Authorization: Bearer wrong-token" http://localhost:8000/api/v1/data
   
   # Test 500
   curl http://localhost:8000/api/v1/trigger-error
   ```

## Quick Start (Docker)

```bash
docker build -t api-failure-lab .
docker run -p 8000:8000 api-failure-lab
```
