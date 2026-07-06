from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.api.routes import auth, scout, ai, outreach, crm, copilot, documents, analytics
from app.core.config import settings
from app.database.session import connect_db, disconnect_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url=None,
    openapi_url="/api/v1/openapi.json" if settings.ENVIRONMENT != "production" else None
)

@app.on_event("startup")
async def startup():
    await connect_db()
    logger.info("Connected to MongoDB")

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()
    logger.info("Disconnected from MongoDB")

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response



app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(scout.router, prefix="/api/v1/scout", tags=["scout"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])
app.include_router(outreach.router, prefix="/api/v1/outreach", tags=["outreach"])
app.include_router(crm.router, prefix="/api/v1/crm", tags=["crm"])
app.include_router(copilot.router, prefix="/api/v1/copilot", tags=["copilot"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "database": "mongodb"}
