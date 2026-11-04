from backend.app.api.users import router as users_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="DeepTrace AI",
    description=(
        "Multimodal Deepfake Detection "
        "and Digital Media Intelligence Platform"
    ),
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)
app.include_router(users_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/health", tags=["System"])
async def health_check():
    return {
        "service": "DeepTrace AI",
        "status": "operational",
        "version": "1.0.0"
    }
