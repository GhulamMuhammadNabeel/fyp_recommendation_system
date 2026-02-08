# routes/personalized_recommendations.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from ..services.embedding_service import df, embeddings
from sentence_transformers import SentenceTransformer
router = APIRouter()

from dotenv import load_dotenv
import os
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")


# For private models, use use_auth_token
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", use_auth_token=os.getenv("HF_TOKEN"))

# Request schema
class UserProfile(BaseModel):
    skills: List[str]
    interests: List[str]
    difficulty: str = None
    hardware_required: bool = None
    top_k: int = 5

@router.post("/personalized_recommendations")
def personalized_recommendations(profile: UserProfile):
    # 1️⃣ Combine skills + interests
    combined_text = " ".join(profile.skills + profile.interests)

    # 2️⃣ Embed user profile
    user_vec = model.encode([combined_text], normalize_embeddings=True)

    # 3️⃣ Compute cosine similarity with all embeddings
    sims = cosine_similarity(user_vec, embeddings)[0]

    # 4️⃣ Start with full dataframe
    filtered_df = df.copy()

    # 5️⃣ Apply optional filters only if user passed them
    if profile.difficulty and "difficulty" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["difficulty"].str.lower() == profile.difficulty.lower()]

    if profile.hardware_required is not None and "hardware_required" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["hardware_required"] == profile.hardware_required]

    # 6️⃣ Recompute similarity after filtering
    if filtered_df.empty:
        return []  # return empty list if no projects match filters

    filtered_embeddings = embeddings[filtered_df.index]
    filtered_sims = cosine_similarity(user_vec, filtered_embeddings)[0]

    # 7️⃣ Pick top-K projects
    top_indices = filtered_sims.argsort()[::-1][:profile.top_k]

    results = filtered_df.iloc[top_indices].copy()
    results["similarity_score"] = filtered_sims[top_indices]

    return results.to_dict(orient="records")
