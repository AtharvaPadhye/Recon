# Available API Endpoints

Examples for using the Recon API.

## 1. Ingest an Event
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

## 2. Create a Case
```bash
curl -X POST http://localhost:8000/v1/cases \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Possible Convoy Movement",
    "location": { "lat": 34.05, "lon": -118.25 },
    "initial_event_id": "YOUR_EVENT_ID_HERE"
  }'
```

## 3. Task a Recon Asset
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

## 4. View All Active Cases
```bash
curl http://localhost:8000/v1/cases
```

---

Future plans include Swagger UI, a frontend dashboard, and additional API endpoints.
