Absolutely. **Level 21 — Retrieval** is one of the most important levels in your Agentic AI roadmap.

You already learned:

* **Chunking** → how to split documents
* **Embeddings** → how to represent meaning as vectors
* **Vector Databases** → where vectors are stored and searched

Now we're learning the actual mechanism that answers:

> **"Given this user query, which pieces of information should I retrieve?"**

That mechanism is **Retrieval**.

---

# 🚀 LEVEL 21 — RETRIEVAL

## 1. First, understand the big picture

A basic RAG system looks like:

```text
Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Database
    ↓
          ← RETRIEVAL ← User Query
    ↓
Relevant Chunks
    ↓
LLM
    ↓
Answer
```

Retrieval is the bridge between:

```text
User's question
        ↓
Relevant information
```

For example:

> "How many annual leave days do employees get?"

Your knowledge base may contain 100,000 chunks.

Retrieval's job is to find:

```text
Chunk 17 → "Employees receive 20 days of annual leave..."
```

rather than returning:

```text
Chunk 9281 → password policy
Chunk 1842 → office parking
Chunk 5512 → reimbursement
```

---

# 2. What exactly is Retrieval?

### Interview definition ⭐

> **Retrieval is the process of finding and selecting the most relevant information from a knowledge source in response to a user query.**

The knowledge source could be:

* Vector database
* Search engine
* SQL database
* Document store
* Knowledge graph
* APIs
* Web search

In RAG, retrieval usually means:

```text
Query
 ↓
Retriever
 ↓
Relevant documents/chunks
```

---

# 3. Retriever

This is your first major concept.

A **retriever** is a component that takes a query and returns relevant documents.

Conceptually:

```python
documents = retriever.invoke(
    "How many vacation days do employees get?"
)
```

Result:

```text
[
    "Employees receive 20 days of annual leave.",
    "Annual leave must be approved by the employee's manager."
]
```

The retriever doesn't normally generate the final answer.

It retrieves information.

---

# 4. Retriever vs Vector Database

This distinction is extremely important.

You learned:

```text
Vector DB
```

Now:

```text
Retriever
```

They aren't the same thing.

### Vector database

Responsible for:

```text
Store vectors
Index vectors
Search vectors
Filter metadata
```

### Retriever

Responsible for:

```text
Take query
 ↓
Perform retrieval strategy
 ↓
Return relevant documents
```

Think:

```text
                Retriever
                    ↓
             ┌──────┴──────┐
             ↓             ↓
       Vector Search    Keyword Search
             ↓             ↓
             └──────┬──────┘
                    ↓
                Documents
```

A retriever can therefore use a vector DB underneath.

---

# 5. Retriever as an abstraction

This is especially important once you start using LangChain.

Instead of your application caring about:

```text
Pinecone API
Qdrant API
FAISS API
Chroma API
```

you can interact with a retriever abstraction:

```python
docs = retriever.invoke(query)
```

The underlying implementation might use:

```text
Vector DB
BM25
Hybrid search
Custom search
```

That's why retrievers are so useful in application architecture.

---

# 6. Basic Retrieval Pipeline

Let's build the simplest possible version.

```text
User Query
    ↓
Query Embedding
    ↓
Vector Search
    ↓
Top-K
    ↓
Documents
```

Example:

```text
Query:
"How do I reset my password?"
```

Embedding:

```text
[0.12, -0.42, 0.77, ...]
```

Vector search:

```text
Document A → 0.94
Document B → 0.88
Document C → 0.52
```

Top-K = 2:

```text
A
B
```

Those become the retrieved context.

---

# 7. Similarity Search

You've already learned this in Level 20.

Similarity search asks:

> "Which stored vectors are closest to my query vector?"

Suppose:

```text
Query = [0.9, 0.1]
```

Documents:

```text
A = [0.8, 0.2]
B = [0.1, 0.9]
C = [0.85, 0.15]
```

Similarity might look like:

```text
C → 0.99
A → 0.98
B → 0.20
```

Therefore:

```text
Top-2 = C, A
```

---

# 8. Top-K Retrieval ⭐⭐⭐

This is one of the most important retrieval concepts.

`K` represents how many results you want.

```python
results = retriever.invoke(query)
```

Depending on the retriever configuration, perhaps:

```text
K = 5
```

Then:

```text
Query
 ↓
Retrieve 5 most relevant chunks
```

---

# 9. Why not retrieve everything?

Imagine:

```text
1,000,000 chunks
```

You don't want:

```text
1,000,000 chunks
       ↓
       LLM
```

That's:

* expensive
* slow
* noisy
* potentially confusing

Instead:

```text
1,000,000 chunks
       ↓
Retrieval
       ↓
Top 5 / 10 / 20
       ↓
LLM
```

---

# 10. The Top-K tradeoff

This is a very important interview topic.

### K too small

```text
K = 1
```

Potential problem:

```text
You may miss useful information.
```

### K too large

```text
K = 100
```

Potential problems:

```text
Too much context
More tokens
Higher cost
More noise
Potentially worse generation
```

So:

> **Top-K is a retrieval-quality vs context-noise tradeoff.**

---

# 11. Metadata Filtering

Suppose your knowledge base contains:

```text
1,000,000 documents
```

Each has:

```json
{
  "department": "engineering",
  "country": "India",
  "year": 2026
}
```

User asks:

> "What is the engineering leave policy?"

You can first filter:

```text
department = engineering
```

Then perform semantic retrieval.

Conceptually:

```text
1,000,000 documents
       ↓
department = engineering
       ↓
50,000 documents
       ↓
Similarity search
       ↓
Top-K
```

This is much more targeted.

---

# 12. Metadata Filtering vs Similarity Search

Don't confuse them.

### Metadata filtering

Structured:

```text
year = 2026
department = engineering
country = India
```

### Similarity search

Semantic:

```text
"How do I take vacation?"
```

Finds documents with similar meaning.

Together:

```text
Metadata filter
      +
Semantic similarity
      ↓
Better retrieval
```

---

# 13. Dense Retrieval ⭐⭐⭐

Now we get into the most important part of Level 21.

Dense retrieval uses **dense embeddings**.

Pipeline:

```text
Query
 ↓
Embedding Model
 ↓
Dense Vector
 ↓
Vector Search
 ↓
Relevant Documents
```

Example:

```text
Query:
"How can I recover my account?"
```

Embedding:

```text
[0.12, -0.41, 0.77, 0.22, ...]
```

Stored documents also have embeddings.

Similarity is calculated.

---

# 14. Why is it called "dense"?

Because most dimensions contain meaningful numerical values.

Example:

```text
[0.12, -0.42, 0.77, 0.21, 0.63, -0.11, ...]
```

Many dimensions are non-zero.

Therefore:

```text
Dense vector
```

Dense retrieval is good at understanding:

> **meaning and semantic similarity**

---

# 15. Example of Dense Retrieval

Database:

```text
A: "How do I reset my password?"
B: "How do I change my email?"
C: "How do I recover my account?"
```

Query:

> "I forgot my login credentials."

A dense embedding model may recognize that:

```text
"forgot my login credentials"
```

is semantically related to:

```text
"reset my password"
```

even though the exact words aren't identical.

That's the power of dense retrieval.

---

# 16. But Dense Retrieval has weaknesses

Consider:

```text
Query:

"ERR_CONNECTION_RESET"
```

A semantic embedding may understand the general meaning.

But exact keyword matching is extremely valuable here.

Another example:

```text
"Product ID: XJ-3948-A"
```

Exact token matching can be better than semantic similarity.

This is where **sparse retrieval** comes in.

---

# 17. Sparse Retrieval ⭐⭐⭐

Sparse retrieval represents documents/queries using sparse representations where only some terms/features have non-zero weights.

Classic examples include:

```text
TF-IDF
BM25
```

For interviews, **BM25** is the key one to know.

Sparse retrieval is particularly useful for:

* exact keywords
* product IDs
* names
* error codes
* technical terms
* rare terms

---

# 18. Dense vs Sparse

This comparison is extremely important.

| Dense Retrieval               | Sparse Retrieval              |
| ----------------------------- | ----------------------------- |
| Uses embeddings               | Uses term/token statistics    |
| Semantic meaning              | Lexical/keyword matching      |
| Good for paraphrases          | Good for exact terms          |
| Handles conceptual similarity | Handles rare/exact terms well |
| Vector search                 | BM25/keyword search           |

Example:

Query:

> "How can I recover my login credentials?"

Dense search may retrieve:

> "How to reset your password"

Excellent.

Query:

> `"ERR_CONNECTION_RESET"`

Sparse search may be better because the exact string matters.

---

# 19. BM25 ⭐⭐⭐

Now let's understand BM25.

BM25 is a classic ranking algorithm used for information retrieval.

It's based primarily on:

* Term frequency
* Inverse document frequency
* Document length normalization

You don't need to memorize the mathematical formula for most Agentic AI interviews.

But you should understand the intuition.

---

# 20. Term Frequency

Suppose:

```text
Document A:
"Python is great. Python is powerful. Python is popular."
```

The word:

```text
Python
```

appears multiple times.

Higher term frequency generally increases relevance.

But there's a catch.

If a word appears 1,000 times just because the document is huge, that shouldn't automatically make it the best result.

BM25 handles this better than simple raw term counting.

---

# 21. Inverse Document Frequency

Suppose you have 10,000 documents.

Word:

```text
"the"
```

appears in:

```text
9,900 documents
```

It's not very informative.

But:

```text
"Qdrant"
```

appears in:

```text
50 documents
```

That's much more informative.

So rare terms get more importance.

Conceptually:

```text
Common word
→ low importance

Rare word
→ high importance
```

---

# 22. Document Length

BM25 also accounts for document length.

Why?

Imagine:

```text
Document A = 100 words
Document B = 10,000 words
```

If both contain the query terms, the huge document shouldn't automatically win simply because it has more opportunities to contain those terms.

BM25 normalizes for document length.

---

# 23. BM25 intuition

You can think:

```text
BM25 relevance
≈
Term importance
+
Query term frequency
+
Document length normalization
```

More formally, BM25 scores documents based on term frequency and inverse document frequency with saturation and length normalization.

For interviews, the conceptual explanation is usually more important than the formula.

---

# 24. Simple BM25 example

Documents:

```text
D1:
"Python programming tutorial"

D2:
"Python programming and machine learning tutorial"

D3:
"Cooking recipes"
```

Query:

```text
"Python programming"
```

BM25 might rank:

```text
D1 → high
D2 → high
D3 → very low
```

Because D1 and D2 contain the exact query terms.

---

# 25. Dense + Sparse = Hybrid Search ⭐⭐⭐⭐⭐

This is probably the **most important concept of this level after basic retrieval**.

Dense retrieval:

```text
Meaning
```

Sparse retrieval:

```text
Keywords
```

Hybrid search:

```text
Dense Retrieval
       +
Sparse Retrieval
       ↓
Combined Results
```

This gives you the best of both worlds.

---

# 26. Example of Hybrid Search

Query:

> "How do I fix ERR_CONNECTION_RESET in Chrome?"

Dense retrieval understands:

```text
connection problems
network errors
browser issues
```

Sparse retrieval recognizes:

```text
ERR_CONNECTION_RESET
Chrome
```

Together:

```text
Semantic understanding
       +
Exact keyword matching
       ↓
Better retrieval
```

---

# 27. Why hybrid search can outperform pure vector search

Suppose your documents contain:

```text
"ERR_CONNECTION_RESET"
```

A user searches:

```text
"ERR_CONNECTION_RESET"
```

Keyword search is extremely strong.

Now user searches:

```text
"My browser keeps losing the connection"
```

Dense search can understand the semantic relationship.

Therefore:

```text
Dense
→ meaning

Sparse
→ exact words

Hybrid
→ meaning + exact words
```

---

# 28. Hybrid Search Architecture

```text
                    User Query
                        ↓
                ┌───────┴───────┐
                ↓               ↓
         Dense Retrieval   Sparse Retrieval
                ↓               ↓
         Vector Search        BM25
                ↓               ↓
                └───────┬───────┘
                        ↓
                  Result Fusion
                        ↓
                   Top Results
```

---

# 29. How do we combine the results?

There are multiple approaches.

You may see:

```text
Weighted score combination
```

For example:

```text
Final Score =
0.7 × Dense Score
+
0.3 × BM25 Score
```

Conceptually:

```python
final_score = (
    0.7 * dense_score +
    0.3 * sparse_score
)
```

The weights depend on your data and evaluation.

---

# 30. Another approach: Reciprocal Rank Fusion

You may encounter:

> **RRF — Reciprocal Rank Fusion**

Instead of directly combining scores from systems that may use incompatible score scales, RRF combines rankings.

Conceptually:

```text
Dense ranking:

A
B
C
D

BM25 ranking:

B
A
D
C
```

RRF combines their rankings to produce:

```text
A
B
...
```

The exact implementation isn't the key thing at your stage.

Just remember:

> **RRF is a common technique for combining rankings from multiple retrieval systems.**

---

# 31. Reranking ⭐⭐⭐⭐⭐

Now we reach another extremely important concept.

Suppose we retrieve:

```text
Top 20 documents
```

The initial retriever is fast, but some results may not actually be the best.

So we introduce:

```text
Reranker
```

Pipeline:

```text
Query
 ↓
Retriever
 ↓
Top 20 candidates
 ↓
Reranker
 ↓
Best 5
 ↓
LLM
```

---

# 32. Why do we need a reranker?

Vector similarity is a relatively coarse first-stage retrieval mechanism.

A reranker can evaluate:

```text
Query
+
Candidate document
```

more deeply.

For example:

```text
Query:
"What is the company's parental leave duration?"
```

Initial retrieval:

```text
1. General leave policy
2. Vacation policy
3. Parental leave policy
4. Sick leave policy
5. Holiday policy
```

A reranker might reorder:

```text
1. Parental leave policy
2. General leave policy
3. Sick leave
4. Vacation
5. Holiday
```

Now send the best few to the LLM.

---

# 33. Retriever vs Reranker

Very important interview distinction.

### Retriever

Fast:

```text
1,000,000 documents
       ↓
Top 50
```

### Reranker

More expensive/deeper:

```text
50 candidates
       ↓
Top 5
```

So:

```text
Retriever
→ high recall

Reranker
→ high precision
```

That's a useful mental model.

---

# 34. Two-stage retrieval ⭐⭐⭐⭐⭐

This is a production-quality concept.

```text
                Query
                  ↓
        ┌─────────────────┐
        │ First Retrieval │
        │                 │
        │ Dense / BM25    │
        └────────┬────────┘
                 ↓
            Top 50/100
                 ↓
        ┌─────────────────┐
        │    Reranker     │
        └────────┬────────┘
                 ↓
              Top 5
                 ↓
                LLM
```

Why?

Because applying an expensive reranker to one million documents would be expensive.

Instead:

```text
Cheap retrieval
      ↓
Small candidate set
      ↓
Expensive reranking
```

This is an extremely useful architecture pattern.

---

# 35. Retrieval vs Reranking vs Generation

Don't mix these up.

```text
Retrieval
→ Finds candidates

Reranking
→ Orders candidates

Generation
→ Produces the answer
```

For example:

```text
User Question
     ↓
Retriever
     ↓
20 candidates
     ↓
Reranker
     ↓
5 best chunks
     ↓
LLM
     ↓
Answer
```

---

# 36. A simple Python Retriever

Let's build the concept ourselves.

```python
import numpy as np

documents = [
    "Employees receive 20 days of annual leave.",
    "Password resets require email verification.",
    "Engineering teams have weekly on-call rotations.",
    "Employees can claim approved travel expenses."
]

vectors = np.array([
    [0.90, 0.10, 0.20],
    [0.10, 0.90, 0.10],
    [0.20, 0.20, 0.90],
    [0.40, 0.30, 0.20]
])

query_vector = np.array([0.85, 0.15, 0.20])
```

Cosine similarity:

```python
def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )
```

Retriever:

```python
def retrieve(query_vector, k=2):
    results = []

    for i, vector in enumerate(vectors):
        score = cosine_similarity(query_vector, vector)
        results.append((documents[i], score))

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return results[:k]
```

Run:

```python
results = retrieve(query_vector, k=2)

for document, score in results:
    print(score, document)
```

This is the conceptual core of dense retrieval.

Real vector databases optimize this process dramatically.

---

# 37. Simple BM25 code

For learning purposes, you can use `rank_bm25`.

Install:

```bash
pip install rank-bm25
```

Then:

```python
from rank_bm25 import BM25Okapi

documents = [
    "How to reset your password",
    "How to change your email address",
    "How to update your profile",
    "How to recover your account"
]

tokenized_docs = [
    doc.lower().split()
    for doc in documents
]

bm25 = BM25Okapi(tokenized_docs)
```

Query:

```python
query = "reset password"

tokenized_query = query.lower().split()

scores = bm25.get_scores(tokenized_query)

print(scores)
```

Retrieve:

```python
ranked = sorted(
    zip(documents, scores),
    key=lambda x: x[1],
    reverse=True
)

for document, score in ranked:
    print(score, document)
```

You should expect the password-reset document to rank highly.

This is **sparse/lexical retrieval**.

---

# 38. Dense vs BM25 example

Consider:

```text
Document:
"How to reset your password"

Query:
"I forgot my login credentials"
```

### BM25

May struggle because:

```text
forgot
login
credentials
```

don't exactly match:

```text
reset
password
```

### Dense retrieval

Can recognize:

```text
forgot login credentials
≈
reset password
```

Now consider:

```text
Document:
"ERR_CONNECTION_RESET occurs when..."
```

Query:

```text
"ERR_CONNECTION_RESET"
```

BM25 can be extremely effective because the exact term matches.

Therefore:

```text
Dense + Sparse
```

is often stronger than either alone.

---

# 39. Metadata + Hybrid Search

You can combine everything.

Suppose:

```text
1 million documents
```

Query:

> "How do I resolve ERR_CONNECTION_RESET?"

Metadata:

```text
product = Chrome
year >= 2025
```

Pipeline:

```text
Query
 ↓
Metadata filtering
 ↓
 ┌─────────────────────┐
 │                     │
 ↓                     ↓
Dense Search        BM25
 │                     │
 └──────────┬──────────┘
            ↓
        Fusion
            ↓
        Reranking
            ↓
          Top-K
            ↓
           LLM
```

This is a strong production retrieval pipeline.

---

# 40. Retrieval Quality

Now think like an AI engineer.

Your RAG system produces a bad answer.

Don't immediately blame the LLM.

Ask:

> **Did we retrieve the right information?**

You should evaluate retrieval separately.

For example:

```text
Question:
"What is the leave policy?"

Expected relevant chunk:
Chunk 47

Retrieved:
Chunk 2
Chunk 18
Chunk 91
```

Generation can't reliably answer if retrieval failed.

This leads to an important principle:

> **Garbage retrieval → garbage context → potentially garbage answer.**

---

# 41. Retrieval metrics

You should know these at a conceptual level.

### Precision

Of retrieved results:

> How many were relevant?

### Recall

Of all relevant results:

> How many did we retrieve?

Example:

```text
There are 10 relevant documents.

Retriever returns 5.

4 are relevant.
```

Then:

```text
Precision = 4 / 5 = 80%

Recall = 4 / 10 = 40%
```

---

# 42. Recall@K

You'll see:

```text
Recall@5
Recall@10
Recall@20
```

Meaning:

> How much relevant information was retrieved within the first K results?

Example:

```text
Expected relevant chunk = Chunk 42

Retrieved Top-5:
1. Chunk 7
2. Chunk 19
3. Chunk 42
4. Chunk 80
5. Chunk 91
```

Then:

```text
Recall@5 = successful
```

because the relevant chunk appeared within the top 5.

---

# 43. MRR

Another retrieval metric you may encounter:

> **MRR — Mean Reciprocal Rank**

Suppose the relevant document appears at rank:

```text
1
```

Reciprocal rank:

```text
1/1 = 1
```

If it appears at rank:

```text
5
```

Then:

```text
1/5 = 0.2
```

MRR rewards systems that place the correct result near the top.

You don't need to obsess over the formula now.

Know the purpose:

> **MRR measures how highly the first relevant result is ranked.**

---

# 44. NDCG

You may encounter:

> **NDCG — Normalized Discounted Cumulative Gain**

It evaluates ranking quality when multiple results can have different degrees of relevance.

For example:

```text
Highly relevant
Relevant
Somewhat relevant
Irrelevant
```

NDCG rewards putting highly relevant results near the top.

For Agentic AI interviews:

```text
Precision
Recall
Recall@K
MRR
NDCG
```

are good concepts to recognize.

---

# 45. Retrieval failure modes

This is where you start thinking like an engineer.

### Failure 1 — Wrong chunking

```text
Chunks too large
```

→ retrieval becomes less precise.

### Failure 2 — Chunks too small

```text
Not enough context
```

→ retrieved chunk lacks necessary information.

### Failure 3 — Poor embedding model

```text
Semantic relationship not captured
```

→ wrong documents retrieved.

### Failure 4 — K too low

```text
Relevant information missed
```

### Failure 5 — K too high

```text
Too much noise
```

### Failure 6 — Exact keyword problem

```text
Dense retrieval misses rare technical terms
```

→ use hybrid search.

### Failure 7 — No reranking

```text
Relevant document appears at rank 8
```

but you only pass top 5 to the LLM.

### Failure 8 — Bad metadata filtering

You accidentally filter out the correct document.

---

# 46. Query Transformation

This is slightly beyond your listed topics, but it's important for modern retrieval.

User asks:

> "What about the other one?"

This query is ambiguous.

A conversational agent may transform it into:

```text
"What is the company's parental leave policy?"
```

before retrieval.

This is called **query rewriting/transformation**.

Pipeline:

```text
Conversation
 ↓
Query Rewriter
 ↓
Better Search Query
 ↓
Retriever
```

Very useful for conversational RAG.

---

# 47. Multi-query retrieval

Another useful technique.

Suppose user asks:

> "How secure is our authentication system?"

Instead of one query, generate multiple:

```text
1. Authentication security policy
2. Login security mechanisms
3. MFA and password security
4. Account protection controls
```

Then retrieve using each.

```text
Query
 ↓
Generate multiple queries
 ↓
Retrieve for each
 ↓
Merge results
 ↓
Rerank
```

This can improve recall.

You don't need to master implementation yet, but know the idea.

---

# 48. Parent-Child Retrieval

You learned parent-child chunking earlier.

Retrieval might work like:

```text
Small child chunk
      ↓
Precise retrieval
      ↓
Parent document/section
      ↓
More context
```

This solves a common problem:

```text
Small chunk
→ good precision
→ insufficient context
```

So you retrieve a small child chunk but return its larger parent context.

---

# 49. Contextual Retrieval

Modern RAG systems may add contextual information to chunks before embedding.

Instead of embedding:

```text
"20 days."
```

you may create context such as:

```text
"Company HR leave policy: Employees receive 20 days of annual leave."
```

Then embed that richer representation.

Why?

Because an isolated chunk may lose important context.

This connects directly back to your **chunking level**.

---

# 50. Retrieval architecture you should understand

A modern retrieval pipeline could be:

```text
                      USER QUERY
                          ↓
                   Query Rewriting
                          ↓
              ┌───────────┴───────────┐
              ↓                       ↓
        Dense Retrieval          Sparse Retrieval
              ↓                       ↓
        Vector Search                BM25
              ↓                       ↓
              └───────────┬───────────┘
                          ↓
                    Result Fusion
                          ↓
                    Metadata Filter
                          ↓
                      Top-N
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

Not every application needs every component.

That's important.

---

# 51. Don't over-engineer

For a small application:

```text
Query
 ↓
Embedding
 ↓
Vector DB
 ↓
Top-5
 ↓
LLM
```

may be perfectly sufficient.

For a large production system:

```text
Query rewriting
+
Hybrid retrieval
+
Metadata filtering
+
Reranking
+
Evaluation
```

may be appropriate.

You choose based on:

* dataset
* query types
* latency
* cost
* accuracy requirements

---

# 52. How LangChain fits into this

You're approaching LangChain next, so this is important.

Conceptually, LangChain gives you abstractions like:

```text
Document
Retriever
VectorStore
Embedding
LLM
Chain
Agent
Tool
```

The architecture can become:

```python
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)

docs = retriever.invoke(
    "How many vacation days do employees get?"
)
```

The important part isn't memorizing this syntax.

Understand:

```text
vector_store
      ↓
retriever
      ↓
query
      ↓
documents
```

---

# 53. Retriever as an Agent Tool

This is where Level 21 becomes directly relevant to **Agentic AI**.

Imagine an agent has tools:

```text
Tools:

1. calculator
2. web_search
3. database_search
4. company_document_search
```

The agent receives:

> "According to our internal policy, can I carry over unused leave?"

The agent reasons:

```text
I need internal company policy.
```

Then calls:

```text
company_document_search(
    "unused leave carry over policy"
)
```

Retriever:

```text
Query
 ↓
Hybrid Retrieval
 ↓
Relevant documents
 ↓
Agent
```

Then the agent can reason over those results.

---

# 54. Agentic RAG

A simple RAG:

```text
Question
 ↓
Retrieve
 ↓
LLM
 ↓
Answer
```

Agentic RAG:

```text
Question
 ↓
Agent
 ↓
Decide whether retrieval is needed
 ↓
Retriever
 ↓
Evaluate results
 ↓
Maybe search again
 ↓
Maybe use another tool
 ↓
Reason
 ↓
Answer/action
```

This is a major distinction.

---

# 55. Example of Agentic Retrieval

User:

> "Can I take 10 days of leave and work remotely from another country during that period according to company policy?"

The agent might need:

```text
1. Leave policy
2. Remote work policy
3. International work policy
```

It can perform:

```text
Search 1 → Leave policy
Search 2 → Remote work policy
Search 3 → International work policy
```

Then combine the evidence.

That's much more agentic than a single fixed retrieval call.

---

# 56. The most important conceptual hierarchy

Memorize this:

```text
RETRIEVAL
│
├── Dense Retrieval
│     └── Embeddings + Vector Search
│
├── Sparse Retrieval
│     └── BM25
│
├── Hybrid Retrieval
│     └── Dense + Sparse
│
├── Filtering
│     └── Metadata
│
└── Reranking
      └── Reorder retrieved candidates
```

This is essentially your entire Level 21.

---

# 57. Dense vs Sparse vs Hybrid — interview answer

If an interviewer asks:

> "What's the difference between dense and sparse retrieval?"

Give this answer:

> **Dense retrieval represents queries and documents as dense embedding vectors and retrieves them based on semantic similarity. Sparse retrieval, such as BM25, relies more on lexical term matching and term importance. Dense retrieval is strong for semantic similarity and paraphrases, while sparse retrieval is often strong for exact keywords, rare terms, IDs, and error codes. Hybrid retrieval combines both approaches to improve overall retrieval quality.**

That's an excellent interview answer.

---

# 58. Retriever vs Reranker — interview answer

> **A retriever performs the initial search over a large corpus and prioritizes speed and recall, producing a candidate set. A reranker then evaluates those candidates more deeply and reorders them to improve precision. A common architecture is retrieve Top-50, rerank them, and pass the best Top-5 to the LLM.**

Remember:

```text
Retriever → Recall
Reranker → Precision
```

It's a useful simplification, not an absolute rule.

---

# 59. "Why not just use the reranker?"

Excellent interview question.

Because a reranker is generally more computationally expensive.

You don't want:

```text
1,000,000 documents
       ↓
Expensive reranker
       ↓
Answer
```

Instead:

```text
1,000,000
    ↓
Fast retriever
    ↓
100
    ↓
Reranker
    ↓
5
```

This is why two-stage retrieval exists.

---

# 60. "Why hybrid search?"

Answer:

> **Because semantic and lexical retrieval solve different problems. Dense retrieval captures meaning and paraphrases, while sparse retrieval captures exact terms and rare tokens. Combining them can improve robustness across different query types.**

---

# 61. "What if retrieval is poor?"

Strong answer:

> "I'd evaluate retrieval separately from generation. I'd inspect chunking, embedding quality, Top-K, metadata filters, similarity thresholds, dense versus sparse retrieval, hybrid weighting, and reranking. I'd use retrieval metrics such as Recall@K, MRR, or NDCG and inspect actual retrieved chunks for representative queries."

That's an **AI engineer answer**, not merely an LLM-user answer.

---

# 62. Interview Scenario 🔥

### Interviewer:

> "Your RAG system returns correct information, but it's often ranked 8th. The system only sends the top 5 results to the LLM. What would you do?"

You should say:

```text
Increase candidate retrieval K
        ↓
Retrieve Top-20 or Top-50
        ↓
Rerank candidates
        ↓
Select Top-5
```

Potentially also investigate:

```text
Hybrid retrieval
Embedding quality
Chunking
Metadata filtering
```

Excellent.

---

# 63. Another interview scenario

### Interviewer:

> "Users search for product IDs and error codes, but your vector search performs poorly. Why?"

Answer:

> "Dense semantic retrieval isn't always ideal for exact identifiers and rare lexical terms. I'd evaluate sparse retrieval such as BM25 and potentially use hybrid retrieval so that exact keyword matching complements semantic similarity."

---

# 64. Another interview scenario

### Interviewer:

> "Should you always use hybrid search?"

No.

Say:

> "Not necessarily. It depends on the query distribution and corpus. If semantic similarity dominates and the data doesn't contain many exact-match terms, dense retrieval may be enough. If the corpus contains technical identifiers, codes, names, or exact terminology, hybrid search can be valuable. I'd evaluate it empirically."

That's the kind of nuanced answer interviewers like.

---

# 65. Your complete Level 21 mental model

You should now be able to visualize:

```text
                        USER
                         ↓
                    Query
                         ↓
                Query Processing
                         ↓
              ┌──────────┴──────────┐
              ↓                     ↓
        Dense Retrieval       Sparse Retrieval
              ↓                     ↓
       Embedding Search             BM25
              ↓                     ↓
              └──────────┬──────────┘
                         ↓
                    Hybrid/Fusion
                         ↓
                 Metadata Filtering
                         ↓
                    Candidate Set
                         ↓
                      Reranker
                         ↓
                       Top-K
                         ↓
                 Relevant Context
                         ↓
                       Agent
                         ↓
              ┌──────────┴──────────┐
              ↓                     ↓
             Tools                Memory
              ↓                     ↓
              └──────────┬──────────┘
                         ↓
                        LLM
                         ↓
                      Answer
```

---

# 🎯 LEVEL 21 — What you MUST know

Before moving on, make sure these are clear:

### 🔥🔥🔥 Absolutely mandatory

```text
☑ What is retrieval?
☑ What is a retriever?
☑ Retriever vs vector database
☑ Similarity search
☑ Top-K
☑ Metadata filtering
☑ Dense retrieval
☑ Sparse retrieval
☑ BM25
☑ Dense vs sparse
☑ Hybrid search
☑ Reranking
☑ Retriever vs reranker
☑ Two-stage retrieval
```

### 🔥 Important

```text
☑ Precision
☑ Recall
☑ Recall@K
☑ MRR
☑ NDCG
☑ Similarity threshold
☑ Query rewriting
☑ Multi-query retrieval
☑ Parent-child retrieval
☑ Contextual retrieval
☑ Retrieval failure analysis
```

### Know conceptually

```text
☑ Result fusion
☑ Weighted hybrid search
☑ Reciprocal Rank Fusion
```

---

# 🧠 The 10-second memory trick

Remember this:

```text
RETRIEVAL
   ↓
"Find useful information"

DENSE
   ↓
"Find similar meaning"

SPARSE / BM25
   ↓
"Find matching words"

HYBRID
   ↓
"Meaning + words"

TOP-K
   ↓
"How many candidates?"

FILTER
   ↓
"Which subset?"

RERANKER
   ↓
"Which candidates are actually best?"
```

And the production pattern:

```text
                    1M Documents
                         ↓
                Fast Retrieval
              Dense + Sparse/BM25
                         ↓
                     Top-50
                         ↓
                    Reranker
                         ↓
                      Top-5
                         ↓
                       LLM
```

## 🔥 The single most important thing to take away

**Don't think of RAG retrieval as simply "search the vector database."**

Modern retrieval is often a pipeline:

> **Query → retrieve candidates → filter/fuse → rerank → select context → give it to the LLM/agent.**

Once you understand that pipeline, **LangChain's retrievers, vector stores, BM25 retrievers, ensemble/hybrid retrievers, and rerankers will become much easier to understand instead of feeling like random APIs.**

Your next logical level after this should be **LEVEL 22 — RAG (Retrieval-Augmented Generation)**, where we put **chunking + embeddings + vector DB + retrieval + reranking + LLM** together into a complete RAG architecture and then implement it in Python.
