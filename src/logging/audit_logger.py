import json
import uuid
from datetime import datetime


AUDIT_LOG_FILE = "audit_log.jsonl"


def generate_trace_id():
    return str(uuid.uuid4())


def log_event(event: dict):
    event["timestamp"] = datetime.utcnow().isoformat()
    with open(AUDIT_LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")
