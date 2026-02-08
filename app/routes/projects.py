# routes/projects.py
from fastapi import APIRouter, Query
from ..services.embedding_service import df

router = APIRouter()

@router.get("/projects")
def get_projects(
    domain: str = Query(None),
    technology: str = Query(None),
    year: int = Query(None),
    difficulty: str = Query(None),
    hardware_required: bool = Query(None)
):
    data = df.copy()

    # domain filter
    if domain and "domain" in data.columns:
        data = data[data["domain"].str.lower() == domain.lower()]

    # technology filter
    if technology and "technologies" in data.columns:
        data = data[data["technologies"].str.lower().str.contains(technology.lower())]

    # year filter
    if year and "Year" in data.columns:
        data = data[data["Year"] == year]

    # difficulty filter – optional
    if difficulty and "difficulty" in data.columns:
        data = data[data["difficulty"].str.lower() == difficulty.lower()]

    # hardware_required filter – optional
    if hardware_required is not None and "hardware_required" in data.columns:
        data = data[data["hardware_required"] == hardware_required]

    # Return JSON
    return data.to_dict(orient="records")
