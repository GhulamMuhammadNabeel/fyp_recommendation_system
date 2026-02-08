from fastapi import APIRouter
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from ..services.embedding_service import embeddings, df

router = APIRouter()
from dotenv import load_dotenv
import os
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", use_auth_token=os.getenv("HF_TOKEN"))

@router.post("/search")
def search(query: str, top_k: int = 5):
    q_vec = model.encode([query], normalize_embeddings=True)
    sims = cosine_similarity(q_vec, embeddings)[0]

    top_idx = sims.argsort()[::-1][:top_k]
    results = df.iloc[top_idx].copy()
    results["similarity_score"] = sims[top_idx]

    return results.to_dict(orient="records")
