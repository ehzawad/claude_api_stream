# Define the paragraphs and specific sentences
paragraph1 = """
In the heart of the bustling city, the gentle hum of morning traffic begins to swell. Commuters weave through the streets, their steps hurried and purposeful under the soft glow of the rising sun. At a small corner cafe, a barista steams milk, the frothy sound blending with the morning's murmurs. Nearby, a street artist lays out her vibrant canvases, each a splash of color more vivid than the last. The scent of rain still lingers from the night's downpour, mingling with the crispness of a new day. A dog barks in the distance, eager for its morning walk. As the city awakens, its symphony of sounds and smells creates a tapestry of urban life. The rhythm of the city, with its predictable unpredictability, comforts the residents who call it home. A dog barks in the distance, eager for its morning walk.
"""

paragraph2 = """
In the heart of the bustling city, the gentle hum of morning traffic begins to swell. Commuters weave through the streets, their steps hurried and purposeful under the soft glow of the rising sun. At the central park, joggers hit their stride, the tap of sneakers on pavement in sync with the city's pulse. A dog barks in the distance, eager for its morning walk. At a small corner cafe, a barista steams milk, the frothy sound blending with the morning's murmurs. A dog barks in the distance, eager for its morning walk. Office buildings flicker to life as workers arrive, their reflections shimmering against the glass facades. The rhythm of the city, with its predictable unpredictability, comforts the residents who call it home. Nearby, a street artist lays out her vibrant canvases, each a splash of color more vivid than the last. The early bus rumbles down the avenue, its doors opening to welcome the day's first passengers. The scent of rain still lingers from the night's downpour, mingling with the crispness of a new day. The scent of rain still lingers from the night's downpour, mingling with the crispness of a new day.
"""

sentences = [
    "A dog barks in the distance, eager for its morning walk.",
    "The scent of rain still lingers from the night's downpour, mingling with the crispness of a new day."
]

# Function to get embeddings
def get_embeddings(texts):
    response = client.embeddings.create(input=texts, model="text-embedding-3-small")
    return [embedding.embedding for embedding in response.data]

# Function to calculate cosine similarity
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# Compute embeddings for the paragraphs and sentences
paragraph_embeddings = get_embeddings([paragraph1, paragraph2])
sentence_embeddings = get_embeddings(sentences)

# Extract embeddings from response
embeddings_p1 = np.array(paragraph_embeddings[0])
embeddings_p2 = np.array(paragraph_embeddings[1])
embeddings_s1 = np.array(sentence_embeddings[0])
embeddings_s2 = np.array(sentence_embeddings[1])

# Calculate similarities within each paragraph
similarity_s1_p1 = cosine_similarity(embeddings_p1, embeddings_s1)
similarity_s2_p1 = cosine_similarity(embeddings_p1, embeddings_s2)
similarity_s1_p2 = cosine_similarity(embeddings_p2, embeddings_s1)
similarity_s2_p2 = cosine_similarity(embeddings_p2, embeddings_s2)

# Calculate similarity between paragraphs
paragraph_similarity = cosine_similarity(embeddings_p1, embeddings_p2)

# Output results
print("Embedding vector for paragraph 1:")
print(embeddings_p1)
print("\nEmbedding vector for paragraph 2:")
print(embeddings_p2)
print("\nEmbedding vector for sentence 1:")
print(embeddings_s1)
print("\nEmbedding vector for sentence 2:")
print(embeddings_s2)
print("\nSimilarity of sentence 1 to paragraph 1:", similarity_s1_p1)
print("Similarity of sentence 2 to paragraph 1:", similarity_s2_p1)
print("Similarity of sentence 1 to paragraph 2:", similarity_s1_p2)
print("Similarity of sentence 2 to paragraph 2:", similarity_s2_p2)
print("\nSimilarity between paragraphs:", paragraph_similarity)
