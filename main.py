from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import api_router
from app.core.database import create_tables, test_connection, init_pool
import uvicorn
import os
import logging
import sys
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize connection pool for Azure PostgreSQL 
# Azure recommends min=1, max=10 for most apps
init_pool(minconn=1, maxconn=10)

# Test database connection before creating tables
logger.info("Testing database connection...")
if not test_connection():
    logger.error("Failed to connect to database. Check your connection settings.")
    sys.exit(1)

try:
    # Create database tables
    logger.info("Creating database tables if they don't exist...")
    create_tables()
except Exception as e:
    logger.error(f"Failed to create database tables: {e}")
    sys.exit(1)

app = FastAPI(
    title="PDF Filler Chatbot API",
    description="API for conversational PDF filling using LLMs",
    version="0.1.0",
)

# Add timing middleware to monitor performance
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # Log slower operations (over 1 second)
    if process_time > 1:
        logger.warning(f"Slow response for {request.url.path}: {process_time:.2f}s")
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Set up CORS - Azure recommendation: specify origins in production
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

@app.get("/health", tags=["status"])
async def health_check():
    """Health check endpoint for Azure App Service"""
    db_status = "healthy" if test_connection() else "unhealthy"
    return {
        "status": "ok" if db_status == "healthy" else "error",
        "database": db_status
    }

# if __name__ == "__main__":
#     port = int(os.getenv("PORT", 8080))
#     # Azure App Service specific settings
#     uvicorn.run("main:app", host="0.0.0.0", port=port)