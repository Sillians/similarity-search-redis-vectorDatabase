# Similarity search model abstraction
from sentence_transformers import SentenceTransformer
from src.utils.logger import get_logger
from src.utils.config import get_config

config = get_config()
logger = get_logger("Get the Pre-trained Sentence Transformer Model")

def model():
    try:
        embedder = SentenceTransformer(config.PRETRAINED_TRANSFORMER_MODEL)
        logger.info("embedding using sentence transformers model")
        return embedder
    except Exception as e:
        logger.error(f"Failed to get the embedded sentence transfomer model {e}")

