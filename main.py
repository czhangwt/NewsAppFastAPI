"""Folder Structure
    config: setting files
    routers: api endpoints
    models: database models
    schemas: data validation models
    utils: utility functions
"""
from fastapi import FastAPI
from routers import news
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# register routers in the main app for better organization
app.include_router(news.router)

# enable cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # allowed origins, default is [*] for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

