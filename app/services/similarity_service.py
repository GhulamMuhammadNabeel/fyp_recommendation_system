from sklearn.metrics.pairwise import cosine_similarity
from .embedding_service import embeddings, df

def get_similar_projects(index, top_k=5):
    query_vec = embeddings[index].reshape(1, -1)
    sims = cosine_similarity(query_vec, embeddings)[0]

    top_idx = sims.argsort()[::-1][1:top_k+1]

    results = df.iloc[top_idx].copy()
    results["similarity_score"] = sims[top_idx]

    return results
