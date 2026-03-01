import re
import time

from src.metrics.prometheus_metrics import (
    SECURITY_OVERHEAD,
)

# ==============================
# Config
# ==============================

PII_POLICY_MODE = "block"  # options: "block", "redact", "log"

# ==============================
# Regex Patterns
# ==============================

PII_PATTERNS = {
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
    "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
    "api_key": r"\bsk-[A-Za-z0-9]{20,}\b",
}


def detect_pii(text: str):
    start = time.time()
    findings = []

    for pii_type, pattern in PII_PATTERNS.items():
        matches = re.findall(pattern, text)
        for match in matches:
            findings.append({
                "type": pii_type,
                "value": match
            })

    latency_ms = (time.time() - start) * 1000

    return {
        "found": len(findings) > 0,
        "findings": findings,
        "latency_ms": latency_ms
    }


def redact_pii(text: str):
    redacted_text = text

    for pii_type, pattern in PII_PATTERNS.items():
        redacted_text = re.sub(pattern, f"[REDACTED_{pii_type.upper()}]", redacted_text)

    return redacted_text
