from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from database import engine, Base
import models
from routers import articles

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AACIE V6 API", version="6.0.0", description="Autonomous Intelligence Enterprise Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(articles.router)

@app.get("/")
def read_root():
    return {"status": "System Nominal", "engine": "AACIE V6", "inference": "Llama-3 70B"}

@app.get("/health")
def health_check():
    return {"status": "ok", "db_connected": True}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
