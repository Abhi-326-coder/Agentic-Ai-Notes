from pathlib import Path

documents = []

folder = Path(__file__).resolve().parent / "knowledge"

for file_path in folder.glob("*.txt"):
    text = file_path.read_text(encoding="utf-8")

    document = {
        "page_content": text,
        "metadata": {
            "source": file_path.name
        }
    }
    print(file_path)

    documents.append(document)


for document in documents:
    print(document)
    
def split_text(text, chunk_size=100):
    return [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
    ]


chunks = []

for document in documents:
    pieces = split_text(document["page_content"])

    for piece in pieces:
        chunks.append({
            "page_content": piece,
            "metadata": document["metadata"]
        })

print(f"Loaded {len(documents)} documents and created {len(chunks)} chunks.")
print(chunks)
