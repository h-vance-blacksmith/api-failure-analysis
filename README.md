# 🛠️ Technical Support API Diagnostic Suite

An open-source Python diagnostic CLI and Postman collection engineered for modern Customer Experience (CX) and Support teams to automate API endpoint health checks, capture raw HTTP headers, and isolate client-side vs. server-side bugs in seconds.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/h-vance/api-failure-analysis)

---

## 🎯 Recruiter Cheatsheet: Why This Project Matters
If you are looking at my profile for a **Technical Support Specialist** or **Support Engineer** role, here is what this project demonstrates about my skills:
* **API Literacy:** Proves deep, practical understanding of REST APIs, payloads, headers, query parameters, and webhooks.
* **Support Automation:** Shows my ability to write Python tools that eliminate manual triage, lowering MTTR.
* **Engineering Empathy:** Instead of passing vague customer complaints to engineering, this tool generates a complete, clean JSON reproduction packet that developers can use to fix bugs instantly.

---

## 🚀 Quick Start: "How to Use" (Recruiter Edition)

This tool is designed to be extremely easy to use. Support agents or recruiters can run it to analyze any failing API call with a single command.

### Step 1: Run the analyzer command
To diagnose a customer's API connection (for example, a failing login or checkout endpoint):

```bash
python diagnose.py --url https://api.yoursaas.com/v1/checkout --method POST
```

### Step 2: Read the Diagnostic Result
The tool immediately outputs a clean, color-coded triage recommendation:

```text
============================================================
🔍 API DIAGNOSTIC RESULTS
============================================================
Target URL:  https://api.yoursaas.com/v1/checkout
HTTP Status: 400 Bad Request (Client-Side Error)
Triage Rule: MISSING_REQUIRED_PAYLOAD_FIELD

------------------------------------------------------------
🚨 ROOT CAUSE ANALYSIS & ACTIONABLE REMEDIATION
------------------------------------------------------------
👉 The client's API request failed because the mandatory field
   "customer_email" was missing from the JSON payload.

📋 RECOMMENDED CX RESPONSE ACTION:
   "Hi customer! It looks like your API call is missing the 
   required 'customer_email' field in your POST body. Please
   add this field and retry your request."

🛠️ ENGINEER-READY DATA:
   Raw logs & a generated curl command have been saved to
   ./logs/diag_20260521_121700.json for engineering reference.
============================================================
```

---

## 🛠️ Key Features & Technical Details

1. **Auto-Triage for Common API Errors:**
   * **400 Bad Request:** Scans JSON payloads for syntax errors or missing required fields.
   * **401/403 Unauthorized:** Checks `Authorization` headers for expired, malformed, or missing tokens.
   * **429 Too Many Requests:** Parses rate limit headers (`X-RateLimit-Limit`, `Retry-After`) to give precise wait times.
   * **5xx Server Errors:** Automatically captures server response headers and latency metrics to isolate outages.

2. **Postman Collection Included:**
   * Includes a pre-configured JSON collection (`/postman`) containing standard reproduction test patterns for common 4xx/5xx errors, reducing debugging time for support teams during customer API failures.

3. **Log Export for Developers:**
   * Automatically packages full network traces, payload variables, and environment specs into a single JSON diagnostic report ready to attach to Jira tickets.

---

## 📥 Installation & Getting Started

```bash
# Clone the repository
git clone https://github.com/h-vance/api-failure-analysis.git

# Navigate into the directory
cd api-failure-analysis

# Install dependencies
pip install -r app/requirements.txt

# Run the Flask-based failure simulation API
python app/api.py
```

Run tests to validate endpoint health under fault conditions:
```bash
pytest tests/
```

---

## 📄 License & Maintainer
* **License:** MIT License - see the [LICENSE](LICENSE) file for details.
* **Maintainer:** Harrison Vance | Technical Support & Operations
