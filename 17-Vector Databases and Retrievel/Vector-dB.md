Absolutely. Since you're learning **Agentic AI step-by-step**, treat Level 20 as a core foundation for **RAG, agents, memory, and tool-using systems**.

The most important thing is **not memorizing FAISS/Chroma/Pinecone APIs**. You need to understand what a vector database is doing underneath and why an agentic system needs it.

# 🚀 LEVEL 20 — VECTOR DATABASES

## 0. First: Where are we in your Agentic AI journey?

You've already covered:

* Chunking
* Embeddings
* ReAct / agent concepts
* Memory
* RAG fundamentals

Now we're connecting them:

```text
                DOCUMENTS
                    ↓
                 Chunking
                    ↓
                Embeddings
                    ↓
             Vector Database
                    ↓
            Similarity Search
                    ↓
              Top-K Results
                    ↓
           Relevant Context
                    ↓
                  LLM
                    ↓
               Final Answer
```

This is the backbone of many **RAG systems**.

---

# 1. What is a Vector Database?

Let's start with the interview-friendly definition.

> **A vector database is a database designed to store, index, and efficiently search high-dimensional vectors, usually embeddings, based on similarity.**

Suppose we have:

```text
Document 1:
"How can I reset my password?"

Document 2:
"How do I change my account password?"

Document 3:
"How do I update my profile picture?"
```

We convert them into embeddings:

```text
Document 1 → [0.12, -0.42, 0.77, ...]
Document 2 → [0.15, -0.40, 0.74, ...]
Document 3 → [-0.81, 0.21, 0.11, ...]
```

The first two vectors should be close because their meanings are similar.

A vector DB stores these vectors and allows us to ask:

```text
"What documents are most similar to:
'I forgot my password'?"
```

It finds:

```text
Document 1
Document 2
```

---

# 2. Why do we need a Vector Database?

This is a **very important interview question**.

You might ask:

> "Why can't I just store embeddings in a normal SQL database?"

Technically, you can store vectors in some databases.

But traditional databases are primarily designed for queries like:

```sql
SELECT * FROM users
WHERE age > 25;
```

That's fundamentally different from:

> "Find the 10 vectors most similar to this 1536-dimensional vector."

Vector databases are optimized for this type of search.

---

# 3. Normal Database vs Vector Database

Imagine:

```text
Traditional DB

ID | Name    | Age
---|---------|----
1  | Alice   | 25
2  | Bob     | 30
3  | Charlie | 27
```

You query:

```sql
WHERE age > 26
```

That's exact/structured filtering.

Vector DB:

```text
ID | Vector
---|-------------------------
1  | [0.12, -0.44, ...]
2  | [0.15, -0.41, ...]
3  | [-0.71, 0.22, ...]
```

You query:

```text
Find vectors most similar to:

[0.13, -0.43, ...]
```

That's **similarity search**.

---

# 4. The complete RAG pipeline

This is something you should be able to explain on a whiteboard.

Suppose you're building a chatbot for company documentation.

Your documents:

```text
employee_handbook.pdf
company_policies.pdf
leave_policy.pdf
insurance_policy.pdf
```

## Step 1 — Load documents

```text
PDF
 ↓
Text
```

---

## Step 2 — Chunk documents

Suppose:

```text
10,000 words
```

We split them:

```text
Chunk 1
Chunk 2
Chunk 3
...
Chunk 100
```

---

## Step 3 — Create embeddings

Each chunk goes through an embedding model.

```text
Chunk 1
   ↓
Embedding Model
   ↓
[0.12, -0.43, 0.71, ...]
```

---

## Step 4 — Store vectors

We store:

```text
Vector
+
Original text
+
Metadata
```

For example:

```json
{
  "vector": [0.12, -0.43, 0.71],
  "text": "Employees receive 20 days of annual leave...",
  "metadata": {
    "source": "leave_policy.pdf",
    "page": 4,
    "department": "HR"
  }
}
```

---

# 5. Query time

User asks:

> "How many annual leave days do employees get?"

We embed the query:

```text
"How many annual leave days do employees get?"
                 ↓
          Embedding Model
                 ↓
       [0.11, -0.40, 0.73, ...]
```

Then:

```text
Query vector
     ↓
Vector DB
     ↓
Similarity search
     ↓
Top-K chunks
```

Maybe:

```text
Chunk 47 → similarity 0.92
Chunk 12 → similarity 0.87
Chunk 81 → similarity 0.82
```

Those chunks are passed to the LLM.

```text
Relevant chunks
      +
User question
      ↓
     LLM
      ↓
Answer
```

---

# 6. Vector

A **vector** is simply an ordered collection of numbers.

Example:

```python
vector = [0.12, -0.42, 0.77, 0.31]
```

Real embeddings are much larger.

For example:

```text
384 dimensions
768 dimensions
1024 dimensions
1536 dimensions
3072 dimensions
```

depending on the embedding model.

Think:

```text
Text
 ↓
Embedding model
 ↓
Vector
```

The vector represents semantic information in numerical form.

---

# 7. Embedding dimension

Suppose an embedding model produces:

```python
[0.12, -0.42, 0.77, 0.31]
```

This vector has:

```text
4 dimensions
```

If:

```python
[0.1, 0.2, 0.3, ..., 0.9]
```

contains 1536 numbers:

```text
dimension = 1536
```

### Important interview point

The vector database index must generally be configured for the **same dimensionality** as the vectors you're inserting.

For example:

```text
Embedding model → 768 dimensions
```

Your vector collection/index needs:

```text
dimension = 768
```

You can't arbitrarily put a 1536-dimensional vector into a 768-dimensional index.

---

# 8. Similarity Search

This is the heart of vector databases.

We want to answer:

> "Which vectors are closest to my query vector?"

There are several similarity/distance metrics.

The important ones:

1. Cosine similarity
2. Euclidean distance
3. Dot product

---

# 9. Cosine Similarity ⭐⭐⭐

You learned cosine similarity in the previous Embeddings level.

The formula:

$$
\cos(\theta)=\frac{A\cdot B}{||A||||B||}
$$

The basic intuition:

```text
Same direction
     ↓
High similarity
```

Example:

```text
A = [1, 0]
B = [0.9, 0.1]
```

They're pointing almost in the same direction.

Therefore:

```text
similarity ≈ 1
```

But:

```text
A = [1, 0]
B = [-1, 0]
```

They point in opposite directions.

```text
similarity = -1
```

---

# 10. Euclidean Distance

Another approach is measuring physical distance.

```text
A ●
   \
    \
     ● B
```

Smaller distance means:

```text
More similar
```

Formula:

$$
d(A,B)=\sqrt{\sum_i(A_i-B_i)^2}
$$

So:

```text
Euclidean distance ↓
        =
similarity ↑
```

---

# 11. Dot Product

Another common metric:

$$
A \cdot B = \sum_i A_iB_i
$$

For example:

```python
A = [1, 2]
B = [3, 4]

dot_product = 1*3 + 2*4
             = 11
```

Higher dot product generally means greater alignment, depending on how vectors are normalized and how the index is configured.

---

# 12. Very Important: Similarity vs Distance

Different systems can expose different scoring conventions.

For example:

```text
Cosine similarity:
higher = more similar

Euclidean distance:
lower = more similar
```

This sounds trivial, but it causes bugs in real RAG systems.

### Interview question

> "What similarity metrics do vector databases use?"

Answer:

> Common metrics include cosine similarity, Euclidean/L2 distance, and dot product. The appropriate metric depends on the embedding model and how the vectors are normalized.

---

# 13. What is an Index?

This is one of the **most important concepts**.

Suppose your database contains:

```text
10 vectors
```

You can compare your query against all 10.

No big deal.

But suppose:

```text
10 million vectors
```

And each vector has:

```text
1536 dimensions
```

Brute-force comparison can become expensive.

So vector databases use **indexes** to make nearest-neighbor search much faster.

Think:

```text
Without index

Query
 ↓
Compare against vector 1
Compare against vector 2
Compare against vector 3
...
Compare against 10 million
```

Versus:

```text
With index

Query
 ↓
Index
 ↓
Likely nearest candidates
 ↓
Top results
```

---

# 14. Exact vs Approximate Search

Another **must-know interview concept**.

## Exact nearest neighbor

Compare the query against every vector.

```text
Query
 ↓
ALL vectors
 ↓
Find actual nearest vectors
```

Advantages:

```text
Very accurate
```

Disadvantages:

```text
Can be expensive/slow at large scale
```

---

## Approximate Nearest Neighbor — ANN ⭐⭐⭐

Instead of checking every vector, use an index to quickly find **very likely nearest neighbors**.

```text
Query
 ↓
ANN Index
 ↓
Candidate vectors
 ↓
Nearest results
```

It's called **approximate** because the search trades a small amount of exactness for a large improvement in speed.

This is fundamental to scalable vector search.

---

# 15. ANN — interview explanation

If an interviewer asks:

> "What is ANN?"

Say:

> **Approximate Nearest Neighbor search is a technique for efficiently finding vectors that are very close to a query vector without exhaustively comparing the query against every vector. It trades some recall for significantly better search performance.**

Excellent answer.

---

# 16. Common ANN Index Algorithms

You don't need to implement these from scratch, but you should recognize them.

### HNSW

Hierarchical Navigable Small World graphs.

Very important.

```text
Layer 2
      A -------- D
     /            \
    B              E

Layer 1
A ---- B ---- C ---- D ---- E
```

The structure allows you to navigate toward nearby vectors efficiently.

Commonly used in:

* Qdrant
* Weaviate
* Milvus
* pgvector
* other vector search systems

---

# 17. IVF

IVF = **Inverted File Index**

Basic idea:

```text
Millions of vectors
       ↓
Group into clusters
       ↓
Cluster 1
Cluster 2
Cluster 3
...
```

Query:

```text
Query
 ↓
Find relevant clusters
 ↓
Search only those clusters
```

Instead of searching everything.

---

# 18. Product Quantization

You'll sometimes hear:

```text
PQ
Product Quantization
```

It compresses vectors to reduce memory/storage requirements and can accelerate search, potentially at the cost of some accuracy.

You don't need deep mathematical knowledge for most Agentic AI interviews.

Know:

```text
HNSW
IVF
PQ
```

and understand the general purpose.

---

# 19. Top-K

This is extremely important in RAG.

Suppose:

```text
100,000 documents
```

User asks:

> "What's our vacation policy?"

The vector DB might return:

```text
Top 5
```

Meaning:

```text
K = 5
```

Results:

```text
1 → 0.94
2 → 0.91
3 → 0.87
4 → 0.82
5 → 0.79
```

Those are the five most relevant candidates according to the configured search.

---

# 20. Why Top-K matters

Imagine:

```text
K = 1
```

You might miss useful context.

```text
K = 100
```

You may give the LLM too much irrelevant context.

So:

```text
Too small K
→ insufficient context

Too large K
→ noisy context
→ more tokens
→ potentially worse answer
```

This is a retrieval tuning problem.

---

# 21. Metadata

This is another concept you **must understand**.

A vector isn't just:

```python
[0.12, -0.42, ...]
```

Usually you also store metadata.

Example:

```json
{
  "text": "Employees get 20 days of annual leave.",
  "metadata": {
    "source": "leave_policy.pdf",
    "page": 4,
    "department": "HR",
    "year": 2026
  }
}
```

Metadata helps you identify and filter documents.

---

# 22. Why metadata is important in RAG

Suppose your company has:

```text
HR documents
Finance documents
Engineering documents
Legal documents
```

User asks:

> "What is the engineering on-call policy?"

Instead of searching everything:

```text
ALL DOCUMENTS
```

you can filter:

```text
department = "engineering"
```

Then perform semantic search.

Conceptually:

```text
Query
 ↓
Metadata Filter
 ↓
Candidate documents
 ↓
Similarity Search
 ↓
Top-K
```

---

# 23. Metadata Filtering ⭐⭐⭐

This is frequently asked.

Suppose:

```json
metadata = {
    "department": "engineering",
    "year": 2026
}
```

You could search:

```text
department = engineering
AND
year = 2026
```

while also searching semantically.

This is different from semantic similarity.

### Metadata filter

```text
Exact/structured condition
```

### Vector similarity

```text
Semantic relationship
```

Together they are powerful.

---

# 24. Example

Suppose you have:

```text
Document A
department = HR

Document B
department = Engineering

Document C
department = Engineering
```

Query:

> "How does the on-call process work?"

Filter:

```text
department = Engineering
```

Now:

```text
A ❌
B ✓
C ✓
```

Then vector similarity ranks B and C.

---

# 25. The complete retrieval process

Now put everything together:

```text
                  USER QUERY
                      ↓
               Query Embedding
                      ↓
              [0.12, -0.43, ...]
                      ↓
              Metadata Filter
                      ↓
             Candidate Vectors
                      ↓
             ANN / Vector Index
                      ↓
             Similarity Search
                      ↓
                  Ranking
                      ↓
                  Top-K
                      ↓
             Relevant Chunks
                      ↓
                    LLM
                      ↓
                  Answer
```

This diagram is worth memorizing.

---

# 26. Vector DB vs Embedding Model

This distinction is **very important**.

An embedding model:

```text
Text → Vector
```

A vector database:

```text
Vector → Store + Index + Search
```

Therefore:

```text
Embedding Model ≠ Vector Database
```

Example:

```text
"Reset my password"
        ↓
Embedding Model
        ↓
[0.12, -0.43, 0.77, ...]
        ↓
Vector DB
        ↓
Find similar vectors
```

---

# 27. Vector DB vs LLM

Another common interview question.

### LLM

Understands/generates language:

```text
Question
 ↓
LLM
 ↓
Answer
```

### Vector DB

Retrieves relevant information:

```text
Query vector
 ↓
Vector DB
 ↓
Relevant documents
```

The vector DB doesn't replace the LLM.

They work together.

---

# 28. Let's build a tiny vector search ourselves

Before using a real database, understand the mechanics.

We'll use Python.

```python
import numpy as np

documents = [
    "How to reset my password",
    "How to change my email address",
    "How to update my profile",
]

vectors = np.array([
    [0.90, 0.10, 0.20],
    [0.20, 0.80, 0.10],
    [0.10, 0.20, 0.90]
])

query = np.array([0.85, 0.15, 0.20])
```

Now calculate cosine similarity.

```python
def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )
```

Search:

```python
scores = []

for i, vector in enumerate(vectors):
    score = cosine_similarity(query, vector)
    scores.append((documents[i], score))

scores.sort(key=lambda x: x[1], reverse=True)

for doc, score in scores:
    print(score, doc)
```

Conceptually:

```text
0.99 → How to reset my password
0.40 → How to change my email address
0.30 → How to update my profile
```

That's essentially the basic idea behind vector search.

Real vector databases make this scalable and much more sophisticated.

---

# 29. FAISS ⭐⭐⭐

![Image](https://images.openai.com/static-rsc-4/1e2NusC3WKvjVPgx8-F118MBpahMEOHiN6Aj39D0LdfsGYeuNY0U-VmqT_VeJBLhvK45lLTCo0KGkq8kJIHKfkhmzRYP5oiQKLBHXU82msm_aSRgvt5PPBvsvX71_YhKlD3x_M3kznX9QhEVelos3Kl7U4Exq_suaSMqj99_QutlQl5T6JpfQQSeC7UH92pE?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/VWd-nL9bGjc0f9pUGR7zVYFUKnRA16qFTgCOuu6csTTw-o89EbgkBVOyOUJbIZbcVGg9dmJGIH6WpA0Tk7dIEIrWW4FZHLJ5YWrGExQ1x7TvysPu2428k3P04Wq0iWVLBaVFG9O92Gg65vzR0njAbO8ou_uNpLLx7Q2pq7uL_DAsX8vSgS54CDQzDOeEPIv8?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/3BaUuz81_NYx_7kK985ntVzW4aa-tObkd-vkB_oqwuax_rvXZh2Q9dIbMPkkQKtA1eMeAo9VsJQhXokO-Ta-RECyXAb-VkHCuAc4cDzML4ik8d1-lK67NEg_xhdKAfDFEUHEnxK9hFG3N3qkXR-PmZbIF4jdL3A3WDLZAxJb6kI0_co2kKag_BU8UP-zZVfm?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/1eEFyGb6X5fc1A9cDbxxovigOBbkJ6GjV2ifgldA2dj6LbUpP6PhnsHd7OQgZU07oktF89dutpArXftCGWO4QuvdH9Bd1DOy25J3Ip84NjC9lEpKRko1M3FcDHq0l00VoX1_J1MgHjymgBKjmWVqMcepoX2pz0NVVH8bFDCczWdMBpVe4zhTqoo_iPLkfLSO?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/R4sym_WlUMvOYyBtVDrrbyykW7fPSioxw5SXMwXMlr2zFyx_93dTSH_gglt3bYrKaRqtnsLfICfnifHT50nj0w7JxZzA1HrMQfOn3k_uQSROZ8opDxjpB-YftU32NSsGZ11x_TdH1q2ucIePiPKHO_ogl-XCAp2dhtvic5VgfUCyzD3oSJot3xFHLWU_hvG6?purpose=fullsize)

FAISS stands for:

> **Facebook AI Similarity Search**

It is an open-source library from Meta for efficient similarity search and clustering of dense vectors.

Important distinction:

> **FAISS is primarily a vector similarity search library, not a complete server-based vector database in the same sense as Pinecone or Qdrant.**

That's an excellent interview distinction.

---

# 30. Basic FAISS example

Install:

```bash
pip install faiss-cpu
```

Then:

```python
import faiss
import numpy as np

vectors = np.array([
    [0.1, 0.2, 0.3],
    [0.2, 0.3, 0.4],
    [0.9, 0.8, 0.7]
], dtype="float32")

index = faiss.IndexFlatL2(3)

index.add(vectors)
```

Now query:

```python
query = np.array([
    [0.1, 0.2, 0.25]
], dtype="float32")

distances, indices = index.search(query, k=2)

print(distances)
print(indices)
```

Conceptually:

```text
Query
 ↓
FAISS Index
 ↓
Top 2 nearest vectors
```

---

# 31. What does `IndexFlatL2` mean?

```python
faiss.IndexFlatL2(3)
```

means roughly:

```text
Index
 ↓
Flat
 ↓
L2 / Euclidean distance
 ↓
dimension = 3
```

`Flat` is an exact brute-force index.

So:

```text
IndexFlatL2
```

is useful for understanding the fundamentals and for smaller datasets, while other indexes can provide faster approximate search at scale.

---

# 32. Chroma

![Image](https://images.openai.com/static-rsc-4/mQ7ViN21hYlznAfEJtSIY-csaUcgy6erudU38Jd85387jmVo4TzyA3WodJwowMtPylfbZYXRxkcyWAwRQdvFyZJvC2y-CnOhIucYmLrcNzDyEENG0AA6K8O8XDDdXGzNCRGojBwEgApfbaL_KtXz2cfgS40xRkEmi-1n60Rs43KYcERtN5Eolt9Dj3T8k6h7?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/mSfrqSS5LCIdRTQ8j1DCYDCd9Hus7wuTZAOzGaCsdLuAt2DN_1KRJdniNLy_YUFstYkMga4s3g1HtfBBJKTdI6ppuaSi7KoVHXi4hPq68dI2VR6zmBxS0HyGRa8ZYRWXGaidtCS3xyHZEH-9FYLp6sXYoZmuYD5t5WBipM4fxURuj6qkZQCNdtkitQ5Y7ywu?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/HAUkFcdbvvMvULr1f2_7e-yBF6Lrm7nZoUR6VQcPTKkfiOQBtTUf9S1fuy9KJT45xTZ35Ku495dIHjjz7yC7nLM50ancJe-icgskmcgFvvXk6IoNNDanYmLmSewsUB_S3IcLlsGBrs669yntBZaaDziiShFt5dAWyNmSUBMF_knz5fy1v3mPVPxkSG50s811?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/4RdFYrijMbW804fhqc76J8qr1j3xhHqkzXYik9edih7PTwiL8E_Wyq0r6_qEU4e6aIQMXSg0xUthslcRRNFOhaEcfWNc9i3Q5BdEPS59ltrZiI-SmQIyaqy02aSWJxlvXmqPuyKlTX6Nf8BV6nfqDWi-7M--0PTDH8sk74Xd_B5UcS0cIJh_--stVH8Tza-N?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/KJ_tTALeiNPYKwAcEvADToGTQhfxmZyqWQgR0qXHXprz7wA8H95oz70x7EToBw4FAhUti-JICzZpo2TijETPFoLS3xTdEHdZ2j-9rEO7WKj7WOZj7dvso1daY6Oi1ESLxu6MlSNd7RJ5kLq9qZYzePh7ScHIA0zB62uLwdYMm87-YJHN6qEsO06r5fmHkbhZ?purpose=fullsize)

Chroma is popular in:

* prototypes
* local RAG
* experimentation
* learning
* small applications

Example:

```bash
pip install chromadb
```

Then:

```python
import chromadb

client = chromadb.Client()

collection = client.create_collection(
    name="documents"
)
```

Add documents:

```python
collection.add(
    documents=[
        "Employees receive 20 days of annual leave.",
        "Engineering teams have weekly on-call rotations.",
        "Password resets require email verification."
    ],
    ids=["doc1", "doc2", "doc3"]
)
```

Then:

```python
results = collection.query(
    query_texts=["How many vacation days do employees get?"],
    n_results=2
)

print(results)
```

Chroma can handle the embedding/retrieval workflow for you depending on configuration.

---

# 33. Pinecone

![Image](https://images.openai.com/static-rsc-4/6dgpiCR4Lf2netm2jEDgzEdpau92rjn_T3pXiqZ9Qx4EjPCTP6vOtyJvQs5A_6yWZNvi2QMLfmfrrgo2urTDMwsUtamY1X0BHTCkLwzGIhg3nenYajYtHuj92xgw_w0lIXDA7fbB9OwcxydYlBvnhpqWuCT2KImYnlh6eRMPSMSSOhrqjqddUxxNst7M84EP?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/MxqKIwtHg-g63-CXXph0Ap2Qgz6Jd2KdYSyrhn6ZUoUMLMu_80uJZMSqszkbzwh9BDgQtA6YItS4svmSWc5daqmiKg5617nQZKAX-TDS8kr83a67ewKnGl-SoEoM2WnKTNt4Mk6pFu0y8gstxds-9DihfAXZn-2dVawOf-eFQv16ryt2TOlHBAYf_QRwHbfq?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/GfE_R1h0uRnchQ7QlWzuCuiP0TrGgh6SO3RyjbfZfZMeLwo-Y08_UzyrHDPeKKLcKhNrxvXHDO2fTPHLAEOMrE7MR_Cc6GBPHWJ-Xd47iEf_3TvqJcWLLQP3hDRj7is1hJFtWzChFN7W36UGaIeZGb5R3rcSeexTsSHXXEptRLou1FxIkNKoXURbprBztDtq?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/w22qMS96AZionhlOSZqpJWOCOPyUuyQeQ-RgM-cv4WyvQowrwBcTcT2CdJHIf1UPMhpoxrlSJho2IirEczbV3ibvFC7FSPx6j8RieORvLLKc-eOXSxWNh2J970PJ_PooJAT-eGoozMKqY3axXgVjjWDo4CVmmgueIHvGHEvaXbrbk8-pLd7Hjp-cI2j1ucxE?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/4Xewvk_U4Uo_85s521nEGjDF_5zzgigXFIQgSB-pmCXPvuZhI9Dp0hk8jHoM4nCkiSHBJeslniHINeASg1J5x0OBiwQonIs_oeWGArrmN-tD9n1BAdrN9f5vssBD4v73Ck0n4f6s2G76ceujRdh3Mgc8O_4kPrKjwNr4VEGXFEEK85KR46ehj9k9dgKBXXHm?purpose=fullsize)

Pinecone is a managed vector database/service.

The important concept isn't memorizing its API.

Understand:

```text
Application
     ↓
Pinecone
     ↓
Vectors
     ↓
Similarity Search
```

You don't generally manage the underlying infrastructure yourself in the same way you would with a self-hosted database.

Typical concepts include:

```text
Index
Namespace
Vector
Metadata
Query
Top-K
Filtering
```

---

# 34. Qdrant

![Image](https://images.openai.com/static-rsc-4/eR1Us521_pf0w-5E05Gw0d2_x9-he0uNpGiPNz8WnXu1agvY1gGykkbOpMrVU78vJJUbx6_gjoueeFEQdOekZKyzqS8acHQDxx6CJBv-mrBCYpQZRFuRCrCSAaCFOfJaW6YAn6lMzoP1EXcgMtp6HhoKkE0jEFMhNhD2LSIRYmt4n1xiOZfZnWcTMordJFVt?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/3R1GmOkAzdcr4snNhT827BgrOteUGMD4q9VRpI5_yAtX6gBLFvd78LoV9qO3M2B2fjxbD0TVyxRvckTZYDIHEFfRej-9KgQfoM8hp3uupq2s1jNNSpsZ_DsvpcXgfvzBt-bhxo9tmPOAYBufx6DZYZleIRNyAzZ3sDecKpL197A0LlCdknP8Nk6ZJIBJ5_2z?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/hHa1_8Sb2cYxV3euoJy8nzEoAIId-HZFsP817ZPG8WheWLzZjsCNIoSpcD44-Z9RsdqRJsGIpfX5AsbtpohAzGIFRX6nWdLMcVP7QPaeFuZejBoCZNFNVI5BOB9EpspeJeV0XjABl7Q6V-tsfSKF0Y4AiZBvKTHX48y04rxy6QKIZbOQQS77NsSQlB4z86W5?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/76VXS_BHIsXtluywu80KxbBZFw_GA8vUg5se4-oJizmu-IQpY7eWmhjRNnBwvj1YAEmSUKYXhOSlGoe9yiGw1HBSUKvsPtbG7kO2SmhKplhl1VR0BJd29g-k14lmGjbAlypA7dLCH3-LEVZ6MjIXZe20f5DLgOvi-gutG_KbNDsWYhD-PCSGCTz2Jrli2MJ6?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/yVKH_ttSG9ezissmm5p2MviANyEECOgQf0W0wb9-39thYQbiv7ht8iGhJxnhg2dO8J_WO1lgFg91p67ZP5eXj5GvCl7BTHK3-Tf9vKriE_qMnAYdsMiL7WvKy1MWO9vkus9VTJQsQmZSExq7GveB6xH19CewbH2g-RP6a4Rcu-SbNUGt9Y_vxa5p70LYkEzG?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/udVYgahEULxLjUw0lQh5DL4fAub4rv2ek3WlQgh-I9xlTYjImjP9iLTOe8OSwKTr_c56adraI4x8YGzlrfoczd76rau-B_WaK71dzsCvJnpyWkfEiG_pCFxnd4Qzgop4kL-ojDTq5sZ8S3Bbq8gZzbYM8LF5-ObBMhD1mTJXWwRjG5TJ9M8kSaQl6J_xtW2O?purpose=fullsize)

Qdrant is another popular vector database.

It's particularly useful to know because it's commonly encountered in modern RAG applications.

Conceptually:

```text
Collection
    ↓
Points
    ↓
Vector + Payload
```

Qdrant calls its metadata associated with vectors **payload**.

For example:

```json
{
  "department": "engineering",
  "year": 2026
}
```

Then you can perform vector search plus filtering.

---

# 35. Weaviate

![Image](https://images.openai.com/static-rsc-4/3E9KBgQRbpb7vYyamdGM6Z3pQKer1mJOrkR2p1xB49v-iX7uHGvHBS6bxbDdGwcDragUBLkEt-iLEA3wUe3HCKB2m89x_cFgiYdGmbNAz31uFAsE5wU6CDvoveaAhucX5hTfXATo8ca1Rpt0a5b_z8h41CZ1MqZIuvk5dFaW2NGJ6S9yEQOdeh6ejq2-RmdT?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/g1RWaLqEs7eOIKNSl5bU2aUQokhhjL4J6tm89RyJcqi7YATpOStr8l82C4ekg7E0ac-FO8lt54BTtvU-ud6xUQWWO0Q4oN2DPgCexwY3cYiPuQUyhJdY6HVGs0PB0kVvC7ylJ6c1C37rh8yudwLuZKBTjxpwWYE-zBwHTyIoOKNUhIKqT0gu-dYgPFCUvD0B?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/0IoNRyB5l3SHw8x3ntpfzhH_zI64EGcYlC6bm8Bizui7IjhS3l1RR5ZUm9TDC6f1EWgZLwMMrf7yM6fzzvitFHSwXwP5orerjsdNUiRTHv0CWeLWgQn4uR6casp_7XFhIZDK6a2HMGxr9JWJ_QxCO6pUcWZFBgPiOYpGsKOQ4OQB7KkdWbMGi0ZcCSnTljj7?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/jedoTXadEnvKvdKxYPX1uwVCMn_XjJjzo4ApwVcW80LiMvGBKL8nZC34KdpdFOYa0pPf-lZ5TJSHDe1wLU9bjAn-1QtiIJvcYg6y0cnKyUgYQkyj_W_2WdwEfEK02MPmhquBiWhZ4D4icTp05L-5zvGLue4cbB9klFVtX0LzQOVE17VxWXfmzxAkrYStB2J8?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/rKn8lQ0yUmHS9Tz9YiMODoxKJaYTHekcuOqv2bjms8sQI-NenYK3spfKljLPuWAv2sEqDHpG7G-EerndzIXv5CTviVLGfQc0wu7mFzQDVR9LoZfJZ_dPHYpuCNx-hJm7h0hsu8kYnkRxiRseY38iz1BRX2H2rkR2AZjkJNjNmNSOBYKnrkJB0gXXH-dsMbyl?purpose=fullsize)

Weaviate is an open-source vector database/platform.

It supports:

```text
Vector search
Metadata filtering
Hybrid search
Semantic search
```

The important interview takeaway:

```text
Weaviate = vector database
```

rather than memorizing dozens of APIs.

---

# 36. Milvus

![Image](https://images.openai.com/static-rsc-4/8a8lzyqpjtDI0QrCxNgVKjIrp_TR85_gOIc1qoSrLVpm9kJAhNiJwdRaPsV5XtaR5Eb_-lVWoDnWhxvDabct84fIJgU0Sds9pOTHcvFo1JK2BZZGXXJSSMvPuESAdnGdFmsJzmj0C62tMRGEz07AdOU6NY7nG9xjdVR66TEBtSOI32WedFj1Vpm_ld6p4yzj?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/TpQT0NO7w8riOtop03Mfmd2klRxnXgOcy9NT9jm5BpYzPM-47LMpYSGoULdayKtVpZf7dJxKPOCofBORU10qzHEr1Sa9kaOKbcvmmFvKwtp6KfRUV4nY7ixNdvNN6sjklu8VTIDbHKkN3TTHBOad9XAJvZLIxN8D3mW4zNT6mvq2xur55r42TxTFwmwXVCdc?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/2vEqB-rCz571MS_PH8IvPW9da5YkoSLJwRqFEGd-vQ_a-mmfs5evOWkyBNYSEyiCIHRNwQbRYsNR1J1e1aKH1XgTRrosA23va6gim39wyLGF31Stgb3s2ENkmZubGcfrnhtrci6DNwKAF0b7TVn5TztjnWiZ1fZYFdZdIsplz5qj0n2qvsCqgXtedqmr46gY?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/_Cokbv2WWn3C92YvLiGaCU1KcnUZx6rSgEITTHCQGgZ9QHSBrnFXgBttIm87iNaa01I7AoVIH22-u4heAkHgFt2tVcGJpWRbJiNSNOZsJ8wWz3YyrIZqvgg8UutXZwXcWxrOMydQO1kWvJlsxOTN5gBr0olbRc_vBhW_BEcenfSQL-ndLRdS5ddtzxfnodEF?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/frDNwuM0i2hN47q96pXqCztT3KEPvxAHa5A8OaC0r9n7TkaFIQlJnQ7xbwI5Ly20oMJyBsatMiTQjzshSe743kac6RIvtO8iywrHJLHPQn2DVkLTOBliG5EoAp6stXl2SFtp3Z0sphWRrHHl0soH2XLvRYYfttHgUAgGfVHEMY4bFerBw-xelBBwnu8XbKDD?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/sbipleTOLxtO58Xx9LoSLJOjjF0Jg2zQgpXr-ZJ__yNjMWAqf4GrdvrnyZbo7AjtGmHTCfS9h_qNNLXO0iKz47zG388H5vhJ8ddvUYJBg7eo4U88cE_YL5K0oV9Xg-iUa2nGT_yKxgwQ8Hz4uXTGQzqajq44nnNryenE6jDzppVkFFyGgQaTzhRvAoaSyRtG?purpose=fullsize)

Milvus is designed for large-scale vector search.

Think:

```text
Large datasets
       ↓
Distributed vector database
       ↓
Scalable similarity search
```

It's worth knowing for architecture discussions.

---

# 37. pgvector ⭐⭐⭐

This one is particularly interesting.

pgvector adds vector similarity search capabilities to PostgreSQL.

So instead of:

```text
PostgreSQL
+
Separate Vector DB
```

you can sometimes use:

```text
PostgreSQL
+
pgvector
```

Example conceptual table:

```sql
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(1536)
);
```

Now your relational database can store embeddings alongside normal application data.

This is very useful when your application's existing data already lives in PostgreSQL.

---

# 38. When would you choose pgvector?

Imagine your application already has:

```text
Users
Orders
Products
Payments
Documents
```

in PostgreSQL.

And now you want RAG.

Instead of introducing another infrastructure component:

```text
Postgres
      +
Pinecone
```

you could potentially use:

```text
Postgres
   +
pgvector
```

depending on your scale and performance requirements.

---

# 39. Comparison you should know

| Technology | What to remember                            |
| ---------- | ------------------------------------------- |
| FAISS      | Similarity-search library                   |
| Chroma     | Simple/local RAG-friendly vector DB         |
| Pinecone   | Managed vector database                     |
| Qdrant     | Popular vector DB, strong filtering         |
| Weaviate   | Vector DB with semantic/hybrid capabilities |
| Milvus     | Large-scale/distributed vector search       |
| pgvector   | Vector search inside PostgreSQL             |

**Don't memorize marketing differences.**

Understand the underlying concepts.

---

# 40. Vector Database vs Vector Store

You'll hear both terms.

People often use:

```text
Vector database
Vector store
```

somewhat interchangeably.

But in practice, "vector database" often implies a more complete database system with things like:

```text
Persistence
Indexing
Filtering
Scaling
APIs
Updates
Management
```

A simple library like FAISS is more accurately described as a **similarity-search library**.

---

# 41. What exactly is stored?

A common misconception:

> "Vector DB only stores vectors."

Not necessarily.

A record commonly looks conceptually like:

```text
ID
+
Vector
+
Text/document reference
+
Metadata
```

Example:

```json
{
  "id": "chunk_101",
  "vector": [0.12, -0.44, 0.77],
  "text": "Employees get 20 days of leave.",
  "metadata": {
      "source": "leave_policy.pdf",
      "page": 4,
      "department": "HR"
  }
}
```

---

# 42. Why store metadata?

Imagine retrieval returns:

```text
chunk_101
```

You need to know:

```text
Which document?
Which page?
Which department?
Which customer?
Which date?
```

Metadata provides that information.

It also enables filtering.

---

# 43. Filtering + Semantic Search

This is an important real-world pattern.

Suppose your database contains:

```text
1 million documents
```

Metadata:

```text
country
department
language
date
document_type
```

User asks:

> "What was our sales strategy?"

But user belongs to:

```text
department = sales
country = India
year = 2026
```

You can retrieve:

```text
department = sales
AND country = India
AND year = 2026
```

then perform semantic similarity search.

This improves both:

```text
relevance
+
performance
```

---

# 44. Hybrid Search ⭐⭐⭐

You should know this even though it wasn't explicitly in your list.

Vector search is not always enough.

Suppose user searches:

```text
"ERR_CONNECTION_RESET"
```

Exact keyword matching can be very useful.

But semantic search might understand:

```text
"connection keeps getting reset"
```

Hybrid search combines:

```text
Keyword search
       +
Vector search
       ↓
Combined ranking
```

Common keyword approaches include:

```text
BM25
```

This is a very important modern RAG concept.

---

# 45. Dense vs Sparse Retrieval

Another interview topic.

### Dense retrieval

Uses embeddings:

```text
Text
 ↓
Dense vector
 ↓
Semantic similarity
```

Good for:

```text
Meaning
Paraphrases
Semantic relationships
```

### Sparse retrieval

Uses sparse representations, often based on token/term importance.

Good for:

```text
Exact terms
Rare words
Product IDs
Error codes
Names
```

Hybrid retrieval combines both.

---

# 46. Reranking ⭐⭐⭐

Here's a major improvement to basic RAG.

Instead of:

```text
Query
 ↓
Vector DB
 ↓
Top 5
 ↓
LLM
```

you can do:

```text
Query
 ↓
Vector DB
 ↓
Top 20 candidates
 ↓
Reranker
 ↓
Best 5
 ↓
LLM
```

Why?

Vector similarity gives you a fast initial retrieval.

A reranker can examine:

```text
query + candidate document
```

more deeply and reorder the candidates.

---

# 47. Retrieval architecture

A more production-grade RAG system can therefore look like:

```text
                    USER QUERY
                        ↓
                 Query Embedding
                        ↓
               ┌────────┴────────┐
               ↓                 ↓
        Dense Retrieval      Keyword Search
               ↓                 ↓
               └────────┬────────┘
                        ↓
                  Hybrid Ranking
                        ↓
                    Reranker
                        ↓
                     Top-K
                        ↓
                   Context
                        ↓
                      LLM
                        ↓
                     Answer
```

That's a much more realistic architecture than simply:

```text
Embedding → Vector DB → LLM
```

---

# 48. What happens when documents change?

Suppose:

```text
leave_policy.pdf
```

changes.

You can't blindly keep the old embedding.

Usually:

```text
New document
 ↓
Chunk
 ↓
Generate new embeddings
 ↓
Upsert/update vectors
```

The vector DB therefore needs to support operations such as:

```text
Insert
Update
Delete
Upsert
```

---

# 49. Upsert

You'll hear this constantly.

**Upsert = update + insert.**

Conceptually:

```text
If ID exists:
    update

If ID doesn't exist:
    insert
```

Example:

```python
collection.upsert(...)
```

This is useful for keeping your vector index synchronized with source documents.

---

# 50. Deletion is important

Suppose:

```text
document_123
```

is removed.

You need:

```text
Source document deleted
        ↓
Delete corresponding vectors
```

Otherwise your RAG system might answer from stale information.

This is called **stale retrieval data**.

---

# 51. Namespaces / Collections

Different vector systems use different terminology.

You may encounter:

```text
Collection
Index
Namespace
Partition
```

The exact terminology differs.

The general purpose is to organize/isolate vector data.

For example:

```text
company_docs
    ├── HR
    ├── Engineering
    └── Finance
```

or:

```text
tenant_A
tenant_B
tenant_C
```

---

# 52. Multi-tenancy

This becomes important in production Agentic AI.

Imagine a SaaS application:

```text
Customer A
Customer B
Customer C
```

Each customer has private documents.

You **must not** accidentally retrieve:

```text
Customer B's document
```

for:

```text
Customer A
```

Vector databases can support isolation using approaches such as:

```text
Namespaces
Collections
Tenant IDs
Metadata filters
```

The exact design depends on the system.

This is both a **security** and **architecture** issue.

---

# 53. A very important Agentic AI connection

Now let's connect this to agents.

Imagine an agent:

```text
User
 ↓
Agent
 ↓
"What information do I need?"
 ↓
Retriever Tool
 ↓
Vector DB
 ↓
Relevant documents
 ↓
Agent
 ↓
LLM reasoning
 ↓
Answer/action
```

The vector DB becomes a **tool used by the agent**.

For example:

```python
def search_company_docs(query):
    """
    Search company documentation
    """
    results = vector_db.search(query)
    return results
```

The agent can call:

```text
search_company_docs(...)
```

when it needs knowledge.

---

# 54. Vector DB as long-term knowledge

This is where vector databases intersect with **memory**.

Suppose an agent interacts with a user.

You might store useful information:

```text
User prefers Python
User works on RAG project
User previously discussed vector databases
```

Then embed relevant memories and store them.

Later:

```text
User:
"Continue from what we discussed yesterday."
```

The system can:

```text
Query
 ↓
Memory embedding
 ↓
Vector DB
 ↓
Relevant memories
 ↓
Agent
```

So vector databases can be used for:

```text
RAG knowledge
+
Semantic memory
```

But **vector DB ≠ memory system by itself**. Memory requires policies around what to store, retrieve, update, and forget.

---

# 55. Important distinction: Knowledge vs Memory

### RAG knowledge

```text
Company documents
Books
Manuals
Policies
Web pages
```

### Agent memory

```text
Past interactions
Preferences
Previous tasks
Useful historical context
```

Both can use vector databases, but the application semantics are different.

---

# 56. Chunking affects vector search

Remember your previous Level 18.

Suppose:

```text
Huge chunk
```

contains:

```text
Password policy
Vacation policy
Expense policy
Security policy
```

Embedding represents a mixture of concepts.

Retrieval may become less precise.

Instead:

```text
Chunk 1 → Password policy
Chunk 2 → Vacation policy
Chunk 3 → Expense policy
Chunk 4 → Security policy
```

Now semantic retrieval can target the right concept more accurately.

So:

```text
Chunking
   ↓
Embedding
   ↓
Vector DB
   ↓
Retrieval
```

are tightly connected.

---

# 57. Query embedding vs Document embedding

You learned this earlier, but now connect it to vector DBs.

During ingestion:

```text
Document chunk
     ↓
Embedding
     ↓
Vector DB
```

During retrieval:

```text
User query
     ↓
Embedding
     ↓
Vector DB search
```

So both need to be represented in the **same embedding space** for meaningful similarity search.

---

# 58. One critical mistake

Don't do:

```text
Document → Embedding Model A
Query → Embedding Model B
```

and assume similarity scores will be meaningful.

Normally, your query and stored documents should use a compatible embedding setup/space.

---

# 59. Similarity score ≠ truth

This is a subtle but very important RAG concept.

Suppose:

```text
Chunk A → 0.91
Chunk B → 0.87
```

That does **not** mean:

```text
A is definitely correct.
```

It only means:

```text
A is more similar according to the retrieval metric/model.
```

Semantic similarity is not factual verification.

That's why production RAG may use:

```text
Hybrid search
+
Reranking
+
Metadata filtering
+
LLM evaluation
+
Source citations
```

---

# 60. Retrieval failure

Suppose the user asks:

> "What is our maternity leave policy?"

But your database contains:

```text
vacation policy
sick leave policy
holiday policy
```

Nothing relevant exists.

A vector database might still return:

```text
Top 5 documents
```

because something will usually be mathematically "closest."

This is a critical insight:

> **Top-K retrieval does not guarantee relevant retrieval.**

You may need:

```text
similarity threshold
+
reranking
+
"no relevant document found" logic
```

---

# 61. Similarity threshold

Instead of blindly saying:

```text
Give me top 5.
```

you can also consider:

```text
Only return documents
with similarity >= threshold
```

Conceptually:

```text
Query

Chunk A → 0.92 ✓
Chunk B → 0.88 ✓
Chunk C → 0.41 ❌
Chunk D → 0.38 ❌
```

This can help detect retrieval failures.

But thresholds aren't universal. Scores depend on the embedding model, metric, normalization, and data.

---

# 62. Recall vs Precision

This becomes important when tuning retrieval.

### Precision

Of what we retrieved:

> How much was actually relevant?

### Recall

Of everything relevant:

> How much relevant information did we successfully retrieve?

Imagine:

```text
10 relevant chunks exist.

We retrieve 5.

4 are relevant.
```

Then:

```text
Precision = 4/5 = 80%

Recall = 4/10 = 40%
```

RAG systems often need to balance these.

---

# 63. Top-K and recall

Increasing K:

```text
K = 3
```

might improve recall.

But:

```text
K = 50
```

can introduce noise.

So production systems often use:

```text
Retrieve many
      ↓
Rerank
      ↓
Keep fewer high-quality chunks
```

---

# 64. Index tuning

For ANN systems such as HNSW, there are tradeoffs among:

```text
Search speed
Memory
Recall
Index build time
```

Generally:

```text
More exhaustive search
→ better recall
→ more computation

Less exhaustive search
→ faster
→ potentially lower recall
```

You don't need to memorize every parameter yet.

Understand the **tradeoff**.

---

# 65. A practical mini-RAG with Chroma

Here's a conceptual example using Chroma.

```python
import chromadb

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="company_docs"
)

documents = [
    "Employees receive 20 days of annual leave.",
    "Engineering teams follow a weekly on-call rotation.",
    "Password resets require email verification.",
    "Employees can claim approved business expenses."
]

collection.add(
    ids=["1", "2", "3", "4"],
    documents=documents
)
```

Query:

```python
results = collection.query(
    query_texts=[
        "How many vacation days do employees get?"
    ],
    n_results=2
)

print(results["documents"])
```

You should conceptually expect something like:

```text
[
    [
        "Employees receive 20 days of annual leave.",
        ...
    ]
]
```

The exact output depends on the configured embedding function and Chroma version/configuration.

---

# 66. Metadata example

Let's add metadata:

```python
collection.add(
    ids=["1", "2", "3"],
    documents=[
        "Employees receive 20 days of annual leave.",
        "Engineering teams follow a weekly on-call rotation.",
        "Password resets require email verification."
    ],
    metadatas=[
        {
            "department": "HR",
            "year": 2026
        },
        {
            "department": "Engineering",
            "year": 2026
        },
        {
            "department": "IT",
            "year": 2026
        }
    ]
)
```

Then you can combine semantic search with metadata constraints, depending on the database's filtering syntax.

---

# 67. Production architecture

A production RAG system might look like:

```text
                  ┌──────────────┐
                  │  Documents   │
                  └──────┬───────┘
                         ↓
                    Extraction
                         ↓
                      Chunking
                         ↓
                   Embedding Model
                         ↓
              ┌─────────────────────┐
              │    Vector Database  │
              │                     │
              │ Vector              │
              │ Metadata            │
              │ Index               │
              └──────────┬──────────┘
                         ↑
                         │
                    User Query
                         ↓
                   Query Embedding
                         ↓
                  Metadata Filter
                         ↓
                  Vector Retrieval
                         ↓
                   Hybrid Search
                         ↓
                     Reranker
                         ↓
                      Top-K
                         ↓
                    Context
                         ↓
                       LLM
                         ↓
                      Answer
```

This is the architecture you should be able to explain in an interview.

---

# 68. How an Agent changes this

Now make it agentic:

```text
                     USER
                       ↓
                     AGENT
                       ↓
                ┌──────┴──────┐
                ↓             ↓
          Vector Search    Web Search
                ↓             ↓
          Company Docs     Internet
                ↓             ↓
                └──────┬──────┘
                       ↓
                    Reasoning
                       ↓
                  Tool Calling
                       ↓
                     Answer
```

The agent decides:

> "I need company documentation."

So it invokes:

```text
vector_search()
```

This is where **RAG becomes a tool available to an agent**.

---

# 69. What you absolutely MUST know for interviews

If you're preparing for an **Agentic AI / GenAI interview**, I'd prioritize these:

### Tier 1 — MUST KNOW 🔥🔥🔥

```text
What is a vector database?
Why do we need it?
Embedding → Vector DB → Similarity Search
Cosine similarity
Euclidean distance
Dot product
Top-K
Metadata
Metadata filtering
ANN
Index
```

### Tier 2 — VERY IMPORTANT 🔥🔥

```text
HNSW
IVF
Exact vs approximate search
Hybrid search
Dense vs sparse retrieval
Reranking
Similarity threshold
Precision vs recall
```

### Tier 3 — Know conceptually

```text
FAISS
Chroma
Pinecone
Qdrant
Weaviate
Milvus
pgvector
```

You don't need to memorize seven APIs.

---

# 70. Interview questions you should be able to answer

### Q1. What is a vector database?

> A vector database stores and indexes high-dimensional vectors, typically embeddings, and enables efficient similarity-based retrieval.

---

### Q2. Why use a vector DB in RAG?

> Because RAG needs to retrieve semantically relevant document chunks for a user's query. The vector database makes similarity search over potentially large numbers of embeddings efficient.

---

### Q3. What is Top-K?

> Top-K is the number of highest-ranked results returned by a retrieval operation.

---

### Q4. What is ANN?

> Approximate Nearest Neighbor search efficiently finds vectors that are close to a query without exhaustively comparing against every vector.

---

### Q5. Why approximate search?

> Exact search can become computationally expensive at large scale. ANN trades a small amount of retrieval accuracy for significantly better latency and scalability.

---

### Q6. What is HNSW?

> HNSW is a graph-based approximate nearest-neighbor indexing algorithm that organizes vectors into navigable layers to efficiently find nearby vectors.

---

### Q7. Difference between metadata filtering and similarity search?

> Metadata filtering applies structured conditions such as `department = engineering`, while similarity search finds vectors based on semantic or geometric closeness. They can be combined.

---

### Q8. Vector DB vs embedding model?

> The embedding model converts text into vectors. The vector database stores, indexes, and retrieves those vectors.

---

### Q9. FAISS vs Pinecone?

> FAISS is primarily a similarity-search library, while Pinecone is a managed vector database/service. FAISS gives you lower-level similarity-search capabilities; a managed vector DB provides broader database infrastructure and operational capabilities.

---

### Q10. Why not just use SQL?

> Traditional SQL databases are optimized primarily for structured queries. Vector search requires efficient nearest-neighbor search over high-dimensional vectors. However, systems such as PostgreSQL with pgvector can combine relational and vector capabilities.

---

### Q11. What is hybrid search?

> Hybrid search combines semantic vector retrieval with lexical/keyword retrieval, often using techniques such as BM25, to improve retrieval quality across both semantic queries and exact terms.

---

### Q12. Why can increasing Top-K hurt RAG?

> Increasing K can improve recall but may introduce irrelevant chunks, increase context size and cost, and potentially confuse the LLM.

---

# 71. One interview scenario

Interviewer:

> "Your RAG chatbot gives irrelevant answers. What would you investigate?"

Don't say:

> "I'll change the LLM."

Instead think through the entire pipeline:

```text
1. Chunking
      ↓
2. Embedding model
      ↓
3. Vector DB
      ↓
4. Similarity metric
      ↓
5. Top-K
      ↓
6. Metadata filters
      ↓
7. Hybrid search
      ↓
8. Reranking
      ↓
9. Context construction
      ↓
10. LLM
```

You could say:

> "I'd first evaluate retrieval quality independently from generation. I'd inspect chunk sizes and overlap, embedding-model suitability, similarity metric, Top-K, metadata filters, retrieval thresholds, and whether hybrid retrieval or reranking is needed. I'd also check whether the required information actually exists in the indexed corpus."

**That is a much stronger engineering answer.**

---

# 72. The biggest misconception to avoid

Don't think:

```text
Vector DB = magic semantic search
```

Instead:

```text
Embedding model
      ↓
creates representation

Vector index
      ↓
makes search efficient

Similarity metric
      ↓
defines closeness

Metadata
      ↓
adds structured constraints

Retriever
      ↓
selects useful context

Reranker
      ↓
improves ordering

LLM
      ↓
generates answer
```

Each component has a different job.

---

# 73. Your mental model 🧠

I want you to remember this exact analogy.

Imagine a **huge library**.

### Embedding model

The librarian converts the meaning of every book/chapter into coordinates.

```text
Book meaning → Vector
```

### Vector DB

The library's organized search system.

```text
Vectors
+
Index
+
Metadata
```

### Similarity search

You say:

> "Find books about machine learning."

The system finds nearby meanings.

### Top-K

You say:

> "Give me the best 5."

### Metadata filtering

You say:

> "Only books published after 2024."

### ANN

Instead of checking every book in the entire library, use an efficient map to quickly locate likely relevant areas.

### Reranker

A specialist looks at the candidate books and decides which ones are **actually most relevant**.

### LLM

Finally:

> "Read these selected passages and answer my question."

That is RAG.

---

# 74. The complete mental model for your Agentic AI journey

At this point, connect your previous levels:

```text
                ┌──────────────┐
                │   Documents  │
                └──────┬───────┘
                       ↓
                    Chunking
                       ↓
                   Embeddings
                       ↓
               ┌───────────────┐
               │ Vector DB     │
               │               │
               │ Vectors       │
               │ Metadata      │
               │ Index         │
               └───────┬───────┘
                       ↑
                       │
                 Query Embedding
                       ↑
                    User Query
                       ↓
               Similarity Search
                       ↓
                     Top-K
                       ↓
                   Reranking
                       ↓
                   Context
                       ↓
                    Agent
                       ↓
                 ┌─────┴─────┐
                 ↓           ↓
              Tools       Memory
                 ↓           ↓
                 └─────┬─────┘
                       ↓
                      LLM
                       ↓
                    Answer
```

**This is the bigger picture.**

---

# 🎯 Your Level 20 checklist

Before moving to the next level, you should be able to explain these without looking at notes:

```text
☑ What is a vector database?
☑ Why do RAG systems need vector databases?
☑ Vector vs embedding
☑ Embedding model vs vector DB
☑ What is an index?
☑ What is similarity search?
☑ Cosine similarity
☑ Euclidean distance
☑ Dot product
☑ What is Top-K?
☑ What is metadata?
☑ What is metadata filtering?
☑ Exact search vs ANN
☑ What is HNSW?
☑ What is IVF?
☑ What is Product Quantization?
☑ What is hybrid search?
☑ Dense vs sparse retrieval
☑ What is reranking?
☑ Precision vs recall
☑ Similarity threshold
☑ FAISS
☑ Chroma
☑ Pinecone
☑ Qdrant
☑ Weaviate
☑ Milvus
☑ pgvector
☑ How vector DB fits into RAG
☑ How vector DB can become an Agent tool
☑ How vector DB can support semantic memory
```

## 🔥 The one sentence to memorize

If an interviewer asks you:

**"Explain how a vector database works in an Agentic AI application."**

Your answer should be:

> **"We chunk the source documents, generate embeddings for those chunks, and store the embeddings along with their metadata in a vector database. At query time, we embed the user's query and perform similarity search, often using an ANN index and metadata filters, retrieve the Top-K relevant chunks, optionally rerank them, and provide the resulting context to the LLM or agent so it can generate a grounded response or use the retrieved information as part of its reasoning."**

If you can explain that naturally and then drill down into **HNSW, Top-K, metadata filtering, hybrid search, reranking, and FAISS vs vector databases**, you're in very good shape for this level.

**Next logical level:** we should move from *"how vector databases work"* to **building a real RAG pipeline with LangChain + Gemini + a vector DB**, because that will connect the concepts you've learned into an actual Agentic AI application.
