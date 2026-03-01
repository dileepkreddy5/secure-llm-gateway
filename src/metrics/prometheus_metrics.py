from prometheus_client import Counter, Histogram, Gauge

# Total requests
REQUESTS_TOTAL = Counter(
    "llm_requests_total",
    "Total LLM requests received"
)

# Injection blocks
INJECTION_BLOCK_COUNT = Counter(
    "injection_block_count",
    "Number of blocked prompt injections"
)

# Injection probability distribution
INJECTION_PROBABILITY = Histogram(
    "injection_probability",
    "Distribution of injection probabilities",
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

# Detection latency
INJECTION_LATENCY = Histogram(
    "injection_detection_latency_ms",
    "Injection detection latency in milliseconds",
    buckets=[1, 2, 5, 10, 20, 50]
)

# Security overhead
SECURITY_OVERHEAD = Histogram(
    "security_overhead_ms",
    "Total security layer overhead",
    buckets=[5, 10, 20, 30, 50, 100]
)
# PII detections
PII_DETECTED_COUNT = Counter(
    "pii_detected_count",
    "Number of requests containing PII"
)

PII_REDACTION_COUNT = Counter(
    "pii_redaction_count",
    "Number of responses redacted for PII"
)

PII_DETECTION_LATENCY = Histogram(
    "pii_detection_latency_ms",
    "PII detection latency in milliseconds",
    buckets=[1, 2, 5, 10, 20, 50]
)
