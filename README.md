# API Failure Analysis Lab

A structured laboratory for analyzing common API failure modes in distributed systems. This repository provides an intentional failure lab to practice diagnosing HTTP errors, understanding root causes, and implementing resiliency patterns.

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![API](https://img.shields.io/badge/API-green?style=for-the-badge)](https://en.wikipedia.org/wiki/API)
[![HTTP](https://img.shields.io/badge/HTTP-blue?style=for-the-badge)](https://en.wikipedia.org/wiki/HTTP)
[![DevOps](https://img.shields.io/badge/DevOps-007ACC?style=for-the-badge)](https://en.wikipedia.org/wiki/DevOps)

## Failure Mode Classification

| Status Code | Failure Type | Common Operational Root Causes |
| :--- | :--- | :--- |
| **401** | Unauthorized | Invalid API key, expired token, or missing Authorization header. |
| **403** | Forbidden | Valid token but insufficient permissions or restricted resource access. |
| **404** | Not Found | Resource deleted, incorrect endpoint path, or DNS propagation delay. |
| **500** | Internal Error | Application crash, unhandled exceptions, or database disconnection. |
| **504** | Gateway Timeout | Upstream service latency or Load Balancer timeout exceeded. |

## Diagnostic Workflow

1. **Connectivity Check**: Does the request reach the server?
   - If no, inspect DNS, VPC settings, and Security Group rules.
2. **Error Classification**: Is it a Client error (4xx) or Server error (5xx)?
   - **401/403**: Verify credential format and token scopes.
   - **404**: Confirm URL paths and parameters against documentation.
   - **500**: Inspect application logs and stack traces for resource exhaustion or logic errors.
3. **Latency Analysis**: Is the response delayed?
   - Review upstream dependencies and database query performance.

## Practical Scenarios

### Authentication and Authorization
- **Symptom**: 401 Unauthorized despite providing credentials.
- **Investigation**: Check for case-sensitivity, extra whitespace, or incorrect token prefixes (e.g., missing `Bearer `).

### Resource Scoping
- **Symptom**: 403 Forbidden for specific endpoints.
- **Investigation**: Verify if the session token carries the required permission scopes for the requested resource.

### Server-Side Failures
- **Symptom**: Intermittent 500 Internal Server Errors.
- **Investigation**: Identify unhandled exceptions such as database connection loss or arithmetic errors in the application logic.

## Lab Setup

### Local Installation
1. Install dependencies:
   ```bash
   pip install -r app/requirements.txt
   ```
2. Launch the lab server:
   ```bash
   python app/api.py
   ```
3. Test using `curl`:
   ```bash
   curl -X POST http://localhost:8000/login -d '{"username": "admin", "password": "wrong-password"}'
   ```

### Docker Deployment
```bash
docker build -t api-failure-lab .
docker run -p 8000:8000 api-failure-lab
```

## Repository Structure

- `app/`: FastAPI application code with intentional failure endpoints.
- `infra/`: Terraform configuration for deploying the lab environment.
- `scripts/`: Helper scripts for automated testing and scenario triggering.
- `tests/`: Pytest suite to verify failure mode detection.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
