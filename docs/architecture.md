# Enterprise Secure LLM Gateway – Architecture

## System Overview

```mermaid
flowchart TD

Client --> API[FastAPI Gateway]

API --> Inj[Injection Detector]
API --> PII[PII Scanner]
API --> RBAC[Policy Engine]
API --> Rate[Rate Limiter]

Inj --> Router
PII --> Router
RBAC --> Router
Rate --> Router

Router --> LLM[(LLM Provider)]

LLM --> Validation[Response Validation Layer]
Validation --> Hallucination[Hallucination Risk Scoring]
Validation --> Redaction[PII Redaction]

Validation --> Logger[Audit Logger]
Validation --> Metrics[Prometheus Metrics]

Logger --> Storage[(Postgres / JSON)]
Metrics --> Prometheus
```

---

## Design Goals

- Layered security detection
- Minimal latency overhead (<30ms target)
- Cost-aware architecture
- Full auditability
- Production observability
- Concurrency stability

---

## Latency Breakdown Model

| Component | Target |
|-----------|--------|
| Injection Detection | <15 ms |
| PII Scan | <5 ms |
| Policy Check | <3 ms |
| Hallucination Scoring | <10 ms |
| Total Security Overhead | <30 ms |
