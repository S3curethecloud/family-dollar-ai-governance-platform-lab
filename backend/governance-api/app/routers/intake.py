from fastapi import APIRouter, HTTPException

from app.core.risk_engine import evaluate_risk
from app.data.store import create_request, get_request, list_requests
from app.schemas.intake import (
    IntakeRequestCreate,
    IntakeRequestListResponse,
    IntakeRequestResponse,
    RiskEvaluation,
)

router = APIRouter()


@router.post("/evaluate", response_model=RiskEvaluation)
def evaluate_intake_request(payload: IntakeRequestCreate) -> RiskEvaluation:
    return evaluate_risk(payload)


@router.post("/requests", response_model=IntakeRequestResponse, status_code=201)
def submit_intake_request(payload: IntakeRequestCreate) -> IntakeRequestResponse:
    record = create_request(payload)
    return IntakeRequestResponse(request=record)


@router.get("/requests", response_model=IntakeRequestListResponse)
def get_intake_requests() -> IntakeRequestListResponse:
    requests = list_requests()
    return IntakeRequestListResponse(requests=requests, count=len(requests))


@router.get("/requests/{request_id}", response_model=IntakeRequestResponse)
def get_intake_request(request_id: str) -> IntakeRequestResponse:
    request = get_request(request_id)

    if request is None:
        raise HTTPException(status_code=404, detail="AI intake request not found.")

    return IntakeRequestResponse(request=request)
