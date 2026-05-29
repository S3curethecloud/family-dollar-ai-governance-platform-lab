from fastapi import APIRouter

from app.core.observability import (
    build_observability_dashboard,
    evaluate_cost_guardrail,
)
from app.schemas.observability import (
    CostGuardrailRequest,
    CostGuardrailResponse,
    ObservabilityDashboard,
)

router = APIRouter()


@router.get("/dashboard", response_model=ObservabilityDashboard)
def get_observability_dashboard() -> ObservabilityDashboard:
    return build_observability_dashboard()


@router.post("/cost-guardrail", response_model=CostGuardrailResponse)
def cost_guardrail(payload: CostGuardrailRequest) -> CostGuardrailResponse:
    return evaluate_cost_guardrail(payload)
