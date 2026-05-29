from fastapi import APIRouter

from app.core.policy_gates import (
    evaluate_action_gate,
    evaluate_deployment_gate,
    evaluate_environment_promotion,
    evaluate_human_approval,
    evaluate_prompt_approval,
    list_policy_gates,
)
from app.schemas.policy import (
    ActionGateRequest,
    DeploymentGateRequest,
    EnvironmentPromotionRequest,
    HumanApprovalRequest,
    PolicyDecisionResponse,
    PolicyGateListResponse,
    PromptApprovalRequest,
)

router = APIRouter()


@router.get("/gates", response_model=PolicyGateListResponse)
def get_policy_gates() -> PolicyGateListResponse:
    gates = list_policy_gates()
    return PolicyGateListResponse(gates=gates, count=len(gates))


@router.post("/prompt-approval", response_model=PolicyDecisionResponse)
def prompt_approval_gate(payload: PromptApprovalRequest) -> PolicyDecisionResponse:
    return evaluate_prompt_approval(payload)


@router.post("/deployment-gate", response_model=PolicyDecisionResponse)
def deployment_gate(payload: DeploymentGateRequest) -> PolicyDecisionResponse:
    return evaluate_deployment_gate(payload)


@router.post("/action-gate", response_model=PolicyDecisionResponse)
def action_gate(payload: ActionGateRequest) -> PolicyDecisionResponse:
    return evaluate_action_gate(payload)


@router.post("/environment-promotion", response_model=PolicyDecisionResponse)
def environment_promotion_gate(
    payload: EnvironmentPromotionRequest,
) -> PolicyDecisionResponse:
    return evaluate_environment_promotion(payload)


@router.post("/human-approval", response_model=PolicyDecisionResponse)
def human_approval_gate(payload: HumanApprovalRequest) -> PolicyDecisionResponse:
    return evaluate_human_approval(payload)
