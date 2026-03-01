import asyncio
import aiohttp
import time
import numpy as np

URL = "http://127.0.0.1:8000/generate"

PAYLOAD = {
    "prompt": "Hello",
    "role": "admin",
    "model": "gpt-4",
    "max_tokens": 1000
}

TOTAL_REQUESTS = 500
CONCURRENT_REQUESTS = 50


async def send_request(session):
    start = time.time()
    async with session.post(URL, json=PAYLOAD) as response:
        await response.text()
    return (time.time() - start) * 1000


async def run_test():
    connector = aiohttp.TCPConnector(limit=CONCURRENT_REQUESTS)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [send_request(session) for _ in range(TOTAL_REQUESTS)]
        return await asyncio.gather(*tasks)


if __name__ == "__main__":
    start_time = time.time()

    latencies = asyncio.run(run_test())
    total_time = time.time() - start_time

    latencies = np.array(latencies)

    print("===== Concurrency Benchmark =====")
    print(f"Total Requests: {TOTAL_REQUESTS}")
    print(f"Concurrency Level: {CONCURRENT_REQUESTS}")
    print(f"Total Time: {total_time:.2f} sec")
    print(f"Throughput: {TOTAL_REQUESTS / total_time:.2f} req/sec")
    print(f"Average Latency: {np.mean(latencies):.2f} ms")
    print(f"p50: {np.percentile(latencies, 50):.2f} ms")
    print(f"p95: {np.percentile(latencies, 95):.2f} ms")
    print(f"p99: {np.percentile(latencies, 99):.2f} ms")
