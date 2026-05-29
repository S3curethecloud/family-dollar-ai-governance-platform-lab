from app.core.risk_engine import evaluate_risk
from app.schemas.intake import (
    AutonomousActionLevel,
    BusinessUnit,
    DataSensitivity,
    IntakeRequestCreate,
    ModelType,
    OperationalImpact,
    RetailSystem,
    RiskTier,
)


def make_request(**overrides):
    base = {
        "business_unit": BusinessUnit.store_operations,
        "requester": "Test Requester",
        "use_case": "Inventory Replenishment Assistant",
        "retail_system": RetailSystem.inventory,
        "data_sensitivity": DataSensitivity.internal,
        "customer_data": False,
        "payment_data": False,
        "operational_impact": OperationalImpact.store_level,
        "expected_business_value": "Reduce stockouts and improve shelf availability.",
        "model_type": ModelType.agentic,
        "autonomous_action_level": AutonomousActionLevel.recommend_only,
        "human_approval_required": True,
        "dependencies": ["Inventory API", "Supply Chain API"],
        "target_release_window": "Q3 pilot",
    }
    base.update(overrides)
    return IntakeRequestCreate(**base)


def test_internal_recommendation_is_moderate_risk():
    result = evaluate_risk(make_request())

    assert result.risk_tier == RiskTier.tier_2
    assert result.human_approval_required is True
    assert "Architecture Review" in result.required_reviews


def test_customer_data_drives_high_risk_review():
    result = evaluate_risk(
        make_request(
            data_sensitivity=DataSensitivity.pii,
            customer_data=True,
            operational_impact=OperationalImpact.customer_facing,
            autonomous_action_level=AutonomousActionLevel.draft_response,
        )
    )

    assert result.risk_tier == RiskTier.tier_3
    assert "Privacy Review" in result.required_reviews
    assert "Security Review" in result.required_reviews


def test_payment_data_is_restricted():
    result = evaluate_risk(
        make_request(
            data_sensitivity=DataSensitivity.payment,
            customer_data=True,
            payment_data=True,
        )
    )

    assert result.risk_tier == RiskTier.tier_4
    assert "Executive Review" in result.required_reviews
    assert result.blocked_reasons


def test_autonomous_action_is_restricted():
    result = evaluate_risk(
        make_request(
            autonomous_action_level=AutonomousActionLevel.autonomous_action,
        )
    )

    assert result.risk_tier == RiskTier.tier_4
    assert "AI Governance Forum" in result.required_reviews
    assert result.blocked_reasons
