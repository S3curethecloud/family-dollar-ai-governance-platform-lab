from app.core.risk_engine import evaluate_risk
from app.schemas.intake import (
    AutonomousActionLevel,
    BusinessUnit,
    DataSensitivity,
    IntakeRequestCreate,
    IntakeRequestRecord,
    ModelType,
    OperationalImpact,
    RetailSystem,
)

_REQUESTS: list[IntakeRequestRecord] = []


def _next_request_id() -> str:
    return f"FD-AI-{len(_REQUESTS) + 1:03d}"


def create_request(payload: IntakeRequestCreate) -> IntakeRequestRecord:
    evaluation = evaluate_risk(payload)
    record = IntakeRequestRecord(
        request_id=_next_request_id(),
        **payload.model_dump(),
        evaluation=evaluation,
    )
    _REQUESTS.insert(0, record)
    return record


def list_requests() -> list[IntakeRequestRecord]:
    return list(_REQUESTS)


def get_request(request_id: str) -> IntakeRequestRecord | None:
    return next(
        (request for request in _REQUESTS if request.request_id == request_id),
        None,
    )


def seed_demo_data() -> None:
    if _REQUESTS:
        return

    demo_requests = [
        IntakeRequestCreate(
            business_unit=BusinessUnit.store_operations,
            requester="Regional Operations Director",
            use_case="Inventory Replenishment Assistant",
            retail_system=RetailSystem.inventory,
            data_sensitivity=DataSensitivity.internal,
            customer_data=False,
            payment_data=False,
            operational_impact=OperationalImpact.store_level,
            expected_business_value="Reduce stockouts and improve shelf availability.",
            model_type=ModelType.agentic,
            autonomous_action_level=AutonomousActionLevel.recommend_only,
            human_approval_required=True,
            dependencies=[
                "Inventory API",
                "Supply Chain API",
                "Store Manager approval workflow",
            ],
            target_release_window="Q3 pilot",
        ),
        IntakeRequestCreate(
            business_unit=BusinessUnit.customer_support,
            requester="Customer Care Lead",
            use_case="Customer Support Response Assistant",
            retail_system=RetailSystem.crm,
            data_sensitivity=DataSensitivity.pii,
            customer_data=True,
            payment_data=False,
            operational_impact=OperationalImpact.customer_facing,
            expected_business_value=(
                "Improve response time and consistency for support teams."
            ),
            model_type=ModelType.rag,
            autonomous_action_level=AutonomousActionLevel.draft_response,
            human_approval_required=True,
            dependencies=["CRM API", "Identity API", "Prompt approval"],
            target_release_window="Q4 controlled rollout",
        ),
        IntakeRequestCreate(
            business_unit=BusinessUnit.marketing,
            requester="Loyalty Marketing Manager",
            use_case="Personalized Promotion Generator",
            retail_system=RetailSystem.crm,
            data_sensitivity=DataSensitivity.payment,
            customer_data=True,
            payment_data=True,
            operational_impact=OperationalImpact.customer_facing,
            expected_business_value=(
                "Increase promotion relevance and campaign conversion."
            ),
            model_type=ModelType.personalization,
            autonomous_action_level=AutonomousActionLevel.autonomous_action,
            human_approval_required=True,
            dependencies=[
                "CRM API",
                "POS history",
                "Legal review",
                "Executive approval",
            ],
            target_release_window="Blocked pending governance",
        ),
    ]

    for request in demo_requests:
        create_request(request)


seed_demo_data()
