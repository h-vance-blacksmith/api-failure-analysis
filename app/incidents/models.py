from pydantic import BaseModel
from typing import Optional


class TimelineEvent(BaseModel):
    ts: str
    event: str
    trace_id: Optional[str] = None


class LogLine(BaseModel):
    level: str
    message: str
    trace_id: Optional[str] = None


class RequestSample(BaseModel):
    method: str
    path: str
    status: int


class ReplayStep(BaseModel):
    description: str
    command: str
    expected_status: Optional[int] = None


class Incident(BaseModel):
    id: str
    summary: str
    timeline: list[TimelineEvent] = []
    log_lines: list[LogLine] = []
    request_samples: list[RequestSample] = []
    related_endpoints: list[str] = []
    replay_steps: list[ReplayStep] = []
