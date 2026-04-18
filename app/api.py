import os
import random
import time

from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI(title="API Failure Lab")

# Simulated database
USERS = {"admin": "password123"}
SESSIONS = {"valid-token-xyz": "admin"}


@app.middleware("http")
async def simulate_system_load(request: Request, call_next):
    """Middleware to inject random failure modes for analysis."""
    if os.getenv("SIMULATE_FLAKY_NETWORK") == "true":
        if random.random() < 0.2:
            time.sleep(10)  # Simulate a long network delay

    response = await call_next(request)
    return response


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/login")
async def login(request: Request):
    """Login endpoint to demonstrate 401 and 403."""
    body = await request.json()
    username = body.get("username")
    password = body.get("password")

    if username not in USERS:
        # 404 User not found (but often returned as 401 for security)
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if USERS[username] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"token": "valid-token-xyz"}


@app.get("/api/v1/data")
async def get_data(authorization: str = Header(None)):
    """Data endpoint to demonstrate 401 and 403."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = authorization.replace("Bearer ", "")
    if token not in SESSIONS:
        raise HTTPException(status_code=403, detail="Forbidden - Invalid session")

    return {"data": "Secret research results", "access": "admin"}


@app.get("/api/v1/resource/{id}")
async def get_resource(id: int):
    """Resource endpoint to demonstrate 404."""
    if id > 100:
        raise HTTPException(status_code=404, detail="Resource not found")
    return {"id": id, "name": f"Resource {id}"}


@app.get("/api/v1/trigger-error")
async def trigger_error():
    """Internal error endpoint to demonstrate 500."""
    # Deliberate ZeroDivisionError
    result = 1 / 0
    return {"result": result}


@app.get("/api/v1/external-call")
async def external_call():
    """Simulates an external call that times out."""
    time.sleep(15)  # Simulate long upstream processing
    return {"status": "success"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
