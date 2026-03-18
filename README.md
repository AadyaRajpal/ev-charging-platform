# EV Charging Aggregator

A web app to find nearby EV charging stations using real-time data from Open Charge Map.

## Tech Stack

- **Backend** — Python, FastAPI
- **Frontend** — HTML, CSS, JavaScript
- **Map** — Leaflet + OpenStreetMap
- **Data** — Open Charge Map API

## Features

- Search EV stations by location and radius
- Interactive map with clickable markers
- Station details — connector types, availability status, operator
- "Use My Location" for quick search

## Project Structure

```
ev-charging-platform/
├── backend/
│   ├── main.py           # FastAPI server
│   └── requirements.txt
└── frontend/
    └── index.html        # Single-page web app
```

## Setup

**Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend**

Open `frontend/index.html` in your browser. No build step required.

## API

`GET /stations?lat={lat}&lng={lng}&radius={km}&max_results={n}`

Returns a list of nearby EV charging stations with location, status, and connector info.
