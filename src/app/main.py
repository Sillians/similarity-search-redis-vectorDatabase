import uvicorn
from fastapi import FastAPI
from src.app.routes import router
from src.utils.logger import get_logger
from src.utils.config import get_config

logger = get_logger("Semantic Search API")
config = get_config()

# FastAPI app
app = FastAPI(
    title=config.PROJECT_NAME,
    description=config.DESCRIPTION,
    version=config.VERSION
)

# application routes
logger.info("Including routes for semantic search...")
app.include_router(router, prefix="/vss")


# Health check endpoint
@app.get("/health")
def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}


# server start function
def start_server():
    logger.info("Starting Semantic Search API with Uvicorn Server Programmatically...")

    # Uvicorn configuration
    config_file = uvicorn.Config(
        app="src.app.main:app",  # Point to your FastAPI app
        host="0.0.0.0",  # Bind to all network interfaces
        port=8000,  # Port number
        reload=True,  # Enable auto-reload (for development)
        workers=2,  # Number of worker processes (set based on CPU cores for production)
    )

    # Create server
    server = uvicorn.Server(config_file)
    server.run()


# Entry point for running the server
if __name__ == "__main__":
    start_server()