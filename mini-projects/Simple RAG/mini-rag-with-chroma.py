import chromadb

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="company_docs"
)


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

results = collection.query(
    query_texts=[
        "How many vacation days do employees get?"
    ],
    n_results=2
)

print(results["documents"])