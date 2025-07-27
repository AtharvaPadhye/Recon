from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import events, cases, tasks, entities

app = FastAPI(title="Recon API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "file://"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router)
app.include_router(cases.router)
app.include_router(tasks.router)
app.include_router(entities.router)
