from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
from app.core.config import settings
from app.api.routes import auth, stations, payments, sessions, user

app = FastAPI(
    title="EV Charging Platform API",
    description="Unified aggregator platform for EV charging and payments",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An error occurred"
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "ev-charging-api"
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "EV Charging Platform API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(stations.router, prefix="/api/stations", tags=["Stations"])
app.include_router(payments.router, prefix="/api/payments", tags=["Payments"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["Sessions"])
app.include_router(user.router, prefix="/api/user", tags=["User"])

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("🚀 Starting EV Charging Platform API...")
    print(f"📝 API Documentation: http://localhost:8000/api/docs")
    
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 Shutting down EV Charging Platform API...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
