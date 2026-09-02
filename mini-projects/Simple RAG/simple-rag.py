from collections import Counter
import math




documents = [
    "Students must maintain at least 75 percent attendance.",
    "The final examination contributes 60 percent of total marks.",
    "The library is open from 8 AM to 8 PM.",
    "Students can borrow five books from the library."
]

def tokenize(text):
    return text.lower().split()


def vectorize(text, vocabulary):
    words = tokenize(text)
    counts = Counter(words)

    return [counts[word] for word in vocabulary]


vocabulary = sorted(
    set(
        word
        for document in documents
        for word in tokenize(document)
    )
)


vectors = [
    vectorize(document, vocabulary)
    for document in documents
]



def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))

    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(x * x for x in b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot / (magnitude_a * magnitude_b)


query = "What attendance percentage is required?"

query_vector = vectorize(query, vocabulary)

scores = []

for document, vector in zip(documents, vectors):
    score = cosine_similarity(query_vector, vector)
    scores.append((score, document))


scores.sort(reverse=True)

for score, document in scores:
    print(score, document)