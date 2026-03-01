from fastapi import FastAPI
from prometheus_client import make_asgi_app
import asyncio

from src.middleware.pipeline import SecurityPipeline
from src.middleware.injection_detector import batch_worker
from src.llm.claude_client import call_claude


app = FastAPI()
pipeline = SecurityPipeline()


# --------------------------------
# STARTUP: launch batch worker
# --------------------------------
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(batch_worker())


# --------------------------------
# Metrics endpoint
# --------------------------------
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


# --------------------------------
# Generate endpoint
# --------------------------------
@app.post("/generate")
async def generate(body: dict):

    # -------------------------
    # Security Layer
    # -------------------------
    context = await pipeline.pre_request(body)

    if context["blocked"]:
        return context

    # -------------------------
    # Real Claude LLM Call
    # -------------------------
    llm_result = await call_claude(
        prompt=body.get("prompt"),
        model=body.get("model", "claude-3-haiku-20240307"),
        max_tokens=body.get("max_tokens", 500)
    )

    # -------------------------
    # Post-Response Security
    # -------------------------
    final_response = pipeline.post_response(llm_result["response"])

    return {
        "trace_id": context["trace_id"],
        "blocked": False,
        "response": final_response,
        "injection": context["injection"],
        "security_overhead_ms": context["security_overhead_ms"],
        "llm_latency_ms": llm_result["latency_ms"],
        "tokens_used": llm_result["tokens"],
        "estimated_cost_usd": llm_result["estimated_cost_usd"]
    }
