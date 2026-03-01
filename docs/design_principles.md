# Design Principles

## 1. Defense in Depth
No single detection layer is trusted.

## 2. Observability First
Every decision must be measurable.

## 3. Cost Transparency
Every request tracks token cost and LLM overhead.

## 4. Failure Visibility
False positives and false negatives must be documented.

## 5. Production Mindset
- No blocking I/O
- Structured logging
- Async-first design
- Rate limiting at edge
