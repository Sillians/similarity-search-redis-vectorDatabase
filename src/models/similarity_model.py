# Similarity search model abstraction
from sentence_transformers import SentenceTransformer
from src.utils.logger import get_logger
from src.utils.config import get_config

class SimilarityModel:
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger("Pre-trained Sentence Transformer Model")
        self.embedder = None

    def load_model(self):
        try:
            self.embedder = SentenceTransformer(self.config.PRETRAINED_TRANSFORMER_MODEL)
            self.logger.info("Embedding using sentence transformers model")
        except Exception as e:
            self.logger.error(f"Failed to load the sentence transformer model: {e}")
        return self.embedder
