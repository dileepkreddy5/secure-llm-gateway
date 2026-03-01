import os
import time
import anthropic

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

MODEL_COST = {
    "claude-3-haiku-20240307": 0.00025,
    "claude-3-sonnet-20240229": 0.003,
    "claude-3-opus-20240229": 0.015,
}

async def call_claude(prompt: str,
                      model: str = "claude-3-haiku-20240307",
                      max_tokens: int = 500):

    start = time.time()

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    latency_ms = (time.time() - start) * 1000

    content = response.content[0].text
    usage = response.usage

    total_tokens = usage.input_tokens + usage.output_tokens

    cost = (total_tokens / 1000) * MODEL_COST.get(model, 0)

    return {
        "response": content,
        "latency_ms": latency_ms,
        "tokens": total_tokens,
        "estimated_cost_usd": cost
    }
