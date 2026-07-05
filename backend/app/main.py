from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, scout, ai, outreach, crm, copilot, documents
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(scout.router, prefix="/api/v1/scout", tags=["scout"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])
app.include_router(outreach.router, prefix="/api/v1/outreach", tags=["outreach"])
app.include_router(crm.router, prefix="/api/v1/crm", tags=["crm"])
app.include_router(copilot.router, prefix="/api/v1/copilot", tags=["copilot"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
