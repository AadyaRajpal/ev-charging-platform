import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.core.config import settings

class ProviderAggregator:
    """Aggregator service to consolidate multiple EV charging provider APIs"""
    
    def __init__(self):
        self.providers = {
            'chargepoint': ChargePointProvider(),
            'evgo': EVgoProvider(),
            'electrify_america': ElectrifyAmericaProvider(),
        }
    
    async def get_all_stations(
        self,
        latitude: float,
        longitude: float,
        radius: int = 5000
    ) -> List[Dict[str, Any]]:
        """Aggregate stations from all providers"""
        all_stations = []
        
        for provider_name, provider in self.providers.items():
            try:
                stations = await provider.get_nearby_stations(latitude, longitude, radius)
                # Add provider information to each station
                for station in stations:
                    station['provider'] = provider_name
                all_stations.extend(stations)
            except Exception as e:
                print(f"Error fetching from {provider_name}: {e}")
        
        return all_stations
    
    async def get_station_details(self, station_id: str, provider: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a station from specific provider"""
        if provider not in self.providers:
            return None
        
        return await self.providers[provider].get_station_details(station_id)
    
    async def start_charging_session(
        self,
        station_id: str,
        charger_id: str,
        provider: str,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """Start a charging session with specific provider"""
        if provider not in self.providers:
            return None
        
        return await self.providers[provider].start_session(station_id, charger_id, user_id)
    
    async def stop_charging_session(
        self,
        session_id: str,
        provider: str
    ) -> Optional[Dict[str, Any]]:
        """Stop a charging session with specific provider"""
        if provider not in self.providers:
            return None
        
        return await self.providers[provider].stop_session(session_id)
    
    async def get_session_status(
        self,
        session_id: str,
        provider: str
    ) -> Optional[Dict[str, Any]]:
        """Get real-time status of a charging session"""
        if provider not in self.providers:
            return None
        
        return await self.providers[provider].get_session_status(session_id)


class ChargePointProvider:
    """ChargePoint API integration"""
    
    def __init__(self):
        self.api_key = settings.CHARGEPOINT_API_KEY
        self.base_url = settings.CHARGEPOINT_API_URL
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    async def get_nearby_stations(
        self,
        latitude: float,
        longitude: float,
        radius: int = 5000
    ) -> List[Dict[str, Any]]:
        """Get nearby ChargePoint stations"""
        # Mock implementation - replace with actual API calls
        return [
            {
                'station_id': 'cp_001',
                'name': 'ChargePoint Station - Downtown',
                'latitude': latitude + 0.01,
                'longitude': longitude + 0.01,
                'address': '123 Main St',
                'chargers': [
                    {
                        'charger_id': 'cp_001_1',
                        'connector_type': 'CCS',
                        'power_kw': 50,
                        'available': True,
                        'price_per_kwh': 0.35
                    },
                    {
                        'charger_id': 'cp_001_2',
                        'connector_type': 'CHAdeMO',
                        'power_kw': 50,
                        'available': False,
                        'price_per_kwh': 0.35
                    }
                ],
                'amenities': ['wifi', 'restroom', 'restaurant'],
                'operating_hours': '24/7'
            }
        ]
    
    async def get_station_details(self, station_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed station information"""
        # Mock implementation
        return {
            'station_id': station_id,
            'name': 'ChargePoint Station',
            'description': 'Fast charging station with multiple connectors',
            'chargers': [],
            'pricing': {'per_kwh': 0.35, 'per_minute': 0.05}
        }
    
    async def start_session(
        self,
        station_id: str,
        charger_id: str,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """Start charging session"""
        # Mock implementation
        return {
            'session_id': f'cp_session_{datetime.utcnow().timestamp()}',
            'status': 'active',
            'started_at': datetime.utcnow().isoformat()
        }
    
    async def stop_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Stop charging session"""
        # Mock implementation
        return {
            'session_id': session_id,
            'status': 'completed',
            'ended_at': datetime.utcnow().isoformat(),
            'energy_delivered_kwh': 25.5,
            'duration_minutes': 45
        }
    
    async def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session status"""
        # Mock implementation
        return {
            'session_id': session_id,
            'status': 'active',
            'energy_delivered_kwh': 15.2,
            'current_power_kw': 48.5,
            'elapsed_minutes': 20
        }


class EVgoProvider:
    """EVgo API integration"""
    
    def __init__(self):
        self.api_key = settings.EVGO_API_KEY
        self.base_url = settings.EVGO_API_URL
    
    async def get_nearby_stations(
        self,
        latitude: float,
        longitude: float,
        radius: int = 5000
    ) -> List[Dict[str, Any]]:
        """Get nearby EVgo stations"""
        # Mock implementation
        return [
            {
                'station_id': 'evgo_001',
                'name': 'EVgo Fast Charging - Mall',
                'latitude': latitude - 0.01,
                'longitude': longitude - 0.01,
                'address': '456 Shopping Center',
                'chargers': [
                    {
                        'charger_id': 'evgo_001_1',
                        'connector_type': 'CCS',
                        'power_kw': 100,
                        'available': True,
                        'price_per_kwh': 0.42
                    }
                ],
                'amenities': ['shopping', 'food'],
                'operating_hours': '6:00 AM - 10:00 PM'
            }
        ]
    
    async def get_station_details(self, station_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed station information"""
        return {
            'station_id': station_id,
            'name': 'EVgo Station',
            'chargers': [],
            'pricing': {'per_kwh': 0.42}
        }
    
    async def start_session(
        self,
        station_id: str,
        charger_id: str,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """Start charging session"""
        return {
            'session_id': f'evgo_session_{datetime.utcnow().timestamp()}',
            'status': 'active',
            'started_at': datetime.utcnow().isoformat()
        }
    
    async def stop_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Stop charging session"""
        return {
            'session_id': session_id,
            'status': 'completed',
            'ended_at': datetime.utcnow().isoformat()
        }
    
    async def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session status"""
        return {
            'session_id': session_id,
            'status': 'active'
        }


class ElectrifyAmericaProvider:
    """Electrify America API integration"""
    
    def __init__(self):
        self.api_key = settings.ELECTRIFY_AMERICA_API_KEY
        self.base_url = settings.ELECTRIFY_AMERICA_API_URL
    
    async def get_nearby_stations(
        self,
        latitude: float,
        longitude: float,
        radius: int = 5000
    ) -> List[Dict[str, Any]]:
        """Get nearby Electrify America stations"""
        # Mock implementation
        return [
            {
                'station_id': 'ea_001',
                'name': 'Electrify America - Highway Rest Stop',
                'latitude': latitude + 0.02,
                'longitude': longitude - 0.02,
                'address': '789 Highway Exit',
                'chargers': [
                    {
                        'charger_id': 'ea_001_1',
                        'connector_type': 'CCS',
                        'power_kw': 150,
                        'available': True,
                        'price_per_kwh': 0.48
                    },
                    {
                        'charger_id': 'ea_001_2',
                        'connector_type': 'CCS',
                        'power_kw': 350,
                        'available': True,
                        'price_per_kwh': 0.52
                    }
                ],
                'amenities': ['restroom', 'convenience_store'],
                'operating_hours': '24/7'
            }
        ]
    
    async def get_station_details(self, station_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed station information"""
        return {
            'station_id': station_id,
            'name': 'Electrify America Station',
            'chargers': [],
            'pricing': {'per_kwh': 0.48}
        }
    
    async def start_session(
        self,
        station_id: str,
        charger_id: str,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """Start charging session"""
        return {
            'session_id': f'ea_session_{datetime.utcnow().timestamp()}',
            'status': 'active',
            'started_at': datetime.utcnow().isoformat()
        }
    
    async def stop_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Stop charging session"""
        return {
            'session_id': session_id,
            'status': 'completed',
            'ended_at': datetime.utcnow().isoformat()
        }
    
    async def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session status"""
        return {
            'session_id': session_id,
            'status': 'active'
        }


# Singleton instance
provider_aggregator = ProviderAggregator()
