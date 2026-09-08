from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from backend.detection.behavior import analyze_behavior
from backend.detection.engine import analyze_events
from backend.detection.report import format_report


app = FastAPI(
    title="SYLTHEN",
    description="Ethical spyware simulation and detection framework",
    version="1.0.0",
)


class AnalysisRequest(BaseModel):
    events: list[dict[str, Any]]


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "SYLTHEN",
        "status": "operational",
        "version": "1.0.0",
    }


@app.post("/api/analyze")
def analyze(request: AnalysisRequest) -> dict[str, Any]:
    detection = analyze_events(request.events)
    behavior = analyze_behavior(request.events)

    return {
        "detection": detection,
        "behavior": behavior,
        "report": format_report(detection),
    }