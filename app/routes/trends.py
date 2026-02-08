from fastapi import APIRouter
from ..services.embedding_service import df

router = APIRouter()

@router.get("/trends")
def trends():
    return {
        "by_domain": df["domain"].value_counts().to_dict(),
        "by_year": df["Year"].value_counts().sort_index().to_dict(),
        "by_technology": df["technologies"].str.split(",").explode().value_counts().to_dict()
    }
