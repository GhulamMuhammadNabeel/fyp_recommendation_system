from fastapi import FastAPI
from .routes import projects, recommend, search, trends,personalized_recommendations,chatbot
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI(title="Intelligent FYP Recommendation System")

origins = [
    "http://localhost:3000",  # frontend dev URL
    "http://127.0.0.1:3000",
    "*",  # optional, dev only: allows all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(projects.router)
app.include_router(recommend.router)
app.include_router(search.router)
app.include_router(trends.router)
app.include_router(chatbot.router)
app.include_router(personalized_recommendations.router)
