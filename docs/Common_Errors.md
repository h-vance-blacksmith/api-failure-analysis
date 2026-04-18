# Common API Error Codes

- **401**: Missing or malformed Auth header.
- **403**: Token valid but lacks 'admin' permission.
- **404**: Endpoint path typo or resource ID not in DB.
- **500**: Uncaught exception (see stack trace).
- **504**: Upstream timeout (typically >30s).
