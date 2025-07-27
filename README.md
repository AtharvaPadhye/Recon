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

### Docker

Build the image and run the API without installing Python locally:

```bash
docker build -t recon-api .
docker run --rm -p 8000:8000 recon-api
```

The API will be available at `http://localhost:8000` and includes automatic Swagger UI documentation at `http://localhost:8000/docs`.

Cross-origin requests from `http://localhost:8000` and pages served via `file://` are allowed so the included frontend can communicate with the API.

## Example Endpoints

You can test the API using `curl`, Postman or any HTTP client.

### 1. Ingest an event
```bash
curl -X POST http://localhost:8000/v1/events \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "osint",
    "source_id": "telegram_watchdog",
    "timestamp": "2025-07-25T10:00:00Z",  # ISO 8601 datetime
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
# created_date and updated_date are automatically set by the server

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

Allowed sensor types are `optical`, `infrared`, and `radar`. Urgency levels can
be `low`, `medium`, or `high`.

### 4. View all active cases
```bash
curl http://localhost:8000/v1/cases
```

### 5. List all events
```bash
curl http://localhost:8000/v1/events
```

### 6. List all recon tasks
```bash
curl http://localhost:8000/v1/task_recon
```

### 7. List tasks for a case
```bash
curl http://localhost:8000/v1/task_recon/case/{CASE_ID}
```
### 8. Access case entities
```bash
curl http://localhost:8000/entities/Case
curl http://localhost:8000/entities/Case/{CASE_ID}
```

These endpoints provide a basic demonstration and can be expanded with persistent storage, authentication, additional sensors or a frontend for visualization. Each collection supports standard CRUD operations (create, read, update and delete) for events, cases and tasks.

## Running Tests

`pytest` is used for automated tests located in the `tests/` directory. After installing the dependencies, simply run:

```bash
pytest
```

## Frontend

A simple HTML/JavaScript interface is provided in `frontend/` for interacting with the
Cases API.

1. Start the backend API as described above.
2. Open `frontend/index.html` in your web browser.

From the page you can create, edit and delete cases. The frontend expects the
backend to be available at `http://localhost:8000`.
