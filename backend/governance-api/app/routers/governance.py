from fastapi import APIRouter

from app.data.store import list_requests
from app.schemas.intake import GovernanceDashboard, RiskTier

router = APIRouter()


@router.get("/dashboard", response_model=GovernanceDashboard)
def governance_dashboard() -> GovernanceDashboard:
    requests = list_requests()

    tier_1 = sum(
        1 for request in requests if request.evaluation.risk_tier == RiskTier.tier_1
    )
    tier_2 = sum(
        1 for request in requests if request.evaluation.risk_tier == RiskTier.tier_2
    )
    tier_3 = sum(
        1 for request in requests if request.evaluation.risk_tier == RiskTier.tier_3
    )
    tier_4 = sum(
        1 for request in requests if request.evaluation.risk_tier == RiskTier.tier_4
    )

    high_risk = tier_3 + tier_4
    human_approval = sum(
        1 for request in requests if request.evaluation.human_approval_required
    )
    blocked_dependencies = sum(
        len(request.evaluation.blocked_reasons) for request in requests
    )

    if tier_4 > 0:
        posture = "Restricted requests present: executive review required before release."
    elif tier_3 > 0:
        posture = "High-risk requests present: governance forum review required."
    elif tier_2 > 0:
        posture = (
            "Moderate-risk portfolio: architecture review and controlled prototype path."
        )
    else:
        posture = "Low-risk portfolio: standard controls are sufficient."

    return GovernanceDashboard(
        total_requests=len(requests),
        tier_1_requests=tier_1,
        tier_2_requests=tier_2,
        tier_3_requests=tier_3,
        tier_4_requests=tier_4,
        high_risk_requests=high_risk,
        restricted_requests=tier_4,
        requests_requiring_human_approval=human_approval,
        blocked_dependency_count=blocked_dependencies,
        portfolio_risk_posture=posture,
    )
