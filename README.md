# EV Charging Aggregator

A minimal, working EV station finder. FastAPI backend + React (plain HTML) frontend.
Uses the [Open Charge Map API](https://openchargemap.org) for real station data.

## Project Structure

```
ev-charging-platform/
├── backend/
│   ├── main.py           # FastAPI app — /stations endpoint
│   └── requirements.txt
└── frontend/
    └── index.html        # React-style single-page app
```

## Running the Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

API runs at: http://localhost:8000
Docs at: http://localhost:8000/docs

## Running the Frontend

Just open `frontend/index.html` in your browser. No build step needed.

## API Endpoint

### GET /stations
Returns nearby EV charging stations from Open Charge Map.

**Query params:**
| Param | Type | Default | Description |
|---|---|---|---|
| lat | float | required | Latitude |
| lng | float | required | Longitude |
| radius | int | 10 | Search radius in km |
| max_results | int | 20 | Max stations to return |

**Example:**
```
GET /stations?lat=12.9716&lng=77.5946&radius=10
```

## Future Integrations (not yet built)
- Firebase auth
- Stripe payments
- Real-time availability via WebSockets
