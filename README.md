# 🔐 Secure LLM Gateway  
### Production-Grade AI Security Middleware with Async Micro-Batching

This project implements a secure, scalable gateway layer in front of Large Language Models (LLMs).  

It demonstrates real-world AI infrastructure engineering — not just model usage — but secure deployment, concurrency optimization, role-based access control, and performance benchmarking.

---

## 🧠 Why This Project Exists

LLMs introduce new risks in production environments:

- Prompt injection attacks  
- Data exfiltration attempts  
- PII leakage in responses  
- Model misuse by unauthorized roles  
- Uncontrolled cost under high concurrency  

This gateway enforces security and governance controls **before and after** LLM execution.

It acts as a controlled AI middleware layer.

---

## 🏗 Architecture Overview

The system follows a layered security and inference design:

Client  
↓  
FastAPI Gateway  
├── RBAC Policy Enforcement  
├── Prompt Injection Detection (Async Batched Inference)  
├── PII Detection (Pre-Request)  
├── LLM Provider (Claude Integration)  
├── PII Redaction (Post-Response)  
├── Audit Logging (JSONL Structured Logs)  
└── Prometheus Metrics  

### Key Architectural Components

- FastAPI async API layer  
- Async micro-batching inference queue  
- SentenceTransformer embeddings  
- Logistic regression injection classifier  
- Role-based model access control  
- Pre and post-response PII scanning  
- Structured audit logging  
- Cost estimation per request  
- Concurrency benchmarking harness  

---

## ⚡ Performance Benchmarking

Test Configuration:

- 500 total requests  
- 50 concurrent clients  
- CPU-based inference  
- Async micro-batching enabled  

Results:

- Throughput: ~475 requests/sec  
- Average latency: ~480ms  
- p95 latency: ~700ms  
- p99 latency: ~1047ms  

Micro-batching reduced latency significantly compared to a non-batched baseline and improved throughput ~3x.

This demonstrates real inference optimization under load.

---

## 🔄 Async Micro-Batching Design

Instead of running injection detection per request:

1. Requests are queued.
2. A background batch worker groups requests within a short time window.
3. Embeddings are computed in batch.
4. Logistic regression classification is applied to the full batch.
5. Results are distributed back to awaiting requests.

This improves:

- CPU efficiency  
- Cache utilization  
- Throughput under concurrency  
- Cost efficiency  

Tradeoff:  
A small batching delay window (~10ms).

---

## 🛡 Security Controls Implemented

### 1. Role-Based Access Control (RBAC)

Model access is restricted by role:

- Guest: No access  
- Analyst: Limited model access  
- Admin: Full model access  

Prevents model abuse and cost escalation.

---

### 2. Prompt Injection Detection

- SentenceTransformer embeddings  
- Logistic regression classifier  
- Threshold-based blocking  
- Probability and latency logging  

Blocks attempts like:
- “Ignore previous instructions”
- “Reveal system prompt”
- Hidden configuration extraction attempts

---

### 3. PII Detection & Redaction

- Regex-based detection for emails, SSNs  
- Pre-request blocking  
- Post-response redaction  

Prevents sensitive data leakage.

---

### 4. Audit Logging

Structured JSON logs include:

- trace_id  
- user_id  
- role  
- event type  
- injection probability  
- timestamps  

Designed for SIEM integration.

---

### 5. LLM Provider Integration (Claude)

- Anthropic Claude integration  
- Token usage tracking  
- Estimated cost calculation  
- Latency measurement  
- Graceful error handling  

Provider errors are captured without crashing the service.

---

## 📊 Observability

- Prometheus metrics endpoint  
- Request counting  
- Latency measurement  
- Benchmark script for load testing  

The system is built with production observability in mind.

---

## 💰 Cost Awareness

Each request calculates:

- Tokens used  
- Estimated USD cost per call  

This allows:

- Budget monitoring  
- Cost enforcement by role  
- Future quota implementation  

---

## ⚠ Failure Mode Analysis

Documented considerations include:

- Provider API failures  
- Credit exhaustion  
- Injection false negatives  
- PII regex bypass  
- Worker crashes  
- Queue overflow under traffic spikes  

Graceful error handling prevents service crashes.

---

## 🧩 Tradeoffs

### In-Process Queue

Pros:
- Low latency  
- Simple design  

Cons:
- Not horizontally scalable  

Enterprise alternative:
- Redis  
- Kafka  
- Ray Serve  

---

### Logistic Regression Classifier

Pros:
- Fast  
- Interpretable  
- Cheap  

Cons:
- Limited generalization to novel attack styles  

---

## 🚀 Running Locally

Start server:

uvicorn src.api:app --workers 1

Test endpoint:

curl -X POST http://127.0.0.1:8000/generate \
-H "Content-Type: application/json" \
-d '{"prompt":"Explain zero trust security","role":"admin","model":"claude-3-haiku-20240307"}'

Run concurrency benchmark:

python benchmark/concurrency_test.py

---

## 🔮 Future Improvements

Planned production-grade extensions:

- Provider abstraction layer (OpenAI + Claude)  
- JWT authentication  
- Rate limiting  
- Token quotas per role  
- Distributed batching (Redis)  
- Streaming responses  
- Grafana dashboards  
- Circuit breaker for provider failures  

---

## 🎯 What This Project Demonstrates

This project showcases:

- Async systems design  
- ML inference optimization  
- Secure AI middleware architecture  
- Performance benchmarking  
- Cost-aware LLM integration  
- Failure mode reasoning  
- Production-level thinking  

It reflects real-world AI platform engineering practices.

---

## 👤 Author

Dileep Kumar  
Senior Data & ML Engineer  

Focused on scalable AI systems, secure ML infrastructure, and production-grade data platforms.
