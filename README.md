<center>
<h1>Api Failure Analysis</h1>
<p><em>Advanced diagnostics and resolution patterns for complex API failures and distributed system outages.</em></p>

---

<h1>Api Failure Analysis</h1>


| **403** | Forbidden | Valid token but insufficient permissions or restricted resource access. |
| **404** | Not Found | Resource deleted, incorrect endpoint path, or DNS propagation delay. |
| **500** | Internal Error | Application crash, unhandled exceptions, or database disconnection. |
| **504** | Gateway Timeout | Upstream service latency or Load Balancer timeout exceeded. |




docker run -p 8000:8000 api-failure-lab
```

- `scripts/`: Helper scripts for automated testing and scenario triggering.
- `tests/`: Pytest suite to verify failure mode detection.
