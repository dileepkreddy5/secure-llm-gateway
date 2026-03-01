ROLE_MODEL_ACCESS = {
    "guest": [],
    "analyst": ["claude-3-haiku-20240307"],
    "admin": [
        "claude-3-haiku-20240307",
        "claude-3-sonnet-20240229",
        "claude-3-opus-20240229"
    ]
}


def enforce_policy(body: dict, trace_id: str):

    role = body.get("role", "guest")
    model = body.get("model", None)

    if not model:
        return {
            "blocked": True,
            "reason": "Model not specified"
        }

    allowed_models = ROLE_MODEL_ACCESS.get(role, [])

    if model not in allowed_models:
        return {
            "blocked": True,
            "reason": f"Model {model} not allowed for role {role}"
        }

    return {
        "blocked": False
    }
