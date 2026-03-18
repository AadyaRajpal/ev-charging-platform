from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import Optional

app = FastAPI(title="EV Charging Aggregator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OCM_API_URL = "https://api.openchargemap.io/v3/poi"
OCM_API_KEY = "84fda41f-df34-4e76-9f24-ac91ca337584"


@app.get("/")
def root():
    return {"status": "EV Charging API is running"}


@app.get("/stations")
async def get_stations(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    radius: int = Query(10, description="Search radius in km"),
    max_results: int = Query(20, description="Max number of results"),
):
    params = {
        "output": "json",
        "latitude": lat,
        "longitude": lng,
        "distance": radius,
        "distanceunit": "km",
        "maxresults": max_results,
        "compact": True,
        "verbose": False,
        "levelid": "1,2,3",
        "key":"84fda41f-df34-4e76-9f24-ac91ca337584" ,   # All charge levels
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.get(OCM_API_URL, params=params)
            response.raise_for_status()
            raw = response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Open Charge Map API error: {str(e)}")

    stations = []
    for s in raw:
        addr = s.get("AddressInfo", {})
        connections = s.get("Connections", [])

        # Extract connector types
        connector_types = []
        for c in connections:
            ct = c.get("ConnectionType", {})
            if ct and ct.get("Title"):
                title = ct["Title"]
                if title not in connector_types:
                    connector_types.append(title)

        # Determine operational status
        status_type = s.get("StatusType", {})
        if status_type:
            is_operational = status_type.get("IsOperational", True)
            status_label = "Available" if is_operational else "Unavailable"
        else:
            status_label = "Unknown"

        # Extract operator name
        operator = s.get("OperatorInfo", {})
        operator_name = operator.get("Title", "Unknown Operator") if operator else "Unknown Operator"

        stations.append({
            "id": s.get("ID"),
            "name": addr.get("Title", "Unnamed Station"),
            "address": addr.get("AddressLine1", ""),
            "city": addr.get("Town", ""),
            "state": addr.get("StateOrProvince", ""),
            "country": addr.get("Country", {}).get("ISOCode", "") if addr.get("Country") else "",
            "lat": addr.get("Latitude"),
            "lng": addr.get("Longitude"),
            "operator": operator_name,
            "status": status_label,
            "connectors": connector_types,
            "num_points": s.get("NumberOfPoints") or len(connections),
            "usage_cost": s.get("UsageCost", "Not specified"),
        })

    return {"count": len(stations), "stations": stations}
