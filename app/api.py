import asyncio
import json
import logging
import os
import random
import time
import uuid
from collections import defaultdict
from datetime import datetime, timezone

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware



LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
WEBHOOK_MODE = os.getenv("WEBHOOK_MODE", "valid")

logger = logging.getLogger("failure-lab")


class _TraceFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "request_id"):
            record.request_id = "n/a"
        if not hasattr(record, "trace_id"):
            record.trace_id = "n/a"
        return True


_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter(
    json.dumps({
        "timestamp": "%(asctime)s",
        "level": "%(levelname)s",
        "logger": "%(name)s",
        "request_id": "%(request_id)s",
        "trace_id": "%(trace_id)s",
        "message": "%(message)s",
    }),
))
_handler.addFilter(_TraceFilter())
logger.addHandler(_handler)
logger.setLevel(getattr(logging, LOG_LEVEL))
logger.propagate = False

app = FastAPI(title="API Failure Lab")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Request-ID", "X-Trace-ID", "X-Signature"],
)

USERS = {"admin": "password123"}
SESSIONS = {"valid-token-xyz": "admin"}

request_counters = defaultdict(int)

webhook_inbox = []

incidents_store: dict = {}
incidents_list: list = []


def _load_seeds():
    import json
    import os as _os
    seeds_dir = _os.path.join(_os.path.dirname(__file__), "seeds")
    if not _os.path.isdir(seeds_dir):
        return
    for fname in sorted(_os.listdir(seeds_dir)):
        if fname.endswith(".json"):
            inc_id = fname.replace(".json", "")
            with open(_os.path.join(seeds_dir, fname)) as f:
                data = json.load(f)
            data["id"] = inc_id
            incidents_store[inc_id] = data
            incidents_list.append({"id": inc_id, "summary": data.get("summary", "")})


@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
    trace_id = request.headers.get("X-Trace-ID", f"tx-{uuid.uuid4().hex[:12]}")

    request.state.request_id = request_id
    request.state.trace_id = trace_id

    if os.getenv("SIMULATE_FLAKY_NETWORK") == "true":
        if random.random() < 0.2:
            await asyncio.sleep(10)

    start = time.time()
    response = await call_next(request)
    duration_ms = int((time.time() - start) * 1000)

    request_counters[response.status_code] += 1

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Trace-ID"] = trace_id

    extra = {"request_id": request_id, "trace_id": trace_id}
    logger.info(
        f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms}ms)",
        extra=extra,
    )

    return response


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/d/headers")
async def dump_headers(request: Request):
    headers = dict(request.headers)
    return {
        "headers": headers,
        "request_id": request.state.request_id,
        "trace_id": request.state.trace_id,
    }


@app.get("/metrics")
async def metrics():
    return {
        "counters_by_status": dict(request_counters),
        "total_requests": sum(request_counters.values()),
    }


@app.post("/login")
async def login(request: Request):
    body = await request.json()
    username = body.get("username")
    password = body.get("password")

    extra = {"request_id": request.state.request_id, "trace_id": request.state.trace_id}

    if username not in USERS:
        logger.warning(f"Login failed: unknown user '{username}'", extra=extra)
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if USERS[username] != password:
        logger.warning(f"Login failed: wrong password for '{username}'", extra=extra)
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = "valid-token-xyz"
    logger.info(f"Login success: '{username}'", extra=extra)
    return {"token": token}


@app.get("/api/v1/data")
async def get_data(request: Request, authorization: str = Header(None)):
    extra = {"request_id": request.state.request_id, "trace_id": request.state.trace_id}

    if not authorization:
        logger.warning("Data request: missing Authorization header", extra=extra)
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = authorization.replace("Bearer ", "")
    if token not in SESSIONS:
        logger.warning(f"Data request: invalid token '{token[:8]}...'", extra=extra)
        raise HTTPException(status_code=403, detail="Forbidden - Invalid session")

    logger.info("Data request: authorized", extra=extra)
    return {"data": "Secret research results", "access": "admin"}


@app.get("/api/v1/resource/{id}")
async def get_resource(request: Request, id: int):
    extra = {"request_id": request.state.request_id, "trace_id": request.state.trace_id}

    if id > 100:
        logger.warning(f"Resource {id}: not found", extra=extra)
        raise HTTPException(status_code=404, detail="Resource not found")

    logger.info(f"Resource {id}: found", extra=extra)
    return {"id": id, "name": f"Resource {id}"}


@app.get("/api/v1/trigger-error")
async def trigger_error(request: Request):
    extra = {"request_id": request.state.request_id, "trace_id": request.state.trace_id}
    logger.error("Triggering intentional ZeroDivisionError", extra=extra)
    result = 1 / 0
    return {"result": result}


@app.get("/api/v1/external-call")
async def external_call(request: Request):
    extra = {"request_id": request.state.request_id, "trace_id": request.state.trace_id}
    delay = int(os.getenv("EXTERNAL_DELAY_SECONDS", "15"))
    logger.warning(f"External call: simulating {delay}s upstream delay", extra=extra)
    await asyncio.sleep(delay)
    return {"status": "success", "delay_seconds": delay}


@app.post("/webhooks/inbound")
async def webhook_inbound(request: Request, x_signature: str = Header(None)):
    extra = {"request_id": request.state.request_id, "trace_id": request.state.trace_id}
    body = await request.json()
    payload_hash = str(hash(json.dumps(body, sort_keys=True)))[:12]

    delivery = {
        "id": f"wh-{uuid.uuid4().hex[:8]}",
        "received_at": datetime.now(timezone.utc).isoformat(),
        "payload_hash": payload_hash,
        "headers": dict(request.headers),
        "body": body,
        "signature_provided": x_signature is not None,
        "status": "pending",
        "latency_ms": None,
    }

    if WEBHOOK_MODE == "bad_signature":
        expected = "sha256=expected-hmac-value"
        is_valid = x_signature == expected
        delivery["valid"] = is_valid
        delivery["status"] = "accepted" if is_valid else "rejected"
        delivery["latency_ms"] = random.randint(50, 200)
        if not is_valid:
            logger.warning(
                f"Webhook rejected: bad signature (got={x_signature[:20] if x_signature else 'none'})",
                extra=extra,
            )
        else:
            logger.info("Webhook accepted with valid signature", extra=extra)
    elif WEBHOOK_MODE == "slow_ack":
        await asyncio.sleep(3)
        delivery["valid"] = True
        delivery["status"] = "accepted"
        delivery["latency_ms"] = 3000
        logger.warning("Webhook: slow acknowledgment (3s)", extra=extra)
    else:
        delivery["valid"] = True
        delivery["status"] = "accepted"
        delivery["latency_ms"] = random.randint(20, 100)
        logger.info(f"Webhook accepted: event={body.get('event', 'unknown')}", extra=extra)

    webhook_inbox.insert(0, delivery)
    if len(webhook_inbox) > 50:
        webhook_inbox.pop()

    return delivery


@app.get("/webhooks/inbox")
async def webhook_inbox_list(limit: int = 10):
    return {"deliveries": webhook_inbox[:limit], "total": len(webhook_inbox)}


@app.get("/incidents")
async def list_incidents():
    return {"incidents": incidents_list}


@app.get("/incidents/{incident_id}")
async def get_incident(incident_id: str):
    inc = incidents_store.get(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    return inc


@app.post("/incidents/{incident_id}/replay")
async def replay_incident(incident_id: str, request: Request):
    inc = incidents_store.get(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    steps = inc.get("replay_steps", [])
    results = []
    for step in steps:
        results.append({
            "step": step.get("description", ""),
            "command": step.get("command", ""),
            "expected_status": step.get("expected_status"),
        })
    return {
        "incident_id": incident_id,
        "trace_id": request.state.trace_id,
        "steps": results,
    }


@app.get("/incidents/{incident_id}/evidence-bundle")
async def evidence_bundle(incident_id: str):
    inc = incidents_store.get(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    return {
        "incident_id": inc.get("id", incident_id),
        "summary": inc.get("summary", ""),
        "timeline": inc.get("timeline", []),
        "log_lines": inc.get("log_lines", []),
        "request_samples": inc.get("request_samples", []),
        "related_endpoints": inc.get("related_endpoints", []),
    }


def load_seed(incident_id: str, data: dict):
    data["id"] = incident_id
    incidents_store[incident_id] = data
    incidents_list.append({"id": incident_id, "summary": data.get("summary", "")})


_load_seeds()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
