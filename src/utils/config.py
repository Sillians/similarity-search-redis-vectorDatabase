# configuration management
import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    """Base configuration"""

    DEBUG = False
    TESTING = False

    INDEX_NAME = os.getenv('INDEX_NAME')
    DOC_PREFIX = os.getenv('DOC_PREFIX')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    @classmethod
    def init_app(cls, app):
        """Initialize configuration"""
        app.config.from_object(cls)


class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True
    DATAURL = os.getenv('DATAURL')
    DOC_PREFIX = os.getenv('DOC_PREFIX')
    CLIENT_KEYS = os.getenv('CLIENT_KEYS')

    # Redis connection
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 17971))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

    # pre-trained sentence transformer model
    PRETRAINED_TRANSFORMER_MODEL = os.getenv('PRETRAINED_TRANSFORMER_MODEL')

    PROJECT_NAME = os.getenv("PROJECT_NAME")
    VERSION = os.getenv("VERSION")
    DESCRIPTION = os.getenv("DESCRIPTION")

    FASTAPI_HOST = os.getenv("FASTAPI_HOST")
    FASTAPI_PORT = int(os.getenv('FASTAPI_PORT', 8000))
    FASTAPI_WORKERS = int(os.getenv('FASTAPI_WORKERS', 2))
    FASTAPI_APP = os.getenv("FASTAPI_APP")


class TestingConfig(Config):
    """Testing-specific configuration."""
    TESTING = True
    DATABASE_URI_TESTING = os.getenv('TEST_DATABASE_URI', 'redis-example-database-test')
    LOG_LEVEL = 'DEBUG'  # More verbose during testing


class ProductionConfig(Config):
    """Production-specific configuration."""
    DATABASE_URI_PRODUCTION = os.getenv('PROD_DATABASE_URI', 'redis-example-database-prod')
    LOG_LEVEL = 'WARNING'  # Less verbose for production


# To easily switch between configurations
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}


# Select appropriate configuration based on environment
def get_config():
    """Dynamically load the correct configuration based on the environment."""
    env = os.getenv('VSS_ENV', 'development')
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig
