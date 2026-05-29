from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.agent import router as agent_router
from app.routers.governance import router as governance_router
from app.routers.intake import router as intake_router
from app.routers.retail import router as retail_router
from app.routers.risk import router as risk_router

app = FastAPI(
    title="Family Dollar AI Governance API",
    version="0.2.0",
    description=(
        "Backend governance API for AI intake, risk tiering, portfolio triage, "
        "and architecture review workflows."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(risk_router, prefix="/v1/risk", tags=["risk"])
app.include_router(intake_router, prefix="/v1/intake", tags=["intake"])
app.include_router(governance_router, prefix="/v1/governance", tags=["governance"])
app.include_router(agent_router, prefix="/v1/agents", tags=["agents"])
app.include_router(retail_router, prefix="/v1/retail", tags=["retail"])


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "family-dollar-ai-governance-api",
        "phase": "2",
    }
