<center>
<h1>Api Failure Analysis</h1>
<p><em>Advanced diagnostics and resolution patterns for complex API failures and distributed system outages.</em></p>
<img src="https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white" alt="Terraform">&nbsp;<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">&nbsp;<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">&nbsp;<img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white" alt="Node.js">&nbsp;<img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">&nbsp;<img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white" alt="Prometheus">
</center>

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