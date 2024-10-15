import uvicorn
from fastapi import FastAPI
from src.app.routes import router
from src.utils.logger import get_logger
from src.utils.config import get_config

logger = get_logger("Semantic Search API")
config = get_config()

app = FastAPI(
    title=config.PROJECT_NAME,
    description=config.DESCRIPTION,
    version=config.VERSION
)

logger.info("Including routes for semantic search application...")
app.include_router(router, prefix="/vss")


@app.get("/health")
def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}

def start_server():
    logger.info("Starting Semantic Search API with Uvicorn Server Programmatically...")

    logger.info("setting up the Uvicorn configuration")
    config_file = uvicorn.Config(
        app=config.FASTAPI_APP,
        host=config.FASTAPI_HOST,
        port=config.FASTAPI_PORT,
        workers=config.FASTAPI_WORKERS
        # reload=True,  # Enable auto-reload (for development)
    )

    logger.info("Creating the server.")
    server = uvicorn.Server(config_file)
    server.run()


if __name__ == "__main__":
    start_server()