import googlemaps
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from app.core.config import settings

class MapsService:
    """Service for Google Maps API operations"""
    
    def __init__(self):
        if settings.GOOGLE_MAPS_API_KEY:
            self.client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
        else:
            self.client = None
            print("⚠️  Google Maps API key not configured")
    
    def find_nearby_stations(
        self,
        latitude: float,
        longitude: float,
        radius: int = 5000,  # meters
        keyword: str = "EV charging station"
    ) -> List[Dict[str, Any]]:
        """Find nearby EV charging stations using Places API"""
        if not self.client:
            return []
        
        try:
            # Search for nearby places
            places_result = self.client.places_nearby(
                location=(latitude, longitude),
                radius=radius,
                keyword=keyword,
                type='charging_station'
            )
            
            stations = []
            for place in places_result.get('results', []):
                station = self._format_place_to_station(place)
                stations.append(station)
            
            return stations
        except Exception as e:
            print(f"Error finding nearby stations: {e}")
            return []
    
    def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a place"""
        if not self.client:
            return None
        
        try:
            place_details = self.client.place(
                place_id=place_id,
                fields=[
                    'name', 'formatted_address', 'geometry', 'rating',
                    'opening_hours', 'formatted_phone_number', 'website',
                    'photos', 'reviews', 'price_level'
                ]
            )
            
            return place_details.get('result')
        except Exception as e:
            print(f"Error getting place details: {e}")
            return None
    
    def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """Convert address to coordinates"""
        if not self.client:
            return None
        
        try:
            geocode_result = self.client.geocode(address)
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                return (location['lat'], location['lng'])
            return None
        except Exception as e:
            print(f"Error geocoding address: {e}")
            return None
    
    def reverse_geocode(self, latitude: float, longitude: float) -> Optional[str]:
        """Convert coordinates to address"""
        if not self.client:
            return None
        
        try:
            reverse_geocode_result = self.client.reverse_geocode((latitude, longitude))
            if reverse_geocode_result:
                return reverse_geocode_result[0]['formatted_address']
            return None
        except Exception as e:
            print(f"Error reverse geocoding: {e}")
            return None
    
    def calculate_distance(
        self,
        origin: Tuple[float, float],
        destination: Tuple[float, float],
        mode: str = "driving"
    ) -> Optional[Dict[str, Any]]:
        """Calculate distance and duration between two points"""
        if not self.client:
            return None
        
        try:
            result = self.client.distance_matrix(
                origins=[origin],
                destinations=[destination],
                mode=mode
            )
            
            if result['rows']:
                element = result['rows'][0]['elements'][0]
                if element['status'] == 'OK':
                    return {
                        'distance': element['distance']['value'],  # meters
                        'distance_text': element['distance']['text'],
                        'duration': element['duration']['value'],  # seconds
                        'duration_text': element['duration']['text']
                    }
            return None
        except Exception as e:
            print(f"Error calculating distance: {e}")
            return None
    
    def get_directions(
        self,
        origin: Tuple[float, float],
        destination: Tuple[float, float],
        waypoints: Optional[List[Tuple[float, float]]] = None,
        mode: str = "driving"
    ) -> Optional[List[Dict[str, Any]]]:
        """Get directions between points"""
        if not self.client:
            return None
        
        try:
            directions_result = self.client.directions(
                origin=origin,
                destination=destination,
                waypoints=waypoints,
                mode=mode,
                alternatives=True
            )
            
            routes = []
            for route in directions_result:
                routes.append({
                    'summary': route.get('summary'),
                    'distance': route['legs'][0]['distance']['value'],
                    'duration': route['legs'][0]['duration']['value'],
                    'steps': self._format_directions_steps(route['legs'][0]['steps'])
                })
            
            return routes
        except Exception as e:
            print(f"Error getting directions: {e}")
            return None
    
    def search_text(self, query: str, location: Optional[Tuple[float, float]] = None) -> List[Dict[str, Any]]:
        """Search for places using text query"""
        if not self.client:
            return []
        
        try:
            params = {'query': query}
            if location:
                params['location'] = location
                params['radius'] = 10000  # 10km
            
            places_result = self.client.places(**params)
            
            stations = []
            for place in places_result.get('results', []):
                station = self._format_place_to_station(place)
                stations.append(station)
            
            return stations
        except Exception as e:
            print(f"Error searching places: {e}")
            return []
    
    # Helper methods
    def _format_place_to_station(self, place: Dict[str, Any]) -> Dict[str, Any]:
        """Format Google Places result to station format"""
        location = place.get('geometry', {}).get('location', {})
        
        return {
            'place_id': place.get('place_id'),
            'name': place.get('name'),
            'address': place.get('vicinity') or place.get('formatted_address'),
            'latitude': location.get('lat'),
            'longitude': location.get('lng'),
            'rating': place.get('rating'),
            'user_ratings_total': place.get('user_ratings_total'),
            'business_status': place.get('business_status'),
            'open_now': place.get('opening_hours', {}).get('open_now'),
            'photos': [photo['photo_reference'] for photo in place.get('photos', [])[:3]],
            'types': place.get('types', [])
        }
    
    def _format_directions_steps(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format direction steps"""
        formatted_steps = []
        for step in steps:
            formatted_steps.append({
                'instruction': step.get('html_instructions'),
                'distance': step['distance']['text'],
                'duration': step['duration']['text'],
                'start_location': step['start_location'],
                'end_location': step['end_location']
            })
        return formatted_steps
    
    def get_photo_url(self, photo_reference: str, max_width: int = 400) -> str:
        """Get URL for a place photo"""
        return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={max_width}&photoreference={photo_reference}&key={settings.GOOGLE_MAPS_API_KEY}"

# Singleton instance
maps_service = MapsService()
