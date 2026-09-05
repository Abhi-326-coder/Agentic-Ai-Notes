import chromadb

client = chromadb.Client()

collection = client.create_collection(
    name="documents"
)

collection.add(
    documents=[
        "Employees receive 20 days of annual leave.",
        "Engineering teams have weekly on-call rotations.",
        "Password resets require email verification."
    ],
    ids=["doc1", "doc2", "doc3"]
)

result = collection.query(
    query_texts=["How many vacation days do employees get?"],
    n_results=2
)

print(result)