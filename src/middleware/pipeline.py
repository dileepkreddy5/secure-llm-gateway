import time

from src.middleware.injection_detector import detect_injection
from src.middleware.pii_scanner import detect_pii, redact_pii
from src.middleware.policy_engine import enforce_policy
from src.logging.audit_logger import generate_trace_id, log_event


class SecurityPipeline:

    async def pre_request(self, body: dict):

        trace_id = generate_trace_id()
        start = time.time()

        prompt = body.get("prompt", "")
        user_id = body.get("user_id", "anonymous")
        role = body.get("role", "guest")

        # -------------------------
        # RBAC Policy
        # -------------------------
        policy_result = enforce_policy(body, trace_id)

        if policy_result["blocked"]:
            return {
                "trace_id": trace_id,
                "blocked": True,
                "reason": policy_result["reason"]
            }

        # -------------------------
        # Injection Detection (ASYNC)
        # -------------------------
        injection_result = await detect_injection(prompt)

        if injection_result["blocked"]:
            log_event({
                "trace_id": trace_id,
                "user_id": user_id,
                "role": role,
                "event": "blocked_injection",
                "injection_probability": injection_result["probability"],
                "injection_latency_ms": injection_result["latency_ms"],
            })

            return {
                "trace_id": trace_id,
                "blocked": True,
                "reason": "Prompt Injection Detected",
                "injection": injection_result,
            }

        # -------------------------
        # PII Detection (sync is fine)
        # -------------------------
        pii_result = detect_pii(prompt)

        if pii_result["found"]:
            return {
                "trace_id": trace_id,
                "blocked": True,
                "reason": "PII detected in request",
                "pii": pii_result,
            }

        total_security_latency = (time.time() - start) * 1000

        return {
            "trace_id": trace_id,
            "blocked": False,
            "injection": injection_result,
            "security_overhead_ms": total_security_latency
        }

    def post_response(self, response: str):
        pii_result = detect_pii(response)

        if pii_result["found"]:
            response = redact_pii(response)

        return response
