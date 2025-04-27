from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import api_router
import uvicorn
import os

app = FastAPI(
    title="PDF Filler Chatbot API",
    description="API for conversational PDF filling using LLMs",
    version="0.1.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")


@app.get("/", tags=["status"])
async def root():
    return {"status": "ok", "message": "PDF Filler Chatbot API is running"}


# if __name__ == "__main__":
#     uvicorn.run("main:app", port=8080, reload=True)
