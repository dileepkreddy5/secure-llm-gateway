import asyncio
import time
import joblib
import numpy as np
import torch
from sentence_transformers import SentenceTransformer


# -------------------------------
# Prevent CPU Oversubscription
# -------------------------------
torch.set_num_threads(1)


# -------------------------------
# Load Models Once
# -------------------------------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
classifier = joblib.load("evaluation/injection_model.pkl")

THRESHOLD = 0.6


# -------------------------------
# Async Micro-Batching System
# -------------------------------
request_queue = asyncio.Queue()
BATCH_WINDOW_MS = 5


async def batch_worker():
    while True:
        prompts = []
        futures = []

        try:
            # Wait for first item
            item = await request_queue.get()
            prompts.append(item["prompt"])
            futures.append(item["future"])

            # Collect more items for small window
            start = time.time()

            while (time.time() - start) * 1000 < BATCH_WINDOW_MS:
                try:
                    item = request_queue.get_nowait()
                    prompts.append(item["prompt"])
                    futures.append(item["future"])
                except asyncio.QueueEmpty:
                    await asyncio.sleep(0.001)

            # -----------------------
            # Process batch
            # -----------------------
            embeddings = embedding_model.encode(prompts)
            probs = classifier.predict_proba(embeddings)[:, 1]

            for prob, future in zip(probs, futures):
                result = {
                    "probability": float(prob),
                    "latency_ms": 0.0,  # handled outside
                    "threshold": THRESHOLD,
                    "blocked": bool(prob >= THRESHOLD)
                }
                future.set_result(result)

        except Exception as e:
            print("Batch worker error:", e)


async def detect_injection(prompt: str) -> dict:
    start = time.time()

    loop = asyncio.get_running_loop()
    future = loop.create_future()

    await request_queue.put({
        "prompt": prompt,
        "future": future
    })

    result = await future

    result["latency_ms"] = (time.time() - start) * 1000
    return result
