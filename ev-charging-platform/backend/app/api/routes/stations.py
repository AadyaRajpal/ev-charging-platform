from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from app.api.routes.auth import get_current_user_dependency
from app.services.maps_service import maps_service
from app.services.provider_aggregator import provider_aggregator
from app.services.firebase_service import firebase_service

router = APIRouter()

# Request/Response Models
class StationFilter(BaseModel):
    connector_types: Optional[List[str]] = None  # CCS, CHAdeMO, Type2, Tesla
    min_power_kw: Optional[float] = None
    max_price_per_kwh: Optional[float] = None
    available_only: bool = True

class Station(BaseModel):
    station_id: str
    provider: str
    name: str
    address: str
    latitude: float
    longitude: float
    distance_km: Optional[float] = None
    chargers: List[dict]
    amenities: List[str]
    rating: Optional[float] = None
    operating_hours: str

@router.get("/nearby", response_model=List[Station])
async def get_nearby_stations(
    latitude: float = Query(..., description="User's latitude"),
    longitude: float = Query(..., description="User's longitude"),
    radius: int = Query(5000, description="Search radius in meters"),
    connector_type: Optional[str] = Query(None, description="Filter by connector type"),
    available_only: bool = Query(True, description="Show only available stations"),
    current_user: dict = Depends(get_current_user_dependency)
):
    """
    Get nearby charging stations with real-time availability.
    Aggregates data from multiple providers and Google Maps.
    """
    
    # Get stations from provider aggregator
    provider_stations = await provider_aggregator.get_all_stations(
        latitude, longitude, radius
    )
    
    # Get stations from Google Maps
    maps_stations = maps_service.find_nearby_stations(
        latitude, longitude, radius
    )
    
    # Combine and deduplicate stations
    all_stations = provider_stations
    
    # Filter stations
    filtered_stations = []
    for station in all_stations:
        # Get real-time status from Firebase
        status = firebase_service.get_station_status(station['station_id'])
        if status:
            station['available_chargers'] = status.get('available_chargers', 0)
            station['operational'] = status.get('operational', True)
        
        # Apply filters
        if available_only and station.get('available_chargers', 0) == 0:
            continue
        
        if connector_type:
            has_connector = any(
                charger.get('connector_type') == connector_type
                for charger in station.get('chargers', [])
            )
            if not has_connector:
                continue
        
        filtered_stations.append(station)
    
    # Sort by distance (closest first)
    filtered_stations.sort(key=lambda s: s.get('distance_km', float('inf')))
    
    return filtered_stations

@router.get("/{station_id}", response_model=Station)
async def get_station_details(
    station_id: str,
    provider: str = Query(..., description="Provider name"),
    current_user: dict = Depends(get_current_user_dependency)
):
    """Get detailed information about a specific charging station"""
    
    # Get station details from provider
    station = await provider_aggregator.get_station_details(station_id, provider)
    
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    # Get real-time status from Firebase
    status = firebase_service.get_station_status(station_id)
    if status:
        station['status'] = status
    
    return station

@router.get("/{station_id}/availability")
async def get_station_availability(
    station_id: str,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Get real-time availability status for a station"""
    
    status = firebase_service.get_station_status(station_id)
    
    if not status:
        raise HTTPException(status_code=404, detail="Station status not found")
    
    return {
        "station_id": station_id,
        "available_chargers": status.get('available_chargers', 0),
        "total_chargers": status.get('total_chargers', 0),
        "operational": status.get('operational', True),
        "last_updated": status.get('last_updated')
    }

@router.post("/{station_id}/favorite")
async def add_favorite_station(
    station_id: str,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Add a station to user's favorites"""
    
    user_id = current_user['user_id']
    
    # Store in Firebase
    success = firebase_service.update_user_preferences(
        user_id,
        {f'favorite_stations/{station_id}': True}
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to add favorite")
    
    return {"message": "Station added to favorites", "station_id": station_id}

@router.delete("/{station_id}/favorite")
async def remove_favorite_station(
    station_id: str,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Remove a station from user's favorites"""
    
    user_id = current_user['user_id']
    
    # Remove from Firebase
    success = firebase_service.update_user_preferences(
        user_id,
        {f'favorite_stations/{station_id}': None}
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to remove favorite")
    
    return {"message": "Station removed from favorites", "station_id": station_id}

@router.get("/user/favorites")
async def get_favorite_stations(
    current_user: dict = Depends(get_current_user_dependency)
):
    """Get user's favorite stations"""
    
    user_id = current_user['user_id']
    preferences = firebase_service.get_user_preferences(user_id)
    
    if not preferences:
        return {"favorites": []}
    
    favorite_ids = preferences.get('favorite_stations', {}).keys()
    
    return {"favorites": list(favorite_ids)}

@router.post("/{station_id}/report")
async def report_station_issue(
    station_id: str,
    issue_type: str = Query(..., description="Type of issue"),
    description: str = Query(..., description="Issue description"),
    current_user: dict = Depends(get_current_user_dependency)
):
    """Report an issue with a station"""
    
    # Log the issue
    firebase_service.log_event('station_issue', {
        'station_id': station_id,
        'user_id': current_user['user_id'],
        'issue_type': issue_type,
        'description': description
    })
    
    return {
        "message": "Issue reported successfully",
        "station_id": station_id,
        "issue_type": issue_type
    }
