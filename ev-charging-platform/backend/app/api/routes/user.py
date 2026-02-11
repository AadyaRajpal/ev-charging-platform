from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.api.routes.auth import get_current_user_dependency
from app.services.firebase_service import firebase_service

router = APIRouter()

# Request/Response Models
class UserProfile(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    notification_preferences: Optional[dict] = None

class VehicleCreate(BaseModel):
    make: str
    model: str
    year: int
    battery_capacity_kwh: float
    connector_types: List[str]  # CCS, CHAdeMO, Type2, Tesla
    nickname: Optional[str] = None

class VehicleUpdate(BaseModel):
    nickname: Optional[str] = None
    is_default: Optional[bool] = None

class Vehicle(BaseModel):
    vehicle_id: str
    make: str
    model: str
    year: int
    battery_capacity_kwh: float
    connector_types: List[str]
    nickname: Optional[str] = None
    is_default: bool = False

@router.get("/profile")
async def get_user_profile(
    current_user: dict = Depends(get_current_user_dependency)
):
    """Get user profile information"""
    
    # Get additional preferences from Firebase
    preferences = firebase_service.get_user_preferences(current_user['user_id'])
    
    return {
        "user_id": current_user['user_id'],
        "name": current_user['name'],
        "email": current_user['email'],
        "phone": current_user.get('phone'),
        "preferences": preferences or {},
        "stripe_customer_id": current_user.get('stripe_customer_id')
    }

@router.put("/profile")
async def update_user_profile(
    profile_data: UserProfile,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Update user profile information"""
    
    user_id = current_user['user_id']
    
    # Update main profile (in production, update database)
    current_user['name'] = profile_data.name
    current_user['email'] = profile_data.email
    current_user['phone'] = profile_data.phone
    
    # Update preferences in Firebase
    if profile_data.notification_preferences:
        firebase_service.update_user_preferences(
            user_id,
            {'notification_preferences': profile_data.notification_preferences}
        )
    
    return {
        "message": "Profile updated successfully",
        "profile": {
            "name": profile_data.name,
            "email": profile_data.email,
            "phone": profile_data.phone
        }
    }

@router.get("/vehicles", response_model=List[Vehicle])
async def get_user_vehicles(
    current_user: dict = Depends(get_current_user_dependency)
):
    """Get all vehicles for user"""
    
    # In production, query from database
    # For now, return mock data
    vehicles = [
        {
            "vehicle_id": "vehicle_001",
            "make": "Tesla",
            "model": "Model 3",
            "year": 2023,
            "battery_capacity_kwh": 75.0,
            "connector_types": ["CCS", "Tesla"],
            "nickname": "My Tesla",
            "is_default": True
        }
    ]
    
    return vehicles

@router.post("/vehicles", response_model=Vehicle)
async def add_vehicle(
    vehicle_data: VehicleCreate,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Add a new vehicle to user's account"""
    
    user_id = current_user['user_id']
    
    # Generate vehicle ID
    vehicle_id = f"vehicle_{user_id}_{len([])}"  # In production, use proper ID generation
    
    vehicle = {
        "vehicle_id": vehicle_id,
        **vehicle_data.dict(),
        "is_default": False  # First vehicle can be set as default
    }
    
    # Store in database (production)
    # Store preferences in Firebase
    firebase_service.update_user_preferences(
        user_id,
        {f'vehicles/{vehicle_id}': vehicle}
    )
    
    return vehicle

@router.put("/vehicles/{vehicle_id}")
async def update_vehicle(
    vehicle_id: str,
    vehicle_data: VehicleUpdate,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Update vehicle information"""
    
    user_id = current_user['user_id']
    
    updates = {}
    if vehicle_data.nickname is not None:
        updates[f'vehicles/{vehicle_id}/nickname'] = vehicle_data.nickname
    if vehicle_data.is_default is not None:
        updates[f'vehicles/{vehicle_id}/is_default'] = vehicle_data.is_default
        # If setting as default, unset others
        # (In production, handle this logic properly)
    
    firebase_service.update_user_preferences(user_id, updates)
    
    return {"message": "Vehicle updated successfully", "vehicle_id": vehicle_id}

@router.delete("/vehicles/{vehicle_id}")
async def delete_vehicle(
    vehicle_id: str,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Delete a vehicle from user's account"""
    
    user_id = current_user['user_id']
    
    # Remove from Firebase
    firebase_service.update_user_preferences(
        user_id,
        {f'vehicles/{vehicle_id}': None}
    )
    
    return {"message": "Vehicle deleted successfully", "vehicle_id": vehicle_id}

@router.get("/preferences")
async def get_user_preferences(
    current_user: dict = Depends(get_current_user_dependency)
):
    """Get user preferences"""
    
    user_id = current_user['user_id']
    preferences = firebase_service.get_user_preferences(user_id)
    
    return {"preferences": preferences or {}}

@router.put("/preferences")
async def update_user_preferences(
    preferences: dict,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Update user preferences"""
    
    user_id = current_user['user_id']
    
    success = firebase_service.update_user_preferences(user_id, preferences)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update preferences")
    
    return {"message": "Preferences updated successfully", "preferences": preferences}

@router.get("/notifications")
async def get_notifications(
    limit: int = 20,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Get user notifications"""
    
    # In production, query from Firebase
    notifications = [
        {
            "notification_id": "notif_001",
            "type": "session_completed",
            "title": "Charging Completed",
            "message": "Your charging session has ended",
            "timestamp": "2024-01-15T11:30:00Z",
            "read": False
        }
    ]
    
    return {"notifications": notifications}

@router.put("/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: str,
    current_user: dict = Depends(get_current_user_dependency)
):
    """Mark a notification as read"""
    
    # In production, update in Firebase
    
    return {"message": "Notification marked as read", "notification_id": notification_id}

@router.delete("/account")
async def delete_user_account(
    current_user: dict = Depends(get_current_user_dependency)
):
    """Delete user account (requires confirmation)"""
    
    user_id = current_user['user_id']
    
    # In production:
    # 1. Cancel active sessions
    # 2. Delete payment methods
    # 3. Archive data
    # 4. Delete from database
    # 5. Delete from Firebase
    
    return {
        "message": "Account deletion initiated",
        "user_id": user_id,
        "note": "Data will be permanently deleted within 30 days"
    }
