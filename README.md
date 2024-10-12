# Similarity Search Using Redis as the Vector Database. 
(A Modular Vector Similarity Search with Redis as a Vector Database.)

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





























