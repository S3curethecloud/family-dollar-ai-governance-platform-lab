from fastapi import APIRouter

from app.schemas.intake import RiskTier, RiskTierDefinition

router = APIRouter()


@router.get("/tiers", response_model=list[RiskTierDefinition])
def risk_tier_definitions() -> list[RiskTierDefinition]:
    return [
        RiskTierDefinition(
            tier=RiskTier.tier_1,
            label="Low Risk",
            description=(
                "Internal productivity or summarization use case with limited "
                "sensitivity and no operational execution."
            ),
            examples=["Internal policy summarizer", "Meeting notes assistant"],
            required_controls=["Standard logging", "Prompt versioning"],
        ),
        RiskTierDefinition(
            tier=RiskTier.tier_2,
            label="Moderate Risk",
            description=(
                "Business workflow support that touches internal systems or "
                "operational processes but keeps human approval."
            ),
            examples=[
                "Inventory replenishment recommendation",
                "Invoice exception summarizer",
            ],
            required_controls=[
                "Architecture review",
                "Human approval",
                "Dependency mapping",
            ],
        ),
        RiskTierDefinition(
            tier=RiskTier.tier_3,
            label="High Risk",
            description=(
                "Customer data, sensitive output, or customer-facing workflow "
                "requiring governance review."
            ),
            examples=[
                "Customer support response assistant",
                "CRM knowledge assistant",
            ],
            required_controls=[
                "Governance forum review",
                "Privacy review",
                "Security review",
                "Data governance review",
            ],
        ),
        RiskTierDefinition(
            tier=RiskTier.tier_4,
            label="Restricted / Executive Review",
            description=(
                "Payment data, autonomous action, regulated impact, or "
                "enterprise-critical operations."
            ),
            examples=[
                "Autonomous promotion execution",
                "Payment dispute automation",
            ],
            required_controls=[
                "Executive approval",
                "Security review",
                "Privacy review",
                "Rollback plan",
                "Release gate",
            ],
        ),
    ]
