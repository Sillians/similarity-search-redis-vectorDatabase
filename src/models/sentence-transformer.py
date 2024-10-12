"""
Sentence Transformers (a.k.a. SBERT) is the go-to Python module for accessing, using, and training state-of-the-art text and image embedding models.
It can be used to compute embeddings using Sentence Transformer models or to calculate similarity scores using Cross-Encoder models.
This unlocks a wide range of applications, including semantic search, semantic textual similarity, and paraphrase mining.


"""
from typing import Optional, List
from sentence_transformers import SentenceTransformer

class EmbeddingSimilarities:
    def __init__(self, corpus: Optional[List] = None) -> None:
        self._corpus = corpus

    def _model(self) -> None:
        # Load a pretrained Sentence Transformer model
        model = SentenceTransformer("all-MiniLM-L6-v2")
        return model

    def calculate_embeddings(self) -> List:
        # Calculate embeddings by calling model.encode()
        embeddings = self._model().encode(self._corpus)
        return embeddings

    def calculate_similarities(self) -> List:
        # Calculate the embedding similarities
        similarities = self._model().similarity(self.calculate_embeddings(), self.calculate_embeddings())
        return similarities

if __name__ == "__main__":
    # The sentences to encode
    sentences = [
        "Allow client to close connection and re-connect.",
        "Use the protocol handler to implement an append-only command log",
        "Sentence Transformers (a.k.a. SBERT) is the go-to Python module for accessing, using, and training state-of-the-art text and image embedding models.",
        "Sentence Transformers was created by UKPLab and is being maintained by 🤗 Hugging Face."
    ]
    similarities = EmbeddingSimilarities(corpus=sentences)
    print(similarities.calculate_similarities())


"""
With `SentenceTransformer("all-MiniLM-L6-v2")` we pick which Sentence Transformer model we load. 
In the example above, we load `all-MiniLM-L6-v2`, which is a `MiniLM` model finetuned on a large dataset of over 1 billion training pairs. 
Using `SentenceTransformer.similarity()`, we compute the similarity between all pairs of sentences. 

As expected, the similarity between the last two sentences (0.5180) is higher than the similarity between the first two sentences (0.1530) 
or the second and the third sentence (0.0637).
"""