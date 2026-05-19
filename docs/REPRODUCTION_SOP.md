# Standard Operating Procedure (SOP): Technical Issue Reproduction

> **Purpose:** To provide a systematic, evidence-based framework for reproducing and documenting technical issues reported by customers. This SOP ensures that all escalations to Engineering are actionable, reproducible, and context-rich, thereby reducing MTTR (Mean Time To Resolution).

---

## 1. The Triage Mindset: "Evidence Over Assumption"
Before attempting reproduction, gather the **Customer Context Cluster**:
- **User ID / Org ID:** Who is impacted?
- **Timestamp:** Exactly when did it happen? (Check server logs for this window).
- **Environment:** Browser version, OS, and any specific feature flags enabled.
- **The "Success Path":** What was the user *trying* to achieve when the error occurred?

---

## 2. Browser-Side Troubleshooting (The T1/T2 Foundation)
90% of "API failures" reported by customers are visible in the browser's Network layer.

### Step A: Chrome DevTools Network Tab
1. Open DevTools (`F12` or `Cmd+Option+I`).
2. Go to the **Network** tab and check "Preserve Log."
3. Ask the user to reproduce the action.
4. **Identify the Culprit:** Look for Red (4xx/5xx) status codes.
5. **Inspect the Payload:**
   - **Request:** Are the parameters correct?
   - **Response:** What is the specific error message from the server? (e.g., `{"error": "invalid_auth_token"}`).

### Step B: The HAR File (Gold Standard)
If you cannot reproduce the issue on your machine, ask the customer for a **HAR (HTTP Archive)** file.
- *Instruction for Customer:* "Right-click any row in the Network tab -> Save all as HAR with content."

---

## 3. Isolation: Frontend vs. Backend
Determine if the bug lives in the UI (JavaScript) or the Server (API).

| If you see... | Location | Next Step |
| :--- | :--- | :--- |
| **Console Errors (Uncaught Type Error)** | Frontend | Check recent UI deployments. |
| **401 / 403 Forbidden** | Auth Layer | Verify user permissions/token expiry. |
| **500 Internal Server Error** | Backend | Search logs for Request ID / Trace ID. |
| **422 Unprocessable Entity** | Validation | Check if the UI is sending a malformed payload. |

---

## 4. CLI Reproduction (Isolating the API)
Once you have the Request Payload from the browser, attempt to reproduce it using `cURL` or Postman. This confirms if the issue is independent of the browser.

```bash
# Example Triage cURL
curl -X POST https://api.service.com/v1/resource \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

---

## 5. The Perfect Escalation Template
When handing off to Engineering, use this format to ensure they don't send it back for "more info":

### **Subject: [BUG] {Brief Description} | Impact: {Low/Med/High}**

**1. Summary:** {Short description of the behavior}
**2. Reproduction Steps:**
   1. Log in as {User ID}
   2. Navigate to {URL}
   3. Click {Button}
**3. Expected Behavior:** {What should happen}
**4. Actual Behavior:** {What happened instead}
**5. Evidence:**
- **Request ID:** `req_12345abcde`
- **Browser Logs:** {Paste snippet or link to HAR}
- **Server Logs:** {Link to Datadog/Splunk search}
**6. Potential Root Cause (Optional):** {Your T2 hypothesis based on isolation steps}

---

## 6. Closing the Loop (CX Excellence)
Once Engineering provides a fix:
1. **Verify** the fix in a staging/sandbox environment.
2. **Update the KB**: If this was a common point of confusion, draft a Knowledge Base article to prevent future tickets.
3. **Notify the User**: Communicate the resolution with empathy and clarity.
