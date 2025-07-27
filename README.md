# Recon

A starting framework for a recon data ingestion and tasking API. This repository includes a minimal FastAPI backend with in-memory storage that demonstrates how events, cases, and recon tasking requests can be handled.

## Folder Structure

```
backend/
  app/
    main.py            # FastAPI application
    models.py          # Pydantic models
    routers/
      events.py        # /v1/events endpoint
      cases.py         # /v1/cases endpoint
      tasks.py         # /v1/task_recon endpoint
  requirements.txt     # Python dependencies
```

## Running the API

1. Install dependencies (preferably in a virtual environment):

```bash
pip install -r backend/requirements.txt
```

2. Start the development server:

```bash
uvicorn backend.app.main:app --reload
```

The API will be available at `http://localhost:8000` and includes automatic Swagger UI documentation at `http://localhost:8000/docs`.

## Example Endpoints

You can test the API using `curl`, Postman or any HTTP client.

### 1. Ingest an event
```bash
curl -X POST http://localhost:8000/v1/events \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "osint",
    "source_id": "telegram_watchdog",
    "timestamp": "2025-07-25T10:00:00Z",
    "location": { "lat": 34.05, "lon": -118.25 },
    "summary": "Unusual troop movement near highway"
  }'
```

### 2. Create a case
```bash
curl -X POST http://localhost:8000/v1/cases \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Possible Convoy Movement",
    "location": { "lat": 34.05, "lon": -118.25 },
    "initial_event_id": "YOUR_EVENT_ID_HERE"
  }'
```

### 3. Task a recon asset
```bash
curl -X POST http://localhost:8000/v1/task_recon \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "YOUR_CASE_ID_HERE",
    "sensor_types": ["optical"],
    "urgency": "high",
    "preferred_assets": ["uav"]
  }'
```

### 4. View all active cases
```bash
curl http://localhost:8000/v1/cases
```

These endpoints provide a basic demonstration and can be expanded with persistent storage, authentication, additional sensors or a frontend for visualization.
