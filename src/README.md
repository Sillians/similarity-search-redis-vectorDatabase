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


### Adopted Approach to making the bikes collection searchable
Redis Stack provides a powerful search engine [Redis Search](https://redis.io/docs/stack/search/) that introduces [commands](https://redis.io/docs/stack/search/commands/)
to create and maintain search indices for both collections of `HASHES` and [JSON](https://redis.io/docs/stack/search/indexing_json/) documents.

To create a search index for the bikes collection, we'll use the [FT.CREATE](https://redis.io/docs/latest/commands/ft.create/) command:
```md
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

So, there is a lot to unpack here; let's take it from the top:

- 1️⃣ We start by specifying the name of the index; `idx:bikes` indexing keys of type `JSON`.
- 2️⃣ The keys being indexed are found using the `bikes:` key prefix.
- 3️⃣ The `SCHEMA` keyword marks the beginning of the schema field definitions.
- 4️⃣ Declares that field in the JSON document at the JSONPath `$.model` will be indexed as a `TEXT` field, allowing full-text search queries (disabling stemming).
- 5️⃣ The `$.brand` field will also be treated as a `TEXT` schema field.
- 6️⃣ The `$.price` field will be indexed as a `NUMERIC` allowing numeric range queries.
- 7️⃣ The `$.type` field will be indexed as a `TAG` field. Tag fields allow exact-match queries, and are suitable for categorical values.
- 8️⃣ The `$.description` field will also be indexed as a `TEXT` field.
- 9️⃣ Finally, the vector embeddings in `$.description_embeddings` are indexed as a `VECTOR` field and assigned to the alias `vector`.


Let's break down the `VECTOR` schema field definition to better understand the inner workings of Vector Similarity in Redis:

- `FLAT:` Specifies the indexing method, which can be `FLAT` or `HNSW`. FLAT (brute-force indexing) provides exact results but at a higher computational cost, 
while HNSW (Hierarchical Navigable Small World) is a more efficient method that provides approximate results with lower computational overhead.
- `TYPE:` Set to `FLOAT32`. Current supported types are `FLOAT32` and `FLOAT64`.
- `DIM:` The length or dimension of our embeddings.
- `DISTANCE_METRIC:` One of `L2`, `IP`, `COSINE`.
  - `L2` stands for `"Euclidean distance";` a straight-line distance between the vectors. Preferred when the absolute differences, including magnitude, matter most.
  - `IP` stands for `"Inner Product";` IP measures the projection of one vector onto another. It emphasizes the angle between vectors rather than their absolute positions in the vector space.
  - `COSINE` stands for `"Cosine Similarity";` a normalized form of inner product. This metric measures only the angle between two vectors, making it magnitude-independent.
  
  For our querying purposes, the direction of the vectors carry more meaning (indicating semantic similarity), and the magnitude is largely influenced by the length of the documents, therefore COSINE similarity is chosen. Also, our chosen embedding model is fine-tuned for Cosine Similarity.


### Constructing a "Pure KNN" VSS Query

We are starting with a K-nearest neighbors (KNN) query, `KNN` is a foundational algorithm used in vector similarity search, 
where the goal is to find the most similar items to a given query item. Using the chosen distance metric, the `KNN` algorithm
calculates the distance between the query vector and each vector in the database. It then returns the `K` items with the 
smallest distances to the query vector. These are considered to be the most similar items. 

The syntax for vector similarity `KNN` queries is (*)=>[vector_similarity_query>] where the (*) (the * meaning all) is the filter query for the search engine.
That way, one can reduce the search space by filtering the collection on which the `KNN` algorithm operates.

- The `$query_vector` represents the query parameter we'll use to pass the vectorized query prompt.
- The results will be filtered by `vector_space`, which is a field derived from the name of the field indexed as a Vector by appending `_score` to it,
in our case, vector (the alias for `$.description_embeddings`).
- Our query will return the `vector_score`, the `id` of the match documents, and the `$.brand`, `$.model`, and `$.description`.
- We specified `DIALECT 2` or greater to utilize a vector similarity query with the `FT.SEARCH` command.

```python
query = (
            Query('(*)=>[KNN 3 @vector $query_vector AS vector_score]')
            .sort_by('vector_score')
            .return_fields('vector_score', 'id', 'brand', 'model', 'description')
            .dialect(2)
        )
```

The references below can help you learn more about Redis search capabilities:

- https://redis.io/docs/stack/search/
- https://redis.io/docs/stack/search/indexing_json/























