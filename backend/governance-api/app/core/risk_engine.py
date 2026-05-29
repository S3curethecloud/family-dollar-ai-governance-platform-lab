from app.schemas.intake import (
    AutonomousActionLevel,
    DataSensitivity,
    GovernanceStatus,
    IntakeRequestCreate,
    OperationalImpact,
    RiskEvaluation,
    RiskTier,
)


SENSITIVITY_SCORE = {
    DataSensitivity.public: 0,
    DataSensitivity.internal: 1,
    DataSensitivity.confidential: 2,
    DataSensitivity.pii: 3,
    DataSensitivity.payment: 5,
}

AUTONOMY_SCORE = {
    AutonomousActionLevel.summarize_only: 0,
    AutonomousActionLevel.recommend_only: 1,
    AutonomousActionLevel.draft_response: 2,
    AutonomousActionLevel.autonomous_action: 5,
}

IMPACT_SCORE = {
    OperationalImpact.internal_productivity: 0,
    OperationalImpact.back_office: 1,
    OperationalImpact.store_level: 2,
    OperationalImpact.customer_facing: 3,
    OperationalImpact.supply_chain: 3,
    OperationalImpact.enterprise_critical: 4,
}


def evaluate_risk(request: IntakeRequestCreate) -> RiskEvaluation:
    score = 0
    rationale: list[str] = []
    required_reviews: list[str] = ["Architecture Review"]
    blocked_reasons: list[str] = []

    sensitivity_score = SENSITIVITY_SCORE[request.data_sensitivity]
    autonomy_score = AUTONOMY_SCORE[request.autonomous_action_level]
    impact_score = IMPACT_SCORE[request.operational_impact]

    score += sensitivity_score
    score += autonomy_score
    score += impact_score

    rationale.append(f"Data sensitivity adds {sensitivity_score} risk points.")
    rationale.append(f"Autonomy level adds {autonomy_score} risk points.")
    rationale.append(f"Operational impact adds {impact_score} risk points.")

    if request.customer_data:
        score += 2
        required_reviews.extend(["Privacy Review", "Security Review"])
        rationale.append(
            "Customer data adds 2 risk points and requires privacy/security review."
        )

    if request.payment_data:
        score += 5
        required_reviews.extend(["PCI Review", "Executive Review"])
        blocked_reasons.append("Payment data requires restricted governance review.")
        rationale.append(
            "Payment data adds 5 risk points and restricts delivery until executive review."
        )

    if request.autonomous_action_level == AutonomousActionLevel.autonomous_action:
        required_reviews.extend(["AI Governance Forum", "Executive Review"])
        blocked_reasons.append("Autonomous action is not allowed without explicit approval.")
        rationale.append("Autonomous action requires executive approval and policy gating.")

    dependency_count = len(request.dependencies)

    if dependency_count >= 3:
        score += 2
        rationale.append("Three or more dependencies add 2 risk points.")
    elif dependency_count == 2:
        score += 1
        rationale.append("Two dependencies add 1 risk point.")

    if request.operational_impact in {
        OperationalImpact.supply_chain,
        OperationalImpact.enterprise_critical,
    }:
        required_reviews.append("Operational Resilience Review")

    if request.data_sensitivity in {
        DataSensitivity.confidential,
        DataSensitivity.pii,
        DataSensitivity.payment,
    }:
        required_reviews.append("Data Governance Review")

    if request.payment_data or request.autonomous_action_level == AutonomousActionLevel.autonomous_action:
        tier = RiskTier.tier_4
    elif score >= 8:
        tier = RiskTier.tier_3
    elif score >= 4:
        tier = RiskTier.tier_2
    else:
        tier = RiskTier.tier_1

    if tier == RiskTier.tier_4:
        status = GovernanceStatus.restricted_review
        owner_team = "AI Governance Forum"
        next_step = (
            "Hold delivery until executive, security, privacy, and architecture "
            "reviews are completed."
        )
    elif tier == RiskTier.tier_3:
        status = GovernanceStatus.governance_review
        owner_team = "AI Platform + Security + Retail Systems"
        next_step = (
            "Schedule governance forum review and define controls before prototype approval."
        )
    elif tier == RiskTier.tier_2:
        status = GovernanceStatus.architecture_review
        owner_team = "AI Platform + Retail Systems"
        next_step = "Proceed to architecture review and controlled prototype planning."
    else:
        status = GovernanceStatus.approved_for_prototype
        owner_team = "AI Platform"
        next_step = (
            "Proceed to lightweight prototype with standard logging and human oversight."
        )

    human_approval_required = (
        request.human_approval_required
        or tier in {RiskTier.tier_3, RiskTier.tier_4}
        or request.customer_data
        or request.payment_data
    )

    return RiskEvaluation(
        risk_tier=tier,
        risk_score=score,
        human_approval_required=human_approval_required,
        governance_status=status,
        owner_team=owner_team,
        required_reviews=sorted(set(required_reviews)),
        blocked_reasons=blocked_reasons,
        risk_rationale=rationale,
        recommended_next_step=next_step,
    )
