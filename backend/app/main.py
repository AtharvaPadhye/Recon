from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .routers import events, cases, tasks, entities

app = FastAPI(title="Recon API")

app.include_router(events.router)
app.include_router(cases.router)
app.include_router(tasks.router)
app.include_router(entities.router)

# Serve the simple frontend bundled in the repository. Using an absolute path
# allows running the application from any working directory.
frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
