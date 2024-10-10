"""
Characteristics of Cross Encoder (a.k.a reranker) models:

- Calculates a similarity score given pairs of texts.
- Generally provides superior performance compared to a Sentence Transformer (a.k.a. bi-encoder) model.
- Often slower than a Sentence Transformer model, as it requires computation for each pair rather than each text.
- Due to the previous 2 characteristics, Cross Encoders are often used to re-rank the top-k results from a Sentence Transformer model.
"""
import numpy as np
from typing import Optional, List, Any
from sentence_transformers.cross_encoder import (CrossEncoder)


class CrossEncoderEmbeddingSimilarities:
    def __init__(self, query: str = None, corpus: Optional[List] = None) -> None:
        self._query = query
        self._corpus = corpus

    def model(self):
        # Load a pretrained CrossEncoder model
        model = CrossEncoder("cross-encoder/stsb-distilroberta-base")
        return model

    def rank_corpus(self) -> int:
        # We rank all sentences in the corpus for the query
        ranks = self.model().rank(self._query, self._corpus)
        return ranks

    def get_scores(self) -> Any:
        print("Query: ", self._query)
        for rank in self.rank_corpus():
            print(f"{rank['score']:.2f}\t{self._corpus[rank['corpus_id']]}")


    def get_scores_two_corpus(self):
        # Alternatively, you can also manually compute the score between two sentences
        sentence_combinations: List = [[self._query, sentence] for sentence in self._corpus]
        scores = self.model().predict(sentence_combinations)

        # Sort the scores in decreasing order to get the corpus indices
        ranked_indices: Any = np.argsort(scores)[::-1]
        print("Scores:", scores)
        print("Indices:", ranked_indices)



if __name__ == "__main__":

    # We want to compute the similarity between the query sentence...
    query = "A man is eating pasta."

    # ... and all sentences in the corpus
    corpus = [
        "A man is eating food.",
        "A man is eating a piece of bread.",
        "A man that loves pasta, thinks it is jam-packed with feelings, infused with meaning.",
        "The girl is carrying a baby.",
        "A man is riding a horse.",
        "A woman is playing violin.",
        "Two men pushed carts through the woods.",
        "A man is riding a white horse on an enclosed ground.",
        "A monkey is playing drums.",
        "A cheetah is running behind its prey.",
    ]

    similarities = CrossEncoderEmbeddingSimilarities(query, corpus)
    similarities.get_scores()
    similarities.get_scores_two_corpus()