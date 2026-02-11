import firebase_admin
from firebase_admin import credentials, db, auth
from typing import Optional, Dict, Any, List
from datetime import datetime
import json
import os
from app.core.config import settings

class FirebaseService:
    """Service for Firebase Realtime Database operations"""
    
    def __init__(self):
        self.initialized = False
        self._initialize()
    
    def _initialize(self):
        """Initialize Firebase Admin SDK"""
        if not self.initialized:
            try:
                # Check if already initialized
                firebase_admin.get_app()
            except ValueError:
                # Initialize if not already done
                if os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
                    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                    firebase_admin.initialize_app(cred, {
                        'databaseURL': settings.FIREBASE_DATABASE_URL or 'https://ev-charging-default-rtdb.firebaseio.com'
                    })
                else:
                    print("⚠️  Firebase credentials not found. Using default credentials.")
                    firebase_admin.initialize_app()
            
            self.initialized = True
    
    # Station Status Operations
    def update_station_status(self, station_id: str, status_data: Dict[str, Any]) -> bool:
        """Update real-time status of a charging station"""
        try:
            ref = db.reference(f'stations/{station_id}/status')
            status_data['last_updated'] = datetime.utcnow().isoformat()
            ref.set(status_data)
            return True
        except Exception as e:
            print(f"Error updating station status: {e}")
            return False
    
    def get_station_status(self, station_id: str) -> Optional[Dict[str, Any]]:
        """Get real-time status of a charging station"""
        try:
            ref = db.reference(f'stations/{station_id}/status')
            return ref.get()
        except Exception as e:
            print(f"Error getting station status: {e}")
            return None
    
    def update_charger_availability(self, station_id: str, charger_id: str, is_available: bool, power_kw: float = 0):
        """Update availability of a specific charger"""
        try:
            ref = db.reference(f'stations/{station_id}/chargers/{charger_id}')
            ref.update({
                'available': is_available,
                'power_kw': power_kw,
                'last_updated': datetime.utcnow().isoformat()
            })
            
            # Update station-level availability count
            self._update_station_availability_count(station_id)
            return True
        except Exception as e:
            print(f"Error updating charger availability: {e}")
            return False
    
    def _update_station_availability_count(self, station_id: str):
        """Update the count of available chargers at a station"""
        try:
            chargers_ref = db.reference(f'stations/{station_id}/chargers')
            chargers = chargers_ref.get() or {}
            
            available_count = sum(1 for charger in chargers.values() if charger.get('available', False))
            total_count = len(chargers)
            
            status_ref = db.reference(f'stations/{station_id}/status')
            status_ref.update({
                'available_chargers': available_count,
                'total_chargers': total_count,
                'operational': available_count > 0
            })
        except Exception as e:
            print(f"Error updating availability count: {e}")
    
    # Charging Session Operations
    def create_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """Create a new charging session in real-time database"""
        try:
            ref = db.reference(f'sessions/{session_id}')
            session_data['created_at'] = datetime.utcnow().isoformat()
            session_data['status'] = 'active'
            ref.set(session_data)
            
            # Add to user's active sessions
            user_id = session_data.get('user_id')
            if user_id:
                user_session_ref = db.reference(f'users/{user_id}/active_sessions/{session_id}')
                user_session_ref.set(True)
            
            return True
        except Exception as e:
            print(f"Error creating session: {e}")
            return False
    
    def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing charging session"""
        try:
            ref = db.reference(f'sessions/{session_id}')
            updates['last_updated'] = datetime.utcnow().isoformat()
            ref.update(updates)
            return True
        except Exception as e:
            print(f"Error updating session: {e}")
            return False
    
    def end_session(self, session_id: str, end_data: Dict[str, Any]) -> bool:
        """End a charging session"""
        try:
            ref = db.reference(f'sessions/{session_id}')
            session = ref.get()
            
            if not session:
                return False
            
            # Update session status
            end_data['status'] = 'completed'
            end_data['ended_at'] = datetime.utcnow().isoformat()
            ref.update(end_data)
            
            # Remove from user's active sessions
            user_id = session.get('user_id')
            if user_id:
                user_session_ref = db.reference(f'users/{user_id}/active_sessions/{session_id}')
                user_session_ref.delete()
            
            # Archive the session
            archive_ref = db.reference(f'sessions_history/{session_id}')
            archive_ref.set(ref.get())
            
            return True
        except Exception as e:
            print(f"Error ending session: {e}")
            return False
    
    def get_active_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all active sessions for a user"""
        try:
            ref = db.reference(f'users/{user_id}/active_sessions')
            session_ids = ref.get() or {}
            
            sessions = []
            for session_id in session_ids.keys():
                session_ref = db.reference(f'sessions/{session_id}')
                session = session_ref.get()
                if session:
                    session['id'] = session_id
                    sessions.append(session)
            
            return sessions
        except Exception as e:
            print(f"Error getting active sessions: {e}")
            return []
    
    # User Preferences
    def update_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        """Update user preferences"""
        try:
            ref = db.reference(f'users/{user_id}/preferences')
            ref.update(preferences)
            return True
        except Exception as e:
            print(f"Error updating user preferences: {e}")
            return False
    
    def get_user_preferences(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user preferences"""
        try:
            ref = db.reference(f'users/{user_id}/preferences')
            return ref.get()
        except Exception as e:
            print(f"Error getting user preferences: {e}")
            return None
    
    # Notifications
    def send_notification(self, user_id: str, notification: Dict[str, Any]) -> bool:
        """Send a notification to user"""
        try:
            ref = db.reference(f'users/{user_id}/notifications')
            notification['timestamp'] = datetime.utcnow().isoformat()
            notification['read'] = False
            ref.push(notification)
            return True
        except Exception as e:
            print(f"Error sending notification: {e}")
            return False
    
    # Analytics
    def log_event(self, event_type: str, event_data: Dict[str, Any]) -> bool:
        """Log an analytics event"""
        try:
            ref = db.reference(f'analytics/{event_type}')
            event_data['timestamp'] = datetime.utcnow().isoformat()
            ref.push(event_data)
            return True
        except Exception as e:
            print(f"Error logging event: {e}")
            return False

# Singleton instance
firebase_service = FirebaseService()
