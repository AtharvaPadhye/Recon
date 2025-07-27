from fastapi import FastAPI
from .routers import events, cases, tasks

app = FastAPI(title="Recon API")

app.include_router(events.router)
app.include_router(cases.router)
app.include_router(tasks.router)
