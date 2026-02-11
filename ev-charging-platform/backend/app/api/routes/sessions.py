from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.api.routes.auth import get_current_user_dependency
from app.services.firebase_service import firebase_service
from app.services.provider_aggregator import provider_aggregator

router = APIRouter()

# Request/Response Models
class SessionStart(BaseModel):
    station_id: str
    charger_id: str
    provider: str
    estimated_kwh: Optional[float] = None

class SessionStop(BaseModel):
    session_id: str
    provider: str

class Session(BaseModel):
    session_id: str
    user_id: str
    station_id: str
    charger_id: str
    provider: str
    status: str
    started_at: str
    ended_at: Optional[str] = None
    energy_delivered_kwh: Optional[float] = None
    duration_minutes: Optional[int] = None
    total_cost: Optional[float] = None

@router.post("/start", response_model=Session)
async def start_charging_session(
    session_data: SessionStart,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Start a new charging session"""
    
    user_id = current_user['user_id']
    
    # Start session with provider
    provider_session = await provider_aggregator.start_charging_session(
        session_data.station_id,
        session_data.charger_id,
        session_data.provider,
        user_id
    )
    
    if not provider_session:
        raise HTTPException(
            status_code=400,
            detail="Failed to start charging session with provider"
        )
    
    session_id = provider_session['session_id']
    
    # Create session in Firebase
    firebase_data = {
        'user_id': user_id,
        'station_id': session_data.station_id,
        'charger_id': session_data.charger_id,
        'provider': session_data.provider,
        'started_at': provider_session['started_at'],
        'estimated_kwh': session_data.estimated_kwh
    }
    
    success = firebase_service.create_session(session_id, firebase_data)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create session record")
    
    # Update charger availability
    firebase_service.update_charger_availability(
        session_data.station_id,
        session_data.charger_id,
        is_available=False
    )
    
    # Send notification
    firebase_service.send_notification(
        user_id,
        {
            'type': 'session_started',
            'title': 'Charging Started',
            'message': f'Your charging session has started at {session_data.station_id}',
            'session_id': session_id
        }
    )
    
    return {
        "session_id": session_id,
        "user_id": user_id,
        "station_id": session_data.station_id,
        "charger_id": session_data.charger_id,
        "provider": session_data.provider,
        "status": "active",
        "started_at": provider_session['started_at']
    }

@router.post("/{session_id}/stop")
async def stop_charging_session(
    session_id: str,
    provider: str,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Stop an active charging session"""
    
    user_id = current_user['user_id']
    
    # Stop session with provider
    provider_session = await provider_aggregator.stop_charging_session(
        session_id,
        provider
    )
    
    if not provider_session:
        raise HTTPException(
            status_code=400,
            detail="Failed to stop charging session with provider"
        )
    
    # Update session in Firebase
    end_data = {
        'ended_at': provider_session['ended_at'],
        'energy_delivered_kwh': provider_session.get('energy_delivered_kwh'),
        'duration_minutes': provider_session.get('duration_minutes')
    }
    
    success = firebase_service.end_session(session_id, end_data)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update session record")
    
    # Get session details to update charger availability
    # (In production, retrieve from database)
    
    # Send notification
    firebase_service.send_notification(
        user_id,
        {
            'type': 'session_completed',
            'title': 'Charging Completed',
            'message': f'Your charging session has ended. Energy delivered: {end_data.get("energy_delivered_kwh", 0)} kWh',
            'session_id': session_id
        }
    )
    
    return {
        "message": "Charging session stopped successfully",
        "session_id": session_id,
        **end_data
    }

@router.get("/active", response_model=List[Session])
async def get_active_sessions(
    current_user: dict = Depends(get_current_user_dependency)
):
    """Get all active charging sessions for user"""
    
    user_id = current_user['user_id']
    
    # Get active sessions from Firebase
    sessions = firebase_service.get_active_sessions(user_id)
    
    # Get real-time status for each session
    for session in sessions:
        provider = session.get('provider')
        session_id = session.get('id')
        
        if provider and session_id:
            status = await provider_aggregator.get_session_status(session_id, provider)
            if status:
                session.update(status)
    
    return sessions

@router.get("/{session_id}/status")
async def get_session_status(
    session_id: str,
    provider: str,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Get real-time status of a charging session"""
    
    # Get status from provider
    status = await provider_aggregator.get_session_status(session_id, provider)
    
    if not status:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return status

@router.get("/history")
async def get_session_history(
    limit: int = 20,
    offset: int = 0,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Get charging session history for user"""
    
    user_id = current_user['user_id']
    
    # In production, query from database with pagination
    # For now, return mock data
    
    sessions = [
        {
            "session_id": "session_001",
            "station_id": "station_001",
            "provider": "chargepoint",
            "started_at": "2024-01-15T10:00:00Z",
            "ended_at": "2024-01-15T11:30:00Z",
            "energy_delivered_kwh": 25.5,
            "duration_minutes": 90,
            "total_cost": 8.93,
            "status": "completed"
        }
    ]
    
    return {
        "sessions": sessions,
        "total": len(sessions),
        "limit": limit,
        "offset": offset
    }

@router.get("/{session_id}")
async def get_session_details(
    session_id: str,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Get detailed information about a specific session"""
    
    # In production, query from database
    # For now, return mock data
    
    session = {
        "session_id": session_id,
        "user_id": current_user['user_id'],
        "station_id": "station_001",
        "station_name": "Downtown Charging Hub",
        "charger_id": "charger_1",
        "provider": "chargepoint",
        "connector_type": "CCS",
        "power_kw": 50,
        "started_at": "2024-01-15T10:00:00Z",
        "ended_at": "2024-01-15T11:30:00Z",
        "energy_delivered_kwh": 25.5,
        "duration_minutes": 90,
        "price_per_kwh": 0.35,
        "total_cost": 8.93,
        "payment_status": "paid",
        "status": "completed"
    }
    
    return session

@router.get("/stats/summary")
async def get_user_charging_stats(
    current_user: dict = Depends(get_current_user_dependency)
):
    """Get charging statistics summary for user"""
    
    user_id = current_user['user_id']
    
    # In production, calculate from database
    stats = {
        "total_sessions": 45,
        "total_energy_kwh": 1250.5,
        "total_cost": 437.68,
        "total_duration_hours": 89.5,
        "average_session_kwh": 27.8,
        "favorite_station": "Downtown Charging Hub",
        "co2_saved_kg": 562.7,  # Compared to gasoline
        "most_used_connector": "CCS"
    }
    
    return stats
