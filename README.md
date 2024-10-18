# Similarity Search Using SentenceTransformer, and Redis as the Vector Database. 
(A Modular Vector Similarity Search Approach with Redis as the Vector Database.)

### Overview of Vector Databases
A vector database stores, manages and indexes high-dimensional vector data. 
Data points are stored as arrays of numbers called “vectors,” which are clustered based on similarity. 
This design enables low-latency queries, making it ideal for AI applications.

### Vector databases versus traditional databases
Unlike traditional relational databases with rows and columns, data points in a vector database are represented by vectors with a fixed number of dimensions. 
Because they use high-dimensional vector embeddings, vector databases are better able to handle unstructured datasets.

The nature of data has undergone a profound transformation. It's no longer confined to structured information easily stored in traditional databases.
Unstructured data—including social media posts, images, videos, audio clips and more—is growing 30% to 60% year over year.

Opposed to this, vector search represents data as dense vectors, which are vectors with most or all elements being nonzero. 
Vectors are represented in a continuous vector space, the mathematical space in which data is represented as vectors.

Vector representations enable similarity search. For example, a vector search for “smartphone” might also return results for “cellphone” and “mobile devices.” 
Each dimension of the dense vector corresponds to a latent feature or aspect of the data.
A latent feature is an underlying characteristic or attribute that is not directly observed but inferred from the data through mathematical models or algorithms.

Latent features capture the hidden patterns and relationships in the data, enabling more meaningful and accurate representations of items as vectors in a high-dimensional space.

#### Data represented as vectors in a high-dimensional space (Vector embeddings)
![Alt text](https://lh3.googleusercontent.com/F3cl6UTiYaeyOOx4R4s0ebI3OQCZ9-0uKCcG8VgJ2eLfudEhvrr2tuOynixfiy1GReyxfdAoW0GUvJiO0psv42AwRWkSO5EU5j6NrbgM7uRXQVRBACsL-gI6EkmDPfr-vFzFWRiOAIoR4PTndXNYmpQ "Vector Embeddings")

### How can a vector representation be used?

Let’s say you have an image of a building — for example, the city hall of some midsize city whose name you forgot
and you’d like to find all other images of this building in the image collection. 
A key/value query that is typically used in `SQL` doesn’t help, because you’ve forgotten the name of the city.

This is where similarity search kicks in. The vector representation for images is designed to produce similar 
vectors for similar images, where similar vectors are defined as those that are nearby in Euclidean space.


### Code Structure
```md
similarity-search/
│
├── src/                     # Application source code
│   ├── __init__.py
│   ├── data/
│   ├── models/ 
│   ├── app/
│   ├── pipelines/
│   ├── utils/
│   ├── tests/
│   ├── README.md            # Overview of the Similarity Search using SentenceTransformer, and Redis as the Vector Database
│   └── ...
│
│
├── k8s/                     # Kubernetes configuration files
│   ├── deployment.yml       # Kubernetes Deployment resource
│   ├── service.yml          # Kubernetes Service resource
│   ├── ingress.yml          # (Optional) Ingress configuration
│   └── secrets.yml          # (Optional) Kubernetes Secrets
│
│
├── .github/                 # CI/CD workflows (e.g., GitHub Actions)
│   └── workflows/
│       └── vss-pipeline.yml # CI/CD pipeline script for building and deploying
│
│
├── .env                     # Environment variables file
├── Dockerfile               # Dockerfile to build the app
├── requirements.txt         # Python dependencies
├── README.md                # Documentation
└── LICENSE                  # License file
```


### Environment Setup
Requires a few packages and intial setups for full implementation; 
- Redis (redis-py)
- Sentence Transformer model (sentence_transformers from HuggingFace, easy to use models for tasks like semantic similarity search, visual search, and many others.)
- FastAPI (Search Query in Swagger UI)
- Kubernetes cluster (Minikube) -> (Optional[😉])
- Setup and Access to a Running Redis Stack instance
- Redis connection configuration credentials (secrets)
- Alternatively run Redis Stack locally using Docker. 


### What happens when code is executed;
Upon code execution;
- The data is loaded and inspected as a Sample JSON data
- Connection to the Redis Database Stack instance is established.
- Generated vector embeddings for the text descriptions.
- The JSON data is saved with embeddings into Redis.
- Creation of a RediSearch index on the data
- Execute vector similarity search queries

### A simple implementation using Cosine Similarity as the Distance Metric (For more details, refer to: [Distance Metrics in Vector Similarity Search](/Users/user/Projects/similarity-search-redis-vectorDatabase/VECTOR-SIMILARITY-SEARCH.md))
```python
pip3 install sentence_transformers --quiet
```

```python
import numpy as np
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer

# Define the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# sample data
sentences = [
    "A monkey is playing drums.",
    "A cheetah is running behind its prey.",
    "A man is riding a white horse on an enclosed ground.",
    "A man is eating a piece of bread.",
    "A man is riding a horse.",
    "A woman is playing violin."
]

# vector embeddings created from dataset
embeddings = model.encode(sentences)

# encode the query vector embedding
query_embedding = model.encode("Someone in a gorilla costume is playing a set of drums.")

# Define the distance metric (Cosine similarity)
def cosine_similarity(A, B):
    return np.dot(A, B)/(norm(A)*norm(B))

# Run semantic similarity search
print("Query: Someone in a gorilla costume is playing a set of drums.")
for e, s in zip(embeddings, sentences):
    print(s, " -> similarity score = ",
          cosine_similarity(e, query_embedding))
```

- Code Output: (Semantic similarity score of each data to the provided query)
```md
Query: Someone in a gorilla costume is playing a set of drums.
A monkey is playing drums.  -> similarity score =  0.6432533
A cheetah is running behind its prey.  -> similarity score =  0.107986785
A man is riding a white horse on an enclosed ground.  -> similarity score =  0.11909153
A man is eating a piece of bread.  -> similarity score =  0.021566957
A man is riding a horse.  -> similarity score =  0.13887261
A woman is playing violin.  -> similarity score =  0.25641555
```


## Key Concepts
The core concepts covered include:

- Using pre-trained NLP models like `SentenceTransformers` to generate semantic vector representations of text
- Storing and indexing vectors along with structured data in Redis (vector database)
- Utilizing vector similarity KNN search and other query types in RediSearch
- Ranking and retrieving results by semantic similarity

The techniques presented allow for building powerful semantic search experiences over unstructured data with Redis.

























