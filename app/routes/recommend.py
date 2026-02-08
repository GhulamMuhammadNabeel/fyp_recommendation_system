from fastapi import APIRouter, HTTPException
from ..services.similarity_service import get_similar_projects
from ..services.embedding_service import df

router = APIRouter()

@router.post("/recommendations")
def recommend(project_title: str, top_k: int = 5):

    if project_title not in df["title"].values:
        raise HTTPException(status_code=404, detail="Project not found")

    idx = df[df["title"] == project_title].index[0]
    results = get_similar_projects(idx, top_k)

    return results.to_dict(orient="records")
