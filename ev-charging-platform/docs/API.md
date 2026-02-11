# API Documentation

## Base URL
```
Development: http://localhost:8000/api
Production: https://api.evcharging.com/api
```

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Get Access Token

**POST** `/auth/login`

Request:
```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

## Endpoints

### Authentication

#### Register User
**POST** `/auth/register`

Request:
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe",
  "phone": "+1234567890"
}
```

#### Login
**POST** `/auth/login`

Form data:
- `username`: Email address
- `password`: Password

#### Refresh Token
**POST** `/auth/refresh`

Request:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

#### Get Current User
**GET** `/auth/me`

Response:
```json
{
  "user_id": "user_123",
  "email": "user@example.com",
  "name": "John Doe",
  "phone": "+1234567890"
}
```

---

### Stations

#### Get Nearby Stations
**GET** `/stations/nearby`

Query Parameters:
- `latitude` (required): User's latitude
- `longitude` (required): User's longitude
- `radius`: Search radius in meters (default: 5000)
- `connector_type`: Filter by connector type (CCS, CHAdeMO, Type2, Tesla)
- `available_only`: Show only available stations (default: true)

Response:
```json
[
  {
    "station_id": "station_001",
    "provider": "chargepoint",
    "name": "Downtown Charging Hub",
    "address": "123 Main St",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "distance_km": 1.2,
    "chargers": [
      {
        "charger_id": "charger_1",
        "connector_type": "CCS",
        "power_kw": 50,
        "available": true,
        "price_per_kwh": 0.35
      }
    ],
    "amenities": ["wifi", "restroom"],
    "rating": 4.5,
    "operating_hours": "24/7"
  }
]
```

#### Get Station Details
**GET** `/stations/{station_id}`

Query Parameters:
- `provider`: Provider name (required)

#### Get Station Availability
**GET** `/stations/{station_id}/availability`

Response:
```json
{
  "station_id": "station_001",
  "available_chargers": 3,
  "total_chargers": 4,
  "operational": true,
  "last_updated": "2024-01-15T10:30:00Z"
}
```

#### Add to Favorites
**POST** `/stations/{station_id}/favorite`

#### Remove from Favorites
**DELETE** `/stations/{station_id}/favorite`

#### Get Favorite Stations
**GET** `/stations/user/favorites`

---

### Charging Sessions

#### Start Charging Session
**POST** `/sessions/start`

Request:
```json
{
  "station_id": "station_001",
  "charger_id": "charger_1",
  "provider": "chargepoint",
  "estimated_kwh": 30.0
}
```

Response:
```json
{
  "session_id": "session_12345",
  "user_id": "user_123",
  "station_id": "station_001",
  "charger_id": "charger_1",
  "provider": "chargepoint",
  "status": "active",
  "started_at": "2024-01-15T10:00:00Z"
}
```

#### Stop Charging Session
**POST** `/sessions/{session_id}/stop`

Query Parameters:
- `provider`: Provider name (required)

Response:
```json
{
  "message": "Charging session stopped successfully",
  "session_id": "session_12345",
  "ended_at": "2024-01-15T11:30:00Z",
  "energy_delivered_kwh": 25.5,
  "duration_minutes": 90
}
```

#### Get Active Sessions
**GET** `/sessions/active`

Response:
```json
[
  {
    "session_id": "session_12345",
    "station_id": "station_001",
    "status": "active",
    "started_at": "2024-01-15T10:00:00Z",
    "energy_delivered_kwh": 15.2,
    "current_power_kw": 48.5
  }
]
```

#### Get Session Status
**GET** `/sessions/{session_id}/status`

Query Parameters:
- `provider`: Provider name (required)

#### Get Session History
**GET** `/sessions/history`

Query Parameters:
- `limit`: Number of records (default: 20)
- `offset`: Pagination offset (default: 0)

#### Get Session Details
**GET** `/sessions/{session_id}`

#### Get Charging Statistics
**GET** `/sessions/stats/summary`

Response:
```json
{
  "total_sessions": 45,
  "total_energy_kwh": 1250.5,
  "total_cost": 437.68,
  "total_duration_hours": 89.5,
  "average_session_kwh": 27.8,
  "favorite_station": "Downtown Charging Hub",
  "co2_saved_kg": 562.7
}
```

---

### Payments

#### Add Payment Method
**POST** `/payments/methods`

Request:
```json
{
  "payment_method_id": "pm_1234567890"
}
```

#### Get Payment Methods
**GET** `/payments/methods`

Response:
```json
{
  "payment_methods": [
    {
      "payment_method_id": "pm_1234567890",
      "type": "card",
      "card": {
        "brand": "visa",
        "last4": "4242",
        "exp_month": 12,
        "exp_year": 2025
      }
    }
  ]
}
```

#### Remove Payment Method
**DELETE** `/payments/methods/{payment_method_id}`

#### Create Payment Intent
**POST** `/payments/create-intent`

Request:
```json
{
  "amount": 25.50,
  "currency": "usd",
  "session_id": "session_12345",
  "station_id": "station_001",
  "payment_method_id": "pm_1234567890"
}
```

Response:
```json
{
  "payment_intent": {
    "payment_intent_id": "pi_1234567890",
    "client_secret": "pi_1234567890_secret_xxx",
    "status": "requires_confirmation",
    "amount": 2550,
    "currency": "usd"
  }
}
```

#### Confirm Payment
**POST** `/payments/confirm`

Query Parameters:
- `payment_intent_id`: Payment intent ID (required)

#### Get Payment Intent
**GET** `/payments/intent/{payment_intent_id}`

#### Create Refund
**POST** `/payments/refund`

Request:
```json
{
  "payment_intent_id": "pi_1234567890",
  "amount": 10.00,
  "reason": "requested_by_customer"
}
```

#### Get Payment History
**GET** `/payments/history`

Query Parameters:
- `limit`: Number of records (default: 10)

---

### User Profile

#### Get User Profile
**GET** `/user/profile`

Response:
```json
{
  "user_id": "user_123",
  "name": "John Doe",
  "email": "user@example.com",
  "phone": "+1234567890",
  "preferences": {},
  "stripe_customer_id": "cus_1234567890"
}
```

#### Update User Profile
**PUT** `/user/profile`

Request:
```json
{
  "name": "John Doe",
  "email": "user@example.com",
  "phone": "+1234567890",
  "notification_preferences": {
    "email_notifications": true,
    "push_notifications": true
  }
}
```

#### Get User Vehicles
**GET** `/user/vehicles`

Response:
```json
[
  {
    "vehicle_id": "vehicle_001",
    "make": "Tesla",
    "model": "Model 3",
    "year": 2023,
    "battery_capacity_kwh": 75.0,
    "connector_types": ["CCS", "Tesla"],
    "nickname": "My Tesla",
    "is_default": true
  }
]
```

#### Add Vehicle
**POST** `/user/vehicles`

Request:
```json
{
  "make": "Tesla",
  "model": "Model 3",
  "year": 2023,
  "battery_capacity_kwh": 75.0,
  "connector_types": ["CCS", "Tesla"],
  "nickname": "My Tesla"
}
```

#### Update Vehicle
**PUT** `/user/vehicles/{vehicle_id}`

Request:
```json
{
  "nickname": "My New Tesla",
  "is_default": true
}
```

#### Delete Vehicle
**DELETE** `/user/vehicles/{vehicle_id}`

#### Get User Preferences
**GET** `/user/preferences`

#### Update User Preferences
**PUT** `/user/preferences`

#### Get Notifications
**GET** `/user/notifications`

Query Parameters:
- `limit`: Number of notifications (default: 20)

#### Mark Notification as Read
**PUT** `/user/notifications/{notification_id}/read`

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

- **Rate Limit**: 60 requests per minute per user
- **Header**: `X-RateLimit-Remaining` indicates remaining requests

---

## Webhooks

### Stripe Webhook
**POST** `/payments/webhook`

Headers:
- `Stripe-Signature`: Webhook signature for verification

Events handled:
- `payment_intent.succeeded`
- `payment_intent.payment_failed`

---

## Testing

### Test Stripe Card Numbers

- Success: `4242 4242 4242 4242`
- Decline: `4000 0000 0000 0002`
- 3D Secure: `4000 0025 0000 3155`

### Test User Credentials

```
Email: test@example.com
Password: password123
```

---

## Interactive Documentation

Visit `/api/docs` for interactive Swagger UI documentation where you can test all endpoints directly.

Visit `/api/redoc` for ReDoc documentation with a clean, three-panel design.
