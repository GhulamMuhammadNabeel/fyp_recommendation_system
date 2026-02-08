# routes/chatbot.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from ..services.embedding_service import df, embeddings
from sentence_transformers import SentenceTransformer
import requests, threading, re, time

router = APIRouter()
from dotenv import load_dotenv
import os
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", use_auth_token=os.getenv("HF_TOKEN"))


# ---------------- LONGCAT CONFIG ---------------- #
api_keys = os.getenv("LONGCAT_API_KEYS").split(",")
LONGCAT_URL = "https://api.longcat.chat/openai/v1/chat/completions"
api_index = 0
lock = threading.Lock()
MAX_WORKERS = 6
SLEEP_BETWEEN_CALLS = 0.5

# ---------------- PROMPT BUILDER ---------------- #
def build_prompt(context_text, user_message):
    return f"""
You are an intelligent assistant for recommending final year projects.
Use the following project context to answer the user's question.
Provide a concise, helpful, conversational answer.

Project Context:
{context_text}

User Question:
{user_message}
"""

# ---------------- LONGCAT API CALL ---------------- #
def call_longcat(prompt):
    global api_index
    for _ in range(len(api_keys)):
        with lock:
            api_key = api_keys[api_index]
            api_index = (api_index + 1) % len(api_keys)

        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "LongCat-Flash-Chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0
        }

        try:
            response = requests.post(LONGCAT_URL, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                text = response.json()["choices"][0]["message"]["content"].strip()
                text_clean = re.sub(r"[^\w\s,.-]", "", text)
                text_clean = re.sub(r"\s{2,}", " ", text_clean).strip()
                return text_clean if text_clean else None
        except Exception as e:
            print("API error:", e)
        time.sleep(SLEEP_BETWEEN_CALLS)
    return "Sorry, I couldn't process your request right now."

# ---------------- REQUEST MODEL ---------------- #
class ChatRequest(BaseModel):
    user_message: str
    conversation_history: List[dict] = []
    top_k: int = 5

# ---------------- CHATBOT ENDPOINT ---------------- #
@router.post("/chatbot")
def chatbot(req: ChatRequest):
    # 1️⃣ Embed user query
    query_vec = model.encode([req.user_message], normalize_embeddings=True)

    # 2️⃣ Retrieve top-K relevant projects
    sims = cosine_similarity(query_vec, embeddings)[0]
    top_indices = sims.argsort()[::-1][:req.top_k]
    top_projects = df.iloc[top_indices].copy()
    top_projects["similarity_score"] = sims[top_indices]

    # 3️⃣ Build context string for LongCat
    context_text = ""
    for i, row in top_projects.iterrows():
        context_text += f"- {row['title']}: {row['abstract']}\n"

    # 4️⃣ Build prompt with user message
    prompt = build_prompt(context_text, req.user_message)

    # 5️⃣ Call LongCat API
    bot_response = call_longcat(prompt)

    return {
        "bot_response": bot_response,
        "recommended_projects": top_projects.to_dict(orient="records")
    }
