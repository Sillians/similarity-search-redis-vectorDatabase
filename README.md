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


### How can a vector representation be used?

Let’s say you have an image of a building — for example, the city hall of some midsize city whose name you forgot
and you’d like to find all other images of this building in the image collection. 
A key/value query that is typically used in `SQL` doesn’t help, because you’ve forgotten the name of the city.

This is where similarity search kicks in. The vector representation for images is designed to produce similar 
vectors for similar images, where similar vectors are defined as those that are nearby in Euclidean space.


## Overview of the Similarity Search using SentenceTransformer, and Redis as the Vector Database

The core aim of this, is to demonstrate how to do semantic searched on unstructured data using vector similarity and Redis. Vector similarity
search measures how different (or similar) two or more vectors are. It is a technique used to find similar content or data according to 
their representations. Vectors are compared using a distance metric, such as Euclidean distance or cosine similarity. The closer two vectors are,
the more similar they are. 

Approach adopted:
- Generating vector embeddings for text data using SentenceTransformers.
- Storing JSON documents containing text and vector embeddings in Redis Database.
- Creating a RediSearch index on the JSON data.
- Performing semantic searches using vector similarity queries.
- Query types demonstrated:
  - KNN similarity search
  - Hybrid search using filters
  - Range queries

### Dataset 
To implement the Vector Similarity Search, we'll use a subset of the Bikes dataset, a relatively simple synthetic dataset.
The dataset has `11` bicycle records in JSON format, and includes the fields below;

```json
{
  "model": "Hillcraft",
  "brand": "Bicyk",
  "price": 550,
  "type": "Kids Mountain bikes",
  "specs": {
    "material": "carbon",
    "weight": "12"
  },
  "description": "Small and powerful, the Hillcraft is the best ride for the smallest of tikes! The Hillcraft will ship with a coaster brake. A freewheel kit is provided at no cost. ",
}
```
The description field is particularly interesting for our purposes since it consists of a free-form textual description of a bicycle.

### Text Embeddings using SentenceTransformers
We will use the [SentenceTransformers](https://www.sbert.net/) framework to generate embeddings for the bikes descriptions. 
Sentence-BERT `(SBERT)` is a BERT model modification that produces consistent and contextually rich sentence embeddings. 
`SBERT` improves tasks like semantic search and text grouping by allowing for efficient and meaningful comparison of sentence-level semantic similarity.


#### Selecting a suitable pre-trained Model
Our objective is to query for bicycles using short sentences against the longer bicycle descriptions. This is referred to as `"Asymmetric Semantic Search,"` often
employed in cases where the search query and the documents being searched are different nature or structure.

To pick a suitable model based on the task when generating embeddings, suitable models for asymmetric semantic search include pre-trained [MS MARCO Models](https://microsoft.github.io/msmarco/).
MS MARCO models are trained on the MicroSoft MAchine Reading COmprehension dataset, and are optimized for understanding real-world queries and retrieving
relevant responses. They are widely used in search engines, chatbots, and other AI applications. For this project, we'll be using the `msmarco-distilbert-base-v4` model
tuned for `cosine-similarity` available from SentenceTranformers.


### Making the bikes collection searchable
Redis Stack provides a powerful search engine [Redis Search](https://redis.io/docs/stack/search/) that introduces [commands](https://redis.io/docs/stack/search/commands/)
to create and maintain search indices for both collections of HASHES and [JSON](https://redis.io/docs/stack/search/indexing_json/) documents.

To create a search index for the bikes collection, we'll use the `FT.CREATE` command:
```
1️⃣ FT.CREATE idx:bikes_vss ON JSON 
2️⃣  PREFIX 1 bikes: SCORE 1.0 
3️⃣  SCHEMA 
4️⃣    $.model TEXT WEIGHT 1.0 NOSTEM 
5️⃣    $.brand TEXT WEIGHT 1.0 NOSTEM 
6️⃣    $.price NUMERIC 
7️⃣    $.type TAG SEPARATOR "," 
8️⃣    $.description AS description TEXT WEIGHT 1.0 
9️⃣    $.description_embeddings AS vector VECTOR FLAT 6 TYPE FLOAT32 DIM 768 DISTANCE_METRIC COSINE
```

There is a lot to unpack here; let's take it from the top:







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
│   ├── README.md
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
- Sentence Transformer model (sentence_transformers)
- FastAPI
- Kubernetes cluster (Minikube) -> (Optional[😉])
- Setup and Access to a Running Redis Stack instance
- Redis connection configuration credentials (secrets)
- Alternatively run Redis Stack locally using Docker. 


### What happens when code is executed;
Upon code execution, 
- The data is loaded and inspected as a Sample JSON data
- Connection to the Redis Database Stack instance is established.
- Generated vector embeddings for the text descriptions.
- The JSON data is saved with embeddings into Redis.
- Creation of a RediSearch index on the data
- Execute vector similarity search queries


### FastAPI
After following these steps, you should be able to access the Swagger UI by navigating to http://localhost:8001/docs in your browser.

## Key Concepts
The core concepts covered include:

- Using pre-trained NLP models like SentenceTransformers to generate semantic vector representations of text
- Storing and indexing vectors along with structured data in Redis
- Utilizing vector similarity KNN search and other query types in RediSearch
- Ranking and retrieving results by semantic similarity

The techniques presented allow for building powerful semantic search experiences over unstructured data with Redis.

























